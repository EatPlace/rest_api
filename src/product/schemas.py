from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    price: int
    weight: int
    link: str
    currency_id: int
    type_id: int
    source_id: int

    calories: Optional[int]
    total_fat: Optional[int]
    total_carb: Optional[int]
    total_protein: Optional[int]
    vitamin_d: Optional[int]
    calcium: Optional[int]
    iron: Optional[int]
    potassium: Optional[int]
    available: Optional[bool]

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Мармелад Дольки лимонные Мармеландия «Ударница»",
                "price": 100,
                "weight": 250,
                "link": "https://lavka.yandex.ru/213/good/marmelad-dolki-limonnye-marmelandiya-udarnica-250-gram",
                "currency_id": 1,
                "type_id": 1,
                "source_id": 1,
                "calories": 150,
                "total_fat": 5,
                "total_carb": 25,
                "total_protein": 1,
                "vitamin_d": 2,
                "calcium": 20,
                "iron": 1,
                "potassium": 100,
                "available": True,
            }
        }
    }


class ProductRead(ProductBase):
    id: int
    # currency: CurrencyRead
    # type: ProductTypeRead
    # source: ProductSourceRead

    model_config = ConfigDict(from_attributes=True)  # type: ignore


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass
