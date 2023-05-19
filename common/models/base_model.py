from datetime import date, datetime
from typing import Any, Dict, Optional
from bson import ObjectId
from pydantic import BaseModel, Field


class BaseClassModel(BaseModel):
    id: Optional[str] = Field(default_factory= lambda: str(ObjectId()))

    def to_database(self, *args, **kwargs) -> Dict:
        update = kwargs.pop("update", False)
        data = self.dict(*args, by_alias=True, **kwargs)
        data["_id"] = ObjectId(data.pop("id"))
        if update:
            data = {f_name: f_value for f_name, f_value in data.items() if f_name in self._income}
        return data

    @classmethod
    def from_database(cls, data, *args, **kwargs) -> "BaseClassModel":
        try:
            data["id"] = str(data.pop("_id"))
        except Exception:
            print(data)
        return cls(*args, **data, **kwargs)
    
    def dict_repsonse(self, **kwargs: Any) -> Dict:
        data = self.dict(by_alias=True)
        for field_name, value in self.__fields__.items():
            data_field = data.get(value.alias)
            if data_field:
                if value.type_ is datetime:
                    data[value.alias] = data[value.alias].strftime("%Y-%m-%dT%H:%M:%SZ")
                elif value.type_ is date:
                    data[value.alias] = str(data[value.alias])
                elif hasattr(value.type_, "dict_repsonse"):
                    field = getattr(self, field_name)
                    if not isinstance(field, list):
                        data[value.alias] = field.dict_repsonse(**kwargs)
            elif data_field == "":
                data[value.alias] = None
        return data


class BaseClassModelWithTimeStamp(BaseClassModel):
    created_date: datetime = Field(
        default_factory=lambda: datetime.utcnow(), alias="createdDate"
    )
    updated_date: datetime = Field(
        default_factory=lambda: datetime.utcnow(), alias="updatedDate"
    )

    def to_database(self, *args, **kwargs) -> Dict:
        """Update timestamp for updated_date."""
        self.updated_date = datetime.utcnow()
        return super().to_database(*args, **kwargs)
