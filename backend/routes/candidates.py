from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional, List
import logging

from backend.database import get_db
from backend.models import Candidate, State, Constituency, Affidavit, CriminalCase, ElectionResult, ParliamentaryScore

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/{candidate_id}")
async def get_candidate(
    candidate_id: int, 
    include_scores: bool = Query(True, description="Include parliamentary scores"),
    include_details: bool = Query(True, description="Include all details"),
    db: Session = Depends(get_db)
):
    """
    Get complete candidate details including:
    - Personal information
    - Constituency and state details
    - Affidavit with assets
    - Criminal cases
    - Election history
    - Parliamentary performance scores
    """
    
    logger.info(f"Fetching candidate details for ID: {candidate_id}")
    
    # Load candidate with all relationships
    query = db.query(Candidate).options(
        joinedload(Candidate.state),
        joinedload(Candidate.constituency),
        joinedload(Candidate.affidavit),
        joinedload(Candidate.criminal_cases),
        joinedload(Candidate.election_results),
        joinedload(Candidate.parliamentary_score)
    )
    
    candidate = query.filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Candidate with ID {candidate_id} not found")
    
    # Build base response
    result = {
        "id": candidate.id,
        "name": candidate.name,
        "party": candidate.party,
        "age": candidate.age,
        "gender": candidate.gender,
        "education": candidate.education,
        "profession": candidate.profession,
        "photo_url": candidate.photo_url,
        "is_current": candidate.is_current,
        "created_at": candidate.created_at.isoformat() if candidate.created_at else None,
        "updated_at": candidate.updated_at.isoformat() if candidate.updated_at else None
    }
    
    # Add constituency information
    if candidate.constituency:
        result["constituency"] = {
            "id": candidate.constituency.id,
            "name": candidate.constituency.name,
            "type": candidate.constituency.type,
            "district": candidate.constituency.district,
            "total_voters": candidate.constituency.total_voters,
            "reservation": candidate.constituency.reservation
        }
    else:
        result["constituency"] = None
    
    # Add state information
    if candidate.state:
        result["state"] = {
            "id": candidate.state.id,
            "code": candidate.state.code,
            "name": candidate.state.name,
            "capital": candidate.state.capital
        }
    else:
        result["state"] = None
    
    # Add affidavit details
    if candidate.affidavit and include_details:
        result["affidavit"] = {
            "total_assets": candidate.affidavit.total_assets,
            "movable_assets": candidate.affidavit.movable_assets,
            "immovable_assets": candidate.affidavit.immovable_assets,
            "total_liabilities": candidate.affidavit.total_liabilities,
            "annual_income": candidate.affidavit.annual_income,
            "education_details": candidate.affidavit.education_details,
            "profession_details": candidate.affidavit.profession_details,
            "filed_on": candidate.affidavit.filed_on.isoformat() if candidate.affidavit.filed_on else None
        }
    else:
        result["affidavit"] = None
    
    # Add criminal cases
    if candidate.criminal_cases and include_details:
        result["criminal_cases"] = []
        for case in candidate.criminal_cases:
            result["criminal_cases"].append({
                "id": case.id,
                "case_number": case.case_number,
                "case_type": case.case_type,
                "sections": case.sections,
                "court_name": case.court_name,
                "status": case.status,
                "filed_before_election": case.filed_before_election,
                "filed_after_election": case.filed_after_election,
                "case_details": case.case_details
            })
    else:
        result["criminal_cases"] = []
    
    # Add election results
    if candidate.election_results:
        result["election_results"] = []
        for election in candidate.election_results:
            result["election_results"].append({
                "id": election.id,
                "election_year": election.election_year,
                "election_type": election.election_type,
                "constituency_id": election.constituency_id,
                "votes_received": election.votes_received,
                "vote_percentage": election.vote_percentage,
                "winner": election.winner,
                "margin": election.margin
            })
        
        # Calculate election statistics
        total_elections = len(candidate.election_results)
        wins = sum(1 for e in candidate.election_results if e.winner)
        total_votes = sum(e.votes_received for e in candidate.election_results if e.votes_received)
        
        result["election_statistics"] = {
            "total_elections_contested": total_elections,
            "total_elections_won": wins,
            "win_percentage": round((wins / total_elections * 100), 2) if total_elections > 0 else 0,
            "total_votes_received": total_votes,
            "average_vote_percentage": round(sum(e.vote_percentage for e in candidate.election_results if e.vote_percentage) / total_elections, 2) if total_elections > 0 else 0
        }
    else:
        result["election_results"] = []
        result["election_statistics"] = {}
    
    # Add parliamentary score
    if candidate.parliamentary_score and include_scores:
        result["parliamentary_score"] = {
            "year": candidate.parliamentary_score.year,
            "attendance_percentage": candidate.parliamentary_score.attendance_percentage,
            "questions_asked": candidate.parliamentary_score.questions_asked,
            "debates_participated": candidate.parliamentary_score.debates_participated,
            "private_member_bills": candidate.parliamentary_score.private_member_bills,
            "composite_score": candidate.parliamentary_score.composite_score
        }
        
        # Determine performance rating
        score = candidate.parliamentary_score.composite_score
        if score >= 80:
            rating = "Excellent"
        elif score >= 65:
            rating = "Good"
        elif score >= 50:
            rating = "Average"
        else:
            rating = "Needs Improvement"
        
        result["parliamentary_score"]["rating"] = rating
    else:
        result["parliamentary_score"] = None
    
    return result


@router.get("/by-state/{state_code}")
async def get_candidates_by_state(
    state_code: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    is_current: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all candidates from a specific state with pagination."""
    
    # Find state
    state = db.query(State).filter(State.code == state_code.upper()).first()
    if not state:
        raise HTTPException(status_code=404, detail=f"State with code {state_code} not found")
    
    # Build query
    query = db.query(Candidate).filter(Candidate.state_id == state.id)
    
    if is_current is not None:
        query = query.filter(Candidate.is_current == is_current)
    
    total = query.count()
    offset = (page - 1) * per_page
    candidates = query.offset(offset).limit(per_page).all()
    
    return {
        "state": {
            "code": state.code,
            "name": state.name,
            "capital": state.capital
        },
        "total_candidates": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page,
        "candidates": [
            {
                "id": c.id,
                "name": c.name,
                "party": c.party,
                "age": c.age,
                "constituency_name": c.constituency.name if c.constituency else None,
                "is_current": c.is_current,
                "criminal_cases": len(c.criminal_cases)
            }
            for c in candidates
        ]
    }


@router.get("/by-party/{party_name}")
async def get_candidates_by_party(
    party_name: str,
    state_code: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Get all candidates from a specific party."""
    
    query = db.query(Candidate).filter(Candidate.party.ilike(f"%{party_name}%"))
    
    if state_code:
        query = query.join(Candidate.state).filter(State.code == state_code.upper())
    
    total = query.count()
    offset = (page - 1) * per_page
    candidates = query.offset(offset).limit(per_page).all()
    
    return {
        "party": party_name,
        "total_candidates": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page,
        "candidates": [
            {
                "id": c.id,
                "name": c.name,
                "age": c.age,
                "state_name": c.state.name if c.state else None,
                "constituency_name": c.constituency.name if c.constituency else None,
                "is_current": c.is_current,
                "election_wins": sum(1 for r in c.election_results if r.winner)
            }
            for c in candidates
        ]
    }


@router.get("/compare/")
async def compare_candidates(
    ids: str = Query(..., description="Comma-separated candidate IDs (e.g., 1,2,3)"),
    db: Session = Depends(get_db)
):
    """
    Compare multiple candidates side by side.
    Max 5 candidates at a time.
    """
    
    candidate_ids = [int(x.strip()) for x in ids.split(",")]
    
    if len(candidate_ids) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 candidates can be compared at once")
    
    if len(candidate_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 candidates required for comparison")
    
    candidates = db.query(Candidate).filter(Candidate.id.in_(candidate_ids)).all()
    
    if len(candidates) != len(candidate_ids):
        found_ids = [c.id for c in candidates]
        missing = set(candidate_ids) - set(found_ids)
        raise HTTPException(status_code=404, detail=f"Candidates not found: {missing}")
    
    comparison = []
    for candidate in candidates:
        comparison.append({
            "id": candidate.id,
            "name": candidate.name,
            "party": candidate.party,
            "age": candidate.age,
            "education": candidate.education,
            "profession": candidate.profession,
            "state": candidate.state.name if candidate.state else None,
            "constituency": candidate.constituency.name if candidate.constituency else None,
            "is_current": candidate.is_current,
            "criminal_cases": len(candidate.criminal_cases),
            "election_wins": sum(1 for r in candidate.election_results if r.winner),
            "total_votes": sum(r.votes_received for r in candidate.election_results if r.votes_received),
            "assets": candidate.affidavit.total_assets if candidate.affidavit else None,
            "liabilities": candidate.affidavit.total_liabilities if candidate.affidavit else None
        })
    
    return {
        "total_candidates": len(comparison),
        "comparison": comparison
    }


@router.get("/search/by-name/")
async def search_candidates_by_name(
    name: str = Query(..., min_length=2),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Quick search candidates by name (autocomplete)."""
    
    candidates = db.query(Candidate).filter(
        Candidate.name.ilike(f"%{name}%")
    ).limit(limit).all()
    
    return [
        {
            "id": c.id,
            "name": c.name,
            "party": c.party,
            "constituency": c.constituency.name if c.constituency else None,
            "state": c.state.code if c.state else None
        }
        for c in candidates
    ]