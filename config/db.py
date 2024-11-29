from sqlalchemy.engine import Engine
from sqlmodel import create_engine, Session
from config.settings import settings
from utils.exceptions import CustomException

database_url = settings.database_url
print("database_url:", database_url)
engine: Engine = create_engine(database_url)


def get_db_session():
    try:
        session = Session(engine)
        yield session
    except Exception as e:
        raise CustomException(e)
