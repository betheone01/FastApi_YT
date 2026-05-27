
from pydantic import BaseModel,EmailStr,conint
from typing import Optional
from datetime import datetime

    
class PostBase(BaseModel):
    title:str
    content:str
    published:bool =True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


class UserOut(BaseModel):
    email:EmailStr 
    id:int
    created_at:datetime
    class Config:
        orm_mode=True   
        
# Response Model for Post 
class PostOut(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner: UserOut
    class Config:
        orm_mode=True    

# New schema
class PostVote(BaseModel):
    Post: PostOut
    votes: int

    class Config:
        from_attributes = True    

class UserCreate(BaseModel):
    email:EmailStr 
    password:str


        
        

# Login Schema
class UserLogin(BaseModel):
    email:EmailStr 
    password:str
    

class Token(BaseModel):
    access_token:str
    token_type:str
    

class TokenData(BaseModel):
    id:Optional[int]=None
    
    
    
class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)