

from typing import List
from .. import dbmodels,schemas
from sqlalchemy.orm import Session
from fastapi import Response,status ,HTTPException,Depends,APIRouter
from ..database import get_db


router=APIRouter(prefix="/posts",tags=["post"])


@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db)):
    posts=db.query(dbmodels.Post).all()
    print(posts)
    return posts


@router.post("/",response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate,db:Session=Depends(get_db)):
    post_dict=post.dict()
    new_post=dbmodels.Post(**post_dict)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
def get_posts(id:int,db:Session=Depends(get_db)):
    
    post=db.query(dbmodels.Post).filter(dbmodels.Post.id==id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail="NOT FOUND")
    return post



@router.put("/{id}",response_model=schemas.PostOut)
def update_post(id:int,post:schemas.PostUpdate,db:Session=Depends(get_db)):
    
    updated_post=db.query(dbmodels.Post).filter(dbmodels.Post.id==id)
    print(updated_post)
     
    if updated_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} was not found")
    updated_post.update(post.dict(),synchronize_session=False)
    db.commit()
    return updated_post.first()



@router.delete("/{id}")
def delete_post(id:int,db:Session = Depends(get_db)):
    
    post=db.query(dbmodels.Post).filter(dbmodels.Post.id==id)
    print(post)
     
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)


