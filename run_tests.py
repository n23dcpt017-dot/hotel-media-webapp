"""
RUN ALL TESTS
Script để chạy cả Unit Test và Selenium Test
"""
import subprocess
import sys
import os
from datetime import datetime


def print_header(text):
    """In header đẹp"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def run_unit_tests():
    """Chạy Unit Tests"""
    print_header("🧪 RUNNING UNIT TESTS")
    
    try:
        result = subprocess.run(
            [sys.executable, 'tests/unit_test_login.py'],
            capture_output=False,
            text=True
        )
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running unit tests: {e}")
        return False


def run_selenium_tests():
    """Chạy Selenium Tests"""
    print_header("🌐 RUNNING SELENIUM TESTS")
    
    print("⚠️  LƯU Ý: Đảm bảo Flask app đang chạy ở http://localhost:5000")
    print("   Bạn có thể chạy: python run.py")
    input("\nNhấn Enter khi app đã sẵn sàng...")
    
    try:
        result = subprocess.run(
            [sys.executable, 'tests/selenium_test_login.py'],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\n✅ Selenium tests completed!")
            print("📊 Xem báo cáo tại: selenium_test_report.html")
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running selenium tests: {e}")
        return False


def main():
    """Main function"""
    print_header("🚀 HOTEL MEDIA WEBAPP - TEST SUITE")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check if we're in the right directory
    if not os.path.exists('tests'):
        print("❌ Folder 'tests' không tồn tại!")
        print("💡 Hãy tạo folder 'tests' và copy các file test vào đó.")
        return
    
    print("Chọn test để chạy:")
    print("1. Unit Tests only")
    print("2. Selenium Tests only")
    print("3. All Tests (Unit + Selenium)")
    print("0. Exit")
    
    choice = input("\nLựa chọn của bạn (1/2/3/0): ").strip()
    
    unit_passed = True
    selenium_passed = True
    
    if choice == '1':
        unit_passed = run_unit_tests()
    
    elif choice == '2':
        selenium_passed = run_selenium_tests()
    
    elif choice == '3':
        unit_passed = run_unit_tests()
        if unit_passed:
            selenium_passed = run_selenium_tests()
    
    elif choice == '0':
        print("👋 Bye!")
        return
    
    else:
        print("❌ Lựa chọn không hợp lệ!")
        return
    
    # Print final summary
    print_header("📊 FINAL SUMMARY")
    
    if choice in ['1', '3']:
        status = "✅ PASSED" if unit_passed else "❌ FAILED"
        print(f"Unit Tests: {status}")
    
    if choice in ['2', '3']:
        status = "✅ PASSED" if selenium_passed else "❌ FAILED"
        print(f"Selenium Tests: {status}")
    
    if (choice == '1' and unit_passed) or \
       (choice == '2' and selenium_passed) or \
       (choice == '3' and unit_passed and selenium_passed):
        print("\n🎉 ALL TESTS PASSED! 🎉")
    else:
        print("\n⚠️  SOME TESTS FAILED")
    
    print("\n" + "="*70)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
