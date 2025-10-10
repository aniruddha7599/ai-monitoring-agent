import os
# NEW: Import necessary components from SQLAlchemy
from sqlalchemy import create_engine, Column, BigInteger, String, Integer, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# The engine is the main entry point to the database for SQLAlchemy
engine = create_engine(DATABASE_URL)

# Each instance of the SessionLocal class will be a new database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This Base class will be used as a parent for our database models (the tables)
Base = declarative_base()


# NEW: Define our database table as a Python class
class LLMUsageLog(Base):
    __tablename__ = "llm_usage_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(String, index=True)
    # We use DateTime here for proper timestamp handling
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    latency_ms = Column(Integer)
    cost_usd = Column(Float)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    is_error = Column(Boolean, default=False)