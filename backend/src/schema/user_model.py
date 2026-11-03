from pydantic import BaseModel, Field


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
    favorites: list[dict]


class UserLoginModel(BaseModel):
    username: str
    pwd: str


class UserSelfUpdateModel(BaseModel):
    current_pwd: str
    new_username: str | None = Field(default=None, min_length=1)
    new_pwd: str | None = Field(default=None, min_length=1)
