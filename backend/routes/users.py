from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import hashlib
import secrets
from typing import Optional

from backend.database import get_db
from backend.models import User, Bookmark, Candidate

router = APIRouter()

# Simple password hashing (no external dependencies)
def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"{salt}:{hash_obj.hexdigest()}"

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    try:
        salt, original_hash = hashed.split(':')
        new_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return new_hash == original_hash
    except:
        return False

def generate_session_token() -> str:
    """Generate simple session token"""
    return secrets.token_urlsafe(32)

@router.post("/register")
async def register_user(
    email: str,
    password: str,
    name: Optional[str] = None,
    voter_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    
    # Check if user exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user = User(
        email=email,
        password_hash=hash_password(password),
        name=name,
        voter_id=voter_id,
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Generate session token
    session_token = generate_session_token()
    
    return {
        "message": "User created successfully",
        "user_id": user.id,
        "session_token": session_token,
        "name": user.name
    }

@router.post("/login")
async def login_user(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    """Login user"""
    
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    session_token = generate_session_token()
    
    return {
        "message": "Login successful",
        "user_id": user.id,
        "session_token": session_token,
        "name": user.name,
        "email": user.email
    }

@router.post("/bookmark/{candidate_id}")
async def add_bookmark(
    candidate_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Add candidate to user's bookmarks"""
    
    # Check if candidate exists
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Check if already bookmarked
    existing = db.query(Bookmark).filter(
        Bookmark.user_id == user_id,
        Bookmark.candidate_id == candidate_id
    ).first()
    
    if existing:
        return {"message": "Bookmark already exists", "bookmarked": True}
    
    bookmark = Bookmark(
        user_id=user_id,
        candidate_id=candidate_id,
        created_at=datetime.utcnow()
    )
    db.add(bookmark)
    db.commit()
    
    return {"message": "Bookmark added", "bookmarked": True}

@router.delete("/bookmark/{candidate_id}")
async def remove_bookmark(
    candidate_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Remove bookmark"""
    
    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == user_id,
        Bookmark.candidate_id == candidate_id
    ).first()
    
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    db.delete(bookmark)
    db.commit()
    
    return {"message": "Bookmark removed", "bookmarked": False}

@router.get("/bookmarks/{user_id}")
async def get_bookmarks(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user's bookmarked candidates"""
    
    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == user_id).all()
    
    candidates = []
    for b in bookmarks:
        candidate = db.query(Candidate).filter(Candidate.id == b.candidate_id).first()
        if candidate:
            candidates.append({
                "id": candidate.id,
                "name": candidate.name,
                "party": candidate.party,
                "constituency_name": candidate.constituency_name,
                "is_current": candidate.is_current
            })
    
    return {
        "total": len(candidates),
        "bookmarks": candidates
    }

@router.get("/check-bookmark/{candidate_id}")
async def check_bookmark(
    candidate_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Check if candidate is bookmarked by user"""
    
    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == user_id,
        Bookmark.candidate_id == candidate_id
    ).first()
    
    return {"bookmarked": bookmark is not None}