
from typing import List
from .. import dbmodels,schemas
from sqlalchemy.orm import Session
from fastapi import Response,status ,HTTPException,Depends,APIRouter
from ..database import get_db
from .. import dbmodels,schemas,utils


router=APIRouter(prefix="/users",tags=["user"])





@router.get("/",response_model=List[schemas.UserOut])
def get_users(db:Session=Depends(get_db)):
    users=db.query(dbmodels.User).all()
    print(users)
    return users

@router.post("/",response_model=schemas.UserOut,status_code=status.HTTP_201_CREATED)
def create_post(user: schemas.UserCreate,db:Session=Depends(get_db)):
    # hash the password - user.password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    
    user_dict=user.dict()
    new_user=dbmodels.User(**user_dict) 
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(dbmodels.User ).filter(dbmodels.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not found")
    
    return user
    