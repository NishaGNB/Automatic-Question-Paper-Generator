import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "question_paper_db")

    # URL-encode the password to safely handle special characters like @, : etc.
    _DB_PASSWORD_ENCODED: str = quote_plus(DB_PASSWORD)

    DATABASE_URL: str = (
        f"mysql+pymysql://{DB_USER}:{_DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "CHANGE_ME")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    FILE_UPLOAD_DIR: str = os.getenv("FILE_UPLOAD_DIR", "uploaded_files")


settings = Settings()
