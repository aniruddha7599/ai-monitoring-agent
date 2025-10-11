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
            "total_cost": round(float(result.total_cost), 6) if result.total_cost else 0,
            # MODIFIED: Convert Decimal to float before rounding
            "avg_latency_ms": round(float(result.avg_latency), 2) if result.avg_latency else 0
        }
    else:
        stats = {
            "time_window_start": one_hour_ago.isoformat(),
            "total_requests": 0,
            "total_cost": 0,
            "avg_latency_ms": 0
        }
    
    return stats

def find_top_cost_users(db: Session, top_n: int = 5):
    """
    Finds the top N users by their total incurred cost in the last hour.
    """
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    
    # This query groups by user_id, sums the cost, orders by that sum, and limits the result.
    results = db.query(
        models.LLMUsageLog.user_id,
        func.sum(models.LLMUsageLog.cost_usd).label("total_cost")
    ).filter(
        models.LLMUsageLog.timestamp >= one_hour_ago
    ).group_by(
        models.LLMUsageLog.user_id
    ).order_by(
        func.sum(models.LLMUsageLog.cost_usd).desc()
    ).limit(top_n).all()
    
    # Format the results into a list of dictionaries for the agent
    top_users = [
        {"user_id": user_id, "total_cost": round(float(total_cost), 6)}
        for user_id, total_cost in results
    ]
    
    return top_users