
"""
Database configuration module.
- Docker 환경과 로컬 환경 모두 지원
- 커넥션 풀 및 컨텍스트 매니저 패턴 제공
"""
from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import pymysql
from dotenv import load_dotenv
from pymysql.cursors import DictCursor

logger = logging.getLogger(__name__)

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


class DatabaseConfig:
    """데이터베이스 설정 클래스"""

    def __init__(self) -> None:
        # docker-compose 환경변수와 동일한 이름 사용
        self.host = os.getenv("DB_HOST", "127.0.0.1")
        self.port = int(os.getenv("DB_PORT", "3306"))
        self.database = os.getenv("DB_NAME", os.getenv("MYSQL_DATABASE", "crawlerdb"))
        self.user = os.getenv("DB_USER", os.getenv("MYSQL_USER", "crawler"))
        self.password = os.getenv("DB_PASSWORD", os.getenv("MYSQL_PASSWORD", "crawler1234"))
        self.charset = os.getenv("DB_CHARSET", "utf8mb4")

    def validate(self) -> None:
        """필수 환경변수 검증"""
        missing = []
        if not self.database:
            missing.append("DB_NAME 또는 MYSQL_DATABASE")
        if not self.user:
            missing.append("DB_USER 또는 MYSQL_USER")
        if not self.password:
            missing.append("DB_PASSWORD 또는 MYSQL_PASSWORD")

        if missing:
            raise RuntimeError(
                f"DB 연결 환경변수가 설정되지 않았습니다: {', '.join(missing)}\n"
                f"crawler/.env 또는 프로젝트 루트 .env 파일을 확인하세요."
            )

    def __repr__(self) -> str:
        return f"DatabaseConfig(host={self.host}, port={self.port}, database={self.database}, user={self.user})"


# 싱글턴 설정 인스턴스
_config: DatabaseConfig | None = None


def get_config() -> DatabaseConfig:
    """설정 인스턴스 반환 (싱글턴)"""
    global _config
    if _config is None:
        _config = DatabaseConfig()
    return _config


def get_connection() -> pymysql.connections.Connection:
    """
    새로운 DB 커넥션 생성.

    사용 후 반드시 close() 호출 필요.
    가능하면 get_db() 컨텍스트 매니저 사용 권장.
    """
    config = get_config()
    config.validate()

    try:
        conn = pymysql.connect(
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
            database=config.database,
            charset=config.charset,
            cursorclass=DictCursor,
            connect_timeout=10,
            read_timeout=30,
            write_timeout=30,
            autocommit=False,
        )
        logger.debug("DB 연결 성공: %s:%s/%s", config.host, config.port, config.database)
        return conn
    except pymysql.Error as e:
        logger.error("DB 연결 실패: %s", e)
        raise


@contextmanager
def get_db() -> Generator[pymysql.connections.Connection, None, None]:
    """
    DB 커넥션 컨텍스트 매니저.

    사용 예시:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM brand")
                rows = cursor.fetchall()
            conn.commit()

    - 정상 종료 시 자동 commit 없음 (명시적 commit 필요)
    - 예외 발생 시 자동 rollback
    - 종료 시 자동 close
    """
    conn = get_connection()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def test_connection() -> bool:
    """DB 연결 테스트"""
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                logger.info("DB 연결 테스트 성공: %s", result)
                return True
    except Exception as e:
        logger.error("DB 연결 테스트 실패: %s", e)
        return False


# 모듈 직접 실행 시 연결 테스트
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print(f"설정: {get_config()}")
    print(f"연결 테스트: {'성공' if test_connection() else '실패'}")