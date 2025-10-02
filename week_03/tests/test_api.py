import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000/api/v1"

def test_books_api():
    """Test the Books API endpoints"""
    print("=== TESTING BOOKS API ===\n")
    
    # Test 1: Add a new book
    print("1. Adding new books...")
    books_data = [
        {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "total_copies": 5
        },
        {
            "title": "Design Patterns",
            "author": "Gang of Four",
            "total_copies": 3
        },
        {
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt",
            "total_copies": 4
        }
    ]
    
    book_ids = []
    for book_data in books_data:
        response = requests.post(f"{BASE_URL}/books", json=book_data)
        print(f"POST /books: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            book_ids.append(data['data']['id'])
            print(f"   Added: {data['data']['title']} (ID: {data['data']['id']})")
        else:
            print(f"   Error: {response.text}")
    print()
    
    # Test 2: Get all books
    print("2. Getting all books...")
    response = requests.get(f"{BASE_URL}/books")
    print(f"GET /books: {response.status_code}")
    if response.status_code == 200:
        books = response.json()['data']
        print(f"   Found {len(books)} books:")
        for book in books:
            print(f"   - {book['title']} by {book['author']} ({book['available_copies']}/{book['total_copies']} available)")
    print()
    
    # Test 3: Get specific book
    if book_ids:
        print(f"3. Getting book with ID {book_ids[0]}...")
        response = requests.get(f"{BASE_URL}/books/{book_ids[0]}")
        print(f"GET /books/{book_ids[0]}: {response.status_code}")
        if response.status_code == 200:
            book = response.json()['data']
            print(f"   {book['title']} by {book['author']}")
        print()
    
    # Test 4: Update book
    if book_ids:
        print(f"4. Updating book with ID {book_ids[0]}...")
        update_data = {
            "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
            "total_copies": 6
        }
        response = requests.put(f"{BASE_URL}/books/{book_ids[0]}", json=update_data)
        print(f"PUT /books/{book_ids[0]}: {response.status_code}")
        if response.status_code == 200:
            print(f"   Updated successfully")
        print()
    
    return book_ids

def test_borrows_api(book_ids):
    """Test the Borrows API endpoints"""
    print("=== TESTING BORROWS API ===\n")
    
    if not book_ids:
        print("No books available for borrowing tests")
        return []
    
    # Test 1: Borrow books
    print("1. Borrowing books...")
    borrow_data = [
        {"user_id": 1, "book_id": book_ids[0]},
        {"user_id": 2, "book_id": book_ids[0]},
        {"user_id": 1, "book_id": book_ids[1] if len(book_ids) > 1 else book_ids[0]}
    ]
    
    borrow_ids = []
    for borrow in borrow_data:
        response = requests.post(f"{BASE_URL}/borrows", json=borrow)
        print(f"POST /borrows (user {borrow['user_id']}, book {borrow['book_id']}): {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            borrow_ids.append(data['data']['borrow_id'])
            print(f"   Borrowed successfully (Borrow ID: {data['data']['borrow_id']})")
        else:
            print(f"   Error: {response.text}")
    print()
    
    # Test 2: Get all borrows
    print("2. Getting all borrow records...")
    response = requests.get(f"{BASE_URL}/borrows")
    print(f"GET /borrows: {response.status_code}")
    if response.status_code == 200:
        borrows = response.json()['data']
        print(f"   Found {len(borrows)} borrow records:")
        for borrow in borrows:
            print(f"   - User {borrow['user_id']} borrowed '{borrow['book_title']}' ({borrow['status']})")
    print()
    
    # Test 3: Return a book
    if borrow_ids:
        print(f"3. Returning book (Borrow ID: {borrow_ids[0]})...")
        response = requests.put(f"{BASE_URL}/borrows/{borrow_ids[0]}/return")
        print(f"PUT /borrows/{borrow_ids[0]}/return: {response.status_code}")
        if response.status_code == 200:
            print(f"   Book returned successfully")
        print()
    
    # Test 4: Get borrows filtered by user
    print("4. Getting borrows for user 1...")
    response = requests.get(f"{BASE_URL}/borrows?user_id=1")
    print(f"GET /borrows?user_id=1: {response.status_code}")
    if response.status_code == 200:
        borrows = response.json()['data']
        print(f"   User 1 has {len(borrows)} borrow records")
    print()
    
    return borrow_ids

def test_error_cases():
    """Test error handling"""
    print("=== TESTING ERROR CASES ===\n")
    
    # Test 1: Get non-existent book
    print("1. Getting non-existent book...")
    response = requests.get(f"{BASE_URL}/books/999")
    print(f"GET /books/999: {response.status_code}")
    if response.status_code == 404:
        print("   Correctly returned 404 for non-existent book")
    print()
    
    # Test 2: Add book with missing data
    print("2. Adding book with missing data...")
    response = requests.post(f"{BASE_URL}/books", json={"title": "Incomplete Book"})
    print(f"POST /books (missing author): {response.status_code}")
    if response.status_code == 400:
        print("   Correctly returned 400 for missing data")
    print()
    
    # Test 3: Borrow non-existent book
    print("3. Borrowing non-existent book...")
    response = requests.post(f"{BASE_URL}/borrows", json={"user_id": 1, "book_id": 999})
    print(f"POST /borrows (non-existent book): {response.status_code}")
    if response.status_code == 404:
        print("   Correctly returned 404 for non-existent book")
    print()

def main():
    """Run all tests"""
    print("Starting API Tests...\n")
    
    try:
        # Test if server is running
        response = requests.get(f"{BASE_URL}/books")
        if response.status_code != 200:
            print("Server might not be running. Please start the Flask app first.")
            return
    except requests.exceptions.ConnectionError:
        print("Cannot connect to server. Please make sure the Flask app is running at http://localhost:5000")
        return
    
    # Run tests
    book_ids = test_books_api()
    borrow_ids = test_borrows_api(book_ids)
    test_error_cases()
    
    print("=== TEST SUMMARY ===")
    print("All tests completed!")
    print("Check the output above for any failures.")

if __name__ == "__main__":
    main()