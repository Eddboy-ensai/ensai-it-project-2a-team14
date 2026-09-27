class User:

    def __init__(
        self,
        username: str,
        pwdh: str,
        id_user: int | None = None,
        admin: bool = False,
        access_token: str | None = None
    ):
        """Constructor"""
        self.id_user = id_user
        self.username = username
        self.pwdh = pwdh
        self.admin = admin
        self.access_token = access_token
