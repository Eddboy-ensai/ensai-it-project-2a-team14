from fastapi import APIRouter, HTTPException

from schema.user_model import UserCreateModel
from service.user_service import UserService
from utils.log_utils import get_logger

router = APIRouter()

logger = get_logger(__name__)


@router.post("/", tags=["Users"])
async def create_user(u: UserCreateModel):
    user = UserService().create(u.pseudo, u.pwdh)
    if not user:
        raise HTTPException(status_code=500, detail="Error while creating user.")
    return user



