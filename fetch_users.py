import requests
import json

BASE_URL = "http://localhost:8000"

def get_users():
    """Fetch all users from the API"""
    try:
        response = requests.get(f"{BASE_URL}/users/")
        response.raise_for_status()
        users = response.json()
        print(f"Successfully retrieved {len(users)} users:")
        print(json.dumps(users, indent=2))
        return users
    except requests.exceptions.RequestException as e:
        print(f"Error fetching users: {e}")
        return []

def create_user(name):
    """Create a new user"""
    try:
        response = requests.post(f"{BASE_URL}/users/", json={"name": name})
        response.raise_for_status()
        user = response.json()
        print(f"Successfully created user: {user}")
        return user
    except requests.exceptions.RequestException as e:
        print(f"Error creating user: {e}")
        return None

if __name__ == "__main__":
    print("--- Fetching Users ---")
    get_users()
