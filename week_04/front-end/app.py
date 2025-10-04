import requests
import unittest
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"
BASE_URL_V2 = "http://127.0.0.1:5000/api/v2"

class TestAPI(unittest.TestCase):

    def test_get_books_v1(self):
        response = requests.get(f"{BASE_URL}/getbooks")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_borrows_v1(self):
        response = requests.get(f"{BASE_URL}/getborrows")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_books_v2(self):
        response = requests.get(f"{BASE_URL_V2}/getbooks")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_borrows_v2(self):
        response = requests.get(f"{BASE_URL_V2}/getborrows")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

def interactive_menu():
    while True:
        print("\nChọn một tùy chọn:")
        print("1. Kiểm tra /getbooks (v1)")
        print("2. Kiểm tra /getborrows (v1)")
        print("3. Kiểm tra /getbooks (v2)")
        print("4. Kiểm tra /getborrows (v2)")
        print("5. Chạy tất cả các kiểm thử tự động")
        print("6. Thoát")

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
            response = requests.get(f"{BASE_URL_V2}/getbooks")
            print(f"Trạng thái: {response.status_code}")
            print(f"Phản hồi: {json.dumps(response.json(), indent=2)}")
        elif choice == '4':
            response = requests.get(f"{BASE_URL_V2}/getborrows")
            print(f"Trạng thái: {response.status_code}")
            print(f"Phản hồi: {json.dumps(response.json(), indent=2)}")
        elif choice == '5':
            print("Chạy tất cả các kiểm thử tự động...")
            unittest.main(argv=['first-arg-is-ignored'], exit=False)
        elif choice == '6':
            print("Thoát.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == '__main__':
    interactive_menu()