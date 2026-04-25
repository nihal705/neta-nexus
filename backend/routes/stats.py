from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models import Candidate, State, Constituency

router = APIRouter()

@router.get("/state-counts")
async def get_state_candidate_counts(db: Session = Depends(get_db)):
    """Get candidate counts per state"""
    
    results = db.query(
        State.id,
        State.code,
        State.name,
        func.count(Candidate.id).label('candidate_count')
    ).outerjoin(
        Candidate, Candidate.state_id == State.id
    ).group_by(
        State.id
    ).all()
    
    return {r.code: r.candidate_count for r in results if r.candidate_count > 0}

@router.get("/constituency-counts")
async def get_constituency_counts(db: Session = Depends(get_db)):
    """Get constituency counts per state"""
    
    results = db.query(
        State.code,
        State.name,
        func.count(Constituency.id).label('constituency_count')
    ).outerjoin(
        Constituency, Constituency.state_id == State.id
    ).group_by(
        State.id
    ).all()
    
    return [{"code": r.code, "name": r.name, "count": r.constituency_count} for r in results]

@router.get("/dashboard")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    
    total_candidates = db.query(Candidate).count()
    total_states = db.query(State).count()
    total_constituencies = db.query(Constituency).count()
    
    # Candidates with criminal cases
    from backend.models import CriminalCase
    candidates_with_cases = db.query(Candidate).filter(Candidate.criminal_cases.any()).count()
    
    # Current representatives
    current_reps = db.query(Candidate).filter(Candidate.is_current == True).count()
    
    # Parties count
    parties = db.query(Candidate.party).distinct().filter(Candidate.party.isnot(None)).count()
    
    return {
        "total_candidates": total_candidates,
        "total_states": total_states,
        "total_constituencies": total_constituencies,
        "candidates_with_criminal_cases": candidates_with_cases,
        "current_representatives": current_reps,
        "total_parties": parties
    }