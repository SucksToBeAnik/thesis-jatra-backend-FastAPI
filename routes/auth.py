from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from config.auth import LoginCredentials, validate_login_credentials
from config.settings import settings
from config.db import get_db_session
from sqlmodel import Session, select, text
from models.users import User, UserCreate
from models.profiles import Profile
from datetime import timedelta
from pydantic import ValidationError
from utils.helpers import hash_password
from utils.exceptions import CustomException


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Session = Depends(get_db_session),
):
    try:
        login_credentials = LoginCredentials(
            email=form_data.username, password=form_data.password
        )
        token_expire_time = timedelta(minutes=settings.access_token_expire_minutes)
        token = await validate_login_credentials(
            login_credentials, token_expire_time, db_session
        )
    except Exception as e:
        raise CustomException(e)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
async def register(user: UserCreate, db_session: Session = Depends(get_db_session)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    user_data = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db_session.begin()
    try:
        db_session.add(user_data)
        db_session.commit()
        profile_data = Profile(
            fullname=user.fullname, user_id=user_data.id, profile_type=user.profile_type
        )
        db_session.add(profile_data)
    except Exception as e:
        db_session.rollback()
        raise e
    db_session.commit()
    return {"message": "User registered successfully"}


@router.get("/users")
async def get_users(db_session: Session = Depends(get_db_session)):
    try:
        users = db_session.exec(select(User)).all()
        users_without_hashed_password = [
            User.model_validate(user).model_dump(exclude={"hashed_password"})
            for user in users
        ]
    except Exception as e:
        raise e
    return users_without_hashed_password


from sqlmodel import select
from sqlalchemy.orm import selectinload


@router.get("/users/{user_id}")
async def get_user_by_id(user_id: str, db_session: Session = Depends(get_db_session)):
    try:
        user = db_session.exec(select(User).where(User.id == user_id)).first()

        if not user:
            raise Exception("User not found")

        user_dict = user.model_dump(exclude={"hashed_password"})
        profile_dict = user.profile.model_dump(exclude={"user_id"})
        user_dict["profile"] = profile_dict

        return user_dict

    except Exception as e:
        print(e)
        raise CustomException(str(e))


# @router.get("/users/{user_id}/profile")
# async def get_profile_by_user_id(
#     user_id: str, db_session: Session = Depends(get_db_session)
# ):

#     try:
#         profile = db_session.exec(
#             select(Profile).where(Profile.user_id == user_id)
#         ).first()
#     except Exception as e:
#         raise CustomException(e)
#     return profile
