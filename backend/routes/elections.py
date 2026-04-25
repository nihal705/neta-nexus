from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import asyncio
from datetime import datetime
import random

from backend.database import get_db
from backend.models import ElectionResult, Candidate, Constituency
from backend.schemas import LiveResultsResponse

router = APIRouter()

# Store WebSocket connections
active_connections: List[WebSocket] = []

# Mock live results (in production, fetch from ECI)
current_results = {
    "bjp": 245,
    "inc": 142,
    "others": 156,
    "last_updated": None
}

@router.get("/live-results")
async def get_live_results(
    election_id: int = Query(2024, description="Election year"),
    db: Session = Depends(get_db)
):
    """Get current live election results"""
    
    # In production, this would scrape ECI or use their API
    # For now, return mock data with realistic trends
    
    total_seats = 543
    declared = 400
    
    # Simulate realistic trends
    bjp_seats = current_results["bjp"]
    inc_seats = current_results["inc"]
    others_seats = total_seats - bjp_seats - inc_seats
    
    return LiveResultsResponse(
        election_id=election_id,
        trends={
            "bjp": bjp_seats,
            "inc": inc_seats,
            "others": others_seats
        },
        last_updated=current_results["last_updated"],
        is_counting_day=True,
        total_seats=total_seats,
        constituencies_declared=declared
    )

@router.get("/results/{election_id}/constituency/{constituency_id}")
async def get_constituency_result(
    election_id: int,
    constituency_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed results for a specific constituency"""
    
    results = db.query(ElectionResult).filter(
        ElectionResult.election_year == election_id,
        ElectionResult.constituency_id == constituency_id
    ).order_by(
        ElectionResult.votes_received.desc()
    ).all()
    
    constituency = db.query(Constituency).filter(Constituency.id == constituency_id).first()
    
    return {
        "constituency_name": constituency.name if constituency else "Unknown",
        "election_year": election_id,
        "results": [
            {
                "candidate_name": r.candidate.name if r.candidate else "Unknown",
                "party": r.candidate.party if r.candidate else "Unknown",
                "votes": r.votes_received,
                "percentage": r.vote_percentage,
                "winner": r.winner,
                "margin": r.margin if r.winner else None
            }
            for r in results
        ],
        "total_votes": sum(r.votes_received for r in results),
        "turnout_percentage": 67.8  # Mock value
    }

@router.get("/upcoming")
async def get_upcoming_elections(db: Session = Depends(get_db)):
    """Get upcoming election schedule"""
    
    # Mock data - in production, fetch from ECI
    return {
        "elections": [
            {
                "state": "Madhya Pradesh",
                "election_type": "Assembly",
                "date": "November 17, 2024",
                "seats": 230,
                "status": "Scheduled"
            },
            {
                "state": "Rajasthan",
                "election_type": "Assembly",
                "date": "November 23, 2024",
                "seats": 200,
                "status": "Scheduled"
            },
            {
                "state": "Telangana",
                "election_type": "Assembly",
                "date": "November 30, 2024",
                "seats": 119,
                "status": "Scheduled"
            }
        ]
    }

@router.websocket("/live-ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time election updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Simulate random updates every 30 seconds
            await asyncio.sleep(30)
            
            # Random variation for demo
            variation = random.randint(-3, 3)
            current_results["bjp"] = max(0, min(543, current_results["bjp"] + variation))
            current_results["inc"] = max(0, min(543, current_results["inc"] - variation))
            current_results["others"] = 543 - current_results["bjp"] - current_results["inc"]
            current_results["last_updated"] = datetime.now().isoformat()
            
            # Broadcast to all connected clients
            for connection in active_connections:
                try:
                    await connection.send_json({
                        "type": "live_update",
                        "data": current_results,
                        "timestamp": datetime.now().isoformat()
                    })
                except:
                    pass
    except WebSocketDisconnect:
        active_connections.remove(websocket)