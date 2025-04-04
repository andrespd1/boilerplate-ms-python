import logging
import os
from contextlib import contextmanager
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

_database_url = os.getenv("DATABASE_URL_PYTHON")
engine = create_engine(_database_url)


SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        # Optionally log the error here
        logging.error("Database operation failed", exc_info=True)
        raise
    finally:
        session.close()


def with_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with get_session() as session:
            return func(*args, **kwargs, session=session)

    return wrapper
