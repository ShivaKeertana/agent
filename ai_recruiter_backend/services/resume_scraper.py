import requests
import re
import pdfplumber
import io
from bs4 import BeautifulSoup

def extract_text_from_link(link: str) -> str:
    link = link.strip()
    
    # 1. Fallback: If the user pasted raw text instead of a URL, just return it!
    if not link.startswith("http"):
        if len(link) > 50:
            return link[:4000] # Treat it as raw resume text
        return "ERROR: INVALID_URL_OR_TOO_SHORT"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 2. Google Drive Smart Extractor
    drive_match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', link)
    if drive_match:
        file_id = drive_match.group(1)
        # Force Google to give us the raw download, not the web viewer
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        
        try:
            session = requests.Session()
            response = session.get(url, headers=headers, stream=True, timeout=10)
            
            # If Google Drive serves the actual PDF
            if 'application/pdf' in response.headers.get('Content-Type', ''):
                with pdfplumber.open(io.BytesIO(response.content)) as pdf:
                    text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                    return text[:4000]
            else:
                return "ERROR: GOOGLE_DRIVE_PERMISSION_DENIED_OR_NOT_PDF"
        except Exception as e:
            return f"ERROR: GOOGLE_DRIVE_FAILED - {str(e)}"

    # 3. Standard URL Extractor (Webpages, GitHub, Direct PDFs)
    try:
        response = requests.get(link, headers=headers, timeout=10)
        
        # If the link is a direct PDF file
        if 'application/pdf' in response.headers.get('Content-Type', ''):
            with pdfplumber.open(io.BytesIO(response.content)) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                return text[:4000]
        
        # If the link is a standard Web Page (use BeautifulSoup)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove invisible elements (scripts, styles)
        for script in soup(["script", "style", "nav", "footer"]):
            script.extract()
            
        text = soup.get_text(separator=' ')
        
        # Clean up weird spacing
        lines = (line.strip() for line in text.splitlines())
        text = '\n'.join(line for line in lines if line)
        
        if len(text) < 50:
            return "ERROR: PAGE_BLOCKED_OR_NO_TEXT"
            
        return text[:4000]
        
    except Exception as e:
        return f"ERROR: SCRAPING_FAILED - {str(e)}"