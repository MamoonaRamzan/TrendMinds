from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests, os, json
from pathlib import Path
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

GITHUB_PAT = os.getenv("GITHUB_PAT")
OWNER = "MamoonaRamzan"
REPO = "News-Hub"
WORKFLOW_FILE = "subscribe.yml"

NEWS_FILE = Path("output/latest.json")  # store latest newsletter data

app = FastAPI(title="News Hub API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.post("/subscribe")
async def subscribe(request: Request):
    body = await request.json()
    email = body.get("email")
    niche = body.get("niche")

    if not email or not niche:
        return {"error": "Email and niche are required"}

    if not GITHUB_PAT:
        return {"error": "GitHub token not configured"}

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_PAT}",
        "Accept": "application/vnd.github+json"
    }
    payload = {"ref": "main", "inputs": {"email": email, "niche": niche}}

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        if r.status_code == 204:
            return {"message": f"✅ Subscribed {email} to {niche}"}
        else:
            return {"error": "GitHub API failed", "details": r.text}
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception: {e}")
        return {"error": "Network request failed"}

@app.get("/headlines/{niche}")
def get_headlines(niche: str):
    """Return full top stories (title, summary, why, url) for a given niche."""
    logger.info(f"Getting headlines for niche: {niche}")
    logger.info(f"NEWS_FILE path: {NEWS_FILE.absolute()}")
    logger.info(f"NEWS_FILE exists: {NEWS_FILE.exists()}")
    
    if not NEWS_FILE.exists():
        return {"error": "No newsletter generated yet."}

    try:
        # Try different encodings to handle the file
        content = None
        for encoding in ['utf-8', 'latin-1', 'cp1252', 'utf-8-sig']:
            try:
                content = NEWS_FILE.read_text(encoding=encoding)
                logger.info(f"Successfully read file with encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            logger.error("Could not decode file with any encoding")
            return {"error": "Newsletter data has encoding issues"}
            
        data = json.loads(content)
        logger.info(f"Available niches: {list(data.keys())}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return {"error": "Newsletter data is corrupted - invalid JSON"}
    except Exception as e:
        logger.error(f"Unexpected error reading file: {e}")
        return {"error": f"Error reading newsletter data: {str(e)}"}

    if niche not in data:
        logger.warning(f"Niche '{niche}' not found. Available: {list(data.keys())}")
        return {"error": f"No data found for niche: {niche}. Available: {list(data.keys())}"}

    stories = data[niche].get("stories", [])
    logger.info(f"Returning {len(stories)} stories for {niche}")
    return {"niche": niche, "stories": stories}

# Add a health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

# Add an endpoint to list available niches
@app.get("/niches")
def get_available_niches():
    """Return list of available niches."""
    if not NEWS_FILE.exists():
        return {"error": "No newsletter generated yet."}
    
    try:
        data = json.loads(NEWS_FILE.read_text(encoding="utf-8"))
        return {"niches": list(data.keys())}
    except json.JSONDecodeError:
        return {"error": "Newsletter data is corrupted"}
    

#python -m src.run --niche Climate
#uvicorn backend.api:app --reload