import os, re, hashlib, datetime as dt
from pathlib import Path
from dotenv import load_dotenv
import yaml
import re

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

import re

def clean_llm_output(text: str) -> str:
    """
    Cleans up LLM output by removing reasoning traces, unwanted prefixes,
    and leaving only the polished summary/points.
    """
    if not text:
        return ""

    # 1. Remove <think>...</think> reasoning blocks (common in some LLMs)
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    # 2. Remove meta-intros or reasoning phrases at the start
    bad_starts = [
        r"(?i)^summary of the provided context.*?\.",   # "summary of the provided context..."
        r"(?i)^first, i need to.*?\.",                  # "first, I need to..."
        r"(?i)^next, the.*?\.",                         # "next, the ..."
        r"(?i)^okay, let.?s.*?\.",                      # "okay, let's..."
        r"(?i)^the user wants.*?\.",                    # "the user wants..."
        r"(?i)^task:.*?\.",                             # "task: ..."
    ]
    for pat in bad_starts:
        text = re.sub(pat, "", text, flags=re.DOTALL).strip()

    # 3. Normalize spacing
    text = re.sub(r"\n{3,}", "\n\n", text)  # collapse huge line breaks
    text = text.strip()

    return text

