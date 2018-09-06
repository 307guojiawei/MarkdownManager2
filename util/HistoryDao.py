import json
from operator import attrgetter

import diff_match_patch as dmp_module

from util import FileDao
from util.BaseType import MdFile, MdHistory
from util.DBDriver import DBDriver


def getDBDriver():
    return DBDriver(
        tabledesc=["HISTORY", "id integer primary key autoincrement,"
                           "fid integer,"
                            "version integer,"
                            "patch_content TEXT"
                ])


def initDB():
    dbDriver = getDBDriver()
    dbDriver.cerateDB()
    dbDriver.closeDB()


def getHistory(fid,target_version):
    dbDriver = getDBDriver()
    try:
        resList=dbDriver.getResult("select * from HISTORY where fid=? and version>?",
                        (
                          fid,target_version
                        )
                        )
        resultHistory = list()
        for res in resList:
            history = MdHistory(id=res[0],
                                fid=res[1],
                                version=res[2],
                                patch_content=res[3]
                                )
            resultHistory.append(history)
        dbDriver.closeDB()
        return resultHistory
    except Exception as e:
        raise e
def addHisttory(history):
    dbDriver = getDBDriver()
    try:
        dbDriver.execDB("insert into HISTORY(fid,version,patch_content) values(?,?,?)",
                        (
                            history.fid,
                            history.version,
                            history.patch_content
                        )
                        )
        dbDriver.closeDB()
    except Exception as e:
        raise e
#id
# def addFile(mdFile):
#     dbDriver = getDBDriver()
#     try:
#         dbDriver.execDB("insert into FILE(id,name,date,ownerId,permission,status,content,version) values(?,?,?,?,?,?,?,?)",
#                         (
#                             mdFile.id,
#                             mdFile.name,
#                             mdFile.date,
#                             mdFile.ownerId,
#                             mdFile.permission,
#                             mdFile.status,
#                             mdFile.content,
#                             mdFile.version
#                         )
#                         )
#         dbDriver.closeDB()
#     except Exception as e:
#         raise e
#
#
# def removeFile(id):
#     id = int(id)
#     dbDriver = getDBDriver()
#     try:
#         dbDriver.execDB("delete from FILE where id = ?", [id])
#         dbDriver.closeDB()
#     except Exception as e:
#         raise e
#
#
# def updateFile(mdFile):
#     dbDriver = getDBDriver()
#     try:
#         dbDriver.execDB("update File set date = ?,permission = ?,status = ?,content=?,version=? where id=?",
#                         (
#                             mdFile.date,
#                             mdFile.permission,
#                             mdFile.status,
#                             mdFile.content,
#                             mdFile.version,
#                             mdFile.id
#                         )
#                         )
#         dbDriver.closeDB()
#     except Exception as e:
#         raise e
#
#
# # 获取用户的所有文件 id,name,date,ownerId,permission,status
# def getFileListByUid(uid):
#     uid = int(uid)
#     dbDriver = getDBDriver()
#     try:
#         resList = dbDriver.getResult("select id,name,date,ownerId,permission,status,version from FILE where ownerId=?", [uid])
#         resultFile = list()
#         for res in resList:
#             file = MdFile(id=res[0],
#                           name=res[1],
#                           date=res[2],
#                           ownerId=res[3],
#                           permission=res[4],
#                           status=res[5],
#                           version=res[6]
#                           )
#             resultFile.append(file)
#         dbDriver.closeDB()
#         return resultFile
#     except Exception as e:
#         raise e
#
#
# # 获取公共文件
# def getPublicFileList():
#     dbDriver = getDBDriver()
#
#     try:
#         resList = dbDriver.getResult(
#             "select id,name,date,ownerId,permission,status,version from FILE where permission='public'")
#
#         resultFile = list()
#         for res in resList:
#             file = MdFile(id=res[0],
#                           name=res[1],
#                           date=res[2],
#                           ownerId=res[3],
#                           permission=res[4],
#                           status=res[5],
#                           version=res[6]
#                           )
#
#             resultFile.append(file)
#         dbDriver.closeDB()
#         return resultFile
#     except Exception as e:
#         raise e
#
#
# def getFileById(fid):
#     fid = int(fid)
#     dbDriver = getDBDriver()
#     try:
#         res = dbDriver.getResult("select id,name,date,ownerId,permission,status,content,version from FILE where id=?", [fid])
#         res = res[0]
#         file = MdFile(id=res[0],
#                       name=res[1],
#                       date=res[2],
#                       ownerId=res[3],
#                       permission=res[4],
#                       status=res[5],
#                       content=res[6],
#                       version=res[7]
#                       )
#         dbDriver.closeDB()
#         return file
# #     except Exception as e:
# #         raise e
# def savePatch(new_file):
#     #vesrion=new_file.version
#     old_file = FileDao.getFileById(new_file.id)
#     old_file.version=new_file.version
#     new_file_json=json.dumps(new_file.__dict__)
#     old_file_json = json.dumps(old_file.__dict__)
#     dmp = dmp_module.diff_match_patch()
#     patches = dmp.patch_make(new_file_json,old_file_json)
#     patches_content=dmp.patch_toText(patches)
#     #print(patches_content)
#     history=MdHistory(version=new_file.version,patch_content=patches_content,fid=new_file.id)
#     addHisttory(history)
#     FileDao.updateFile(new_file)

#
#
#
# def viewFilewithVersion(version,file):
#     latest_file=FileDao.getFileById(file.id)
#     print(latest_file)
#     fileList=getHistory(latest_file.id,version)
#     fileList.sort(key=attrgetter("version"),reverse=True)
#     dmp = dmp_module.diff_match_patch()
#     latest_file_json=json.dumps(latest_file.__dict__)
#     for file in fileList:
#         pathces=dmp.patch_fromText(file.patch_content)
#         latest_file_json,_=dmp.patch_apply(pathces,latest_file_json)
#         print("version" + str(file.version-1)+"file content: "+str(latest_file_json))
#     #print(latest_file_json)
#     file=MdFile("temp")
#     file.__dict__=json.loads(latest_file_json)
#     file.version=version
#     return file,latest_file
#
# def restoreFile(version,file):
#     target_file,old_file=viewFilewithVersion(version,file)
#     target_file.version=old_file.version+1
#     savePatch(target_file)

