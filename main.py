
from fastapi import FastAPI, Body,Response,status ,HTTPException
from typing import Optional
from pydantic import BaseModel
from random import randrange
app= FastAPI() #Instantiate Fastapi 

my_posts=[ {"title":"my first post","content":"my first post content","id":1}, 
          {"title":"my second post","content":"my second post content","id":2}
        ]

# path operation or route
#"/" is root path 
@app.get("/") #decorator
def root():
    return {"Message":"Welcome To The FastApi"}



@app.get("/posts")
def get_posts():
    return {"data":my_posts}


class Post(BaseModel):
    title:str
    content:str
    published:bool =True
    rating:Optional[int] =None
    
# @app.post("/posts")
# def create_post(payload:dict=Body(...)):
#     print(payload)
#     return {"Message":payload}

@app.post("/posts")
def create_post(post:Post):
    # pydantic model to dict 
    post_dict=post.dict()
    post_dict['id']=randrange(0,1000000)
    print(post.dict())
    my_posts.append(post_dict)
    return {"Message":f"{post_dict}"} 

def find_post(id):
    for i in my_posts:
        if i['id']==id:
            return i
    
@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    print(id)
    post=find_post(id)
    if not post:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {"message":f"post with id {id} was not found"}
        
    print(post)
    return {"post":post}



def get_index_of_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index
        
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    print(id)
    print(type(id))
    
    index=get_index_of_post(id)
    if index is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
        
        
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {
        "message": "Post Updated Successfully",
        "data": post_dict
    }    


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
        
    index=get_index_of_post(id)
    if index is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
        

    deleted_post=my_posts.pop(index)
    return {
        "message": f"Removed post with id : {id}",
        "data": deleted_post
    }    