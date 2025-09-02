import json
from pathlib import Path

SUB_FILE = Path("subscribers.json")

def load_subscribers() -> dict:
    if SUB_FILE.exists():
        return json.loads(SUB_FILE.read_text(encoding="utf-8"))
    return {}

def save_subscribers(data: dict):
    SUB_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def add_subscriber(email: str, niche: str):
    data = load_subscribers()
    niche_list = data.get(niche, [])
    if email not in niche_list:
        niche_list.append(email)
        data[niche] = niche_list
        save_subscribers(data)
        print(f"✅ Added {email} to {niche}")
    else:
        print(f"⚠️ {email} already subscribed to {niche}")

def remove_subscriber(email: str, niche: str):
    data = load_subscribers()
    if niche in data and email in data[niche]:
        data[niche].remove(email)
        save_subscribers(data)
        print(f"🗑️ Removed {email} from {niche}")
    else:
        print(f"⚠️ {email} not found in {niche}")

def get_subscribers(niche: str) -> list[str]:
    data = load_subscribers()
    return data.get(niche, [])
