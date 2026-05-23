
from fastapi import FastAPI, Body,Response,status ,HTTPException
from typing import Optional
from pydantic import BaseModel
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv



app= FastAPI() #Instantiate Fastapi 

load_dotenv()

my_posts=[ {"title":"my first post","content":"my first post content","id":1}, 
          {"title":"my second post","content":"my second post content","id":2}
        ]

try:
    conn = psycopg2.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("PASSWORD"),
        cursor_factory=RealDictCursor
    )
    cursor=conn.cursor()
    print("Database Connected")
except Exception as error:
    print(error)
    
class Post(BaseModel):
    # id:int
    title:str
    content:str
    published:bool =True
    
    # rating:Optional[int] =None
    
    
# path operation or route
#"/" is root path 
@app.get("/") #decorator
def root():
    return {"Message":"Welcome To The FastApi"}


# Update the Operations from array as storage to DB

@app.get("/posts")
def get_posts():
    cursor.execute("""select * from posts""")
    posts=cursor.fetchall()
    print(posts)
    return {"data":posts}

    
# @app.post("/posts")
# def create_post(payload:dict=Body(...)):
#     print(payload)
#     return {"Message":payload}

# @app.post("/posts")
# def create_post(post:Post):
#     # pydantic model to dict 
#     post_dict=post.dict()
#     post_dict['id']=randrange(0,1000000)
#     print(post.dict())
#     my_posts.append(post_dict)
#     return {"Message":f"{post_dict}"} 

# Updated create_post to store the createdPost in db (posts)

@app.post("/posts")
def create_post(post: Post):

    cursor.execute(
        """
        INSERT INTO posts_practice (id,title, content, published)
        VALUES (%s,%s, %s, %s)
        RETURNING *
        """,
        (id,post.title, post.content, post.published)
    )

    new_post = cursor.fetchone()

    conn.commit()

    return {"data": new_post}


# def find_post(id):
#     for i in my_posts:
#         if i['id']==id:
#             return i
    
# @app.get("/posts/{id}")
# def get_post(id:int,response:Response):
#     print(id)
#     post=find_post(id)
#     if not post:
#         response.status_code=status.HTTP_404_NOT_FOUND
#         return {"message":f"post with id {id} was not found"}
        
#     print(post)
#     return {"post":post}

@app.get("/posts/{id}")
def get_posts(id):
    print(type(id))
    print(id)

    cursor.execute("""Select * from posts_practice where id=%s""",(id))
    post=cursor.fetchone()
    return {"data":post}


# def get_index_of_post(id):
#     for index, post in enumerate(my_posts):
#         if post['id'] == id:
#             return index
        
# @app.put("/posts/{id}")
# def update_post(id:int,post:Post):
#     print(id)
#     print(type(id))
    
#     index=get_index_of_post(id)
#     if index is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
        
        
#     post_dict=post.dict()
#     post_dict['id']=id
#     my_posts[index]=post_dict
#     return {
#         "message": "Post Updated Successfully",
#         "data": post_dict
#     }    

# Update Route with db op

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("""Update posts_practice set title=%s ,content=%s where id=%s RETURNING * """ ,(post.title,post.content,id))
    updated_post=cursor.fetchone()
    conn.commit()
    if update_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} was not found")
    return {"data" :updated_post }


# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
        
#     index=get_index_of_post(id)
#     if index is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
        

#     deleted_post=my_posts.pop(index)
#     return {
#         "message": f"Removed post with id : {id}",
#         "data": deleted_post
#     }    


# Delete Route with db op

@app.delete("/posts/{id}")
def delete_post(id:int):
    
    cursor.execute("""Delete from posts_practice where id=%s returning * """,str(id),)
    deleted_post=cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} was not found")
    conn.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # return {"data" :updated_post }