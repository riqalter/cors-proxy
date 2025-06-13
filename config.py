import os
from dotenv import load_dotenv

load_dotenv()

ALLOWED_DOMAIN: list[str] = os.getenv("ALLOWED_DOMAIN", "").split(",")
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")