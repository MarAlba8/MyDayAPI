from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(url=settings.DATABASE_URL)

SessionFactory = sessionmaker(bind=engine)


# @contextmanager
# def session_manager():
def get_db_session():
    try:
        session = SessionFactory()
        yield session
    except Exception as e:
        ## TODO: send to sentry
        session.rollback()
        raise e
    finally:
        session.close()
