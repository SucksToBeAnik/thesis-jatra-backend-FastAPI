from sqlmodel import SQLModel, Field, ForeignKey


class ProfileThesisGroupLink(SQLModel, table=True):
    profile_id: str = Field(
        foreign_key="profile.id", primary_key=True, ondelete="CASCADE"
    )
    thesisgroup_id: str = Field(
        foreign_key="thesisgroup.id", primary_key=True, ondelete="CASCADE"
    )
