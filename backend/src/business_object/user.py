class User:

    def __init__(
        self,
        pseudo: str,
        pwdh: str,
        id_user: int | None = None,
    ):
        self.id_user = id_user
        self.pseudo = pseudo
        self.pwdh = pwdh
        self.admin = False
