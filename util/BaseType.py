
class User:
    def __init__(self,username=None,password=None):
        self.userName = username
        self.password = password
        self.userId = -1

    def __str__(self):
        return "Platform User("+str(self.userId)+"):\tUserName:"+str(self.userName)+"\tPassword:"+str(self.password)