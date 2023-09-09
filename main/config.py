class Users:
    def __init__(self, account, password, classlist) -> None:
        self.account = account
        self.password = password
        self.classlist = classlist

ACCOUNT = "D1109023"
PASSWORD = "vincent09132362"

f = open('../txt/setting.txt', 'r')
COURSES = f.readlines()
for i in COURSES:
    i = i[:-1]

f.close()

User = Users(ACCOUNT, PASSWORD, COURSES)