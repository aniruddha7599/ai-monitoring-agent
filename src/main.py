from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

# MODIFIED: Import from our new files
from . import database, models, analysis

# MODIFIED: Use the Base from the models file to create the tables
models.Base.metadata.create_all(bind=database.engine)

# Pydantic Model (no changes here)
class LogEntry(BaseModel):
    user_id: str
    latency_ms: int
    cost_usd: float
    prompt_tokens: int
    completion_tokens: int
    is_error: bool = False

# FastAPI App Instance
app = FastAPI()

# Dependency (no changes here)
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
@app.get("/")
def read_root():
    return {"status": "API is running"}

@app.post("/logs")
def create_log_entry(log: LogEntry, db: Session = Depends(get_db)):
    # MODIFIED: Use the model from the models.py file
    db_log = models.LLMUsageLog(**log.model_dump())
    
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    return {"status": "Log saved successfully", "log_id": db_log.id}

@app.get("/analysis/stats")
def get_analysis_stats(db: Session = Depends(get_db)):
    stats = analysis.get_stats_for_last_hour(db)
    return stats