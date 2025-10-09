from fastapi import FastAPI
from pydantic import BaseModel

# 1. NEW: Define the data model for a single log entry using Pydantic
class LogEntry(BaseModel):
    user_id: str
    latency_ms: int
    cost_usd: float
    prompt_tokens: int
    completion_tokens: int
    is_error: bool = False # An optional field with a default value

# Create an instance of the FastAPI application
app = FastAPI()

# We can keep our root endpoint for simple health checks
@app.get("/")
def read_root():
    return {"status": "API is running"}

# 2. NEW: Create the new endpoint to receive logs
@app.post("/logs")
def create_log_entry(log: LogEntry):
    # For now, we'll just print the data to the terminal to confirm we received it
    print("--- Log Received ---")
    print(log.model_dump_json(indent=2))
    print("--------------------")
    
    return {"status": "Log received successfully", "data": log}