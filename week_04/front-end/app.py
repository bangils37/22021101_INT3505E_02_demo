import requests
import unittest
import json

BASE_URL_V1 = "http://127.0.0.1:5000/api/v1"

class TestAPI(unittest.TestCase):

    def test_get_books_pagination(self):
        print("\nKiểm tra GET /books với phân trang...")
        response = requests.get(f"{BASE_URL_V1}/books?page=1&page_size=2")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 2)
        print(f"Phản hồi: {json.dumps(data, indent=2)}")

    def test_search_books_by_title(self):
        print("\nKiểm tra GET /books?title=...")
        response = requests.get(f"{BASE_URL_V1}/books?title=The Lord of the Rings")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertGreater(len(data['data']), 0)
        self.assertIn('The Lord of the Rings', [book['title'] for book in data['data']])
        print(f"Phản hồi: {json.dumps(data, indent=2)}")

    def test_search_books_by_author(self):
        print("\nKiểm tra GET /books?author=...")
        response = requests.get(f"{BASE_URL_V1}/books?author=Jane")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertGreater(len(data['data']), 0)
        self.assertIn('Pride and Prejudice', [book['title'] for book in data['data']])
        print(f"Phản hồi: {json.dumps(data, indent=2)}")

    def test_get_user_borrows(self):
        print("\nKiểm tra GET /users/{id}/borrows...")
        response = requests.get(f"{BASE_URL_V1}/users/1/borrows")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertGreater(len(data['data']), 0)
        print(f"Phản hồi: {json.dumps(data, indent=2)}")

def interactive_menu():
    while True:
        print("\nChọn một tùy chọn:")
        print("1. Kiểm tra GET /books với phân trang")
        print("2. Kiểm tra GET /books?title=...")
        print("3. Kiểm tra GET /books?author=...")
        print("4. Kiểm tra GET /users/{id}/borrows")
        print("5. Chạy tất cả các kiểm thử tự động")
        print("6. Thoát")

        choice = input("Nhập lựa chọn của bạn: ")

        if choice == '1':
            TestAPI().test_get_books_pagination()
        elif choice == '2':
            TestAPI().test_search_books_by_title()
        elif choice == '3':
            TestAPI().test_search_books_by_author()
        elif choice == '4':
            TestAPI().test_get_user_borrows()
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