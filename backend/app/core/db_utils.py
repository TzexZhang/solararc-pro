"""
Database utility functions and context managers
"""
from contextlib import contextmanager
from typing import Generator, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.database import SessionLocal

logger = logging.getLogger(__name__)


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database session with automatic error handling

    Yields:
        Session: SQLAlchemy database session

    Example:
        with get_db_context() as db:
            db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        db.close()


def safe_commit(db: Session, max_retries: int = 3) -> bool:
    """
    Safely commit database transaction with retry logic

    Args:
        db: Database session
        max_retries: Maximum number of retry attempts

    Returns:
        True if commit successful, False otherwise
    """
    for attempt in range(max_retries):
        try:
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            if attempt == max_retries - 1:
                logger.error(f"Failed to commit after {max_retries} attempts: {e}")
                return False
            logger.warning(f"Commit failed (attempt {attempt + 1}/{max_retries}): {e}")
    return False


def bulk_insert_with_chunks(
    db: Session,
    model_class,
    data: list,
    chunk_size: int = 1000,
    return_defaults: bool = False
) -> int:
    """
    Bulk insert data in chunks for better performance

    Args:
        db: Database session
        model_class: SQLAlchemy model class
        data: List of dictionaries to insert
        chunk_size: Number of records per chunk
        return_defaults: Whether to return defaults

    Returns:
        Number of records inserted
    """
    total_inserted = 0

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        try:
            db.bulk_insert_mappings(model_class, chunk, return_defaults=return_defaults)
            db.commit()
            total_inserted += len(chunk)
            logger.info(f"Inserted chunk {i // chunk_size + 1}: {len(chunk)} records")
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Failed to insert chunk {i // chunk_size + 1}: {e}")
            raise

    return total_inserted


def execute_raw_sql(db: Session, sql: str, params: Optional[dict] = None) -> int:
    """
    Execute raw SQL statement safely

    Args:
        db: Database session
        sql: SQL statement
        params: Optional parameters

    Returns:
        Number of rows affected
    """
    from sqlalchemy import text

    try:
        result = db.execute(text(sql), params or {})
        db.commit()
        return result.rowcount
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to execute SQL: {e}")
        raise
