from util.BaseType import User
from util.DBDriver import DBDriver

def getDBDriver():
    return DBDriver(
        tabledesc=["User", "id integer primary key autoincrement, username varchar(50) unique , password varchar(50)"])

def initDB():
    dbDriver = getDBDriver()
    dbDriver.cerateDB()
    dbDriver.closeDB()

def addUser(user):
    dbDriver = getDBDriver()
    try:
        dbDriver.execDB("insert into user(username,password) VALUES (?,?)",(user.userName,user.password))
        dbDriver.closeDB()
    except Exception as e:
        raise e

def removeUser(userId):
    dbDriver = getDBDriver()
    try:
        dbDriver.execDB("delete from user where id= ?",(userId))
        dbDriver.closeDB()
    except Exception as e:
        raise e

def getUserById(userId):
    dbDriver = getDBDriver()
    try:
        res = dbDriver.getResult("select * from user where id= ?", [(int(userId))])
        dbDriver.closeDB()
        user = User(res[0][1],res[0][2])
        user.userId = res[0][0]
        return user
    except Exception as e:
        raise e

def getUserByName(userName):
    dbDriver = getDBDriver()
    try:
        res = dbDriver.getResult("select * from user where username= ?", [(str(userName))])
        #res = dbDriver.getResult("select * from user where username= '%s'"%(userName))
        dbDriver.closeDB()
        user = User(res[0][1],res[0][2])
        user.userId = res[0][0]
        return user
    except Exception as e:
        raise e

if __name__ == '__main__':
    user = User(username="gjw",password="123456")
    addUser(user)


