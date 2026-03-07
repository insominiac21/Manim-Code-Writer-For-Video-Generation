"""
MentorBoxAI - Application Configuration
All settings are loaded from environment variables / .env file.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # App
    APP_NAME: str = "MentorBoxAI"
    VERSION: str = "4.0.0"
    ENV: str = os.getenv("NODE_ENV", "development")
    PORT: int = int(os.getenv("PORT", 8000))
    CORS_ORIGIN: str = os.getenv("CORS_ORIGIN", "*")

    # Groq LLM
    GROQ_API_KEY1: str = os.getenv("GROQ_API_KEY1", "")
    GROQ_API_KEY2: str = os.getenv("GROQ_API_KEY2", "")
    GROQ_API_KEY3: str = os.getenv("GROQ_API_KEY3", "")
    GROQ_API_KEY4: str = os.getenv("GROQ_API_KEY4", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    LLM_GENERATOR_MAX_TOKENS: int = int(os.getenv("LLM_GENERATOR_MAX_TOKENS", "4096"))
    LLM_GENERATOR_TEMPERATURE: float = float(os.getenv("LLM_GENERATOR_TEMPERATURE", "0.01"))

    # AWS (for S3, DynamoDB, Lambda — not Bedrock)
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    S3_BUCKET: str = os.getenv("S3_BUCKET", "mentorbocai-videos")

    # Storage
    BASE_DIR: str = os.getenv("BASE_DIR", "")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "output")

settings = Settings()
