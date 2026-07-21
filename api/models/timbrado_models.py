import uuid
from typing import Optional
from pydantic import BaseModel, Field


class TimbradoBase(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    num: str = Field(...,)
    contribuyente: str = Field(...,)
    expirate: str = Field(...,)
    numeration_range: str = Field(...,)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "num": "14328050",
                "contribuyente": "Juan Vargas",
                "expirate": "31/12/2022",
                "numeration_range": "1000-2500"
            }
        }


class TimbradoUpdate(BaseModel):
    contribuyente: Optional[str]
    num: Optional[str]
    contribuyente: Optional[str]
    expirate: Optional[str]
    numeration_range: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "num": "14328050",
                "contribuyente": "Juan Vargas",
                "expirate": "31/12/2022",
                "numeration_range": "1000-2500"
            }
        }
