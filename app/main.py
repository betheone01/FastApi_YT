
from fastapi import FastAPI, Body,Response,status ,HTTPException,Depends
from typing import Optional,List
from pydantic import BaseModel
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from . import dbmodels,schemas
from .database import SessionLocal,engine,get_db
from sqlalchemy.orm import Session

dbmodels.Base.metadata.create_all(bind=engine)



app= FastAPI() #Instantiate Fastapi 
load_dotenv()




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


@app.get("/posts",response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db)):
    posts=db.query(dbmodels.Post).all()
    print(posts)
    return posts


@app.post("/posts",response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate,db:Session=Depends(get_db)):
    post_dict=post.dict()
    new_post=dbmodels.Post(**post_dict)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}",response_model=schemas.PostOut)
def get_posts(id:int,db:Session=Depends(get_db)):
    
    post=db.query(dbmodels.Post).filter(dbmodels.Post.id==id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail="NOT FOUND")
    return post



@app.put("/posts/{id}",response_model=schemas.PostOut)
def update_post(id:int,post:schemas.PostUpdate,db:Session=Depends(get_db)):
    
    updated_post=db.query(dbmodels.Post).filter(dbmodels.Post.id==id)
    print(updated_post)
     
    if updated_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} was not found")
    updated_post.update(post.dict(),synchronize_session=False)
    db.commit()
    return updated_post.first()



@app.delete("/posts/{id}")
def delete_post(id:int,db:Session = Depends(get_db)):
    
    post=db.query(dbmodels.Post).filter(dbmodels.Post.id==id)
    print(post)
     
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)



# User Routes

@app.get("/users",response_model=List[schemas.UserOut])
def get_users(db:Session=Depends(get_db)):
    users=db.query(dbmodels.User).all()
    print(users)
    return users

@app.post("/users",response_model=schemas.UserOut,status_code=status.HTTP_201_CREATED)
def create_post(user: schemas.UserCreate,db:Session=Depends(get_db)):
    user_dict=user.dict()
    new_user=dbmodels.User(**user_dict)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
