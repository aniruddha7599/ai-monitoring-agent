from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import agent
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager

# MODIFIED: Import from our new files
from . import database, models, analysis

# MODIFIED: Use the Base from the models file to create the tables
models.Base.metadata.create_all(bind=database.engine)


class AgentQuery(BaseModel):
    question: str

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

# --- DEFINE THE SCHEDULED JOB ---
async def perform_scheduled_check():
    """The job that will be run by the scheduler."""
    print("\n--- [Scheduler] Running scheduled check... ---")
    db = database.SessionLocal()
    try:
        # 1. Get the latest stats
        stats = analysis.get_stats_for_last_hour(db)
        print(f"[Scheduler] Current stats: {stats}")
        
        # 2. Check for anomalies
        anomaly_result = analysis.check_for_anomalies(stats)
        
        # 3. If an anomaly is found, generate and print an alert
        if anomaly_result["status"] == "ANOMALY":
            print(f"[Scheduler] ANOMALY DETECTED: {anomaly_result['reason']}")
            alert_message = agent.generate_alert_message(anomaly_result['reason'])
            print("\n--- AI-Generated Alert ---")
            print(alert_message)
            print("--------------------------\n")
        else:
            print("[Scheduler] System status is OK.")
            
    finally:
        db.close()

# --- SETUP LIFESPAN EVENTS FOR THE APP ---
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup, add the job and start the scheduler
    # For testing, we'll run it every 30 seconds.
    scheduler.add_job(perform_scheduled_check, 'interval', seconds=30)
    scheduler.start()
    print("Scheduler started...")
    yield
    # On shutdown, stop the scheduler
    scheduler.shutdown()
    print("Scheduler stopped.")

# --- UPDATE THE APP INSTANCE TO USE THE LIFESPAN ---
app = FastAPI(lifespan=lifespan)


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


# --- Add this new endpoint at the very end of the file ---
@app.post("/agent/query")
def query_agent(query: AgentQuery, db: Session = Depends(get_db)):
    """
    Receives a natural language question and passes it to the agent.
    """
    # Create a new agent executor for each request
    agent_executor = agent.create_monitoring_agent(db)
    
    # Invoke the agent with the user's question
    response = agent_executor.invoke({
        "input": query.question
    })
    
    return {"response": response}