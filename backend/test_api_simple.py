def test_app_imports():
    """Test that the app can be imported without errors"""
    print("🔄 Testing app imports...")
    try:
        from app.main import app
        print("✅ Main app imported successfully")
        
        from app.routers import auth, educational, user_profile, ai_educational
        print("✅ All routers imported successfully")
        
        print("✅ All imports successful")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_structure():
    """Test that the app has the expected structure"""
    print("🔄 Testing app structure...")
    try:
        from app.main import app
        
        # Check if app has the expected routes
        routes = [route.path for route in app.routes]
        print(f"Available routes: {len(routes)} routes found")
        
        # Check for key endpoints
        key_endpoints = ["/", "/health", "/api/auth/register", "/api/auth/login", "/api/ai/explain"]
        found_endpoints = []
        
        for endpoint in key_endpoints:
            if endpoint in routes:
                found_endpoints.append(endpoint)
                print(f"✅ {endpoint} found")
            else:
                print(f"❌ {endpoint} not found")
                return False
        
        print(f"✅ All {len(found_endpoints)} key endpoints found")
        return True
        
    except Exception as e:
        print(f"❌ App structure error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("🔄 Testing database connection...")
    try:
        from app.models.database import engine
        from sqlalchemy import text
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful")
            return True
            
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_models_work():
    """Test that models can be created"""
    print("�� Testing model creation...")
    try:
        from app.models.user import User
        from app.models.user_profile import UserProfile
        from app.models.learning_session import LearningSession
        
        # Test creating model instances (without saving to DB)
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashedpassword"
        )
        print("✅ User model works")
        
        profile = UserProfile(
            user_id=1,
            learning_style="visual",
            subjects_of_interest=["Python", "AI"]
        )
        print("✅ UserProfile model works")
        
        session = LearningSession(
            user_id=1,
            topic="Python Basics",
            session_type="explanation",
            content="Test content"
        )
        print("✅ LearningSession model works")
        
        print("✅ All models work correctly")
        return True
        
    except Exception as e:
        print(f"❌ Model creation error: {e}")
        return False

def test_database_tables():
    """Test that database tables can be created"""
    print("🔄 Testing database table creation...")
    try:
        from app.models.database import Base, engine
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Database table creation error: {e}")
        return False

if __name__ == "__main__":
    print("�� Starting ultra-simple API tests...")
    
    success = True
    success &= test_app_imports()
    success &= test_app_structure()
    success &= test_database_connection()
    success &= test_models_work()
    success &= test_database_tables()
    
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed!")