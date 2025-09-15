from app.models.database import engine, get_db
from sqlalchemy import text

def test_connection():
    print("🔄 Testing database connection...")
    try:
        from app.models.database import engine
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("✅ Database connection successful!")
            assert True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        assert False, f"Database connection failed: {e}"

if __name__ == "__main__":
    test_connection()