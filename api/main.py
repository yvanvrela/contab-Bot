from fastapi import FastAPI
from dotenv import dotenv_values
from api.routers.timbrado_route import router

config = dotenv_values("api/.env")

app = FastAPI(
  title="FastAPI & Mongo CRUD",
  description="this is a simple REST API using fastapi and mongodb",
  version="0.0.1",
)

app.include_router(router=router, prefix='/timbrados')