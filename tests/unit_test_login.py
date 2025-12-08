"""
UNIT TEST - Login Logic (FIXED)
Test các hàm và logic backend của login
"""
import unittest
import sys
import os
from sqlalchemy.exc import IntegrityError # Import để bắt lỗi DB chính xác

# Add parent directory to path để import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import login_manager từ app để fix lỗi user_loader
from app import create_app, db, login_manager 
from app.models.user import User
from flask import session

class LoginUnitTest(unittest.TestCase):
    """Unit test cases cho login functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Setup một lần cho tất cả tests"""
        print("\n" + "="*70)
        print("🧪 BẮT ĐẦU UNIT TEST - LOGIN LOGIC (FIXED VERSION)")
        print("="*70 + "\n")
    
    @classmethod
    def tearDownClass(cls):
        """Cleanup sau khi chạy xong tất cả tests"""
        print("\n" + "="*70)
        print("✅ HOÀN THÀNH UNIT TEST")
        print("="*70 + "\n")
    
    def setUp(self):
        """Setup trước mỗi test case"""
        # Tạo Flask app với test config
        self.app = create_app() 
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # --- FIX QUAN TRỌNG: Đăng ký user_loader cho môi trường test ---
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        # -------------------------------------------------------------
        
        # Tạo database
        db.create_all()
        
        # Tạo test user chuẩn (User Admin dùng chung cho các test login)
        self.test_user = User(
            username='Admin',  # Lưu ý: Username là 'Admin'
            email='admin@hotel.com',
            full_name='Admin User',
            role='admin',
            is_active=True
        )
        self.test_user.set_password('Admin@123')
        
        db.session.add(self.test_user)
        db.session.commit()
    
    def tearDown(self):
        """Cleanup sau mỗi test case"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    # ========================
    # TEST CASES - USER MODEL
    # ========================
    
    def test_01_user_creation(self):
        """Test 1: Tạo user thành công"""
        print("🧪 Test 1: Kiểm tra tạo user...")
        
        # FIX: Tạo user với thông tin KHÁC với self.test_user trong setUp
        user = User(
            username='new_staff',
            email='staff@hotel.com',
            full_name='New Staff',
            role='staff'
        )
        user.set_password('Staff@123')
        
        db.session.add(user)
        db.session.commit()
        
        # Kiểm tra user đã được tạo
        found_user = User.query.filter_by(username='new_staff').first()
        
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.email, 'staff@hotel.com')
        
        print("   ✓ User mới được tạo thành công (không trùng Admin)")
        print("✅ PASSED\n")
    
    def test_02_password_hashing(self):
        """Test 2: Password được hash đúng"""
        print("🧪 Test 2: Kiểm tra password hashing...")
        user = self.test_user
        self.assertNotEqual(user.password_hash, 'Admin@123')
        self.assertIsNotNone(user.password_hash)
        print("✅ PASSED\n")
    
    def test_03_password_verification_correct(self):
        """Test 3: Verify password đúng"""
        print("🧪 Test 3: Kiểm tra verify password đúng...")
        user = self.test_user
        result = user.check_password('Admin@123')
        self.assertTrue(result)
        print("✅ PASSED\n")
    
    def test_04_password_verification_wrong(self):
        """Test 4: Verify password sai"""
        print("🧪 Test 4: Kiểm tra verify password sai...")
        user = self.test_user
        result = user.check_password('WrongPassword')
        self.assertFalse(result)
        print("✅ PASSED\n")
    
    def test_05_user_repr(self):
        """Test 5: User __repr__ method"""
        print("🧪 Test 5: Kiểm tra User repr...")
        user = self.test_user
        repr_str = repr(user)
        
        # FIX: Kiểm tra từ khóa 'Admin' vì setup tạo username='Admin'
        # Điều chỉnh tùy theo hàm __repr__ trong model của bạn trả về gì
        self.assertTrue('Admin' in repr_str or 'admin@hotel.com' in repr_str)
        
        print(f"   ✓ User repr: {repr_str}")
        print("✅ PASSED\n")
    
    # ========================
    # TEST CASES - LOGIN ROUTE
    # ========================
    
    def test_06_login_page_get(self):
        """Test 6: GET request đến trang login"""
        print("🧪 Test 6: Kiểm tra GET /auth/login...")
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        print("✅ PASSED\n")
    
    def test_07_login_with_correct_credentials(self):
        """Test 7: Login với credentials đúng"""
        print("🧪 Test 7: Kiểm tra login với credentials đúng...")
        
        response = self.client.post('/auth/login', data={
            'username': 'Admin', # Dùng Username đúng trong setUp
            'password': 'Admin@123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # FIX: Kiểm tra Session thực tế
        with self.client.session_transaction() as sess:
            self.assertIn('_user_id', sess)
            self.assertEqual(int(sess['_user_id']), self.test_user.id)
            
        print("   ✓ Login thành công, session đã lưu user_id")
        print("✅ PASSED\n")
    
    def test_08_login_with_wrong_username(self):
        """Test 8: Login với username sai"""
        print("🧪 Test 8: Kiểm tra login với username sai...")
        response = self.client.post('/auth/login', data={
            'username': 'wronguser',
            'password': 'Admin@123'
        }, follow_redirects=True)
        
        # Kiểm tra session không có user_id
        with self.client.session_transaction() as sess:
            self.assertNotIn('_user_id', sess)
            
        print("✅ PASSED\n")
    
    def test_09_login_with_wrong_password(self):
        """Test 9: Login với password sai"""
        print("🧪 Test 9: Kiểm tra login với password sai...")
        response = self.client.post('/auth/login', data={
            'username': 'Admin',
            'password': 'WrongPassword'
        }, follow_redirects=True)
        
        with self.client.session_transaction() as sess:
            self.assertNotIn('_user_id', sess)
            
        print("✅ PASSED\n")
    
    def test_10_login_with_empty_fields(self):
        """Test 10: Login với fields trống"""
        print("🧪 Test 10: Kiểm tra login với fields trống...")
        response = self.client.post('/auth/login', data={
            'username': '',
            'password': ''
        })
        # Expect 200 (re-render page with errors) or 400 bad request
        self.assertNotEqual(response.status_code, 302) 
        print("✅ PASSED\n")
    
    def test_11_login_with_inactive_user(self):
        """Test 11: Login với user inactive"""
        print("🧪 Test 11: Kiểm tra login với user inactive...")
        
        inactive_user = User(
            username='inactive',
            email='inactive@example.com',
            full_name='Inactive User',
            role='viewer',
            is_active=False
        )
        inactive_user.set_password('InactivePass123')
        db.session.add(inactive_user)
        db.session.commit()
        
        response = self.client.post('/auth/login', data={
            'username': 'inactive',
            'password': 'InactivePass123'
        }, follow_redirects=True)
        
        # FIX: Assert chắc chắn không login được
        with self.client.session_transaction() as sess:
            self.assertNotIn('_user_id', sess)
            
        print("   ✓ User inactive không thể đăng nhập")
        print("✅ PASSED\n")
    
    def test_12_logout_functionality(self):
        """Test 12: Chức năng logout"""
        print("🧪 Test 12: Kiểm tra logout...")
        
        # Login trước
        self.client.post('/auth/login', data={
            'username': 'Admin', 
            'password': 'Admin@123'
        })
        
        # Logout
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verify session cleared
        with self.client.session_transaction() as sess:
            self.assertNotIn('_user_id', sess)

        print("   ✓ Logout thành công, session cleared")
        print("✅ PASSED\n")
    
    def test_13_user_query_by_username(self):
        """Test 13: Query user bằng username"""
        print("🧪 Test 13: Kiểm tra query user by username...")
        
        # FIX: Dùng username 'Admin' do setUp tạo
        user = User.query.filter_by(username='Admin').first()
        
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'Admin')
        print("✅ PASSED\n")
    
    def test_14_user_query_by_email(self):
        """Test 14: Query user bằng email"""
        print("🧪 Test 14: Kiểm tra query user by email...")
        
        user = User.query.filter_by(email='admin@hotel.com').first()
        
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'admin@hotel.com')
        # FIX: username tương ứng là 'Admin'
        self.assertEqual(user.username, 'Admin')
        print("✅ PASSED\n")
    
    def test_15_unique_username_constraint(self):
        """Test 15: Username phải unique"""
        print("🧪 Test 15: Kiểm tra unique username constraint...")
        
        # FIX: Cố tình tạo user trùng 'Admin'
        duplicate_user = User(
            username='Admin', # Trùng với test_user
            email='another@example.com',
            full_name='Another User'
        )
        duplicate_user.set_password('AnotherPass123')
        
        db.session.add(duplicate_user)
        
        # FIX: Bắt đúng exception IntegrityError
        with self.assertRaises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()
        print("   ✓ IntegrityError được raise khi trùng username")
        print("✅ PASSED\n")

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
    
    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print("\n⚠️  SOME TESTS FAILED")
    
    print("="*70 + "\n")
    return result

if __name__ == '__main__':
    result = run_tests_with_custom_output()
    sys.exit(0 if result.wasSuccessful() else 1)
