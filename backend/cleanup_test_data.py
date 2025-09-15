from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.learning_session import LearningSession
from app.models.quiz import QuizQuestion, QuizResponse
from app.models.learning_progress import LearningProgress

def cleanup_test_data():
    """Clean up all test data"""
    print("🧹 Cleaning up test data...")
    db = next(get_db())
    
    try:
        # Delete in reverse order of dependencies
        print("Deleting quiz responses...")
        db.query(QuizResponse).delete()
        
        print("Deleting quiz questions...")
        db.query(QuizQuestion).delete()
        
        print("Deleting learning sessions...")
        db.query(LearningSession).delete()
        
        print("Deleting learning progress...")
        db.query(LearningProgress).delete()
        
        print("Deleting user profiles...")
        db.query(UserProfile).delete()
        
        print("Deleting users...")
        db.query(User).delete()
        
        db.commit()
        print("✅ Test data cleaned up successfully!")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_test_data()