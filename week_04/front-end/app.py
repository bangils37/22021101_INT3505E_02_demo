import requests
import unittest
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"
BASE_URL_V2 = "http://127.0.0.1:5000/api/v2"
BASE_URL_V3 = "http://127.0.0.1:5000/api/v3"

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

    def test_get_books_v3_caching(self):
        # First request
        response1 = requests.get(f"{BASE_URL_V3}/getbooks")
        self.assertEqual(response1.status_code, 200)
        self.assertIn('ETag', response1.headers)
        self.assertIn('Cache-Control', response1.headers)

        etag = response1.headers['ETag']

        # Second request with If-None-Match
        response2 = requests.get(f"{BASE_URL_V3}/getbooks", headers={'If-None-Match': etag})
        self.assertEqual(response2.status_code, 304)

    def test_get_borrows_v3_caching(self):
        # First request
        response1 = requests.get(f"{BASE_URL_V3}/getborrows")
        self.assertEqual(response1.status_code, 200)
        self.assertIn('ETag', response1.headers)
        self.assertIn('Cache-Control', response1.headers)

        etag = response1.headers['ETag']

        # Second request with If-None-Match
        response2 = requests.get(f"{BASE_URL_V3}/getborrows", headers={'If-None-Match': etag})
        self.assertEqual(response2.status_code, 304)

def interactive_menu():
    while True:
        print("\nChọn một tùy chọn:")
        print("1. Kiểm tra /getbooks (v1)")
        print("2. Kiểm tra /getborrows (v1)")
        print("3. Kiểm tra /getbooks (v2)")
        print("4. Kiểm tra /getborrows (v2)")
        print("5. Kiểm tra /getbooks (v3) với caching")
        print("6. Kiểm tra /getborrows (v3) với caching")
        print("7. Chạy tất cả các kiểm thử tự động")
        print("8. Thoát")

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
            print("Kiểm tra /getbooks (v3) với caching...")
            response1 = requests.get(f"{BASE_URL_V3}/getbooks")
            print(f"Yêu cầu 1 - Trạng thái: {response1.status_code}")
            print(f"Yêu cầu 1 - Phản hồi: {json.dumps(response1.json(), indent=2)}")
            if 'ETag' in response1.headers:
                etag = response1.headers['ETag']
                print(f"ETag từ yêu cầu 1: {etag}")
                response2 = requests.get(f"{BASE_URL_V3}/getbooks", headers={'If-None-Match': etag})
                print(f"Yêu cầu 2 (If-None-Match) - Trạng thái: {response2.status_code}")
                if response2.status_code == 304:
                    print("Phản hồi 304 Not Modified nhận được như mong đợi.")
                else:
                    print(f"Yêu cầu 2 - Phản hồi: {json.dumps(response2.json(), indent=2)}")
            else:
                print("Không tìm thấy ETag trong phản hồi đầu tiên.")
        elif choice == '6':
            print("Kiểm tra /getborrows (v3) với caching...")
            response1 = requests.get(f"{BASE_URL_V3}/getborrows")
            print(f"Yêu cầu 1 - Trạng thái: {response1.status_code}")
            print(f"Yêu cầu 1 - Phản hồi: {json.dumps(response1.json(), indent=2)}")
            if 'ETag' in response1.headers:
                etag = response1.headers['ETag']
                print(f"ETag từ yêu cầu 1: {etag}")
                response2 = requests.get(f"{BASE_URL_V3}/getborrows", headers={'If-None-Match': etag})
                print(f"Yêu cầu 2 (If-None-Match) - Trạng thái: {response2.status_code}")
                if response2.status_code == 304:
                    print("Phản hồi 304 Not Modified nhận được như mong đợi.")
                else:
                    print(f"Yêu cầu 2 - Phản hồi: {json.dumps(response2.json(), indent=2)}")
            else:
                print("Không tìm thấy ETag trong phản hồi đầu tiên.")
        elif choice == '7':
            print("Chạy tất cả các kiểm thử tự động...")
            unittest.main(argv=['first-arg-is-ignored'], exit=False)
        elif choice == '8':
            print("Thoát.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == '__main__':
    interactive_menu()