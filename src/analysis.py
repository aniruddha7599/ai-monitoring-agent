from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models

def get_stats_for_last_hour(db: Session):
    """
    Queries the database for logs in the last hour and calculates
    total requests, total cost, and average latency.
    """
    # CORRECTED: Use timezone.utc which works on Python 3.10
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    
    # This query is now slightly more robust using .first()
    result = db.query(
        func.count(models.LLMUsageLog.id).label("total_requests"),
        func.sum(models.LLMUsageLog.cost_usd).label("total_cost"),
        func.avg(models.LLMUsageLog.latency_ms).label("avg_latency")
    ).filter(models.LLMUsageLog.timestamp >= one_hour_ago).first() # Use .first() for safety
    
    if result and result.total_requests > 0:
        stats = {
            "time_window_start": one_hour_ago.isoformat(),
            "total_requests": result.total_requests,
            "total_cost": round(result.total_cost, 6) if result.total_cost else 0,
            "avg_latency_ms": round(result.avg_latency, 2) if result.avg_latency else 0
        }
    else:
        stats = {
            "time_window_start": one_hour_ago.isoformat(),
            "total_requests": 0,
            "total_cost": 0,
            "avg_latency_ms": 0
        }
    
    return stats