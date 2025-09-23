
"""
Comprehensive mock analytics data for Clinical Decision Support System
Includes usage metrics, clinical outcomes, user behavior, and quality indicators
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
from dataclasses import dataclass
from enum import Enum
import json

class UserRole(Enum):
    PHYSICIAN = "physician"
    NURSE = "nurse"
    PHARMACIST = "pharmacist"
    PHYSICIAN_ASSISTANT = "physician_assistant"
    RESIDENT = "resident"
    STUDENT = "student"

class QueryType(Enum):
    DIAGNOSIS = "diagnosis"
    TREATMENT = "treatment"
    DRUG_INTERACTION = "drug_interaction"
    DOSING = "dosing"
    MONITORING = "monitoring"
    GENERAL = "general"

class Specialty(Enum):
    CARDIOLOGY = "cardiology"
    ENDOCRINOLOGY = "endocrinology"
    EMERGENCY_MEDICINE = "emergency_medicine"
    INFECTIOUS_DISEASE = "infectious_disease"
    NEUROLOGY = "neurology"
    INTERNAL_MEDICINE = "internal_medicine"
    FAMILY_MEDICINE = "family_medicine"
    PEDIATRICS = "pediatrics"

@dataclass
class ClinicalQueryLog:
    query_id: str
    user_id: str
    user_role: UserRole
    specialty: Specialty
    timestamp: datetime
    query_text: str
    query_type: QueryType
    processing_time_ms: float
    confidence_score: float
    recommendations_count: int
    user_feedback_rating: Optional[int]  # 1-5 scale
    recommendation_followed: Optional[bool]
    patient_age_group: str  # "pediatric", "adult", "geriatric"
    clinical_outcome: Optional[str]  # "improved", "unchanged", "declined"
    session_id: str

@dataclass
class UserActivityMetrics:
    user_id: str
    user_role: UserRole
    specialty: Specialty
    total_queries: int
    avg_queries_per_day: float
    avg_session_duration_minutes: float
    last_active: datetime
    certification_status: str  # "certified", "pending", "expired"
    training_completion_rate: float
    avg_feedback_rating: float

@dataclass
class SystemPerformanceMetrics:
    date: datetime
    total_queries: int
    avg_response_time_ms: float
    system_uptime_percentage: float
    error_rate_percentage: float
    peak_concurrent_users: int
    database_query_time_ms: float
    ai_processing_time_ms: float

@dataclass
class ClinicalOutcomeMetrics:
    date: datetime
    specialty: Specialty
    total_recommendations: int
    recommendations_followed: int
    positive_outcomes: int
    neutral_outcomes: int
    negative_outcomes: int
    avg_confidence_score: float
    drug_interactions_prevented: int

class AnalyticsDatabase:
    """Mock analytics database for Clinical Decision Support System"""
    
    def __init__(self):
        self.start_date = datetime.now() - timedelta(days=90)  # 90 days of data
        self.end_date = datetime.now()
        
        # Generate mock data
        self.query_logs = self._generate_query_logs()
        self.user_metrics = self._generate_user_metrics()
        self.performance_metrics = self._generate_performance_metrics()
        self.outcome_metrics = self._generate_outcome_metrics()
        self.specialty_usage = self._calculate_specialty_usage()
        self.quality_metrics = self._calculate_quality_metrics()
    
    def _generate_query_logs(self) -> List[ClinicalQueryLog]:
        """Generate realistic clinical query log data"""
        logs = []
        
        # Common clinical queries by specialty
        query_templates = {
            Specialty.CARDIOLOGY: [
                "chest pain management in {age_group} patient",
                "heart failure treatment guidelines",
                "hypertension medication selection",
                "atrial fibrillation anticoagulation",
                "acute coronary syndrome protocol",
                "statin therapy recommendations"
            ],
            Specialty.ENDOCRINOLOGY: [
                "diabetes management type 2",
                "insulin dosing calculation",
                "thyroid disorder treatment",
                "HbA1c target recommendations",
                "metformin contraindications",
                "diabetic ketoacidosis management"
            ],
            Specialty.EMERGENCY_MEDICINE: [
                "sepsis management protocol",
                "trauma resuscitation guidelines",
                "stroke acute management",
                "anaphylaxis treatment",
                "overdose management",
                "pediatric emergency dosing"
            ],
            Specialty.INFECTIOUS_DISEASE: [
                "antibiotic selection for pneumonia",
                "UTI treatment guidelines",
                "sepsis antibiotic therapy",
                "meningitis treatment protocol",
                "antibiotic resistance management",
                "C. diff treatment options"
            ],
            Specialty.NEUROLOGY: [
                "seizure management acute",
                "migraine treatment options",
                "stroke thrombolysis criteria",
                "multiple sclerosis therapy",
                "Parkinson's medication adjustment",
                "neuropathic pain management"
            ]
        }
        
        # Generate 5000 queries over 90 days
        for day in range(90):
            date = self.start_date + timedelta(days=day)
            
            # More queries on weekdays, fewer on weekends
            if date.weekday() < 5:  # Weekday
                daily_queries = random.randint(45, 75)
            else:  # Weekend
                daily_queries = random.randint(20, 35)
            
            for _ in range(daily_queries):
                specialty = random.choice(list(Specialty))
                user_role = random.choice(list(UserRole))
                
                # Physicians and residents make more complex queries
                if user_role in [UserRole.PHYSICIAN, UserRole.RESIDENT]:
                    query_type = random.choice(list(QueryType))
                    confidence_score = random.uniform(0.75, 0.95)
                else:
                    query_type = random.choice([QueryType.DRUG_INTERACTION, QueryType.DOSING, QueryType.MONITORING])
                    confidence_score = random.uniform(0.65, 0.85)
                
                # Generate query text
                if specialty in query_templates:
                    template = random.choice(query_templates[specialty])
                    age_group = random.choice(["pediatric", "adult", "elderly"])
                    query_text = template.format(age_group=age_group)
                else:
                    query_text = f"Clinical guidance for {specialty.value} case"
                
                # Simulate processing time (faster for simpler queries)
                if query_type == QueryType.DRUG_INTERACTION:
                    processing_time = random.uniform(800, 1500)
                else:
                    processing_time = random.uniform(1500, 3500)
                
                # User feedback (80% provide feedback)
                feedback_rating = None
                if random.random() < 0.8:
                    # Higher ratings for higher confidence
                    if confidence_score > 0.9:
                        feedback_rating = random.choices([4, 5], weights=[30, 70])[0]
                    elif confidence_score > 0.8:
                        feedback_rating = random.choices([3, 4, 5], weights=[20, 40, 40])[0]
                    else:
                        feedback_rating = random.choices([2, 3, 4], weights=[30, 50, 20])[0]
                
                # Recommendation following (70% follow recommendations)
                recommendation_followed = None
                if random.random() < 0.7:
                    recommendation_followed = random.choices([True, False], weights=[85, 15])[0]
                
                # Clinical outcomes (60% have recorded outcomes)
                clinical_outcome = None
                if recommendation_followed and random.random() < 0.6:
                    clinical_outcome = random.choices(
                        ["improved", "unchanged", "declined"], 
                        weights=[75, 20, 5]
                    )[0]
                
                log = ClinicalQueryLog(
                    query_id=f"q_{len(logs)+1:06d}",
                    user_id=f"user_{random.randint(1, 150):03d}",
                    user_role=user_role,
                    specialty=specialty,
                    timestamp=date + timedelta(
                        hours=random.randint(6, 22),
                        minutes=random.randint(0, 59)
                    ),
                    query_text=query_text,
                    query_type=query_type,
                    processing_time_ms=processing_time,
                    confidence_score=confidence_score,
                    recommendations_count=random.randint(1, 4),
                    user_feedback_rating=feedback_rating,
                    recommendation_followed=recommendation_followed,
                    patient_age_group=random.choice(["pediatric", "adult", "geriatric"]),
                    clinical_outcome=clinical_outcome,
                    session_id=f"session_{random.randint(1, 1000):04d}"
                )
                logs.append(log)
        
        return logs
    
    def _generate_user_metrics(self) -> List[UserActivityMetrics]:
        """Generate user activity and engagement metrics"""
        metrics = []
        
        # Generate for 150 users across different roles
        for user_id in range(1, 151):
            user_role = random.choice(list(UserRole))
            specialty = random.choice(list(Specialty))
            
            # Calculate user-specific metrics from query logs
            user_queries = [log for log in self.query_logs if log.user_id == f"user_{user_id:03d}"]
            
            if user_queries:
                total_queries = len(user_queries)
                days_active = len(set(log.timestamp.date() for log in user_queries))
                avg_queries_per_day = total_queries / max(days_active, 1)
                
                # Session duration varies by role
                if user_role == UserRole.PHYSICIAN:
                    avg_session_duration = random.uniform(25, 45)
                elif user_role == UserRole.RESIDENT:
                    avg_session_duration = random.uniform(35, 55)
                else:
                    avg_session_duration = random.uniform(15, 30)
                
                # Training completion varies by role
                if user_role in [UserRole.PHYSICIAN, UserRole.PHARMACIST]:
                    training_completion = random.uniform(0.85, 1.0)
                else:
                    training_completion = random.uniform(0.65, 0.95)
                
                # Feedback ratings
                ratings = [log.user_feedback_rating for log in user_queries if log.user_feedback_rating]
                avg_feedback = sum(ratings) / len(ratings) if ratings else 0
                
                last_active = max(log.timestamp for log in user_queries)
                
                # Certification status
                cert_status = random.choices(
                    ["certified", "pending", "expired"],
                    weights=[80, 15, 5]
                )[0]
                
                metrics.append(UserActivityMetrics(
                    user_id=f"user_{user_id:03d}",
                    user_role=user_role,
                    specialty=specialty,
                    total_queries=total_queries,
                    avg_queries_per_day=avg_queries_per_day,
                    avg_session_duration_minutes=avg_session_duration,
                    last_active=last_active,
                    certification_status=cert_status,
                    training_completion_rate=training_completion,
                    avg_feedback_rating=avg_feedback
                ))
        
        return metrics
    
    def _generate_performance_metrics(self) -> List[SystemPerformanceMetrics]:
        """Generate system performance metrics"""
        metrics = []
        
        for day in range(90):
            date = self.start_date + timedelta(days=day)
            
            # Get daily query count
            daily_queries = [log for log in self.query_logs if log.timestamp.date() == date.date()]
            total_queries = len(daily_queries)
            
            # Calculate average response time
            if daily_queries:
                avg_response_time = sum(log.processing_time_ms for log in daily_queries) / len(daily_queries)
            else:
                avg_response_time = 0
            
            # System performance varies slightly
            uptime = random.uniform(99.5, 99.99)
            error_rate = random.uniform(0.01, 0.5)
            peak_users = random.randint(15, 45) if date.weekday() < 5 else random.randint(8, 20)
            
            # Database and AI processing times
            db_time = random.uniform(50, 200)
            ai_time = avg_response_time - db_time if avg_response_time > db_time else random.uniform(800, 2000)
            
            metrics.append(SystemPerformanceMetrics(
                date=date,
                total_queries=total_queries,
                avg_response_time_ms=avg_response_time,
                system_uptime_percentage=uptime,
                error_rate_percentage=error_rate,
                peak_concurrent_users=peak_users,
                database_query_time_ms=db_time,
                ai_processing_time_ms=ai_time
            ))
        
        return metrics
    
    def _generate_outcome_metrics(self) -> List[ClinicalOutcomeMetrics]:
        """Generate clinical outcome metrics by specialty"""
        metrics = []
        
        for specialty in Specialty:
            for day in range(0, 90, 7):  # Weekly metrics
                date = self.start_date + timedelta(days=day)
                
                # Get specialty queries for the week
                week_end = date + timedelta(days=6)
                specialty_queries = [
                    log for log in self.query_logs
                    if log.specialty == specialty
                    and date <= log.timestamp <= week_end
                    and log.recommendation_followed is not None
                ]
                
                if specialty_queries:
                    total_recommendations = len(specialty_queries)
                    recommendations_followed = sum(1 for log in specialty_queries if log.recommendation_followed)
                    
                    # Count outcomes
                    outcomes = [log.clinical_outcome for log in specialty_queries if log.clinical_outcome]
                    positive_outcomes = sum(1 for outcome in outcomes if outcome == "improved")
                    neutral_outcomes = sum(1 for outcome in outcomes if outcome == "unchanged")
                    negative_outcomes = sum(1 for outcome in outcomes if outcome == "declined")
                    
                    # Average confidence
                    avg_confidence = sum(log.confidence_score for log in specialty_queries) / len(specialty_queries)
                    
                    # Drug interactions prevented (estimate)
                    drug_interaction_queries = [
                        log for log in specialty_queries 
                        if log.query_type == QueryType.DRUG_INTERACTION
                    ]
                    interactions_prevented = int(len(drug_interaction_queries) * 0.3)  # 30% had interactions
                    
                    metrics.append(ClinicalOutcomeMetrics(
                        date=date,
                        specialty=specialty,
                        total_recommendations=total_recommendations,
                        recommendations_followed=recommendations_followed,
                        positive_outcomes=positive_outcomes,
                        neutral_outcomes=neutral_outcomes,
                        negative_outcomes=negative_outcomes,
                        avg_confidence_score=avg_confidence,
                        drug_interactions_prevented=interactions_prevented
                    ))
        
        return metrics
    
    def _calculate_specialty_usage(self) -> Dict[str, Any]:
        """Calculate usage statistics by medical specialty"""
        specialty_stats = {}
        
        for specialty in Specialty:
            specialty_queries = [log for log in self.query_logs if log.specialty == specialty]
            
            if specialty_queries:
                total_queries = len(specialty_queries)
                avg_confidence = sum(log.confidence_score for log in specialty_queries) / len(specialty_queries)
                
                # User distribution
                unique_users = len(set(log.user_id for log in specialty_queries))
                
                # Query types distribution
                query_types = {}
                for query_type in QueryType:
                    count = sum(1 for log in specialty_queries if log.query_type == query_type)
                    query_types[query_type.value] = count
                
                # Feedback ratings
                ratings = [log.user_feedback_rating for log in specialty_queries if log.user_feedback_rating]
                avg_rating = sum(ratings) / len(ratings) if ratings else 0
                
                specialty_stats[specialty.value] = {
                    "total_queries": total_queries,
                    "unique_users": unique_users,
                    "avg_confidence_score": round(avg_confidence, 3),
                    "avg_user_rating": round(avg_rating, 2),
                    "query_types": query_types,
                    "usage_percentage": round(total_queries / len(self.query_logs) * 100, 1)
                }
        
        return specialty_stats
    
    def _calculate_quality_metrics(self) -> Dict[str, Any]:
        """Calculate overall system quality metrics"""
        total_queries = len(self.query_logs)
        
        # Confidence score distribution
        confidence_scores = [log.confidence_score for log in self.query_logs]
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        high_confidence_queries = sum(1 for score in confidence_scores if score >= 0.9)
        
        # User satisfaction
        ratings = [log.user_feedback_rating for log in self.query_logs if log.user_feedback_rating]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        satisfied_users = sum(1 for rating in ratings if rating >= 4)
        
        # Recommendation adoption
        followed_recommendations = [log for log in self.query_logs if log.recommendation_followed is not None]
        adoption_rate = (
            sum(1 for log in followed_recommendations if log.recommendation_followed) / 
            len(followed_recommendations) * 100
        ) if followed_recommendations else 0
        
        # Clinical outcomes
        outcomes = [log.clinical_outcome for log in self.query_logs if log.clinical_outcome]
        positive_outcomes = sum(1 for outcome in outcomes if outcome == "improved")
        outcome_success_rate = (positive_outcomes / len(outcomes) * 100) if outcomes else 0
        
        # Performance metrics
        avg_response_time = sum(log.processing_time_ms for log in self.query_logs) / len(self.query_logs)
        
        return {
            "total_queries": total_queries,
            "avg_confidence_score": round(avg_confidence, 3),
            "high_confidence_percentage": round(high_confidence_queries / total_queries * 100, 1),
            "avg_user_rating": round(avg_rating, 2),
            "user_satisfaction_percentage": round(satisfied_users / len(ratings) * 100, 1) if ratings else 0,
            "recommendation_adoption_rate": round(adoption_rate, 1),
            "clinical_outcome_success_rate": round(outcome_success_rate, 1),
            "avg_response_time_ms": round(avg_response_time, 1),
            "total_users": len(self.user_metrics),
            "active_users_last_30_days": len([
                user for user in self.user_metrics 
                if user.last_active >= datetime.now() - timedelta(days=30)
            ])
        }
    
    def get_usage_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get usage trends over specified time period"""
        cutoff_date = self.end_date - timedelta(days=days)
        recent_queries = [log for log in self.query_logs if log.timestamp >= cutoff_date]
        
        # Daily usage
        daily_usage = {}
        for log in recent_queries:
            date_str = log.timestamp.strftime('%Y-%m-%d')
            daily_usage[date_str] = daily_usage.get(date_str, 0) + 1
        
        # Hourly usage patterns
        hourly_usage = {}
        for log in recent_queries:
            hour = log.timestamp.hour
            hourly_usage[hour] = hourly_usage.get(hour, 0) + 1
        
        # User role distribution
        role_usage = {}
        for log in recent_queries:
            role = log.user_role.value
            role_usage[role] = role_usage.get(role, 0) + 1
        
        return {
            "period_days": days,
            "total_queries": len(recent_queries),
            "daily_usage": daily_usage,
            "hourly_patterns": hourly_usage,
            "user_role_distribution": role_usage,
            "avg_daily_queries": len(recent_queries) / days
        }
    
    def get_performance_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive performance dashboard data"""
        recent_performance = self.performance_metrics[-30:]  # Last 30 days
        
        return {
            "system_health": {
                "avg_uptime": sum(p.system_uptime_percentage for p in recent_performance) / len(recent_performance),
                "avg_error_rate": sum(p.error_rate_percentage for p in recent_performance) / len(recent_performance),
                "avg_response_time": sum(p.avg_response_time_ms for p in recent_performance) / len(recent_performance),
                "peak_concurrent_users": max(p.peak_concurrent_users for p in recent_performance)
            },
            "quality_metrics": self.quality_metrics,
            "usage_trends": self.get_usage_trends(30),
            "specialty_breakdown": self.specialty_usage
        }

# Initialize global analytics database
analytics_db = AnalyticsDatabase()

# Convenience functions for API use
def get_analytics_summary() -> Dict[str, Any]:
    """Get high-level analytics summary"""
    return analytics_db.quality_metrics

def get_usage_trends(days: int = 30) -> Dict[str, Any]:
    """Get usage trends"""
    return analytics_db.get_usage_trends(days)

def get_performance_dashboard() -> Dict[str, Any]:
    """Get performance dashboard data"""
    return analytics_db.get_performance_dashboard()

def get_specialty_analytics() -> Dict[str, Any]:
    """Get specialty-specific analytics"""
    return analytics_db.specialty_usage

def get_user_engagement_metrics() -> Dict[str, Any]:
    """Get user engagement and training metrics"""
    users = analytics_db.user_metrics
    
    # Calculate engagement metrics
    total_users = len(users)
    active_users = len([u for u in users if u.last_active >= datetime.now() - timedelta(days=30)])
    certified_users = len([u for u in users if u.certification_status == "certified"])
    avg_training_completion = sum(u.training_completion_rate for u in users) / total_users
    
    # Role distribution
    role_distribution = {}
    for user in users:
        role = user.user_role.value
        role_distribution[role] = role_distribution.get(role, 0) + 1
    
    return {
        "total_users": total_users,
        "active_users_30_days": active_users,
        "user_activity_rate": round(active_users / total_users * 100, 1),
        "certified_users": certified_users,
        "certification_rate": round(certified_users / total_users * 100, 1),
        "avg_training_completion": round(avg_training_completion * 100, 1),
        "role_distribution": role_distribution,
        "avg_queries_per_active_user": round(
            sum(u.total_queries for u in users if u.last_active >= datetime.now() - timedelta(days=30)) / 
            max(active_users, 1), 1
        )
    }

# Example usage and testing
if __name__ == "__main__":
    print("Testing Analytics Database...")
    
    # Test analytics summary
    summary = get_analytics_summary()
    print(f"\nAnalytics Summary:")
    print(f"Total Queries: {summary['total_queries']}")
    print(f"Average Confidence: {summary['avg_confidence_score']}")
    print(f"User Satisfaction: {summary['user_satisfaction_percentage']}%")
    print(f"Adoption Rate: {summary['recommendation_adoption_rate']}%")
    
    # Test usage trends
    trends = get_usage_trends(30)
    print(f"\nUsage Trends (30 days):")
    print(f"Total Queries: {trends['total_queries']}")
    print(f"Average Daily: {trends['avg_daily_queries']:.1f}")
    
    # Test specialty analytics
    specialty_data = get_specialty_analytics()
    print(f"\nTop Specialties by Usage:")
    sorted_specialties = sorted(
        specialty_data.items(),
        key=lambda x: x[1]['total_queries'],
        reverse=True
    )
    for specialty, data in sorted_specialties[:3]:
        print(f"  {specialty}: {data['total_queries']} queries ({data['usage_percentage']}%)")
    
    # Test user engagement
    engagement = get_user_engagement_metrics()
    print(f"\nUser Engagement:")
    print(f"Active Users: {engagement['active_users_30_days']}/{engagement['total_users']} ({engagement['user_activity_rate']}%)")
    print(f"Certification Rate: {engagement['certification_rate']}%")
    print(f"Training Completion: {engagement['avg_training_completion']}%")