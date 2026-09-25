from pydantic import BaseModel


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
