import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING
from models.profile_group_link import ProfileThesisGroupLink
from pydantic import BaseModel

if TYPE_CHECKING:
    from models.profiles import Profile


class ThesisGroup(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    name: str = Field(min_length=1, max_length=50, unique=True, nullable=False)
    description: str | None = Field(max_length=255, default=None)
    profiles: list["Profile"] = Relationship(
        back_populates="thesisgroups", link_model=ProfileThesisGroupLink
    )


class ThesisGroupCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50, unique=True, nullable=False)
    description: str | None = Field(max_length=255, default=None)
    profile_id: str
