from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, status, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt

router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)

# Secret key for JWT encoding
SECRET_KEY = "your-secret-key"
# Algorithm used for JWT encoding
ALGORITHM = "HS256"
# Token expiration time (e.g., 15 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 15

hashContext = CryptContext(schemes=['bcrypt'],deprecated="auto")
oauth2bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

class UserModel(BaseModel):
    username:str
    firstName:str
    lastName:str
    email:str
    password:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

def creat_access_token(username:str):
    payload = {'sub':username,'exp':datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

def get_current_user(token:Annotated[str,Depends(oauth2bearer)]):
    payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    username = payload.get('sub')
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User Not Validated')
    return{'username':username}


@router.post("/register",status_code=status.HTTP_201_CREATED)
def create_user(db:db_dependency,user_data:UserModel):
    """
    Register a new user.\n
    Parameters:\n
    - user_data (required): Details of the user to be registered.\n
    Returns:\n
    - Status code: 201 Created\n
    - Message: Details of the newly registered user.\n
    Raises:\n
    - HTTPException 400 (Bad Request) if email or username already exists.\n
    """
    try:
        user_model = Users(
            username = user_data.username,
            email = user_data.email,
            firstName = user_data.firstName,
            lastName = user_data.lastName,
            hashed_password = hashContext.hash(user_data.password)
        )
        db.add(user_model)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400,detail="Email or username already exists")


@router.post("/token",status_code=status.HTTP_200_OK)
def login_user(db:db_dependency,login_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    """
    Authenticate and generate access token.\n
    Parameters:\n
    - login_data (required): User credentials for authentication.\n
    Returns:\n
    - Status code: 200 OK\n
    - Message: Access token and token type.\n
    Raises:\n
    - HTTPException 401 (Unauthorized) if user data is not authorized.\n
    """
    user = db.query(Users).filter(Users.username==login_data.username).first()
    if user is None or not hashContext.verify(login_data.password,user.hashed_password) :
        raise HTTPException(status_code=401,detail="User data not authorized")
    
    token = creat_access_token(user.username)
    return {'access_token': token, 'token_type': 'bearer'}
