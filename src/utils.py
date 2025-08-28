import os, re, hashlib, datetime as dt
from pathlib import Path
from dotenv import load_dotenv
import yaml

load_dotenv()

def load_config(path="config.yml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ensure_dir(p: str | Path):
    Path(p).mkdir(parents=True, exist_ok=True)

def today_iso():
    return dt.date.today().isoformat()

def slugify(text: str, max_len=80):
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:max_len]

def sha1(s: str):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

def env(key: str, default: str | None = None):
    return os.getenv(key, default)
