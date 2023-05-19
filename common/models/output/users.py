from enum import Enum
from typing import Optional

from pydantic import EmailStr, Field

from common.models.base_model import BaseClassModel, BaseClassModelWithTimeStamp


# User model
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(BaseClassModelWithTimeStamp):
    username: str
    password: str
    email: Optional[EmailStr]
    phone_number: Optional[str] = None
    role: Optional[UserRole] = UserRole.USER

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        fields = {
            "phone_number": "phoneNumber",
        }

    @classmethod
    def from_database(cls, data, *args, **kwargs) -> "User":
        return super().from_database(data, *args, **kwargs)
    
    
