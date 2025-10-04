import requests
import unittest
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

class TestAPI(unittest.TestCase):

    def test_get_books(self):
        response = requests.get(f"{BASE_URL}/getbooks")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_borrows(self):
        response = requests.get(f"{BASE_URL}/getborrows")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

def interactive_menu():
    while True:
        print("\nChọn một tùy chọn:")
        print("1. Kiểm tra /getbooks")
        print("2. Kiểm tra /getborrows")
        print("3. Chạy tất cả các kiểm thử tự động")
        print("4. Thoát")

        choice = input("Nhập lựa chọn của bạn: ")

        if choice == '1':
            response = requests.get(f"{BASE_URL}/getbooks")
            print(f"Trạng thái: {response.status_code}")
            print(f"Phản hồi: {json.dumps(response.json(), indent=2)}")
        elif choice == '2':
            response = requests.get(f"{BASE_URL}/getborrows")
            print(f"Trạng thái: {response.status_code}")
            print(f"Phản hồi: {json.dumps(response.json(), indent=2)}")
        elif choice == '3':
            print("Chạy tất cả các kiểm thử tự động...")
            unittest.main(argv=['first-arg-is-ignored'], exit=False)
        elif choice == '4':
            print("Thoát.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == '__main__':
    interactive_menu()