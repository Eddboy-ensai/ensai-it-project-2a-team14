from pydantic import BaseModel


class UserModel(BaseModel):
    id_user: int
    pseudo: str
    pwdh: str
    admin: bool


class UserCreateModel(BaseModel):
    pseudo: str
    pwdh: str
