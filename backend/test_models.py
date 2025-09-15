from sqlalchemy.orm import Session
from app.models.database import engine, get_db
from app.models import User, UserProfile, LearningSession, QuizQuestion, QuizResponse, LearningProgress
from sqlalchemy import text
import hashlib
from datetime import datetime

def test_models():
    print("🔄 Creating database tables...")
    try:
        from app.models.database import Base, engine
        from app.models.user import User
        from app.models.user_profile import UserProfile
        from app.models.learning_session import LearningSession
        from app.models.quiz import Quiz
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        assert True
    except Exception as e:
        print(f"❌ Database table creation failed: {e}")
        assert False, f"Database table creation failed: {e}"

if __name__ == "__main__":
    test_models()

# def test_models():
#     """Test all models by creating sample data"""
    
#     # Create all tables
#     print("🔄 Creating database tables...")
#     from app.models.database import Base
#     Base.metadata.create_all(bind=engine)
#     print("✅ Tables created successfully!")
    
#     # Get database session
#     db = next(get_db())
    
#     try:
#         # Test 1: Create a user
#         print("\n🔄 Testing User creation...")
#         test_user = User(
#             username="testuser",
#             email="test@example.com",
#             password_hash=hashlib.sha256("testpassword".encode()).hexdigest()
#         )
#         db.add(test_user)
#         db.commit()
#         db.refresh(test_user)
#         print(f"✅ User created with ID: {test_user.id}")
        
#         # Test 2: Create user profile
#         print("\n🔄 Testing UserProfile creation...")
#         test_profile = UserProfile(
#             user_id=test_user.id,
#             learning_style="visual",
#             difficulty_level="intermediate",
#             subjects_of_interest=["Python", "AI", "Machine Learning"],
#             preferred_explanation_length="detailed"
#         )
#         db.add(test_profile)
#         db.commit()
#         db.refresh(test_profile)
#         print(f"✅ UserProfile created with ID: {test_profile.id}")
        
#         # Test 3: Create learning session
#         print("\n�� Testing LearningSession creation...")
#         test_session = LearningSession(
#             user_id=test_user.id,
#             topic="Python Basics",
#             session_type="explanation",
#             content="Introduction to Python programming",
#             user_input="What is Python?",
#             ai_response="Python is a high-level programming language...",
#             session_data={"difficulty": "beginner", "duration": 300}
#         )
#         db.add(test_session)
#         db.commit()
#         db.refresh(test_session)
#         print(f"✅ LearningSession created with ID: {test_session.id}")
        
#         # Test 4: Create quiz question
#         print("\n🔄 Testing QuizQuestion creation...")
#         test_question = QuizQuestion(
#             session_id=test_session.id,
#             question_text="What is Python primarily used for?",
#             options=["Web development", "Data science", "Game development", "All of the above"],
#             correct_answer=3,  # "All of the above"
#             explanation="Python is versatile and used in many domains",
#             difficulty_level="easy"
#         )
#         db.add(test_question)
#         db.commit()
#         db.refresh(test_question)
#         print(f"✅ QuizQuestion created with ID: {test_question.id}")
        
#         # Test 5: Create quiz response
#         print("\n🔄 Testing QuizResponse creation...")
#         test_response = QuizResponse(
#             question_id=test_question.id,
#             user_id=test_user.id,
#             selected_answer=3,
#             is_correct=True,
#             time_taken=15
#         )
#         db.add(test_response)
#         db.commit()
#         db.refresh(test_response)
#         print(f"✅ QuizResponse created with ID: {test_response.id}")
        
#         # Test 6: Create learning progress
#         print("\n�� Testing LearningProgress creation...")
#         test_progress = LearningProgress(
#             user_id=test_user.id,
#             topic="Python Basics",
#             mastery_level=0.75,
#             total_sessions=1,
#             correct_answers=1,
#             total_questions=1
#         )
#         db.add(test_progress)
#         db.commit()
#         db.refresh(test_progress)
#         print(f"✅ LearningProgress created with ID: {test_progress.id}")
        
#         # Test 7: Test relationships
#         print("\n🔄 Testing relationships...")
        
#         # Test user -> profile relationship
#         user_with_profile = db.query(User).filter(User.id == test_user.id).first()
#         print(f"✅ User profile learning style: {user_with_profile.profile.learning_style}")
        
#         # Test user -> sessions relationship
#         user_sessions = db.query(User).filter(User.id == test_user.id).first()
#         print(f"✅ User has {len(user_sessions.learning_sessions)} learning sessions")
        
#         # Test session -> questions relationship
#         session_questions = db.query(LearningSession).filter(LearningSession.id == test_session.id).first()
#         print(f"✅ Session has {len(session_questions.quiz_questions)} quiz questions")
        
#         print("\n🎉 All model tests passed successfully!")
        
#         # Test 8: Query examples
#         print("\n🔄 Testing query examples...")
        
#         # Find user by email
#         user_by_email = db.query(User).filter(User.email == "test@example.com").first()
#         print(f"✅ Found user by email: {user_by_email.username}")
        
#         # Find sessions by topic
#         python_sessions = db.query(LearningSession).filter(LearningSession.topic.like("%Python%")).all()
#         print(f"✅ Found {len(python_sessions)} Python-related sessions")
        
#         # Find correct quiz responses
#         correct_responses = db.query(QuizResponse).filter(QuizResponse.is_correct == True).all()
#         print(f"✅ Found {len(correct_responses)} correct quiz responses")
        
#         print("\n🎉 All query tests passed successfully!")
        
#     except Exception as e:
#         print(f"❌ Error during testing: {e}")
#         db.rollback()
#         raise
#     finally:
#         db.close()

# def cleanup_test_data():
#     """Clean up test data"""
#     print("\n�� Cleaning up test data...")
#     db = next(get_db())
#     try:
#         # Delete in reverse order of dependencies
#         db.query(QuizResponse).delete()
#         db.query(QuizQuestion).delete()
#         db.query(LearningSession).delete()
#         db.query(LearningProgress).delete()
#         db.query(UserProfile).delete()
#         db.query(User).delete()
#         db.commit()
#         print("✅ Test data cleaned up!")
#     except Exception as e:
#         print(f"❌ Error during cleanup: {e}")
#         db.rollback()
#     finally:
#         db.close()

# if __name__ == "__main__":
#     print("🚀 Starting model tests...")
#     test_models()
    
#     # Uncomment the line below if you want to clean up test data
#     # cleanup_test_data()
    
#     print("\n✨ Model testing completed!")