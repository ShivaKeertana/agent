import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Pointing the OpenAI client to Groq's Free Open Source API
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# We are using Meta's Open Source Llama 3 model
MODEL_NAME = "llama-3.1-8b-instant"

def parse_jd_with_ai(jd_text: str) -> dict:
    prompt = f"""
    Analyze the following Job Description. Extract the required skills, optional skills, 
    experience level, role type (e.g., Frontend, Backend, Fullstack), and any hidden expectations 
    (e.g., "fast-paced" = startup mindset).
    
    Return EXACTLY in this JSON format:
    {{
        "required_skills":[],
        "optional_skills":[],
        "experience_level": "",
        "role_type": "",
        "hidden_expectations": ""
    }}
    
    Job Description: {jd_text}
    """
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": "You are an expert technical recruiter AI. Always output valid JSON."},
                  {"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def match_candidate(jd_json: dict, resume_text: str) -> dict:
    prompt = f"""
    Compare this candidate's resume with the Job Description JSON.
    Calculate a match score (0-100), skill match percentage (0-100), and list missing skills.
    Also extract the candidate's full name.
    
    JD JSON: {json.dumps(jd_json)}
    Resume Text: {resume_text}
    
    Return EXACTLY in this JSON format:
    {{
        "name": "Candidate Name",
        "match_score": 85,
        "skill_match_percentage": 80,
        "missing_skills": ["skill1", "skill2"]
    }}
    """
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": "You are an AI that outputs strictly valid JSON."},
                  {"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def simulate_engagement(candidate_name: str, role_type: str, match_score: int) -> dict:
    prompt = f"""
    Simulate a short 3-turn SMS conversation between an AI Recruiter and {candidate_name} for a {role_type} role.
    Generate a realistic candidate response (can be highly interested, slightly interested, or not interested).
    Based on their response, assign an interest_level ("High", "Medium", "Low") and an interest_score (0-100).
    
    Return EXACTLY in this JSON format:
    {{
        "chat_log":[
            {{"role": "AI", "message": "Hi {candidate_name}, we found your profile relevant for a {role_type} role. Are you open to new opportunities?"}},
            {{"role": "Candidate", "message": "..."}},
            {{"role": "AI", "message": "..."}}
        ],
        "interest_level": "High",
        "interest_score": 95,
        "reason": "Short explanation of their response"
    }}
    """
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": "You are an AI that outputs strictly valid JSON."},
                  {"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)