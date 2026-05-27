
from fastapi import FastAPI,Depends
from dotenv import load_dotenv
from . import dbmodels
from .database import engine,get_db
from sqlalchemy.orm import Session
from .routers import post,user,auth,vote
from pydantic_settings import BaseSettings



dbmodels.Base.metadata.create_all(bind=engine)


app= FastAPI() #Instantiate Fastapi 
load_dotenv()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


    
    
# path operation or route
#"/" is root path 
@app.get("/") #decorator
def root():
    return {"Message":"Welcome To The FastApi"}

@app.get("/sqlalchemy") #decorator
def test_db(db:Session=Depends(get_db)):
    posts=db.query(dbmodels.Post).all()
    return {"Message":posts}



    
    