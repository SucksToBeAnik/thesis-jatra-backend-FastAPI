from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db import get_db_session
from models.profiles import Profile, ProfileUpdate
from utils.exceptions import CustomException

router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)


@router.get("/")
async def get_profiles(
    limit: int = 10, offset: int = 0, db_session: Session = Depends(get_db_session)
):
    try:
        return db_session.query(Profile).offset(offset).limit(limit).all()
    except Exception as e:
        raise CustomException(e)

@router.get("/{profile_id}")
async def get_profile_by_id(
    profile_id: str, db_session: Session = Depends(get_db_session)
):
    try:
        return db_session.get(Profile, profile_id)
    except Exception as e:
        raise CustomException(e)


@router.put("/{profile_id}")
async def update_profile(
    profile_id: str,
    profile: ProfileUpdate,
    db_session: Session = Depends(get_db_session),
):
    try:
        profile_data = db_session.get(Profile, profile_id)
        if profile_data:
            profile_data.fullname = profile.fullname
            profile_data.phone = profile.phone
            profile_data.address = profile.address
            profile_data.profile_type = profile.profile_type
            db_session.commit()
            return profile_data
        else:
            raise CustomException(
                exc=Exception("Profile not found"),
                message="Profile not found",
                status_code=404,
            )
    except Exception as e:
        raise CustomException(e)
