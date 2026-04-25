from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime
from dotenv import load_dotenv

from backend.database import engine, get_db
from backend.models import Base
from backend.routes import candidates, search, elections, compare, exitpolls, parties, users, websocket, news, stats
load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="NetaNexus API",
    description="India's Most Comprehensive Political Data Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(candidates.router, prefix="/api/candidates", tags=["Candidates"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(elections.router, prefix="/api/elections", tags=["Elections"])
app.include_router(compare.router, prefix="/api/compare", tags=["Compare"])
app.include_router(exitpolls.router, prefix="/api/exitpolls", tags=["Exit Polls"])
app.include_router(parties.router, prefix="/api/parties", tags=["Parties"])
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
app.include_router(news.router, prefix="/api/news", tags=["News"])
app.include_router(stats.router, prefix="/api/stats", tags=["Statistics"])

@app.get("/")
async def root():
    return {
        "name": "NetaNexus API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "documentation": "/docs",
        "endpoints": {
            "candidates": "/api/candidates",
            "search": "/api/search",
            "elections": "/api/elections",
            "compare": "/api/compare",
            "exitpolls": "/api/exitpolls"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print("🚀 NetaNexus API Starting...")
    print("=" * 50)
    print("📊 Database: Connected")
    print("📚 API Docs: http://localhost:8000/docs")
    print("=" * 50)

@app.on_event("shutdown")
async def shutdown_event():
    print("👋 NetaNexus API Shutting down...")