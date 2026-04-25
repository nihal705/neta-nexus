from sqlalchemy import Column, Integer, String, Float, Date, Text, Boolean, ForeignKey, JSON, TIMESTAMP, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class State(Base):
    __tablename__ = "states"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(2), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    capital = Column(String(100))
    total_seats_assembly = Column(Integer, default=0)
    total_seats_parliamentary = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    constituencies = relationship("Constituency", back_populates="state")
    candidates = relationship("Candidate", back_populates="state")

class Constituency(Base):
    __tablename__ = "constituencies"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    type = Column(String(20), nullable=False)
    state_id = Column(Integer, ForeignKey("states.id", ondelete="SET NULL"))
    district = Column(String(100))
    total_voters = Column(Integer, default=0)
    reservation = Column(String(20))
    
    state = relationship("State", back_populates="constituencies")
    candidates = relationship("Candidate", back_populates="constituency")

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False, index=True)
    party = Column(String(100), index=True)
    age = Column(Integer)
    gender = Column(String(10))
    education = Column(String(200))
    profession = Column(String(200))
    photo_url = Column(String(500))
    constituency_id = Column(Integer, ForeignKey("constituencies.id", ondelete="SET NULL"))
    state_id = Column(Integer, ForeignKey("states.id", ondelete="SET NULL"))
    is_current = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    constituency = relationship("Constituency", back_populates="candidates")
    state = relationship("State", back_populates="candidates")
    affidavit = relationship("Affidavit", back_populates="candidate", uselist=False)
    criminal_cases = relationship("CriminalCase", back_populates="candidate")
    election_results = relationship("ElectionResult", back_populates="candidate")
    parliamentary_score = relationship("ParliamentaryScore", back_populates="candidate", uselist=False)

class Affidavit(Base):
    __tablename__ = "affidavits"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"), unique=True, nullable=False)
    total_assets = Column(String(50))
    movable_assets = Column(String(50))
    immovable_assets = Column(String(50))
    total_liabilities = Column(String(50))
    annual_income = Column(String(50))
    education_details = Column(Text)
    profession_details = Column(Text)
    filed_on = Column(Date)
    affidavit_data = Column(JSON)
    
    candidate = relationship("Candidate", back_populates="affidavit")

class CriminalCase(Base):
    __tablename__ = "criminal_cases"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    case_number = Column(String(100))
    case_type = Column(String(100))
    sections = Column(String(200))
    court_name = Column(String(200))
    status = Column(String(100))
    filed_before_election = Column(Boolean, default=False)
    filed_after_election = Column(Boolean, default=False)
    case_details = Column(Text)
    
    candidate = relationship("Candidate", back_populates="criminal_cases")

class ElectionResult(Base):
    __tablename__ = "election_results"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    election_year = Column(Integer, nullable=False, index=True)
    election_type = Column(String(50), nullable=False)
    constituency_id = Column(Integer, ForeignKey("constituencies.id", ondelete="SET NULL"))
    votes_received = Column(Integer, default=0)
    vote_percentage = Column(Float, default=0.0)
    winner = Column(Boolean, default=False)
    margin = Column(Integer, default=0)
    
    candidate = relationship("Candidate", back_populates="election_results")

class ParliamentaryScore(Base):
    __tablename__ = "parliamentary_scores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    year = Column(Integer, nullable=False)
    attendance_percentage = Column(Float, default=0.0)
    questions_asked = Column(Integer, default=0)
    debates_participated = Column(Integer, default=0)
    private_member_bills = Column(Integer, default=0)
    composite_score = Column(Float, default=0.0)
    
    candidate = relationship("Candidate", back_populates="parliamentary_score")

class ExitPoll(Base):
    __tablename__ = "exit_polls"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(String(100), nullable=False)
    election_id = Column(Integer, nullable=False)
    election_type = Column(String(50))
    prediction_data = Column(JSON, nullable=False)
    source_url = Column(String(500))
    published_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class PartySymbol(Base):
    __tablename__ = "party_symbols"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    party_name = Column(String(100), unique=True, nullable=False)
    symbol_url = Column(String(500))
    symbol_code = Column(String(50))
    color = Column(String(20))
    short_name = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    voter_id = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    bookmarks = relationship("Bookmark", back_populates="user")

class Bookmark(Base):
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    user = relationship("User", back_populates="bookmarks")
    candidate = relationship("Candidate")

class News(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    link = Column(String(500))
    description = Column(Text)
    source = Column(String(100))
    published_at = Column(TIMESTAMP)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
# Create indexes for MySQL
Index('idx_candidates_name', Candidate.name)
Index('idx_candidates_party', Candidate.party)
Index('idx_election_results_year_type', ElectionResult.election_year, ElectionResult.election_type)