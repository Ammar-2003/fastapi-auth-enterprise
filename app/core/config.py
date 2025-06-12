# config.py (at root level or inside app/)
import os
from dotenv import load_dotenv

# Load from .env at root level
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SECRET_KEY = os.getenv("SECRET_KEY")
