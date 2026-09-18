from fastapi import APIRouter, HTTPException

from schema.user_model import UserCreateModel
from service.user_service import UserService

router = APIRouter()


@router.get("/", tags=["Users"])
async def create_user(self, u: UserCreateModel):
    user = UserService().create(u.pseudo, u.pwdh)
    if not user:
        raise HTTPException(status_code=500, detail="Error while creating user.")
    return user



