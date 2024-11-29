import enum
from sqlmodel import SQLModel, Field, Relationship
import uuid
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from utils.enums import ProfileType
from pydantic import BaseModel
from models.profile_group_link import ProfileThesisGroupLink

if TYPE_CHECKING:
    from models.groups import ThesisGroup
    from models.users import User


class Profile(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    user_id: str = Field(foreign_key="user.id", unique=True, ondelete="CASCADE")
    user: "User" = Relationship(
        back_populates="profile", sa_relationship_kwargs={"uselist": False}
    )
    fullname: str = Field(min_length=1, max_length=50)
    phone: Optional[str] = Field(
        default=None, min_length=1, max_length=50, nullable=True
    )
    address: Optional[str] = Field(
        default=None, min_length=1, max_length=50, nullable=True
    )
    profile_type: ProfileType = Field(default=ProfileType.STUDENT)  # Use Enum here
    thesisgroups: list["ThesisGroup"] = Relationship(
        back_populates="profiles", link_model=ProfileThesisGroupLink
    )


class ProfileUpdate(BaseModel):

    user_id: str
    fullname: str = Field(min_length=1, max_length=50)
    phone: Optional[str] = Field(
        default=None, min_length=1, max_length=50, nullable=True
    )
    address: Optional[str] = Field(
        default=None, min_length=1, max_length=50, nullable=True
    )
    profile_type: ProfileType = Field(default=ProfileType.STUDENT)
