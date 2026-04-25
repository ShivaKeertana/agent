from pydantic import BaseModel
from typing import List

# --- JD Models ---
class JDParsingResult(BaseModel):
    required_skills: List[str]
    optional_skills: List[str]
    experience_level: str
    role_type: str
    hidden_expectations: str

# --- Candidate Models ---
class ChatMessage(BaseModel):
    role: str # "AI" or "Candidate"
    message: str

class CandidateProcessingResult(BaseModel):
    id: str
    name: str
    match_score: int
    skill_match_percentage: int
    missing_skills: List[str]
    chat_log: List[ChatMessage]
    interest_level: str # "High", "Medium", "Low"
    interest_score: int
    final_score: int
    status: str # "⭐ Recommended" or "⚠️ Risk"
    reason: str

# --- API Request Models ---
class ProcessRequest(BaseModel):
    job_description: str
    resume_links: List[str]