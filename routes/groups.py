import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.groups import ThesisGroup, ThesisGroupCreate
from models.profile_group_link import ProfileThesisGroupLink
from models.profiles import Profile
from config.db import get_db_session
from utils.exceptions import CustomException

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/")
async def get_all_groups(db_session: Session = Depends(get_db_session)):
    try:
        return db_session.query(ThesisGroup).all()
    except Exception as e:
        raise CustomException(e)


@router.get("/{group_id}")
async def get_group_by_id(group_id: str, db_session: Session = Depends(get_db_session)):
    try:
        return db_session.get(ThesisGroup, group_id)
    except Exception as e:
        raise CustomException(e)


@router.post("/")
async def create_group(
    group: ThesisGroupCreate, db_session: Session = Depends(get_db_session)
):
    provided_profile_id = group.profile_id
    profile = db_session.get(Profile, provided_profile_id)
    if not profile:
        raise CustomException(
            exc=Exception("Profile not found"),
            message="Profile not found",
            status_code=404,
        )

    thesis_group = ThesisGroup(name=group.name, description=group.description)

    try:
        db_session.add(thesis_group)
        db_session.commit()
        profile_thesis_group_link = ProfileThesisGroupLink(
            profile_id=group.profile_id, thesisgroup_id=thesis_group.id
        )
        db_session.add(profile_thesis_group_link)
    except Exception as e:
        db_session.rollback()
        raise CustomException(e)
    db_session.commit()
    return thesis_group
