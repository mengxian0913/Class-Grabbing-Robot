class Users:
    def __init__(self, account, password) -> None:
        self.account = account
        self.password = password

ACCOUNT = "ACCOUNT"
PASSWORD = "PASSWORD"

User = Users(ACCOUNT, PASSWORD)
