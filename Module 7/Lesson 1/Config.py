import os
from pathlib import Path
from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent
env_file_path = current_dir / ".env"

load_dotenv(dotenv_path=env_file_path)

HF_API_KEY = os.getenv("HF_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not HF_API_KEY:
    raise ValueError("HF_API_KEY was not found in .env")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY was not found in .env")