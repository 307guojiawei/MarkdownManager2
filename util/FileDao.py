from util.BaseType import MdFile
from util.DBDriver import DBDriver


def getDBDriver():
    return DBDriver(
        tabledesc=["FILE", "id integer primary key autoincrement,"
                           " name varchar(50) unique ,"
                           " date varchar(50),"
                           " ownerId integer,"
                           " permission varchar(10),"
                           " status varchar(10),"
                           " content TEXT"])


def initDB():
    dbDriver = getDBDriver()
    dbDriver.cerateDB()
    dbDriver.closeDB()


def addFile(mdFile):
    dbDriver = getDBDriver()
    try:
        dbDriver.execDB("insert into FILE(id,name,date,ownerId,permission,status,content) values(?,?,?,?,?,?,?)",
                        (
                            mdFile.id,
                            mdFile.name,
                            mdFile.date,
                            mdFile.ownerId,
                            mdFile.permission,
                            mdFile.status,
                            mdFile.content
                        )
                        )
        dbDriver.closeDB()
    except Exception as e:
        raise e


def removeFile(id):
    id = int(id)
    dbDriver = getDBDriver()
    try:
        dbDriver.execDB("delete from FILE where id = ?", [id])
        dbDriver.closeDB()
    except Exception as e:
        raise e


def updateFile(mdFile):
    dbDriver = getDBDriver()
    try:
        dbDriver.execDB("update File set date = ?,permission = ?,status = ?,content=? where id=?",
                            (
                                mdFile.date,
                                mdFile.permission,
                                mdFile.status,
                                mdFile.content,
                                mdFile.id
                            )
                        )
        dbDriver.closeDB()
    except Exception as e:
        raise e

#获取用户的所有文件 id,name,date,ownerId,permission,status
def getFileListByUid(uid):
    uid = int(uid)
    dbDriver = getDBDriver()
    try:
        resList = dbDriver.getResult("select id,name,date,ownerId,permission,status from FILE where ownerId=?",[uid])
        resultFile = list()
        for res in resList:
            file = MdFile(id=res[0],
                          name=res[1],
                          date=res[2],
                          ownerId=res[3],
                          permission=res[4],
                          status=res[5]
                          )
            resultFile.append(file)
        dbDriver.closeDB()
        return resultFile
    except Exception as e:
        raise e

#获取公共文件
def getPublicFileList():
    dbDriver = getDBDriver()
    try:
        resList=dbDriver.getResult("select id,name,date,ownerId,permission,status from FILE where permission='public'")
        resultFile = list()
        for res in resList:
            file = MdFile(id=res[0],
                          name=res[1],
                          date=res[2],
                          ownerId=res[3],
                          permission=res[4],
                          status=res[5]
                          )
            resultFile.append(file)
        dbDriver.closeDB()
        return resultFile
    except Exception as e:
        raise e

def getFileById(fid):
    fid = int(fid)
    dbDriver = getDBDriver()
    try:
        res = dbDriver.getResult("select id,name,date,ownerId,permission,status,content from FILE where id=?", [fid])
        res = res[0]
        file = MdFile(id = res[0],
                      name=res[1],
                      date=res[2],
                      ownerId=res[3],
                      permission=res[4],
                      status=res[5],
                      content=res[6]
        )
        dbDriver.closeDB()
        return file
    except Exception as e:
        raise e


if __name__ == '__main__':

    file = MdFile(
                  name='hello1',
                  date='1231233',
                  ownerId=1,
                  permission='private',
                  status='OK',
                  content='abcdefghijksdfsdflmnopqrstuvwxyz'
                  )
    addFile(file)
    fileList = getFileListByUid(1)
    for file in fileList:
        print(file)
    print("")
    file = getFileById(1)
    print(file)
    file.content +="gjwgjwgjw"
    updateFile(file)
    file = getFileById(1)
    print(file)


