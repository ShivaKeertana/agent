**AI Recruiter Agent**

An intelligent, fully automated recruitment assistant that acts as a bridge between recruiters and candidates. This system parses Job Descriptions (JDs), heavily scrapes resume data from various links provided by the users, mathematically matches candidates against the JD, and simulates a realistic AI outreach conversation to gauge candidate interest.

## Key Features

1. **Intelligent JD Parsing**: Automatically extracts required skills, optional skills, experience levels, and hidden expectations (e.g., "fast-paced" = startup mindset).
2. **Heavy-Duty Candidate Scraper**: Bypasses Google Drive security/viewers to download raw PDFs directly, and uses BeautifulSoup to clean and extract text from standard webpage portfolios or GitHub profiles.
3. **Strict Deterministic Matching**: Uses `temperature=0.0` LLM prompting to ruthlessly calculate a `Match Score %` and identify missing skills. Instantly rejects invalid data or cross-industry mismatched resumes.
4. **AI Engagement Agent (Simulated Outreach)**: Simulates a 3-turn SMS conversation between an AI Recruiter and the candidate to gauge their willingness to switch roles, calculating an `Interest Score`.
---

## Tech Stack & Tools

**Frontend**
* **React.js** (User Interface)
* **Tailwind CSS** (Modern styling, unified Hero tables, and Chat Modals)
* **Axios** (API communication)
* **Vite** (Ultra-fast frontend build tool)

**Backend**
* **FastAPI** (High-performance Python web framework)
* **Uvicorn** (ASGI web server)
* **SQLite3** (Lightweight local database for storing candidate records)
* **Pydantic** (Strict data validation and serialization)

**AI & Web Scraping**
* **Groq API (Llama-3.1-8b)** (Lightning-fast, open-source AI engine)
* **OpenAI Python SDK** (Used to interface seamlessly with the Groq API)
* **BeautifulSoup4** (HTML parsing and web text extraction)
* **pdfplumber** (High-fidelity PDF text extraction from memory)

---

## System Workflow & Architecture
<img width="1470" height="956" alt="Screenshot 2026-04-26 at 7 11 01 PM" src="https://github.com/user-attachments/assets/8f259032-1e02-4d61-a7f2-207949a039e6" />


**How to Run the Project (Step-by-Step)**

## Step 1: Clone the Repository
Ensure you have Python 3.10+ and Node.js installed on your machine.

## Step 2: Set up the Backend
Open a terminal and navigate to the backend directory:
          cd ai_recruiter_backend
          
Create a virtual environment (optional but recommended):
          python -m venv venv
          
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install the required Python packages:
          pip install fastapi uvicorn pydantic openai python-dotenv requests beautifulsoup4 pdfplumber

Create a .env file in the backend folder and add your free Groq API key:
          GROQ_API_KEY=gsk_your_api_key_here

Start the FastAPI server:
          uvicorn main:app --reload
          
## Step 3: Set up the Frontend
Open a new terminal and navigate to the frontend directory:
          cd ai-recruiter-ui
          
Install the Node modules:
          npm install

Start the Vite development server:
          npm run dev

Open your browser and go to **http://localhost:5173**.


**Usage Guide**

1. Input JD: Paste the Job Description into the left text box on the UI.
2. Input Links: Paste Candidate Resume Links into the right text box (one per line). Note: Ensure Google Drive links have access set to "Anyone with the link can view".
3. Execute: Click Discover & Screen Candidates.


**Analyze:**
View the parsed JD card on the left.
View the Ranked Shortlist in the center table.
Click "View Chat" to open a modal and read the AI's simulated engagement conversation with the candidate.

**How it looks :**
<img width="1452" height="409" alt="Screenshot 2026-04-26 at 7 13 26 PM" src="https://github.com/user-attachments/assets/ad2bf915-84a8-4c3d-8dcd-ff559a3ebe7d" />
<img width="1364" height="816" alt="Screenshot 2026-04-26 at 7 16 32 PM" src="https://github.com/user-attachments/assets/8d3850af-91c5-49b1-b415-d989f773f144" />
<img width="1367" height="549" alt="Screenshot 2026-04-26 at 7 17 10 PM" src="https://github.com/user-attachments/assets/1039ecef-4283-4189-b817-04e002fc68b9" />

