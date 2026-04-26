import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
MODEL_NAME = "llama-3.1-8b-instant"

def clean_json_response(content: str) -> dict:
    try:
        content = content.strip()
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        print(f"JSON Parsing Error: {e}\nRaw Output: {content}")
        return {}

def parse_jd_with_ai(jd_text: str) -> dict:
    prompt = f"""
    Extract details from this Job Description.
    JD: {jd_text}
    Output ONLY valid JSON:
    {{
        "required_skills": [],
        "optional_skills":[],
        "experience_level": "",
        "role_type": "",
        "hidden_expectations": ""
    }}
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME, 
            messages=[{"role": "user", "content": prompt}], 
            response_format={"type": "json_object"},
            temperature=0.0 # <--- ZERO RANDOMNESS
        )
        return clean_json_response(response.choices[0].message.content)
    except Exception:
        return {"required_skills":[], "optional_skills":[], "experience_level": "Unknown", "role_type": "Unknown", "hidden_expectations": "None"}

def match_candidate(jd_json: dict, resume_text: str) -> dict:
    # 1. Print the text to the terminal so YOU can verify the script actually read the PDF!
    print("\n--- EXTRACTED RESUME TEXT ---")
    print(resume_text[:500] + "...\n-----------------------------\n")

    if "ERROR:" in resume_text[:50]:
        return {"name": "Invalid Link / Data", "match_score": 0, "skill_match_percentage": 0, "missing_skills": [resume_text[:40]]}
        
    prompt = f"""
    You are a RUTHLESS, highly critical AI Recruiter. Your job is to mathematically evaluate the candidate.
    
    CRITICAL RULES:
    1. If the candidate's industry/role does not match the JD (e.g., Software Engineer applying for Property Manager), the match_score MUST be severely penalized (0 to 15 max).
    2. Do NOT guess. Only count skills explicitly written in the resume text.
    3. Be incredibly strict.
    
    JD JSON: {json.dumps(jd_json)}
    Resume Text: {resume_text}
    
    Output ONLY valid JSON:
    {{
        "name": "Candidate Full Name",
        "match_score": <insert strict integer 0-100>, 
        "skill_match_percentage": <insert strict integer 0-100>,
        "missing_skills": ["List missing required skills here"]
    }}
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME, 
            messages=[{"role": "user", "content": prompt}], 
            response_format={"type": "json_object"},
            temperature=0.0 # <--- ZERO RANDOMNESS (Always the exact same score for the same resume)
        )
        return clean_json_response(response.choices[0].message.content)
    except Exception:
        return {"name": "Processing Error", "match_score": 0, "skill_match_percentage": 0, "missing_skills": ["API Failed"]}

def simulate_engagement(candidate_name: str, role_type: str, match_score: int) -> dict:
    if match_score < 30: # Reject them immediately if the score is terrible
        return {
            "chat_log":[{"role": "AI", "message": f"Profile auto-rejected due to exceptionally low match score ({match_score}%)."}], 
            "interest_level": "Low", 
            "interest_score": 0, 
            "reason": "Irrelevant industry or severely lacking skills."
        }

    prompt = f"""
    Simulate a short text message outreach to {candidate_name} for a {role_type} role.
    Output ONLY valid JSON:
    {{
        "chat_log":[
            {{"role": "AI", "message": "Hi..."}}, 
            {{"role": "Candidate", "message": "..."}}
        ],
        "interest_level": "High",
        "interest_score": 90,
        "reason": "Short reason."
    }}
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME, 
            messages=[{"role": "user", "content": prompt}], 
            response_format={"type": "json_object"},
            temperature=0.2 
        )
        return clean_json_response(response.choices[0].message.content)
    except Exception:
        return {"chat_log": [{"role": "AI", "message": "Failed to simulate chat."}], "interest_level": "Low", "interest_score": 0, "reason": "API Failure"}