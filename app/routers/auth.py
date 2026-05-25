from fastapi import Response,status ,HTTPException,Depends,APIRouter
from ..database import get_db
from .. import dbmodels,schemas,utils ,oauth2
from typing import List
from .. import dbmodels,schemas
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])



@router.post("/login",response_model=schemas.Token)
# def login(user_credentials:schemas.UserLogin,db:Session=Depends(get_db)):
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    

    user=db.query(dbmodels.User).filter(dbmodels.User.email==user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    
    
    # create a token 
    access_token=oauth2.create_access_token(data={"user_id":user.id})
     
    
    # return token
    return {"access_token":access_token,"token_type":"bearer"}
    
    
    
    