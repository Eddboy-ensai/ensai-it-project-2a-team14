from pydantic import BaseModel, Field, field_validator


def blank_to_none(value):
    """Turns an empty (or whitespace-only) string into None.

    Swagger and Streamlit send "" for an empty input: it must mean "not provided"
    instead of being rejected by min_length.
    """
    if isinstance(value, str) and not value.strip():
        return None
    return value


class UserModel(BaseModel):
    id_user: int
    username: str
    pwdh: str
    admin: bool


class UserCreateModel(BaseModel):
    username: str
    pwd: str


class UserReadModel(BaseModel):
    id_user: int
    username: str
    admin: bool


class UserDisplayModel(BaseModel):
    id_user: int
    username: str
    admin: bool
    favorites: list[dict]


class UserLoginModel(BaseModel):
    username: str
    pwd: str


class UserSelfUpdateModel(BaseModel):
    current_pwd: str
    new_username: str | None = Field(default=None, min_length=1)
    new_pwd: str | None = Field(default=None, min_length=1)

    _blank_to_none = field_validator("new_username", "new_pwd", mode="before")(blank_to_none)


class UserAdminUpdateModel(BaseModel):
    """Body for an admin updating another user's profile.
    If the username changes, a new password is required, because the admin does
    not know the user's current password and the hash is salted with the username.
    """

    username: str | None = Field(default=None, min_length=1)
    pwd: str | None = Field(default=None, min_length=1)


class AdminRightsModel(BaseModel):
    """Body for granting (True) or revoking (False) admin rights."""

    admin: bool
