import requests
import json
import asyncio
import time

# Base URL for your API
BASE_URL = "http://localhost:8000"

def get_auth_headers():
    """Get authentication headers for API calls"""
    # First, register a test user
    user_data = {
        "username": "aitestuser",
        "email": "aitest@example.com",
        "password": "testpassword123"
    }
    
    # Try to register (might fail if user exists)
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print(f"Registration attempt: {response.status_code}")
    
    # Login to get token
    login_data = {
        "email": "aitest@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"Login: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    else:
        print(f"Login failed: {response.json()}")
        return None

def test_ai_endpoints():
    print("🚀 Testing AI Educational Endpoints...")
    
    # Get authentication headers
    headers = get_auth_headers()
    if not headers:
        print("❌ Failed to authenticate. Cannot test AI endpoints.")
        return
    
    print("\n" + "="*50)
    print("TESTING AI EXPLANATION ENDPOINT")
    print("="*50)
    
    # Test 1: AI Explanation
    explanation_data = {
        "topic": "Python Functions",
        "user_input": "What are functions in Python and how do I use them?"
    }
    
    print(f"\n🔄 Testing AI explanation for: {explanation_data['topic']}")
    response = requests.post(f"{BASE_URL}/api/ai/explain", json=explanation_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Explanation generated successfully!")
        print(f"Session ID: {result['session_id']}")
        print(f"Personalized for: {result['personalized_for']}")
        print(f"Explanation preview: {result['explanation'][:200]}...")
    else:
        print(f"❌ Error: {response.json()}")
    
    print("\n" + "="*50)
    print("TESTING AI QUIZ GENERATION")
    print("="*50)
    
    # Test 2: AI Quiz Generation
    quiz_data = {
        "topic": "Python Functions",
        "difficulty_level": "beginner",
        "num_questions": 3
    }
    
    print(f"\n🔄 Testing AI quiz generation for: {quiz_data['topic']}")
    response = requests.post(f"{BASE_URL}/api/ai/quiz/generate", json=quiz_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Quiz generated successfully!")
        print(f"Session ID: {result['session_id']}")
        print(f"Number of questions: {len(result['questions'])}")
        
        # Display first question
        if result['questions']:
            first_q = result['questions'][0]
            print(f"\nSample Question: {first_q['question']}")
            print(f"Options: {first_q['options']}")
            print(f"Explanation: {first_q['explanation']}")
    else:
        print(f"❌ Error: {response.json()}")
    
    print("\n" + "="*50)
    print("TESTING AI LEARNING PATH GENERATION")
    print("="*50)
    
    # Test 3: AI Learning Path
    learning_path_data = {
        "topic": "Machine Learning",
        "current_level": "beginner",
        "learning_goals": ["Understand basic concepts", "Learn about algorithms", "Build a simple model"]
    }
    
    print(f"\n🔄 Testing AI learning path for: {learning_path_data['topic']}")
    response = requests.post(f"{BASE_URL}/api/ai/learning-path", json=learning_path_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Learning path generated successfully!")
        print(f"Topic: {result.get('topic', 'N/A')}")
        print(f"Current Level: {result.get('current_level', 'N/A')}")
        print(f"Number of modules: {len(result.get('modules', []))}")
        print(f"Total estimated time: {result.get('total_estimated_time', 'N/A')}")
        
        # Display first module
        if result.get('modules'):
            first_module = result['modules'][0]
            print(f"\nSample Module: {first_module.get('title', 'N/A')}")
            print(f"Description: {first_module.get('description', 'N/A')}")
            print(f"Duration: {first_module.get('duration', 'N/A')}")
    else:
        print(f"❌ Error: {response.json()}")
    
    print("\n" + "="*50)
    print("TESTING AI ANSWER EVALUATION")
    print("="*50)
    
    # Test 4: AI Answer Evaluation (if we have a question from quiz generation)
    if 'result' in locals() and result.get('questions'):
        question_id = result['questions'][0]['id']
        user_answer = 0  # User selects first option
        
        print(f"\n🔄 Testing AI answer evaluation for question ID: {question_id}")
        response = requests.post(
            f"{BASE_URL}/api/ai/evaluate?question_id={question_id}&user_answer={user_answer}",
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            eval_result = response.json()
            print("✅ Answer evaluation completed!")
            print(f"Is correct: {eval_result['is_correct']}")
            print(f"Feedback: {eval_result['feedback'][:200]}...")
            print(f"Correct answer: {eval_result['correct_answer']}")
        else:
            print(f"❌ Error: {response.json()}")
    
    print("\n" + "="*50)
    print("AI ENDPOINT TESTING COMPLETED")
    print("="*50)

def test_health_check():
    """Test basic API health"""
    print("🔄 Testing API health...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    return response.status_code == 200

if __name__ == "__main__":
    print("�� Starting AI Endpoint Tests...")
    
    # Test health first
    if not test_health_check():
        print("❌ API is not healthy. Please check if the server is running.")
        exit(1)
    
    # Test AI endpoints
    test_ai_endpoints()
    
    print("\n✨ AI endpoint testing completed!")