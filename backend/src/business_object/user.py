class User:

    def __init__(
        self,
        username: str,
        pwdh: str,
        id_user: int | None = None,
    ):
        self.id_user = id_user
        self.username = username
        self.pwdh = pwdh
        self.admin = False
