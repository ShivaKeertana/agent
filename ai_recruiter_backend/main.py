from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ProcessRequest, JDParsingResult, CandidateProcessingResult
from services.ai_engine import parse_jd_with_ai, match_candidate, simulate_engagement
from services.resume_scraper import extract_text_from_link
import uuid

app = FastAPI(title="AI Recruiter Agent API")

# Enable CORS for Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/process-recruitment", response_model=dict)
async def process_recruitment(request: ProcessRequest):
    # 1️⃣ Parse JD
    jd_data = parse_jd_with_ai(request.job_description)
    
    candidates =[]
    
    # Process each resume link
    for link in request.resume_links:
        # 2️⃣ Fetch Resume Text
        resume_text = extract_text_from_link(link)
        
        # 3️⃣ Candidate Match Scoring
        match_data = match_candidate(jd_data, resume_text)
        
        # 4️⃣ AI Engagement Simulation (The WOW Feature)
        engagement_data = simulate_engagement(
            match_data.get("name", "Candidate"), 
            jd_data.get("role_type", "Tech"), 
            match_data.get("match_score", 50)
        )
        
        # 5️⃣ Calculate Final Score & Status (Weighted Formula)
        # e.g., 60% Match Score + 40% Interest Score
        match_score = match_data.get("match_score", 0)
        interest_score = engagement_data.get("interest_score", 0)
        
        final_score = int((match_score * 0.6) + (interest_score * 0.4))
        
        status = "⭐ Recommended" if final_score >= 75 else "⚠️ Risk"
        
        candidates.append(CandidateProcessingResult(
            id=str(uuid.uuid4())[:8],
            name=match_data.get("name", "Unknown"),
            match_score=match_score,
            skill_match_percentage=match_data.get("skill_match_percentage", 0),
            missing_skills=match_data.get("missing_skills",[]),
            chat_log=engagement_data.get("chat_log",[]),
            interest_level=engagement_data.get("interest_level", "Low"),
            interest_score=interest_score,
            final_score=final_score,
            status=status,
            reason=engagement_data.get("reason", "No reason provided")
        ))
        
    # Sort candidates by final score descending (Ranked Shortlist)
    candidates.sort(key=lambda x: x.final_score, reverse=True)
    
    # Return the exact structure the frontend needs
    return {
        "jd_summary": jd_data,
        "candidates": candidates
    }