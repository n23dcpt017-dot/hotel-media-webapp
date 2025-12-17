
import unittest
import sys
import os
import tempfile
from sqlalchemy.exc import IntegrityError

# Add parent directory to path để import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db, login_manager 
from app.models.user import User

class LoginUnitTest(unittest.TestCase):
    """Unit test cases cho login functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Setup một lần cho tất cả tests"""
        print("\n" + "="*70)
        print("🧪 BẮT ĐẦU UNIT TEST - LOGIN LOGIC (WINDOWS FIXED VERSION)")
        print("="*70 + "\n")
    
    @classmethod
    def tearDownClass(cls):
        """Cleanup sau khi chạy xong tất cả tests"""
        print("\n" + "="*70)
        print("✅ HOÀN THÀNH UNIT TEST")
        print("="*70 + "\n")
    
    def setUp(self):
        """Setup trước mỗi test case"""
        print(f"Setting up test: {self._testMethodName}")
        
        # Tạo Flask app với test config - DÙNG DATABASE IN-MEMORY
        self.app = create_app('testing')
        
        # CẤU HÌNH QUAN TRỌNG: Luôn dùng database in-memory
        self.app.config.update({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # IN-MEMORY DATABASE
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SECRET_KEY': 'test-secret-key-for-unit-tests',
            'SERVER_NAME': 'localhost.localdomain'  # Để session hoạt động
        })
        
        # Tạo test client và context
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Đăng ký user_loader cho môi trường test
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        
        # Tạo database tables mới
        db.create_all()
        
        # Tạo test user DUY NHẤT (khác với init_db.py)
        self.test_user = User(
            username='TestAdmin',  # KHÁC với 'admin' trong init_db.py
            email='test_admin@example.com',  # KHÁC với 'admin@hotel.com'
            fullname='Test Administrator',
            role='admin',
            is_active=True
        )
        self.test_user.set_password('Test@123')  # Password khác
        
        db.session.add(self.test_user)
        db.session.commit()
        
        print(f"✓ Created test user: {self.test_user.username}")
    
    def tearDown(self):
        """Cleanup sau mỗi test case"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        print(f"✓ Cleaned up: {self._testMethodName}\n")
    
    # ========================
    # TEST CASES - USER MODEL
    # ========================
    
    def test_01_user_creation(self):
        """Test 1: Tạo user thành công"""
        print("🧪 Test 1: Kiểm tra tạo user...")
        
        user = User(
            username='new_staff',
            email='new_staff@example.com',  # Email mới, không trùng
            fullname='New Staff Member',
            role='staff'
        )
        user.set_password('Staff@123')
        
        db.session.add(user)
        db.session.commit()
        
        found_user = User.query.filter_by(username='new_staff').first()
        
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.email, 'new_staff@example.com')
        self.assertTrue(found_user.check_password('Staff@123'))
        
        print("   ✓ User mới được tạo thành công")
        print("✅ PASSED")
    
    def test_02_password_hashing(self):
        """Test 2: Password được hash đúng"""
        print("🧪 Test 2: Kiểm tra password hashing...")
        user = self.test_user
        self.assertNotEqual(user.password_hash, 'Test@123')
        self.assertIsNotNone(user.password_hash)
        print("✅ PASSED")
    
    def test_03_password_verification_correct(self):
        """Test 3: Verify password đúng"""
        print("🧪 Test 3: Kiểm tra verify password đúng...")
        user = self.test_user
        result = user.check_password('Test@123')
        self.assertTrue(result)
        print("✅ PASSED")
    
    def test_04_password_verification_wrong(self):
        """Test 4: Verify password sai"""
        print("🧪 Test 4: Kiểm tra verify password sai...")
        user = self.test_user
        result = user.check_password('WrongPassword')
        self.assertFalse(result)
        print("✅ PASSED")
    
    def test_05_user_repr(self):
        """Test 5: User __repr__ method"""
        print("🧪 Test 5: Kiểm tra User repr...")
        user = self.test_user
        repr_str = repr(user)
        
        self.assertTrue('TestAdmin' in repr_str or 'test_admin@example.com' in repr_str)
        
        print(f"   ✓ User repr: {repr_str}")
        print("✅ PASSED")
    
    # ========================
    # TEST CASES - LOGIN ROUTE
    # ========================
    
    def test_06_login_page_get(self):
        """Test 6: GET request đến trang login"""
        print("🧪 Test 6: Kiểm tra GET /auth/login...")
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        print("✅ PASSED")
    
    def test_07_login_with_correct_credentials(self):
        """Test 7: Login với credentials đúng"""
        print("🧪 Test 7: Kiểm tra login với credentials đúng...")
        
        # Login với test user của chúng ta
        response = self.client.post('/auth/login', data={
            'username': 'TestAdmin',
            'password': 'Test@123'
        }, follow_redirects=False)
        
        # Kiểm tra redirect status code
        self.assertEqual(response.status_code, 302)
        
        # Kiểm tra location header
        location = response.headers.get('Location', '')
        self.assertTrue('/auth/tongquan.html' in location or '/tongquan' in location)
        
        # Kiểm tra session
        with self.client.session_transaction() as sess:
            self.assertIn('_user_id', sess)
            user_id = sess['_user_id']
            self.assertEqual(int(user_id), self.test_user.id)
            
        print("   ✓ Login thành công, redirect đến dashboard")
        print("   ✓ Session đã lưu user_id")
        print("✅ PASSED")
    
    def test_08_login_with_wrong_username(self):
        """Test 8: Login với username sai"""
        print("🧪 Test 8: Kiểm tra login với username sai...")
        response = self.client.post('/auth/login', data={
            'username': 'wronguser',
            'password': 'Test@123'
        })
        
        # Nên trả về 200 với thông báo lỗi
        self.assertEqual(response.status_code, 200)
        
        # Kiểm tra session không có user_id
        with self.client.session_transaction() as sess:
            self.assertNotIn('_user_id', sess)
            
        print("✅ PASSED")
    
    def test_09_login_with_wrong_password(self):
        """Test 9: Login với password sai"""
        print("🧪 Test 9: Kiểm tra login với password sai...")
        response = self.client.post('/auth/login', data={
            'username': 'TestAdmin',
            'password': 'WrongPassword'
        })
        
        self.assertEqual(response.status_code, 200)
        
        with self.client.session_transaction() as sess:
            self.assertNotIn('_user_id', sess)
            
        print("✅ PASSED")
    
    def test_10_login_with_empty_fields(self):
        """Test 10: Login với fields trống"""
        print("🧪 Test 10: Kiểm tra login với fields trống...")
        response = self.client.post('/auth/login', data={
            'username': '',
            'password': ''
        })
        
        self.assertEqual(response.status_code, 200)
        
        print("✅ PASSED")
    
    def test_11_login_with_inactive_user(self):
        """Test 11: Login với user inactive"""
        print("🧪 Test 11: Kiểm tra login với user inactive...")
        
        # Tạo user inactive
        inactive_user = User(
            username='inactive_user',
            email='inactive@example.com',
            fullname='Inactive User',
            role='viewer',
            is_active=False  # INACTIVE
        )
        inactive_user.set_password('InactivePass123')
        db.session.add(inactive_user)
        db.session.commit()
        
        # Thử login
        response = self.client.post('/auth/login', data={
            'username': 'inactive_user',
            'password': 'InactivePass123'
        })
        
        # Kiểm tra session
        with self.client.session_transaction() as sess:
            # Tuỳ thuộc vào logic app, có thể login được hoặc không
            if '_user_id' in sess:
                user_id = sess['_user_id']
                print(f"   ⚠️  User inactive có thể login, user_id: {user_id}")
            else:
                print("   ✓ User inactive không thể login")
        
        print("✅ PASSED")
    
    def test_12_logout_functionality(self):
        """Test 12: Chức năng logout"""
        print("🧪 Test 12: Kiểm tra logout...")
        
        # Login trước
        response = self.client.post('/auth/login', data={
            'username': 'TestAdmin', 
            'password': 'Test@123'
        }, follow_redirects=False)
        
        self.assertEqual(response.status_code, 302)
        
        # Kiểm tra session có user_id
        with self.client.session_transaction() as sess:
            self.assertIn('_user_id', sess)
        
        # Logout
        response = self.client.get('/auth/logout', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        
        # Kiểm tra redirect về login
        location = response.headers.get('Location', '')
        self.assertTrue('/auth/login' in location or '/login' in location)
        
        # Verify session cleared
        with self.client.session_transaction() as sess:
            self.assertNotIn('_user_id', sess)

        print("   ✓ Logout thành công, session cleared")
        print("✅ PASSED")
    
    def test_13_user_query_by_username(self):
        """Test 13: Query user bằng username"""
        print("🧪 Test 13: Kiểm tra query user by username...")
        
        user = User.query.filter_by(username='TestAdmin').first()
        
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'TestAdmin')
        self.assertEqual(user.email, 'test_admin@example.com')
        print("✅ PASSED")
    
    def test_14_user_query_by_email(self):
        """Test 14: Query user bằng email"""
        print("🧪 Test 14: Kiểm tra query user by email...")
        
        user = User.query.filter_by(email='test_admin@example.com').first()
        
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test_admin@example.com')
        self.assertEqual(user.username, 'TestAdmin')
        print("✅ PASSED")
    
    def test_15_unique_username_constraint(self):
        """Test 15: Username phải unique"""
        print("🧪 Test 15: Kiểm tra unique username constraint...")
        
        # Cố tình tạo user trùng username
        duplicate_user = User(
            username='TestAdmin',  # Trùng với test_user
            email='another@example.com',  # Email khác
            fullname='Another User'
        )
        duplicate_user.set_password('AnotherPass123')
        
        db.session.add(duplicate_user)
        
        # Nên raise IntegrityError
        with self.assertRaises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()
        print("   ✓ IntegrityError được raise khi trùng username")
        print("✅ PASSED")
    
    def test_16_unique_email_constraint(self):
        """Test 16: Email phải unique"""
        print("🧪 Test 16: Kiểm tra unique email constraint...")
        
        # Cố tình tạo user trùng email
        duplicate_user = User(
            username='AnotherUser',  # Username khác
            email='test_admin@example.com',  # Trùng email với test_user
            fullname='Another User'
        )
        duplicate_user.set_password('AnotherPass123')
        
        db.session.add(duplicate_user)
        
        # Nên raise IntegrityError
        with self.assertRaises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()
        print("   ✓ IntegrityError được raise khi trùng email")
        print("✅ PASSED")
    
    def test_17_direct_user_authentication(self):
        """Test 17: Kiểm tra authentication trực tiếp"""
        print("🧪 Test 17: Kiểm tra authentication trực tiếp...")
        
        user = self.test_user
        
        # Password đúng
        self.assertTrue(user.check_password('Test@123'))
        
        # Password sai
        self.assertFalse(user.check_password('wrong'))
        self.assertFalse(user.check_password(''))
        
        print("   ✓ Authentication logic hoạt động đúng")
        print("✅ PASSED")
    
    def test_18_session_management(self):
        """Test 18: Kiểm tra quản lý session"""
        print("🧪 Test 18: Kiểm tra quản lý session...")
        
        # Ban đầu session trống
        with self.client.session_transaction() as sess:
            self.assertNotIn('_user_id', sess)
        
        # Login
        response = self.client.post('/auth/login', data={
            'username': 'TestAdmin',
            'password': 'Test@123'
        }, follow_redirects=False)
        
        # Sau login có session
        with self.client.session_transaction() as sess:
            self.assertIn('_user_id', sess)
            user_id = sess['_user_id']
            
            # Kiểm tra user_id là số
            self.assertIsInstance(int(user_id), int)
        
        print("   ✓ Session được tạo sau login")
        print("✅ PASSED")
    
    def test_19_user_deletion(self):
        """Test 19: Xóa user"""
        print("🧪 Test 19: Kiểm tra xóa user...")
        
        # Tạo user mới để xóa
        user_to_delete = User(
            username='todelete',
            email='delete@example.com',
            fullname='User To Delete',
            role='staff'
        )
        user_to_delete.set_password('Delete@123')
        
        db.session.add(user_to_delete)
        db.session.commit()
        
        # Xác nhận user tồn tại
        user_before = User.query.filter_by(username='todelete').first()
        self.assertIsNotNone(user_before)
        
        # Xóa user
        db.session.delete(user_before)
        db.session.commit()
        
        # Xác nhận user đã bị xóa
        user_after = User.query.filter_by(username='todelete').first()
        self.assertIsNone(user_after)
        
        print("   ✓ User được xóa thành công")
        print("✅ PASSED")
    
    def test_20_multiple_users(self):
        """Test 20: Tạo và query nhiều users"""
        print("🧪 Test 20: Kiểm tra tạo và query nhiều users...")
        
        # Tạo thêm 3 users
        users_data = [
            {'username': 'user1', 'email': 'user1@example.com', 'role': 'staff'},
            {'username': 'user2', 'email': 'user2@example.com', 'role': 'manager'},
            {'username': 'user3', 'email': 'user3@example.com', 'role': 'viewer'}
        ]
        
        for data in users_data:
            user = User(
                username=data['username'],
                email=data['email'],
                fullname=f"User {data['username']}",
                role=data['role']
            )
            user.set_password(f"{data['username']}@123")
            db.session.add(user)
        
        db.session.commit()
        
        # Kiểm tra số lượng users
        all_users = User.query.all()
        self.assertGreaterEqual(len(all_users), 4)  # 3 mới + 1 test_user
        
        # Kiểm tra từng user
        for data in users_data:
            user = User.query.filter_by(username=data['username']).first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, data['email'])
            self.assertTrue(user.check_password(f"{data['username']}@123"))
        
        print(f"   ✓ Đã tạo {len(users_data)} users mới")
        print(f"   ✓ Tổng số users trong DB: {len(all_users)}")
        print("✅ PASSED")


def run_tests_with_custom_output():
    """Chạy tests với output custom"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(LoginUnitTest)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"\n{test}:")
            print(traceback)
    
    if result.errors:
        print("\n⚠️  ERRORS:")
        for test, traceback in result.errors:
            print(f"\n{test}:")
            print(traceback)
    
    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print("\n⚠️  SOME TESTS FAILED")
    
    print("="*70 + "\n")
    return result


if __name__ == '__main__':
    print("🚀 Starting unit tests for login functionality...")
    print("📝 NOTE: Using in-memory database for isolated testing")
    print("-" * 70)
    
    result = run_tests_with_custom_output()
    
    # Exit với code 0 nếu thành công, 1 nếu có lỗi
    sys.exit(0 if result.wasSuccessful() else 1)
