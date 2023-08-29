from typing import Optional

from pydantic import BaseModel


class ProfileEatList(BaseModel):
    id: int
    name: str
    total_price_per_month: Optional[int]
    currency: Optional[str]
    available: Optional[bool]

    calories_per_month: Optional[int]
    total_fat_per_month: Optional[int]
    total_carb_per_month: Optional[int]
    total_protein_per_month: Optional[int]
    vitamin_d_per_month: Optional[int]
    calcium_per_month: Optional[int]
    iron_per_month: Optional[int]
    potassium_per_month: Optional[int]


class ProfileRead(BaseModel):
    username: str
    lists: list[ProfileEatList]

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "alexander",
                "lists": {
                    "id": 1,
                    "name": "Economy set",
                    "price_per_month": 1500,
                    "currency": "RUB",
                    "calories_per_month": 2700,
                    "total_fat_per_month": 800,
                    "total_carb_per_month": 1200,
                    "total_protein_per_month": 700,
                    "vitamin_d_per_month": 12,
                    "calcium_per_month": 70,
                    "potassium_per_month": 5,
                    "available": True,
                },
            }
        }
    }
