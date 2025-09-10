from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# import psycopg2
# import time
# from psycopg2.extras import RealDictCursor


# SQLACHEMY_DATABASE_URL = "postgresql://postgres:test.1234@localhost/fastapi"
SQLACHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLACHEMY_DATABASE_URL)

SessioLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessioLocal()
    try:
        yield db
    finally:
        db.close()


### connect with raw sql (not sqlalchemy)
# retries = 0
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             # port="5432",
#             database="fastapi",
#             user="postgres",
#             password="test.1234",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("database connection succesful")
#         break
#     except Exception as error:
#         print("database connection failed")
#         print("Error: ", error)
#         time.sleep(5)
#         retries = retries + 1
#         print("retries = ", retries)
#         if retries >= 10:
#             break
