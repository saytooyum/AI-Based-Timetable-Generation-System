from fastapi import FastAPI
from app.routes.generate import router

app = FastAPI()

app.include_router(router)