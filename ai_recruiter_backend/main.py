from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ProcessRequest, CandidateProcessingResult
from services.ai_engine import parse_jd_with_ai, match_candidate, simulate_engagement
from services.resume_scraper import extract_text_from_link
import uuid
import sqlite3 # <--- ADDED DATABASE

app = FastAPI(title="AI Recruiter Agent API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('recruiter.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS candidates 
                 (id TEXT PRIMARY KEY, name TEXT, match_score INTEGER, final_score INTEGER, status TEXT)''')
    conn.commit()
    conn.close()

init_db() # Run DB setup on startup

@app.post("/api/process-recruitment", response_model=dict)
async def process_recruitment(request: ProcessRequest):
    jd_data = parse_jd_with_ai(request.job_description)
    candidates =[]
    
    for link in request.resume_links:
        # 1. Scrape (Will now catch garbage text)
        resume_text = extract_text_from_link(link)
        
        # 2. Match (Will return 0 if garbage)
        match_data = match_candidate(jd_data, resume_text)
        
        # 3. Simulate (Will skip if score is 0)
        match_score = match_data.get("match_score", 0)
        engagement_data = simulate_engagement(match_data.get("name", "Unknown"), jd_data.get("role_type", "Tech"), match_score)
        
        # 4. Final Score & Status
        interest_score = engagement_data.get("interest_score", 0)
        final_score = int((match_score * 0.6) + (interest_score * 0.4))
        
        status = "⚠️ Risk" if final_score < 75 else "⭐ Recommended"
        if match_score == 0:
            status = "❌ Rejected (Invalid Data)"
            
        cand_id = str(uuid.uuid4())[:8]
        name = match_data.get("name", "Unknown")
        
        # --- SAVE TO DATABASE ---
        conn = sqlite3.connect('recruiter.db')
        c = conn.cursor()
        c.execute("INSERT INTO candidates (id, name, match_score, final_score, status) VALUES (?, ?, ?, ?, ?)", 
                  (cand_id, name, match_score, final_score, status))
        conn.commit()
        conn.close()

        candidates.append(CandidateProcessingResult(
            id=cand_id, name=name, match_score=match_score,
            skill_match_percentage=match_data.get("skill_match_percentage", 0),
            missing_skills=match_data.get("missing_skills", []),
            chat_log=engagement_data.get("chat_log",[]),
            interest_level=engagement_data.get("interest_level", "Low"),
            interest_score=interest_score,
            final_score=final_score,
            status=status,
            reason=engagement_data.get("reason", "Invalid Data")
        ))
        
    # Sort candidates by final score descending
    candidates.sort(key=lambda x: x.final_score, reverse=True)
    
    return {
        "jd_summary": jd_data,
        "candidates": candidates
    }

# --- ADD THIS TO PROVE THE DATABASE WORKS! ---
@app.get("/api/database-history")
async def get_database_history():
    conn = sqlite3.connect('recruiter.db')
    c = conn.cursor()
    c.execute("SELECT * FROM candidates ORDER BY final_score DESC")
    rows = c.fetchall()
    conn.close()
    
    history = []
    for r in rows:
        history.append({"id": r[0], "name": r[1], "match_score": r[2], "final_score": r[3], "status": r[4]})
    return {"saved_candidates": history}