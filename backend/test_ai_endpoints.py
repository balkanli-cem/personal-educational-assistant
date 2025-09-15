import requests
import json

BASE_URL = "http://localhost:8000"

def get_auth_headers():
    """Get authentication headers for API calls"""
    # First, try to register a user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    print("Registration attempt:", end=" ")
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print(response.status_code)
    
    if response.status_code != 200:
        print(f"Registration failed: {response.text}")
        return None
    
    # Then login
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    print("Login:", end=" ")
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    print(response.status_code)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        return {"Authorization": f"Bearer {token}"}
    else:
        print(f"Login failed: {response.text}")
        return None

def test_ai_endpoints():
    print("🚀 Testing AI Educational Endpoints...")
    
    # Get authentication headers
    headers = get_auth_headers()
    if not headers:
        print("❌ Could not get authentication headers")
        return False
    
    # Test explanation endpoint
    print("\n🔄 Testing explanation endpoint...")
    explanation_data = {
        "topic": "machine learning",
        "difficulty_level": "beginner",
        "learning_style": "visual"
    }
    response = requests.post(f"{BASE_URL}/api/ai/explain", json=explanation_data, headers=headers)
    print(f"Explanation: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")
    
    # Test quiz generation
    print("\n🔄 Testing quiz generation...")
    quiz_data = {
        "topic": "machine learning",
        "difficulty_level": "beginner",
        "num_questions": 3
    }
    response = requests.post(f"{BASE_URL}/api/ai/generate-quiz", json=quiz_data, headers=headers)
    print(f"Quiz generation: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")
    
    return True

def test_health_check():
    print("🔄 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

if __name__ == "__main__":
    test_ai_endpoints()