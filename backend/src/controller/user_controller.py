from fastapi import APIRouter, Depends, HTTPException

from schema.user_model import (
    AdminRightsModel,
    UserAdminUpdateModel,
    UserCreateModel,
    UserReadModel,
    UserSelfUpdateModel,
)
from service.user_service import UserService
from utils.log_utils import get_logger
from utils.security import require_admin, verify_token

router = APIRouter()

logger = get_logger(__name__)


def get_user_service():
    """Dependency Injection provider for UserService."""
    return UserService()


@router.post("/", response_model=UserReadModel, tags=["Users"])
async def create_user(u: UserCreateModel, user_service=Depends(get_user_service)):
    """Create a new user.
    Args:
        u (UserCreateModel): The user data to create.
        user_service (UserService): The service used to interact with user data.
    Returns:
        UserReadModel: The newly created user data.
    Raises:
        HTTPException: 400 error if the username is already taken.
        HTTPException: 500 error if the creation process fails.
    """
    logger.info("Create a user")
    if user_service.username_already_used(u.username):
        raise HTTPException(status_code=400, detail="Username already used.")
    user = user_service.create(u.username, u.pwd)
    if not user:
        raise HTTPException(status_code=500, detail="Error while creating user.")

    return user


@router.get(
    "/", response_model=list[UserReadModel], tags=["Users"], dependencies=[Depends(require_admin)]
)
async def list_all_users(user_service=Depends(get_user_service)):
    """List all users.
    Returns:
        list[UserReadModel]: A list of all registered users.
    """
    logger.info("List all users")
    users_list = user_service.list_all()
    return users_list


@router.get(
    "/{id_user}",
    response_model=UserReadModel,
    tags=["Users"],
    # dependencies=[Depends(require_admin)],
)
async def user_by_id(id_user: int, user_service=Depends(get_user_service)):
    """Find a user by their unique ID.
    Args:
        id_user (int)
        user_service (UserService): The service used to interact with user data
    Returns:
        UserReadModel: The user data if found
    Raises:
        HTTPException: 404 error if the user is not found
    """
    logger.info("Find a user by id")
    user = user_service.find_by_id(id_user)
    if not user:
        raise HTTPException(status_code=404, detail=f"User (id={id_user}) not found.")
    return user


@router.put("/me", response_model=UserReadModel, tags=["Users"])
async def update_my_profile(
    u: UserSelfUpdateModel,
    user_service=Depends(get_user_service),
    current_user=Depends(verify_token),
):
    """Update the profile (username and/or password) of the logged-in user.
    Args:
        u (UserSelfUpdateModel): current password, new username and/or new password.
        user_service (UserService): The service used to interact with user data.
        current_user (User): The logged-in user, identified by the X-Auth-Token header.
    Returns:
        UserReadModel: The updated user data.
    Raises:
        HTTPException: 401 error if not logged in or if the current password is wrong.
        HTTPException: 400 error if there is nothing to update or the username is already used.
        HTTPException: 500 error if the update process fails.
    """
    logger.info("Update own profile")
    try:
        user = user_service.update_own_profile(
            current_user, u.current_pwd, u.new_username, u.new_pwd
        )
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    if not user:
        raise HTTPException(status_code=500, detail="Error while updating user.")
    return user


@router.delete("/{id_user}", tags=["Users"])
async def delete_user(
    id_user: int,
    user_service=Depends(get_user_service),
    admin=Depends(require_admin),
):
    """Delete a user from the system.
    Args:
        id_user (int)
        user_service (UserService): The service used to interact with user data.
    Returns:
        str: A confirmation message indicating the user was deleted.
    Raises:
        HTTPException: 404 error if the user is not found.
    """
    logger.info("Delete a user")
    user = user_service.find_by_id(id_user)
    if not user:
        raise HTTPException(status_code=404, detail="User (id={id_user}) not found.")

    user_service.delete(user)
    return f"User {user.username} deleted"


@router.put("/{id_user}", response_model=UserReadModel, tags=["Users"])
async def update_user_as_admin(
    id_user: int,
    u: UserAdminUpdateModel,
    user_service=Depends(get_user_service),
    admin=Depends(require_admin),
):
    """Update another user's profile (admin only).
    Args:
        id_user (int): id of the user to modify.
        u (UserAdminUpdateModel): new username and/or new password.
        user_service (UserService): The service used to interact with user data.
        admin (User): The logged-in admin, identified by the X-Auth-Token header.
    Returns:
        UserReadModel: The updated user data.
    Raises:
        HTTPException: 401/403 error if not logged in or not admin.
        HTTPException: 400 error if the admin targets himself (use PUT /user/me),
            if there is nothing to update, if the username is already used,
            or if the username changes without a new password.
        HTTPException: 403 error if a non-first admin tries to modify the first admin.
        HTTPException: 404 error if the user is not found.
        HTTPException: 500 error if the update process fails.
    """
    logger.info("Update a user as admin")
    if id_user == admin.id_user:
        raise HTTPException(status_code=400, detail="Use PUT /user/me to update your own profile.")
    user = user_service.find_by_id(id_user)
    if not user:
        raise HTTPException(status_code=404, detail=f"User (id={id_user}) not found.")
    if user_service.is_first_admin(user):
        raise HTTPException(status_code=403, detail="The first admin's profile cannot be modified.")

    try:
        user = user_service.update_profile_as_admin(user, u.username, u.pwd)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    if not user:
        raise HTTPException(status_code=500, detail="Error while updating user.")
    return user


@router.put("/{id_user}/admin", response_model=UserReadModel, tags=["Users"])
async def set_admin_rights(
    id_user: int,
    rights: AdminRightsModel,
    user_service=Depends(get_user_service),
    admin=Depends(require_admin),
):
    """Grant or revoke admin rights (first admin only).
    Args:
        id_user (int): id of the user whose rights are changed.
        rights (AdminRightsModel): {"admin": true} to grant, {"admin": false} to revoke.
        user_service (UserService): The service used to interact with user data.
        admin (User): The logged-in admin, identified by the X-Auth-Token header.
    Returns:
        UserReadModel: The updated user data.
    Raises:
        HTTPException: 401/403 error if not logged in or not admin.
        HTTPException: 403 error if the logged-in admin is not the first admin.
        HTTPException: 400 error if the first admin tries to change his own rights.
        HTTPException: 404 error if the user is not found.
        HTTPException: 500 error if the update process fails.
    """
    logger.info("Set admin rights")
    user = user_service.find_by_id(id_user)
    if not user:
        raise HTTPException(status_code=404, detail=f"User (id={id_user}) not found.")

    try:
        user = user_service.set_admin_rights(admin, user, rights.admin)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    if not user:
        raise HTTPException(status_code=500, detail="Error while updating user.")
    return user
