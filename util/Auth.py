import jwt
import util.UserDao as UserDao
import time
import util.Config as Config
from util.BaseType import User


class Autentication:
    def __init__(self,secretKey=None,algorithm = 'HS256' ,expireHour = 1 ):
        if secretKey is None:
            config = Config.Config()
            self.secretKey = str(config.properties.get("JWTSecretKey"))
        else:
            self.secretKey = secretKey
        self.algorithm = algorithm
        self.expireTime = expireHour*3600*1000

    def generateToken(self, infoDict):
        return str(jwt.encode(infoDict, self.secretKey, self.algorithm),encoding='utf8')

    def decodeToken(self, token):
        return jwt.decode(token, self.secretKey, self.algorithm)

    def verifyUser(self, username, password):
        try:
            trueUser = UserDao.getUserByName(username)
        except Exception as e:
            print(e)
            return None
        if trueUser.password == password:
            infoDict={
                "time": str(time.time()*1000),
                "expire": str(self.expireTime),
                "id": str(trueUser.userId),
                "username":str(trueUser.userName)
            }
            return self.generateToken(infoDict)
        else:
            return None

    def verifyToken(self,token):
        try:
            info = self.decodeToken(token)
        except Exception as e:
            #print(e)
            return None
        expireTime = float(info["time"])+float(info["expire"])
        if(time.time()*1000>expireTime):
            return None
        else:
            user = User(username=info['username'],password="~protected~")
            user.userId = info['id']
            return user


if __name__ == '__main__':
    pass
