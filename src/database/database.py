from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(url=settings.DATABASE_URL)

SessionFactory = sessionmaker(bind=engine)

@contextmanager
def session_manager():
     try:
          session = SessionFactory()
          yield session
          session.commit()
     except Exception as e:
          ## TODO: send to sentry
          raise e
          session.rollback()
     finally:
          session.close()
