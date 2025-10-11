# No longer need the datetime module here
from sqlalchemy import Column, BigInteger, String, Integer, Float, Boolean, DateTime
# NEW: Import 'func' from sqlalchemy
from sqlalchemy.sql import func

# Import the Base from our database file
from .database import Base

class LLMUsageLog(Base):
    __tablename__ = "llm_usage_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(String, index=True)
    
    # MODIFIED: Let the database handle the timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    latency_ms = Column(Integer)
    cost_usd = Column(Float)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    is_error = Column(Boolean, default=False)