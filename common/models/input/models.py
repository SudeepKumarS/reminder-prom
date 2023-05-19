import re
from pydantic import EmailStr, BaseModel, validator
from typing import Optional



class UserSignUpInput(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: str

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        fields = {
            "phone_number": "phoneNumber",
        }

    @validator("password", always=True)
    def is_phonenumber_valid(cls, v, values, **kwargs):
        if values.get("mobile") and not re.compile(r"^\+\d{1,15}$").match(values.get("mobile")):
            raise ValueError("This is not a valid phone number")
        return v
    

class LoginUserInput(BaseModel):
    username: Optional[str]
    password: str
