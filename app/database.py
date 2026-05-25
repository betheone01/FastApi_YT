# To Handle the DB conection

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,session
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()


# DB_URL= "postgreqsql://user:password@postgresServer:db"

host=os.getenv("HOST")
database=os.getenv("DATABASE")
db_user=os.getenv("DB_USER")
password=os.getenv("PASSWORD")


DB_URL=f"postgresql://{db_user}:{password}@{host}/{database}"

engine=create_engine(DB_URL)
SessionLocal=sessionmaker(autoflush=False, autocommit=False,bind=engine)

Base= declarative_base()



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

