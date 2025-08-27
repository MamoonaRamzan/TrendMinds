import os
from pathlib import Path

# Project structure (empty files for now)
structure = {
    "README.md": "",
    "requirements.txt": "",
    ".env.example": "GROQ_API_KEY=your_groq_key_here\nGROQ_MODEL=llama-3.1-70b-versatile\n",
    "config.yml": "",
    "data": {
        "raw": {},
        "chroma": {}
    },
    "output": {},
    "src": {
        "utils.py": "",
        "fetch.py": "",
        "index.py": "",
        "chains.py": "",
        "newsletter.py": "",
        "run.py": ""
    },
    "app_streamlit.py": ""
}

def create_structure(base_path: str | Path, structure: dict):
    for name, content in structure.items():
        path = Path(base_path) / name
        if isinstance(content, dict):
            path.mkdir(parents=True, exist_ok=True)
            create_structure(path, content)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():  # don’t overwrite if already exists
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)

if __name__ == "__main__":
    base_dir = Path(".")  # current project directory
    create_structure(base_dir, structure)
    print("✅ Project scaffold created. Now paste code into the created files.")
