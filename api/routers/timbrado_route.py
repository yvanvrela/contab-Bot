from fastapi import APIRouter, status, Request, Body
from api.config import db
from api.models import timbrado_models
from fastapi.encoders import jsonable_encoder
from typing import List


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=timbrado_models.TimbradoBase, description='Create a new timbrado', tags=['timbrados'])
def create_timbrado(
    timbrado: timbrado_models.TimbradoBase = Body(...)
) -> timbrado_models.TimbradoBase:
    timbrado = jsonable_encoder(timbrado)

    new_timbrado = db.conn.local.timbrados.insert_one(timbrado)
    timbrado_db = db.conn.local.timbrados.find_one(
        {"_id": new_timbrado.inserted_id}
    )

    return timbrado_db


# @user.post('/users', response_model=User, tags=["users"])
# async def create_user(user: User):
#     new_user = dict(user)
#     new_user["password"] = sha256_crypt.encrypt(new_user["password"])
#     del new_user["id"]
#     id = conn.local.user.insert_one(new_user).inserted_id
#     user = conn.local.user.find_one({"_id": id})
#     return userEntity(user)


@router.get("/", response_description="List all timbrados", response_model=List[timbrado_models.TimbradoBase])
def list_books(request: Request):
    books = list(request.app.database["contabBot"].find(limit=100))
    return books
