import uuid

from pydantic import BaseModel, ConfigDict


class EatListBase(BaseModel):
    name: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Economy set",
            }
        }
    }


class EatListRead(EatListBase):
    id: int
    user_id: uuid.UUID
    # currency: CurrencyRead
    # type: ProductTypeRead
    # source: ProductSourceRead

    model_config = ConfigDict(from_attributes=True)  # type: ignore


class EatListCreate(EatListBase):
    pass


class EatListUpdate(EatListBase):
    pass


class EatListProductBase(BaseModel):
    price: int
    count: int
    product_id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "price": 150,
                "count": 1,
                "product_id": 1,
            }
        }
    }


class EatListProductRead(EatListProductBase):
    id: int
    eat_list_id: int

    # currency: CurrencyRead
    # type: ProductTypeRead
    # source: ProductSourceRead

    model_config = ConfigDict(from_attributes=True)  # type: ignore


class EatListProductCreate(EatListProductBase):
    pass


class EatListProductUpdate(EatListProductBase):
    pass
