from fastapi import APIRouter, Depends, HTTPException

from schema.user_model import UserLoginModel
from service.user_service import UserService
from utils.log_utils import get_logger

router = APIRouter()

logger = get_logger(__name__)


def get_user_service():
    """Dependency provider."""
    return UserService()


@router.post("/", tags=["Login"])
def login(credentials: UserLoginModel, service=Depends(get_user_service)):
    """Authenticates a user.
    Parameters
    ----------
    credentials: UserLoginModel
        username and password
    Returns
    -------
    dict: containing id_user, username and token
    Raises
    ------
        HTTPException: 401 error if the credentials are invalid or the user does not exist."""
    logger.info("Login")
    user = service.login(credentials.username, credentials.pwd)
    if user:
        return {
            "id_user": user.id_user,
            "username": user.username,
            "access_token": user.access_token,
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")
