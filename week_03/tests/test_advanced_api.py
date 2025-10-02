#!/usr/bin/env python3
"""
Advanced API Testing Script with Pagination, Filtering & Sorting
Tests the enhanced Library Management API endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000/api/v1"

def test_server_connection():
    """Test if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/books?limit=1")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def print_response(title, response):
    """Helper function to print formatted response"""
    print(f"\n{'='*50}")
    print(f"🧪 {title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Message: {data.get('message')}")
        
        # Print pagination info if available
        if 'pagination' in data:
            pagination = data['pagination']
            print(f"📄 Pagination: Page {pagination['page']}/{pagination['total_pages']}, Total: {pagination['total_items']}")
        
        # Print filters if available
        if 'filters' in data:
            filters = data['filters']
            active_filters = {k: v for k, v in filters.items() if v is not None}
            if active_filters:
                print(f"🔍 Active Filters: {active_filters}")
        
        # Print sorting if available
        if 'sorting' in data:
            sorting = data['sorting']
            print(f"📊 Sorting: {sorting['sort']} ({sorting['order']})")
        
        # Print sample data
        if 'data' in data and data['data']:
            print(f"📋 Sample Data ({len(data['data'])} items):")
            for i, item in enumerate(data['data'][:2]):  # Show first 2 items
                print(f"  {i+1}. {item}")
    else:
        print(f"Error: {response.text}")

def test_books_pagination():
    """Test books pagination"""
    print("\n🔥 TESTING BOOKS PAGINATION")
    
    # Test basic pagination
    test_cases = [
        {"params": {"page": 1, "limit": 2}, "description": "Page 1, Limit 2"},
        {"params": {"page": 2, "limit": 2}, "description": "Page 2, Limit 2"},
        {"params": {"offset": 1, "limit": 2}, "description": "Offset 1, Limit 2"},
    ]
    
    for case in test_cases:
        response = requests.get(f"{BASE_URL}/books", params=case["params"])
        print_response(case["description"], response)

def test_books_filtering():
    """Test books filtering"""
    print("\n🔥 TESTING BOOKS FILTERING")
    
    test_cases = [
        {"params": {"author": "Robert"}, "description": "Filter by Author 'Robert'"},
        {"params": {"title": "Clean"}, "description": "Filter by Title containing 'Clean'"},
        {"params": {"status": "available"}, "description": "Filter by Status 'available'"},
        {"params": {"author": "Martin", "status": "available"}, "description": "Multiple filters: Author + Status"},
    ]
    
    for case in test_cases:
        response = requests.get(f"{BASE_URL}/books", params=case["params"])
        print_response(case["description"], response)

def test_books_sorting():
    """Test books sorting"""
    print("\n🔥 TESTING BOOKS SORTING")
    
    test_cases = [
        {"params": {"sort": "title", "order": "asc"}, "description": "Sort by Title (ASC)"},
        {"params": {"sort": "author", "order": "desc"}, "description": "Sort by Author (DESC)"},
        {"params": {"sort": "available_copies", "order": "desc"}, "description": "Sort by Available Copies (DESC)"},
    ]
    
    for case in test_cases:
        response = requests.get(f"{BASE_URL}/books", params=case["params"])
        print_response(case["description"], response)

def test_books_combined():
    """Test combined pagination + filtering + sorting"""
    print("\n🔥 TESTING BOOKS COMBINED FEATURES")
    
    test_cases = [
        {
            "params": {
                "author": "Martin",
                "sort": "title", 
                "order": "asc",
                "page": 1,
                "limit": 5
            }, 
            "description": "Combined: Filter by author + Sort by title + Pagination"
        },
        {
            "params": {
                "status": "available",
                "sort": "available_copies", 
                "order": "desc",
                "limit": 3
            }, 
            "description": "Combined: Available books + Sort by copies + Limit 3"
        }
    ]
    
    for case in test_cases:
        response = requests.get(f"{BASE_URL}/books", params=case["params"])
        print_response(case["description"], response)

def test_borrows_pagination():
    """Test borrows pagination"""
    print("\n🔥 TESTING BORROWS PAGINATION")
    
    test_cases = [
        {"params": {"page": 1, "limit": 2}, "description": "Page 1, Limit 2"},
        {"params": {"sort": "borrow_date", "order": "asc"}, "description": "Sort by Borrow Date (ASC)"},
    ]
    
    for case in test_cases:
        response = requests.get(f"{BASE_URL}/borrows", params=case["params"])
        print_response(case["description"], response)

def test_borrows_filtering():
    """Test borrows filtering"""
    print("\n🔥 TESTING BORROWS FILTERING")
    
    test_cases = [
        {"params": {"user_id": 1}, "description": "Filter by User ID 1"},
        {"params": {"status": "borrowed"}, "description": "Filter by Status 'borrowed'"},
        {"params": {"user_id": 1, "status": "borrowed"}, "description": "Multiple filters: User + Status"},
    ]
    
    for case in test_cases:
        response = requests.get(f"{BASE_URL}/borrows", params=case["params"])
        print_response(case["description"], response)

def test_edge_cases():
    """Test edge cases and validation"""
    print("\n🔥 TESTING EDGE CASES")
    
    test_cases = [
        {"params": {"limit": 1000}, "description": "Large limit (should cap at 100)"},
        {"params": {"page": -1}, "description": "Negative page (should default to 1)"},
        {"params": {"sort": "invalid_field"}, "description": "Invalid sort field (should default)"},
        {"params": {"order": "invalid_order"}, "description": "Invalid order (should default)"},
    ]
    
    for case in test_cases:
        response = requests.get(f"{BASE_URL}/books", params=case["params"])
        print_response(case["description"], response)

def main():
    print("🚀 Starting Advanced API Tests...")
    print("Testing Pagination, Filtering & Sorting features")
    
    # Check server connection
    if not test_server_connection():
        print("❌ Cannot connect to server. Please make sure the Flask app is running at http://localhost:5000")
        return
    
    print("✅ Server is running!")
    
    # Run all tests
    test_books_pagination()
    test_books_filtering() 
    test_books_sorting()
    test_books_combined()
    test_borrows_pagination()
    test_borrows_filtering()
    test_edge_cases()
    
    print(f"\n{'='*50}")
    print("🎉 All Advanced API Tests Completed!")
    print("📖 Example URLs you can try:")
    print("• GET /api/v1/books?page=1&limit=2&author=Robert&sort=title&order=asc")
    print("• GET /api/v1/books?status=available&sort=available_copies&order=desc")
    print("• GET /api/v1/borrows?user_id=1&status=borrowed&sort=borrow_date&order=desc")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()