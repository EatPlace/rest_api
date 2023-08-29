import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserProductBase(BaseModel):
    product_id: int
    special_name: Optional[str]
    like: Optional[bool]
    recommend: Optional[bool]
    reason: Optional[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": 1,
                "special_name": "My special product name",
                "like": True,
                "recommend": False,
                "reason": "Too many sugar",
            }
        }
    }


class UserProductRead(UserProductBase):
    id: int
    user_id: uuid.UUID
    # currency: CurrencyRead
    # type: ProductTypeRead
    # source: ProductSourceRead

    model_config = ConfigDict(from_attributes=True)  # type: ignore


class UserProductCreate(UserProductBase):
    pass


class UserProductUpdate(UserProductBase):
    pass
