"""DB 연결 및 세션 팩토리."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

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