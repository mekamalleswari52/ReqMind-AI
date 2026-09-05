import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "devsecret")
AI_API_KEY = os.getenv("AI_API_KEY")
AI_MODEL = os.getenv("AI_MODEL")
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 5242880))
