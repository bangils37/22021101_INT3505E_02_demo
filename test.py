import requests
import json

BASE_URL = "http://localhost:5000"

def register_user(username, password):
    url = f"{BASE_URL}/register"
    headers = {"Content-Type": "application/json"}
    data = {"username": username, "password": password}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Register User ({username}): {response.status_code} - {response.text}")
    return response

def login_user(username, password):
    url = f"{BASE_URL}/login"
    headers = {"Content-Type": "application/json"}
    data = {"username": username, "password": password}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Login User ({username}): {response.status_code} - {response.text}")
    if response.status_code == 200:
        return response.json().get("accessToken")
    return None

def get_books(token):
    url = f"{BASE_URL}/books"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"Get Books: {response.status_code} - {response.text}")
    return response

if __name__ == "__main__":
    test_username = "testuser"
    test_password = "testpassword"

    # 1. Register a new user
    print("\n--- Registering User ---")
    register_user(test_username, test_password)

    # 2. Login user and get JWT token
    print("\n--- Logging in User ---")
    access_token = login_user(test_username, test_password)

    if access_token:
        print(f"Access Token: {access_token}")
        # 3. Access protected /books endpoint with token
        print("\n--- Accessing Protected /books Endpoint ---")
        get_books(access_token)

        # Test with invalid token (optional)
        print("\n--- Accessing Protected /books Endpoint with INVALID Token ---")
        get_books("invalid_token")

        # Test with expired token (requires waiting for 1 minute, as expiresIn is 1m)
        # print("\n--- Waiting for token to expire (1 minute) ---")
        # import time
        # time.sleep(65) # Wait for 65 seconds to ensure token expires
        # print("\n--- Accessing Protected /books Endpoint with EXPIRED Token ---")
        # get_books(access_token)

    else:
        print("Login failed, cannot proceed with /books test.")