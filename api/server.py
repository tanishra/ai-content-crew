from fastapi import FastAPI, BackgroundTasks, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from research_and_blog_crew.crew import ResearchAndBlogCrew
from database.models import SessionLocal, User, ContentJob, generate_api_key, init_db
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from utils.logger import setup_logger
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from dotenv import load_dotenv
import os

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
    enable_logs=True,

)

app = FastAPI(
    title="AI Content Crew API",
    description="""
## 🚀 AI-Powered Content Generation API

Generate comprehensive research reports and SEO-optimized blog posts using AI multi-agent collaboration.

### Features
* 📊 2000-word strategic reports
* 📝 500-word SEO-optimized blogs
* ⚡ 1-2 minute generation time
* 🔍 Real-time web research
* ✅ Fact-checking & quality assurance

### Authentication
All endpoints (except /signup and /health) require an API key in the header:
```
X-API-Key: acc_your_api_key_here
```

### Rate Limits
- **Free**: 10 requests/month
- **Pro**: 100 requests/month
- **Enterprise**: 1000 requests/month
    """,
    version="1.0.0",
    contact={
        "name": "Tanish Rajput",
        "email": "tanishrajput9@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

logger = setup_logger("api", "api.log")


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Key authentication
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db)
):
    """Verify API key and return user"""
    if not api_key:
        raise HTTPException(status_code=401, detail="API Key required")
    
    user = db.query(User).filter(User.api_key == api_key, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    return user

# Models
class ContentRequest(BaseModel):
    topic: str
    email: Optional[EmailStr] = None

class UserSignupRequest(BaseModel):
    email: EmailStr

class JobStatus(BaseModel):
    job_id: str
    status: str
    topic: str
    created_at: str
    completed_at: Optional[str] = None
    result: Optional[dict] = None
    error: Optional[str] = None

# Routes
@app.post(
    "/signup",
    summary="Create New User Account",
    description="Register a new user and receive an API key for authentication.",
    response_description="User created successfully with API key",
    tags=["Authentication"]
)
async def signup(request: UserSignupRequest, db: Session = Depends(get_db)):
    """
        Create a new user account and generate API key.
    
        - **email**: Valid email address (required)
    
        Returns:
        - **api_key**: Your authentication key (keep it secure!)
        - **subscription_tier**: Your plan (free/pro/enterprise)
        - **monthly_limit**: Maximum requests per month
    
        Example:
            ```json
                {
                "email": "user@example.com"
                }
            ```
    """

    logger.info("Signup attempt", extra={"email": request.email})
    # Check if user exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    api_key = generate_api_key()
    new_user = User(
        email=request.email,
        api_key=api_key,
        subscription_tier="free",
        monthly_limit=10
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info("Signup successful", extra={
        "email": request.email,
        "user_id": new_user.id
    })
    
    return {
        "message": "Signup successful",
        "email": request.email,
        "api_key": api_key,
        "subscription_tier": "free",
        "monthly_limit": 10
    }

@app.post(
    "/generate",
    summary="Generate Content",
    description="Create a research report and blog post for the given topic.",
    response_description="Job created successfully",
    tags=["Content Generation"]
)
@limiter.limit("10/hour")  # 10 requests per hour for free tier
async def generate_content(
    request: ContentRequest,
    background_tasks: BackgroundTasks,
    user: User = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """
    Start a new content generation job.
    
    Requires authentication via X-API-Key header.
    
    - **topic**: Subject to research and write about (max 200 characters)
    - **email**: Optional notification email
    
    Returns job_id for status tracking.
    
    Example:
```json
    {
        "topic": "Future of Quantum Computing",
        "email": "notify@example.com"
    }
```
    """

    logger.info("Generation started", extra={
        "job_id": job_id,
        "user_id": user.id,
        "topic": request.topic
    })
    
    # Check usage limits
    if user.usage_count >= user.monthly_limit:
        raise HTTPException(
            status_code=429,
            detail=f"Monthly limit reached ({user.monthly_limit} requests). Upgrade your plan."
        )
    
    # Create job
    job_id = str(uuid.uuid4())
    job = ContentJob(
        job_id=job_id,
        user_id=user.id,
        topic=request.topic,
        status="processing"
    )
    
    db.add(job)
    db.commit()
    
    # Increment usage count
    user.usage_count += 1
    user.last_used_at = datetime.utcnow()
    db.commit()
    
    # Run crew in background
    background_tasks.add_task(run_crew, job_id, request.topic, user.id)
    
    return {
        "job_id": job_id,
        "status": "processing",
        "message": "Job started",
        "usage": f"{user.usage_count}/{user.monthly_limit}"
    }

@app.get(
    "/status/{job_id}",
    summary="Check Job Status",
    description="Get the current status and results of a generation job.",
    response_description="Job status and results",
    tags=["Content Generation"]
)
async def get_status(
    job_id: str,
    user: User = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """
    Check the status of your content generation job.
    
    Requires authentication via X-API-Key header.
    
    - **job_id**: The UUID returned from /generate endpoint
    
    Returns:
    - **status**: processing | completed | failed
    - **result**: File paths when completed
    - **error**: Error message if failed
    """

    job = db.query(ContentJob).filter(
        ContentJob.job_id == job_id,
        ContentJob.user_id == user.id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job.job_id,
        "status": job.status,
        "topic": job.topic,
        "created_at": job.created_at.isoformat(),
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        "result": {
            "report": job.report_path,
            "blog": job.blog_path
        } if job.status == "completed" else None,
        "error": job.error_message
    }

@app.get(
    "/usage",
    summary="Get Usage Statistics",
    description="View your current API usage and limits.",
    response_description="Usage statistics",
    tags=["Account"]
)
async def get_usage(
    user: User = Depends(verify_api_key)
):
    """
    Get your current usage statistics.
    
    Requires authentication via X-API-Key header.
    
    Returns:
    - **usage_count**: Number of requests used this month
    - **monthly_limit**: Total requests allowed per month
    - **remaining**: Requests remaining
    """

    return {
        "email": user.email,
        "subscription_tier": user.subscription_tier,
        "usage_count": user.usage_count,
        "monthly_limit": user.monthly_limit,
        "remaining": user.monthly_limit - user.usage_count
    }

@app.get(
    "/admin/stats",
    summary="Platform Statistics",
    description="Get overall platform usage statistics.",
    response_description="Platform metrics",
    tags=["Admin"]
)
async def admin_stats(db: Session = Depends(get_db)):
    """
    View platform-wide statistics.
    
    ⚠️ TODO: Add admin authentication
    """

    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_jobs = db.query(ContentJob).count()
    completed_jobs = db.query(ContentJob).filter(ContentJob.status == "completed").count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_jobs": total_jobs,
        "completed_jobs": completed_jobs,
        "success_rate": f"{(completed_jobs/total_jobs*100):.1f}%" if total_jobs > 0 else "0%"
    }

@app.get(
    "/admin/users",
    summary="List all users",
    description="Retrieve a list of all registered users with basic account and usage information.",
    response_description="User list with subscription and usage details",
    tags=["Admin"]
)
async def list_users(db: Session = Depends(get_db)):
    """
    List all platform users.
    
    Returns basic user details including email, subscription tier,
    usage metrics, and account creation date.
    
    ⚠️ TODO: Add admin authentication
    """
    
    users = db.query(User).all()
    return [{
        "id": u.id,
        "email": u.email,
        "tier": u.subscription_tier,
        "usage": f"{u.usage_count}/{u.monthly_limit}",
        "created_at": u.created_at.isoformat()
    } for u in users]

@app.get(
    "/admin/costs",
    summary="Cost Analytics",
    description="View platform cost breakdown and estimates.",
    response_description="Cost analytics",
    tags=["Admin"]
)
async def get_costs(db: Session = Depends(get_db)):
    """
    Get detailed cost analytics.
    
    ⚠️ TODO: Add admin authentication
    """

    jobs = db.query(ContentJob).filter(ContentJob.status == "completed").all()
    
    total_cost = sum(j.estimated_cost or 0 for j in jobs)
    total_jobs = len(jobs)
    avg_cost = total_cost / total_jobs if total_jobs > 0 else 0
    
    return {
        "total_jobs": total_jobs,
        "total_cost": f"${total_cost:.2f}",
        "avg_cost_per_job": f"${avg_cost:.4f}",
        "estimated_monthly": f"${total_cost * 30:.2f}"  # If this is daily rate
    }

@app.get(
    "/health",
    summary="Health Check",
    description="Check if the API is operational.",
    response_description="Service health status",
    tags=["System"]
)
async def health_check(db: Session = Depends(get_db)):
    """
    Public health check endpoint (no authentication required).
    
    Returns system status and recent performance metrics.
    """

    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    
    # Check recent job success rate
    recent_jobs = db.query(ContentJob).order_by(
        ContentJob.created_at.desc()
    ).limit(10).all()
    
    success_rate = sum(1 for j in recent_jobs if j.status == "completed") / len(recent_jobs) * 100 if recent_jobs else 0
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
        "recent_success_rate": f"{success_rate:.1f}%",
        "version": "1.0.0"
    }

def run_crew(job_id: str, topic: str, user_id: int):
    """Background task to run crew"""
    db = SessionLocal()
    job = db.query(ContentJob).filter(ContentJob.job_id == job_id).first()
    
    try:
        logger.info("Crew execution started", extra={
            "job_id": job_id,
            "user_id": user_id
        })

        start_time = datetime.utcnow()
        
        crew_instance = ResearchAndBlogCrew()
        result = crew_instance.crew().kickoff(inputs={"topic": topic})

        # Estimate cost (rough calculation)
        # GPT-4: $0.03 per 1K tokens input, $0.06 per 1K tokens output
        # Average generation uses ~15K tokens total
        estimated_tokens = 15000
        estimated_cost = (estimated_tokens / 1000) * 0.045  # Average rate
        
        end_time = datetime.utcnow()
        execution_time = int((end_time - start_time).total_seconds())
        
        job.status = "completed"
        job.completed_at = end_time
        job.execution_time = execution_time
        job.tokens_used = estimated_tokens
        job.estimated_cost = estimated_cost
        job.report_path = f"output/strategic_report_{job_id}.md"
        job.blog_path = f"output/blog_post_{job_id}.md"
        
        db.commit()

        logger.info("Crew execution completed", extra={
            "job_id": job_id,
            "execution_time": execution_time,
            "tokens": estimated_tokens,
            "cost": f"${estimated_cost:.4f}"
        })
        
    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        job.completed_at = datetime.utcnow()
        db.commit()
    
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)