import re
import os
from jose import jwt
from typing import Annotated
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator
from pydantic import BaseModel
from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from api.models import User
from api.deps import db_dependency, bcrypt_context

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")


class UserCreateRequest(BaseModel):
    ''' user model '''
    username: str
    password: str

    @validator("password")
    def password_strength(cls, v):
        ''' password validation '''
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError(
                "Password must contain at least one special character")
        return v


class Token(BaseModel):
    ''' Token serializer '''
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db):
    ''' return true if username nad password matched'''
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False

    if not bcrypt_context.verify(password, user.password):
        return False

    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    ''' create access token '''
    expires = datetime.now(timezone.utc) + expires_delta
    encode = {'sub': username, 'id': user_id, 'exp': expires}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: db_dependency, create_user_request: UserCreateRequest
):
    ''' create user api'''
    try:
        # Create model
        user = User(
            username=create_user_request.username,
            password=bcrypt_context.hash(create_user_request.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "success": True,
            "message": "User created successfully",
            "id": user.id
        }
    except Exception as e:
        db.rollback()  # undo changes
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User creation failed: {str(e)}"
        )


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    """Generate JWT token"""
    try:
        user = authenticate_user(form_data.username, form_data.password, db)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        token = create_access_token(
            user.username,
            user.id,
            timedelta(minutes=20)
        )

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        # Print real error in terminal
        print("----------- LOGIN ERROR:", e)
        raise HTTPException(status_code=500, detail="Login failed")
