# config.py
import os
from dotenv import load_dotenv

# Load .env file only once
load_dotenv()

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Centralize environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# DATABASE_URL = os.getenv("DATABASE_URL")

