from fastapi import FastAPI
from controller import user_controller

app = FastAPI(title="VeloScope")

app.include_router(user_controller.router, prefix="/user", tags=["User"])