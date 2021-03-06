import json
class User:
    def __init__(self,username=None,password=None):
        self.userName = username
        self.password = password
        self.userId = -1

    def __str__(self):
        return "Platform User("+str(self.userId)+"):\tUserName:"+str(self.userName)+"\tPassword:"+str(self.password)

class MdFile:
    def __init__(self,name=None,date=None,ownerId=None,permission=None,status=None,id=None,content=None,version=None):
        self.id = id
        self.name = name
        self.date = date
        self.ownerId = ownerId
        self.permission = permission
        self.status = status
        self.content = content
        self.version = version

    def __str__(self):
        return "Markdown File:\t"+str(json.dumps(self.__dict__))

class MdHistory:
    def __init__(self,fid,version,patch_content,id=None,):
        self.id=id
        self.fid=fid
        self.version=version
        self.patch_content=patch_content

    def __str__(self):
        return "Markdown History:\t"+str(json.dumps(self.__dict__))