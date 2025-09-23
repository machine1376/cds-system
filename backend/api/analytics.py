
"""
Analytics API endpoints for Clinical Decision Support System
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from data.analytics_database import (
    analytics_db,
    get_analytics_summary,
    get_usage_trends,
    get_performance_dashboard,
    get_specialty_analytics,
    get_user_engagement_metrics
)

router = APIRouter(prefix="/analytics", tags=["Analytics & Reporting"])

@router.get("/summary")
async def get_system_analytics_summary():
    """
    Get high-level system analytics summary
    """
    try:
        summary = get_analytics_summary()
        return {
            "system_overview": summary,
            "data_period": "Last 90 days",
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving analytics summary: {str(e)}"
        )

@router.get("/dashboard")
async def get_analytics_dashboard():
    """
    Get comprehensive analytics dashboard data
    """
    try:
        dashboard_data = get_performance_dashboard()
        return {
            **dashboard_data,
            "generated_at": datetime.now().isoformat(),
            "data_freshness": "Real-time"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving dashboard data: {str(e)}"
        )

@router.get("/usage/trends")
async def get_usage_trend_analysis(
    days: int = Query(30, ge=1, le=90, description="Number of days to analyze")
):
    """
    Get usage trends and patterns over specified time period
    """
    try:
        trends = get_usage_trends(days)
        return {
            **trends,
            "analysis_period": f"Last {days} days",
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving usage trends: {str(e)}"
        )

@router.get("/specialties")
async def get_specialty_analytics_breakdown():
    """
    Get detailed analytics breakdown by medical specialty
    """
    try:
        specialty_data = get_specialty_analytics()
        
        # Calculate additional insights
        total_queries = sum(data['total_queries'] for data in specialty_data.values())
        top_specialty = max(specialty_data.items(), key=lambda x: x[1]['total_queries'])
        most_confident = max(specialty_data.items(), key=lambda x: x[1]['avg_confidence_score'])
        
        return {
            "specialty_breakdown": specialty_data,
            "insights": {
                "total_queries_across_specialties": total_queries,
                "most_active_specialty": {
                    "name": top_specialty[0],
                    "queries": top_specialty[1]['total_queries'],
                    "percentage": top_specialty[1]['usage_percentage']
                },
                "highest_confidence_specialty": {
                    "name": most_confident[0],
                    "confidence_score": most_confident[1]['avg_confidence_score']
                }
            },
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving specialty analytics: {str(e)}"
        )

@router.get("/users/engagement")
async def get_user_engagement_analytics():
    """
    Get user engagement and training metrics
    """
    try:
        engagement_data = get_user_engagement_metrics()
        
        # Add engagement insights
        engagement_insights = {
            "engagement_level": "High" if engagement_data['user_activity_rate'] > 70 else 
                             "Medium" if engagement_data['user_activity_rate'] > 50 else "Low",
            "certification_status": "Good" if engagement_data['certification_rate'] > 80 else 
                                  "Needs Improvement" if engagement_data['certification_rate'] > 60 else "Poor",
            "training_effectiveness": "Excellent" if engagement_data['avg_training_completion'] > 90 else
                                    "Good" if engagement_data['avg_training_completion'] > 75 else "Needs Improvement"
        }
        
        return {
            **engagement_data,
            "insights": engagement_insights,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving user engagement data: {str(e)}"
        )

@router.get("/performance/system")
async def get_system_performance_metrics():
    """
    Get system performance metrics and health indicators
    """
    try:
        # Mock system performance data
        performance_data = {
            "response_time_ms": 245,
            "uptime_percentage": 99.8,
            "error_rate": 0.2,
            "active_users": 156,
            "memory_usage_percent": 68,
            "cpu_usage_percent": 45,
            "database_connections": 12,
            "cache_hit_rate": 94.5
        }
        
        return {
            **performance_data,
            "generated_at": datetime.now().isoformat(),
            "status": "healthy"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving system performance metrics: {str(e)}"
        )