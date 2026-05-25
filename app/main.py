
from fastapi import FastAPI, Body,Response,status ,HTTPException,Depends
from typing import Optional,List
from pydantic import BaseModel
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from . import dbmodels,schemas,utils
from .database import SessionLocal,engine,get_db
from sqlalchemy.orm import Session
from .routers import post ,user


dbmodels.Base.metadata.create_all(bind=engine)



app= FastAPI() #Instantiate Fastapi 
load_dotenv()
app.include_router(post.router)
app.include_router(user.router)



try:
    conn = psycopg2.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("DB_USER"),
        password="ani@9355",
        cursor_factory=RealDictCursor
    )
    # print(conn)
    cursor=conn.cursor()
    print("Database Connected")
except Exception as error:
    print(error)
    

    
    
# path operation or route
#"/" is root path 
@app.get("/") #decorator
def root():
    return {"Message":"Welcome To The FastApi"}

@app.get("/sqlalchemy") #decorator
def test_db(db:Session=Depends(get_db)):
    posts=db.query(dbmodels.Post).all()
    return {"Message":posts}



    
    