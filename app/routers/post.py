

from typing import List,Optional
from .. import dbmodels,schemas,oauth2
from sqlalchemy.orm import Session
from fastapi import Response,status ,HTTPException,Depends,APIRouter
from ..database import get_db

from sqlalchemy import func

router=APIRouter(prefix="/posts",tags=["post"])


@router.get("/",response_model=List[schemas.PostVote])
def get_posts(db:Session=Depends(get_db),user_id:int =Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    
    posts=db.query(dbmodels.Post).filter(dbmodels.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    
    
    results=db.query(dbmodels.Post,func.count(dbmodels.Vote.post_id).label("votes")).join(dbmodels.Vote, dbmodels.Vote.post_id==dbmodels.Post.id,isouter=True).group_by(dbmodels.Post.id).filter(dbmodels.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    print(results)
    
    
    return results


@router.post("/",response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate,db:Session=Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    

    print(current_user.id)
    post_dict=post.dict()
    new_post=dbmodels.Post(owner_id=current_user.id,**post_dict)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostVote)
def get_posts(id:int,db:Session=Depends(get_db),user_id:int =Depends(oauth2.get_current_user)):

    # post=db.query(dbmodels.Post).filter(dbmodels.Post.id==id).first()
    results=db.query(dbmodels.Post,func.count(dbmodels.Vote.post_id).label("votes")).join(dbmodels.Vote, dbmodels.Vote.post_id==dbmodels.Post.id,isouter=True).group_by(dbmodels.Post.id).filter(dbmodels.Post.id==id).first()
    # print(post)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail="NOT FOUND")
    return results



@router.put("/{id}",response_model=schemas.PostOut)
def update_post(id:int,post:schemas.PostUpdate,db:Session=Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    updated_post=db.query(dbmodels.Post).filter(dbmodels.Post.id==id)
    print(updated_post)
     
    if updated_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} was not found")
    if updated_post.first().owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform requested action")
    updated_post.update(post.dict(),synchronize_session=False)
    db.commit()
    return updated_post.first()



@router.delete("/{id}")
def delete_post(id:int,db:Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    post=db.query(dbmodels.Post).filter(dbmodels.Post.id==id)
    print(post)
     
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} was not found")

    if post.first().owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform requested action")
    post.delete(synchronize_session=False)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)


