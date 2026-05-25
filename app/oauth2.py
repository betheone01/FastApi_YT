

from jose import JWTError,jwt
from datetime import datetime ,timedelta
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
import os 
from dotenv import load_dotenv
from . import dbmodels,schemas,utils

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

load_dotenv()
secret_key=os.getenv("SECRET_KEY")
algo=os.getenv("ALGORITHM")
expiration_time=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# print(secret_key,algo,expiration_time)


def create_access_token(data:dict):
    
    to_encode=data.copy()
    
    expire=datetime.utcnow()+timedelta(minutes=expiration_time)
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(
        to_encode,
        secret_key,
        algorithm=algo
    )
    return encoded_jwt


def verify_access_token(token:str,credentials_exception):
    try:
        
        payload=jwt.decode(token=token,key=secret_key,algorithms=[algo])
        id:int=payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        
        token_data=schemas.TokenData(id=id)
    
    except JWTError :
        raise credentials_exception
        
    
    return token_data


def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    
    return verify_access_token(token=token,credentials_exception=credentials_exception)