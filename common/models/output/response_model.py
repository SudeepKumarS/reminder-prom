from typing import Optional
from pydantic import BaseModel, Field
from fastapi import status


class Response(BaseModel):
    status_code: int = Field(default=status.HTTP_400_BAD_REQUEST, alias="statusCode")
    data: Optional[dict] = None
    message: Optional[str] = None

    def as_response(self, **kwargs):
        data = super().dict(**kwargs, by_alias=True)
        return data
    

class ListResponse(BaseModel):
    status_code: int = Field(default=status.HTTP_400_BAD_REQUEST, alias="statusCode")
    data: Optional[list] = []
    message: Optional[str] = None

    def as_response(self, **kwargs):
        data = super().dict(**kwargs, by_alias=True)
        return data