"""SQLAlchemy ORM 모델 — DB 스키마와 동일."""
from datetime import datetime
from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base


class Brand(Base):
    __tablename__ = "brand"

    brand_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    brand_name: Mapped[str] = mapped_column(String(100), nullable=False)
    platform: Mapped[str] = mapped_column(String(30), nullable=False)
    account_handle: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="brand")


class Post(Base):
    __tablename__ = "post"

    post_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    brand_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("brand.brand_id"), nullable=False)
    platform: Mapped[str] = mapped_column(String(30), nullable=False)
    external_post_id: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str | None] = mapped_column(Text)
    media_urls: Mapped[dict | None] = mapped_column(JSON)
    hashtags: Mapped[dict | None] = mapped_column(JSON)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    comments: Mapped[int] = mapped_column(Integer, default=0)
    shares: Mapped[int] = mapped_column(Integer, default=0)
    views: Mapped[int] = mapped_column(BigInteger, default=0)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime)
    crawled_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    brand: Mapped["Brand"] = relationship("Brand", back_populates="posts")
