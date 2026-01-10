from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import secrets
import os

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    api_key = Column(String, unique=True, nullable=False)
    subscription_tier = Column(String, default="free")  # free, pro, enterprise
    usage_count = Column(Integer, default=0)
    monthly_limit = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)

class ContentJob(Base):
    __tablename__ = "content_jobs"
    
    id = Column(Integer, primary_key=True)
    job_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    topic = Column(String, nullable=False)
    status = Column(String, default="processing")  # processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    report_path = Column(String, nullable=True)
    blog_path = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    execution_time = Column(Integer, nullable=True)  # in seconds
    tokens_used = Column(Integer, nullable=True)
    estimated_cost = Column(Float, nullable=True)  # in USD

# Database initialization - use /app/data in Docker, current dir locally
DB_DIR = os.getenv("DB_DIR", ".")
os.makedirs(DB_DIR, exist_ok=True)
DATABASE_PATH = os.path.join(DB_DIR, "ai_content_crew.db")

# Database initialization
engine = create_engine('sqlite:///ai_content_crew.db', echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print(f"✅ Database initialized successfully at: {DATABASE_PATH}")
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"✅ Created tables: {', '.join(tables)}")
        
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise

def generate_api_key():
    """Generate secure API key"""
    return f"acc_{secrets.token_urlsafe(32)}"

# Run this to create tables
if __name__ == "__main__":
    init_db()