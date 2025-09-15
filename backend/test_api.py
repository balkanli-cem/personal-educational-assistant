import requests
import json

# Base URL for your API
BASE_URL = "http://localhost:8000"

def test_api():
    print("🚀 Testing API endpoints...")
    
    # Test 1: Health check
    print("\n🔄 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    
    # Test 2: Register a user
    print("\n🔄 Testing user registration...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print(f"Registration: {response.status_code} - {response.json()}")
    
    # Test 3: Login
    print("\n🔄 Testing user login...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"Login: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test 4: Get user profile
        print("\n🔄 Testing get user profile...")
        response = requests.get(f"{BASE_URL}/api/profile/", headers=headers)
        print(f"Profile: {response.status_code} - {response.json()}")
        
        # Test 5: Create learning session
        print("\n🔄 Testing create learning session...")
        session_data = {
            "topic": "Python Basics",
            "session_type": "explanation",
            "content": "Introduction to Python programming",
            "user_input": "What is Python?"
        }
        response = requests.post(f"{BASE_URL}/api/educational/session", json=session_data, headers=headers)
        print(f"Session: {response.status_code} - {response.json()}")
        
        if response.status_code == 200:
            session_id = response.json()["id"]
            
            # Test 6: Create quiz question
            print("\n🔄 Testing create quiz question...")
            question_data = {
                "session_id": session_id,
                "question_text": "What is Python?",
                "options": ["A programming language", "A snake", "A type of coffee", "All of the above"],
                "correct_answer": 3,
                "explanation": "Python is a programming language",
                "difficulty_level": "easy"
            }
            response = requests.post(f"{BASE_URL}/api/educational/quiz/question", json=question_data, headers=headers)
            print(f"Question: {response.status_code} - {response.json()}")
    
    print("\n✨ API testing completed!")

if __name__ == "__main__":
    test_api()