import requests

def extract_text_from_link(link: str) -> str:
    # In a production app, you would download the PDF and parse it using PyPDF2 or pdfplumber.
    # For this MVP, we simulate reading a resume from a URL.
    try:
        # Example if it's a plain text URL
        response = requests.get(link, timeout=5)
        if response.status_code == 200 and 'text' in response.headers.get('Content-Type', ''):
            return response.text[:2000] # Limit text
    except Exception:
        pass
    
    # MOCK DATA if URL scraping fails for the demo
    return f"Simulated Resume Data from {link}. Experience: 5 years. Skills: React, Node.js, AWS, Python. Worked at Fast Startup Inc."
