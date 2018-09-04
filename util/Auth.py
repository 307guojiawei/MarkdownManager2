import jwt
from flask import request

import util.UserDao as UserDao
import time
import util.Config as Config
from util.BaseType import User
from functools import wraps

from util.ErrorHandle import MdmException


globalTokenList = list()  #无效的token列表


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

    def deleteToken(self,token):
        if token not in globalTokenList:
            globalTokenList.append(token)

    def verifyToken(self,token):
        if token in globalTokenList:
            return None
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

    def addUser(self,userName, password):
        try:
            user = User(userName,password)
            UserDao.addUser(user)
            return self.verifyUser(user.userName,user.password)
        except Exception as e:
            raise MdmException(4002,"用户已被注册")


#受token验证保护的API
def requireAuth(**kwargs1):
    def auth(func):
        @wraps(func)
        def authWrapper(**kwargs):
            # print(kwargs['params'])
            token = request.form.get('token')
            auth = Autentication()
            user = auth.verifyToken(token)
            # print(user)
            if user:
                kwargs['userInfo'] = user
                return func(**kwargs)
            else:
                raise MdmException(4002,"login first")
        return authWrapper
    return auth

if __name__ == '__main__':
    pass
