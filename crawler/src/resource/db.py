"""DB 연결 및 세션 팩토리."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드 (crawler/.env 또는 프로젝트 루트 .env)
_BASE_DIR = Path(__file__).resolve().parent.parent  # crawler/
_ENV_FILE = _BASE_DIR / ".env"
if _ENV_FILE.exists():
    load_dotenv(_ENV_FILE)
else:
    # 프로젝트 루트 .env 시도
    _ROOT_ENV = _BASE_DIR.parent / ".env"
    if _ROOT_ENV.exists():
        load_dotenv(_ROOT_ENV)

_DB_URL = (
    "mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"
).format(
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ.get("DB_HOST", "localhost"),
    port=os.environ.get("DB_PORT", "3306"),
    db=os.environ["DB_NAME"],
)

engine = create_engine(_DB_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass