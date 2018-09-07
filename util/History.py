import json

from util import FileDao, HistoryDao
from operator import attrgetter

import diff_match_patch as dmp_module

from util.BaseType import MdHistory, MdFile




'''
保存文件以及变化记录
参数：new_file:文件对象，至少要有id，version两个有效字段
'''
def saveFileWithPatch(new_file):
    #vesrion=new_file.version
    old_file = FileDao.getFileById(new_file.id)
    old_file.version=new_file.version
    new_file_json=json.dumps(new_file.__dict__)
    old_file_json = json.dumps(old_file.__dict__)
    dmp = dmp_module.diff_match_patch()
    patches = dmp.patch_make(new_file_json,old_file_json)
    patches_content=dmp.patch_toText(patches)
    #print(patches_content)
    history=MdHistory(version=new_file.version,patch_content=patches_content,fid=new_file.id)
    HistoryDao.addHisttory(history)
    FileDao.updateFile(new_file)



'''
查看指定版本的文件
参数：version：int 指定的版本
file：文件对象，只要有id这一个有效参数即可
返回值：
file：要求版本的文件
latest_file：当前数据库中的最新版本，不需要用_承接即可
'''
def viewFileWithVersion(version,file):
    latest_file=FileDao.getFileById(file.id)
    #print(latest_file)
    fileList=HistoryDao.getHistory(latest_file.id,version)
    fileList.sort(key=attrgetter("version"),reverse=True)
    dmp = dmp_module.diff_match_patch()
    latest_file_json=json.dumps(latest_file.__dict__)
    for file in fileList:
        pathces=dmp.patch_fromText(file.patch_content)
        latest_file_json,_=dmp.patch_apply(pathces,latest_file_json)
        #print("version" + str(file.version-1)+"file content: "+str(latest_file_json))
    print(latest_file_json)
    file=MdFile("temp")
    file.__dict__=json.loads(latest_file_json)
    file.version=version
    return file,latest_file


'''
恢复到文件到指定版本
参数：version：指定的版本
file：文件对象，只要有id这一个有效参数即可
返回值：
file：要求版本的文件
注：回复文件也会导致文件的版本+1
'''
def restoreFile(version,file):
    target_file,old_file=viewFileWithVersion(version,file)
    target_file.version=old_file.version+1
    saveFileWithPatch(target_file)



if __name__ == '__main__':
    file = MdFile(name="1.md", content="1", version=0,id=1)
    FileDao.addFile(file)
    for i in range(10):
        file.content+=str(i)
        file.version+=1
        print("version: "+str(i)+" content"+str(file))
        saveFileWithPatch(file)
    restoreFile(1,file)

    print("fin")