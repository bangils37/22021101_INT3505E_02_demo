import requests
import unittest
import json

BASE_URL_V4 = "http://127.0.0.1:5000/api/v4"

class TestAPI(unittest.TestCase):

    def test_get_books_v4_caching(self):
        # First request
        response1 = requests.get(f"{BASE_URL_V4}/books")
        self.assertEqual(response1.status_code, 200)
        self.assertIn('ETag', response1.headers)
        self.assertIn('Cache-Control', response1.headers)

        etag = response1.headers['ETag']

        # Second request with If-None-Match
        response2 = requests.get(f"{BASE_URL_V4}/books", headers={'If-None-Match': etag})
        self.assertEqual(response2.status_code, 304)

    def test_get_borrows_v4_caching(self):
        # First request
        response1 = requests.get(f"{BASE_URL_V4}/borrows")
        self.assertEqual(response1.status_code, 200)
        self.assertIn('ETag', response1.headers)
        self.assertIn('Cache-Control', response1.headers)

        etag = response1.headers['ETag']

        # Second request with If-None-Match
        response2 = requests.get(f"{BASE_URL_V4}/borrows", headers={'If-None-Match': etag})
        self.assertEqual(response2.status_code, 304)

def interactive_menu():
    while True:
        print("\nChọn một tùy chọn:")
        print("1. Kiểm tra /books (v4) với caching")
        print("2. Kiểm tra /borrows (v4) với caching")
        print("3. Chạy tất cả các kiểm thử tự động")
        print("4. Thoát")

        choice = input("Nhập lựa chọn của bạn: ")

        if choice == '1':
            print("Kiểm tra /books (v4) với caching...")
            response1 = requests.get(f"{BASE_URL_V4}/books")
            print(f"Yêu cầu 1 - Trạng thái: {response1.status_code}")
            print(f"Yêu cầu 1 - Phản hồi: {json.dumps(response1.json(), indent=2)}")
            if 'ETag' in response1.headers:
                etag = response1.headers['ETag']
                print(f"ETag từ yêu cầu 1: {etag}")
                response2 = requests.get(f"{BASE_URL_V4}/books", headers={'If-None-Match': etag})
                print(f"Yêu cầu 2 (If-None-Match) - Trạng thái: {response2.status_code}")
                if response2.status_code == 304:
                    print("Phản hồi 304 Not Modified nhận được như mong đợi.")
                else:
                    print(f"Yêu cầu 2 - Phản hồi: {json.dumps(response2.json(), indent=2)}")
            else:
                print("Không tìm thấy ETag trong phản hồi đầu tiên.")
        elif choice == '2':
            print("Kiểm tra /borrows (v4) với caching...")
            response1 = requests.get(f"{BASE_URL_V4}/borrows")
            print(f"Yêu cầu 1 - Trạng thái: {response1.status_code}")
            print(f"Yêu cầu 1 - Phản hồi: {json.dumps(response1.json(), indent=2)}")
            if 'ETag' in response1.headers:
                etag = response1.headers['ETag']
                print(f"ETag từ yêu cầu 1: {etag}")
                response2 = requests.get(f"{BASE_URL_V4}/borrows", headers={'If-None-Match': etag})
                print(f"Yêu cầu 2 (If-None-Match) - Trạng thái: {response2.status_code}")
                if response2.status_code == 304:
                    print("Phản hồi 304 Not Modified nhận được như mong đợi.")
                else:
                    print(f"Yêu cầu 2 - Phản hồi: {json.dumps(response2.json(), indent=2)}")
            else:
                print("Không tìm thấy ETag trong phản hồi đầu tiên.")
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