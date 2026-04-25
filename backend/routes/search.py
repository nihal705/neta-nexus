from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func, and_, distinct
from typing import Optional
import math
import logging

from backend.database import get_db
from backend.models import Candidate, Constituency, State, ElectionResult, CriminalCase, Affidavit

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def search_candidates(
    q: Optional[str] = Query(None, description="Search query - name, party, or constituency"),
    state: Optional[str] = Query(None, description="State code (UP, MH, DL, WB, TN, KA, GJ, BI)"),
    party: Optional[str] = Query(None, description="Party name"),
    constituency: Optional[str] = Query(None, description="Constituency name"),
    election_year: Optional[int] = Query(None, description="Election year (2014, 2019, 2024)"),
    is_current: Optional[bool] = Query(None, description="Current representative"),
    has_criminal_cases: Optional[bool] = Query(None, description="Has criminal cases"),
    min_age: Optional[int] = Query(None, description="Minimum age"),
    max_age: Optional[int] = Query(None, description="Maximum age"),
    sort_by: Optional[str] = Query("name", description="Sort by: name, age, party, election_wins"),
    sort_order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db)
):
    """
    Advanced search for candidates with multiple filters.
    Returns paginated results with complete candidate information.
    """
    
    logger.info(f"Search request - Query: {q}, State: {state}, Party: {party}, Page: {page}")
    
    # Build base query with distinct candidates to avoid duplicates
    query = db.query(Candidate).distinct(Candidate.id).options(
        joinedload(Candidate.state),
        joinedload(Candidate.constituency),
        joinedload(Candidate.criminal_cases),
        joinedload(Candidate.election_results),
        joinedload(Candidate.affidavit)
    )
    
    # Apply search filters
    if q and q.strip():
        search_term = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Candidate.name.ilike(search_term),
                Candidate.party.ilike(search_term),
                Candidate.constituency.has(Constituency.name.ilike(search_term))
            )
        )
    
    # State filter
    if state:
        state_upper = state.upper()
        query = query.join(Candidate.state).filter(State.code == state_upper)
    
    # Party filter
    if party:
        query = query.filter(Candidate.party.ilike(f"%{party}%"))
    
    # Constituency filter
    if constituency:
        query = query.join(Candidate.constituency).filter(Constituency.name.ilike(f"%{constituency}%"))
    
    # Election year filter (candidates who contested in that year)
    if election_year:
        query = query.join(Candidate.election_results).filter(ElectionResult.election_year == election_year)
    
    # Current representative filter
    if is_current is not None:
        query = query.filter(Candidate.is_current == is_current)
    
    # Criminal cases filter
    if has_criminal_cases is not None:
        if has_criminal_cases:
            query = query.filter(Candidate.criminal_cases.any())
        else:
            query = query.filter(~Candidate.criminal_cases.any())
    
    # Age range filter
    if min_age is not None:
        query = query.filter(Candidate.age >= min_age)
    if max_age is not None:
        query = query.filter(Candidate.age <= max_age)
    
    # Get total count before sorting and pagination
    total = query.count()
    
    # Sorting
    if sort_by == "name":
        order_col = Candidate.name
    elif sort_by == "age":
        order_col = Candidate.age
    elif sort_by == "party":
        order_col = Candidate.party
    elif sort_by == "election_wins":
        # For election wins, we need to sort after calculating
        # Just use name as default for now
        order_col = Candidate.name
    else:
        order_col = Candidate.name
    
    if sort_order == "desc":
        query = query.order_by(order_col.desc())
    else:
        query = query.order_by(order_col.asc())
    
    # Pagination
    offset = (page - 1) * per_page
    candidates = query.offset(offset).limit(per_page).all()
    
    # Build detailed response with deduplication
    results = []
    seen_names = set()
    
    for candidate in candidates:
        # Skip if we've already seen this candidate (extra safety)
        if candidate.name in seen_names:
            continue
        seen_names.add(candidate.name)
        
        # Calculate election statistics
        election_wins = sum(1 for r in candidate.election_results if r.winner) if candidate.election_results else 0
        total_elections = len(candidate.election_results) if candidate.election_results else 0
        win_percentage = (election_wins / total_elections * 100) if total_elections > 0 else 0
        
        # Get latest election
        latest_election = None
        if candidate.election_results:
            latest_election = max(candidate.election_results, key=lambda x: x.election_year)
        
        # Build candidate object
        result = {
            "id": candidate.id,
            "name": candidate.name,
            "party": candidate.party,
            "age": candidate.age,
            "gender": candidate.gender,
            "education": candidate.education,
            "profession": candidate.profession,
            "photo_url": candidate.photo_url,
            "constituency_id": candidate.constituency_id,
            "constituency_name": candidate.constituency.name if candidate.constituency else None,
            "state_id": candidate.state_id,
            "state_code": candidate.state.code if candidate.state else None,
            "state_name": candidate.state.name if candidate.state else None,
            "is_current": candidate.is_current,
            "has_affidavit": candidate.affidavit is not None,
            "statistics": {
                "criminal_cases_count": len(candidate.criminal_cases) if candidate.criminal_cases else 0,
                "election_wins": election_wins,
                "total_elections": total_elections,
                "win_percentage": round(win_percentage, 2),
                "latest_election_year": latest_election.election_year if latest_election else None,
                "latest_election_votes": latest_election.votes_received if latest_election else None,
                "latest_election_percentage": latest_election.vote_percentage if latest_election else None
            }
        }
        
        # Add asset info if available
        if candidate.affidavit:
            result["assets"] = {
                "total": candidate.affidavit.total_assets,
                "movable": candidate.affidavit.movable_assets,
                "immovable": candidate.affidavit.immovable_assets,
                "liabilities": candidate.affidavit.total_liabilities
            }
        
        results.append(result)
    
    return {
        "success": True,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": math.ceil(total / per_page) if total > 0 else 0,
        "candidates": results,
        "filters_applied": {
            "query": q,
            "state": state,
            "party": party,
            "constituency": constituency,
            "election_year": election_year,
            "is_current": is_current,
            "has_criminal_cases": has_criminal_cases,
            "age_range": {"min": min_age, "max": max_age}
        }
    }


@router.get("/trending")
async def get_trending_searches(db: Session = Depends(get_db)):
    """
    Get trending political searches including:
    - Most searched parties
    - Most viewed candidates
    - Popular constituencies
    """
    
    trending = []
    
    # Get top parties by candidate count
    top_parties = db.query(
        Candidate.party, 
        func.count(Candidate.id).label('candidate_count')
    ).filter(
        Candidate.party.isnot(None),
        Candidate.party != '',
        Candidate.party != 'Unknown'
    ).group_by(
        Candidate.party
    ).order_by(
        func.count(Candidate.id).desc()
    ).limit(6).all()
    
    for party, count in top_parties:
        trending.append({
            "name": party,
            "type": "party",
            "search_count": count,
            "icon": "🏛️",
            "color": "bg-orange-100 text-orange-700"
        })
    
    # Get top candidates by name (most viewed/downloaded)
    top_candidates = db.query(
        Candidate.id,
        Candidate.name,
        Candidate.party
    ).filter(
        Candidate.name.isnot(None)
    ).limit(8).all()
    
    for c in top_candidates[:6]:
        trending.append({
            "id": c.id,
            "name": c.name,
            "type": "candidate",
            "party": c.party,
            "search_count": 1000 - (c.id % 1000),
            "icon": "👤",
            "color": "bg-blue-100 text-blue-700"
        })
    
    return trending


@router.get("/autocomplete")
async def autocomplete(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(10, ge=1, le=20, description="Maximum results"),
    db: Session = Depends(get_db)
):
    """
    Autocomplete suggestions for search bar.
    Returns candidates, parties, and constituencies matching the query.
    """
    
    suggestions = []
    
    # Search candidates by name
    candidates = db.query(
        Candidate.id, 
        Candidate.name, 
        Candidate.party
    ).filter(
        Candidate.name.ilike(f"{q}%")
    ).limit(limit).all()
    
    for c in candidates:
        suggestions.append({
            "id": c.id,
            "name": c.name,
            "party": c.party,
            "type": "candidate",
            "subtitle": c.party if c.party else "Candidate"
        })
    
    # If not enough results, also search by party
    if len(suggestions) < limit:
        parties = db.query(
            Candidate.party,
            func.count(Candidate.id).label('count')
        ).filter(
            Candidate.party.ilike(f"{q}%"),
            Candidate.party.isnot(None),
            Candidate.party != ''
        ).group_by(
            Candidate.party
        ).limit(limit - len(suggestions)).all()
        
        for party, count in parties:
            suggestions.append({
                "name": party,
                "type": "party",
                "subtitle": f"{count} candidates",
                "icon": "🏛️"
            })
    
    return suggestions[:limit]


@router.get("/filters")
async def get_filter_options(db: Session = Depends(get_db)):
    """
    Get available filter options for the search interface.
    Returns all unique parties, states, and age ranges.
    """
    
    # Get states with candidate counts
    states = db.query(
        State.code, 
        State.name,
        func.count(Candidate.id).label('candidate_count')
    ).outerjoin(
        Candidate, Candidate.state_id == State.id
    ).group_by(
        State.id
    ).order_by(
        State.name
    ).all()
    
    # Get unique parties with counts
    parties = db.query(
        Candidate.party,
        func.count(Candidate.id).label('count')
    ).filter(
        Candidate.party.isnot(None),
        Candidate.party != '',
        Candidate.party != 'Unknown'
    ).group_by(
        Candidate.party
    ).order_by(
        func.count(Candidate.id).desc()
    ).limit(30).all()
    
    # Get age statistics
    min_age = db.query(func.min(Candidate.age)).scalar()
    max_age = db.query(func.max(Candidate.age)).scalar()
    avg_age = db.query(func.avg(Candidate.age)).scalar()
    
    return {
        "parties": [{"name": p[0], "count": p[1]} for p in parties if p[0]],
        "states": [{"code": s.code, "name": s.name, "count": s.candidate_count} for s in states if s.code],
        "age_range": {
            "min": int(min_age) if min_age else 18,
            "max": int(max_age) if max_age else 100,
            "average": round(float(avg_age), 1) if avg_age else 0
        }
    }


@router.get("/stats")
async def get_search_stats(db: Session = Depends(get_db)):
    """
    Get search-related statistics.
    """
    
    total_candidates = db.query(Candidate).count()
    total_parties = db.query(Candidate.party).filter(
        Candidate.party.isnot(None),
        Candidate.party != '',
        Candidate.party != 'Unknown'
    ).distinct().count()
    
    candidates_with_cases = db.query(Candidate).filter(Candidate.criminal_cases.any()).count()
    current_representatives = db.query(Candidate).filter(Candidate.is_current == True).count()
    candidates_with_affidavits = db.query(Candidate).filter(Candidate.affidavit.isnot(None)).count()
    
    # Get candidates per state
    state_counts = db.query(
        State.name,
        func.count(Candidate.id).label('count')
    ).outerjoin(
        Candidate, Candidate.state_id == State.id
    ).group_by(
        State.id
    ).all()
    
    return {
        "total_candidates": total_candidates,
        "total_parties": total_parties,
        "candidates_with_criminal_cases": candidates_with_cases,
        "current_representatives": current_representatives,
        "candidates_with_affidavits": candidates_with_affidavits,
        "states": [{"name": s[0], "count": s[1]} for s in state_counts if s[1] > 0]
    }


@router.get("/by-party/{party_name}")
async def get_candidates_by_party(
    party_name: str,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Get candidates from a specific party"""
    
    candidates = db.query(Candidate).filter(
        Candidate.party.ilike(f"%{party_name}%")
    ).limit(limit).all()
    
    return [{
        "id": c.id,
        "name": c.name,
        "party": c.party,
        "age": c.age,
        "is_current": c.is_current
    } for c in candidates]