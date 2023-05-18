from datetime import datetime
from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field


# User model
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    username: str = Field(..., alias="userName")
    password: str
    role: UserRole
    created_date: datetime = Field(
        default_factory=datetime.utcnow, alias="createdDate"
    )
    updated_date: datetime = Field(
        default_factory=datetime.utcnow, alias="updatedDate"
    )

    def to_camel(self) -> dict:
        return self.dict(by_alias=True)

    @classmethod
    def from_camel(cls, data: dict) -> "User":
        return cls(**data)
