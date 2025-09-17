import os
from dotenv import load_dotenv  # if using .env file

load_dotenv()  # if using .env file
token = os.getenv("GITHUB_PAT")

if token:
    print(f"✅ Token found: {token[:10]}...")
    print(f"Token length: {len(token)}")
else:
    print("❌ No token found")
    print("Available env vars:", [k for k in os.environ.keys() if 'GITHUB' in k.upper()])