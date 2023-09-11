class Users:
    def __init__(self, account, password) -> None:
        self.account = account
        self.password = password


ACCOUNT = "Account"
PASSWORD = "Password"

User = Users(ACCOUNT, PASSWORD)
