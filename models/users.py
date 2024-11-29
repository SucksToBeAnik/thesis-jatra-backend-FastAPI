from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr
from utils.enums import ProfileType
from typing import Optional

if TYPE_CHECKING:
    from models.profiles import Profile


class UserCreate(BaseModel):
    username: str = Field(
        ..., description="The name of the user", min_length=1, max_length=50
    )
    email: EmailStr = Field(
        ..., description="The email of the user", min_length=1, max_length=50
    )
    password: str = Field(..., description="The password of the user", min_length=8)
    fullname: str = Field(
        ..., description="The full name of the user", min_length=1, max_length=50
    )
    profile_type: ProfileType = Field(default=ProfileType.STUDENT)


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(min_length=1, max_length=50)
    hashed_password: str = Field(min_length=8)
    profile: "Profile" = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False, "lazy": "joined"},
    )

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
