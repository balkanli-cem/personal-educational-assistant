def test_models_import():
    """Test that all models can be imported without errors"""
    print("🔄 Testing model imports...")
    
    try:
        from app.models.database import Base, engine, get_db
        print("✅ Database imports successful")
        
        from app.models.user import User
        print("✅ User model imported")
        
        from app.models.user_profile import UserProfile
        print("✅ UserProfile model imported")
        
        from app.models.learning_session import LearningSession
        print("✅ LearningSession model imported")
        
        from app.models.quiz import Quiz, QuizQuestion, QuizResponse
        print("✅ Quiz models imported")
        
        from app.models.learning_progress import LearningProgress
        print("✅ LearningProgress model imported")
        
        print("🎉 All model imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_creation():
    """Test that database tables can be created"""
    print("\n🔄 Testing database table creation...")
    
    try:
        from app.models.database import Base, engine
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database creation error: {e}")
        return False

def test_basic_model_creation():
    """Test creating basic model instances"""
    print("\n�� Testing basic model creation...")
    
    try:
        from app.models.user import User
        from app.models.user_profile import UserProfile
        from app.models.learning_session import LearningSession
        from app.models.quiz import Quiz, QuizQuestion, QuizResponse
        from app.models.learning_progress import LearningProgress
        
        # Test User creation
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashedpassword"
        )
        print("✅ User instance created")
        
        # Test UserProfile creation
        profile = UserProfile(
            user_id=1,
            learning_style="visual",
            subjects_of_interest=["Python", "AI"]
        )
        print("✅ UserProfile instance created")
        
        # Test LearningSession creation
        session = LearningSession(
            user_id=1,
            topic="Python Basics",
            session_type="explanation",
            content="Test content"
        )
        print("✅ LearningSession instance created")
        
        # Test Quiz creation
        quiz = Quiz(
            user_id=1,
            topic="Python Quiz",
            questions=["Q1", "Q2"],
            correct_answers=["A1", "A2"]
        )
        print("✅ Quiz instance created")
        
        # Test QuizQuestion creation
        question = QuizQuestion(
            session_id=1,
            question_text="What is Python?",
            options=["Language", "Tool", "Framework", "All"],
            correct_answer="Language"
        )
        print("✅ QuizQuestion instance created")
        
        # Test QuizResponse creation
        response = QuizResponse(
            question_id=1,
            user_id=1,
            selected_answer="Language",
            is_correct="true"
        )
        print("✅ QuizResponse instance created")
        
        # Test LearningProgress creation
        progress = LearningProgress(
            user_id=1,
            topic="Python",
            mastery_level=0.75
        )
        print("✅ LearningProgress instance created")
        
        print("🎉 All model instances created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Model creation error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting model tests...")
    
    success = True
    success &= test_models_import()
    success &= test_database_creation()
    success &= test_basic_model_creation()
    
    if success:
        print("\n🎉 All model tests passed!")
    else:
        print("\n❌ Some model tests failed!")