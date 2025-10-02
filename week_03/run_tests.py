#!/usr/bin/env python3
"""
Test Runner Script
Runs all test suites for the Library Management API
"""

import sys
import os
import importlib.util
import subprocess

def run_test_file(test_file_path, test_name):
    """Run a specific test file"""
    print(f"\n{'='*60}")
    print(f"🧪 Running {test_name}")
    print(f"{'='*60}")
    
    try:
        # Try to run the test file
        result = subprocess.run([
            sys.executable, test_file_path
        ], capture_output=True, text=True, cwd=os.path.dirname(test_file_path))
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {test_name} completed successfully!")
        else:
            print(f"❌ {test_name} failed with exit code {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running {test_name}: {e}")
        return False

def check_server():
    """Check if Flask server is running"""
    import requests
    try:
        response = requests.get("http://localhost:5000/api/v1/books?limit=1", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main test runner function"""
    print("🚀 Library Management API - Test Suite Runner")
    print("=" * 60)
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.join(current_dir, "tests")
    
    # Check if server is running
    print("🔍 Checking if Flask server is running...")
    if not check_server():
        print("⚠️  Flask server is not running at http://localhost:5000")
        print("   Please start the server with: python app.py")
        print("   Then run this test suite again.")
        return
    
    print("✅ Server is running!")
    
    # Test files to run in order
    test_files = [
        ("test_api.py", "Basic API Tests"),
        ("test_basic_api.py", "Basic API Tests (Alternative)"),
        ("test_advanced_api.py", "Advanced Features Tests (Pagination, Filtering, Sorting)")
    ]
    
    results = []
    
    for test_file, test_name in test_files:
        test_path = os.path.join(tests_dir, test_file)
        
        if os.path.exists(test_path):
            success = run_test_file(test_path, test_name)
            results.append((test_name, success))
        else:
            print(f"⚠️  Test file not found: {test_path}")
            results.append((test_name, False))
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    failed = 0
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {len(results)} test suites")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {failed} test suite(s) failed")
    
    print(f"\n📋 Available test commands:")
    print(f"• python tests/test_api.py - Basic API tests")
    print(f"• python tests/test_basic_api.py - Alternative basic tests")
    print(f"• python tests/test_advanced_api.py - Advanced features tests")
    print(f"• python run_tests.py - Run all tests (this script)")

if __name__ == "__main__":
    main()