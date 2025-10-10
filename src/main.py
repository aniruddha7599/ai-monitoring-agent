from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Import our database components from the database.py file
from . import database

# This line tells SQLAlchemy to create all the tables based on our models
# It's safe to run this every time; it won't re-create existing tables
database.Base.metadata.create_all(bind=database.engine)

# --- Pydantic Model (from before) ---
class LogEntry(BaseModel):
    user_id: str
    latency_ms: int
    cost_usd: float
    prompt_tokens: int
    completion_tokens: int
    is_error: bool = False

# --- FastAPI App Instance ---
app = FastAPI()

# --- Dependency for getting a DB session ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"status": "API is running"}

@app.post("/logs")
def create_log_entry(log: LogEntry, db: Session = Depends(get_db)):
    # 1. Create a SQLAlchemy model instance from our Pydantic model
    db_log = database.LLMUsageLog(**log.model_dump())
    
    # 2. Add the new log instance to the session
    db.add(db_log)
    
    # 3. Commit the transaction to the database
    db.commit()
    
    # 4. Refresh the instance to get the new data from the DB (like the auto-generated id)
    db.refresh(db_log)
    
    return {"status": "Log saved successfully", "log_id": db_log.id}