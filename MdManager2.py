import os
import random

from flask import Flask, make_response
from flask import request
from PIL import Image
from flask_cors import CORS
import diff_match_patch as dmp_module
import json

import util.Auth as Auth
import util.Install as Install
import util.Config as Config
import time

from util import HistoryDao
from util.Auth import requireAuth
from util.BaseType import MdFile, MdHistory
from util.ErrorHandle import errorHandle, MdmException
import util.History as History
import util.FileDao as FileDao


app = Flask(__name__)
app.debug = True
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 最大2G
CORS(app, supports_credentials=True, resources=r'/*')


@app.after_request
def af_request(resp):
    """
    #请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


@app.route('/')
def pwd():
    return str(os.path.dirname(os.path.realpath(__file__)))


@app.route('/mdm2/install')
def install():
    conf = Config.Config()
    if not conf.properties.has_key("INSTALL"):
        Install.install()
        conf.properties.put("INSTALL", str(time.time()))
        return "<h1>:)</h1></br>MarkdownManager2 has been suuccessfully installed :)"
    else:
        return "<h1>:(</h1></br>You have already installed.<br>To reinstall,remove <strong>INSTALL</strong> from config.properties "


@app.route('/protected', methods=['POST'])
@errorHandle()
@requireAuth()
def hello_world(**kwargs):
    return str(kwargs['userInfo'])


'''
查看公共文件列表
    /file/public/list POST/GET        

    =
        + code [4001|4002|4003]  成功|失败|token改变
        + msg   string  信息
        {} payload   负载
            [] fileList  文件列表
                + id    文件ID
                + name  文件名
                + date  上次改动时间
                + ownerId   拥有者id
                + permission    权限类型
                + status    状态
                + version   版本号

'''


@app.route('/file/public/list', methods=['POST', 'GET'])
@errorHandle()
def publicListHandler():
    bufList = FileDao.getPublicFileList()
    fileList = list()
    for file in bufList:
        fileList.append(file.__dict__)
    return {'fileList': fileList}


'''
查看某个公共文件内容
    /file/public/getFile POST   
        + id    string 文件id
    =
        + code [4001|4002|4003]  成功|失败|token改变
        + msg   string  信息
        {} payload   负载
            {} file 文件
                + id    文件ID
                + name  文件名
                + date  上次改动时间
                + ownerId   拥有者id
                + permission    权限类型
                + status    状态
                + content   内容
                + version   版本号

'''


@app.route('/file/public/getFile', methods=['POST', 'GET'])
@errorHandle()
def publicFileContentHandler():
    id = int(request.form['id'])
    file = FileDao.getFileById(id)
    if file.permission == "public":
        return {'file': file.__dict__}
    else:
        raise MdmException(4002, "permission denied")


'''
查看用户保存的全部文件列表
    /file/private/list POST
        + token String token
    
    =
        + code [4001|4002|4003]  成功|失败|token改变
        + msg   string  信息
        {} payload   负载
            [] fileList  文件列表
                + id    文件ID
                + name  文件名
                + date  上次改动时间
                + ownerId   拥有者id
                + permission    权限类型
                + status    状态
                + version   版本号
    
'''


@app.route('/file/private/list', methods=['POST'])
@errorHandle()
@requireAuth()
def privateListHandler(**kwargs):
    user = kwargs["userInfo"]
    bufList = FileDao.getFileListByUid(user.userId)
    fileList = list()
    for file in bufList:
        fileList.append(file.__dict__)
    return {'fileList': fileList}


'''
查看用户某个文件
    /file/private/getFile POST
        + token String token
        + id    string 文件id

    =
        + code [4001|4002|4003]  成功|失败|token改变
        + msg   string  信息
        {} payload   负载
            {} file 文件
                + id    文件ID
                + name  文件名
                + date  上次改动时间
                + ownerId   拥有者id
                + permission    权限类型
                + status    状态
                + content   内容
                + version   版本号

'''


@app.route('/file/private/getFile', methods=['POST'])
@errorHandle()
@requireAuth()
def privateFileHandler(**kwargs):
    user = kwargs['userInfo']
    id = int(request.form['id'])
    file = FileDao.getFileById(id)
    if str(file.ownerId) != str(user.userId):
        raise MdmException(4002, "Permission Denied")
    return {'file': file.__dict__}


'''
创建文件
    /file/private/addFile POST
        + token String token
        + name  文件名
        + permission    权限类型
        + content   内容
        + date  上次修改时间

    =
        + code [4001|4002|4003]  成功|失败|token改变
        + msg   string  信息
        {} payload   负载
            None

'''


@app.route('/file/private/addFile', methods=['POST'])
@errorHandle()
@requireAuth()
def addFileHandler(**kwargs):
    user = kwargs['userInfo']
    file = MdFile(
        name=request.form['name'],
        ownerId=user.userId,
        date=request.form['date'],
        permission=request.form['permission'],
        status="OK",
        content=request.form['content'],
        version=1
    )
    FileDao.addFile(file)
    return None


'''
修改文件
    /file/private/updateFile POST
        + token String token
        + id  文件id
        + permission    权限类型
        + content   内容
        + date  上次修改时间
        + version   版本号

    =
        + code [4001|4002|4003]  成功|失败|token改变
        + msg   string  信息
        {} payload   负载
            None

'''

@app.route('/file/private/updateFile', methods=['POST'])
@errorHandle()
@requireAuth()
def updateFileHandler(**kwargs):
    user = kwargs['userInfo']
    fid = int(request.form['id'])
    file = FileDao.getFileById(fid)
    if str(file.ownerId) != str(user.userId):
        raise MdmException(4002, "Permission Denied")
    file.permission = request.form['permission']
    if request.form['content']!="":
        file.content = request.form['content']
    if int(file.version)>=int(request.form['version']):
        raise MdmException(4500,"文件版本落后于远端，请先同步(Sync first)")
    file.version = int(request.form['version'])
    file.date = request.form['date']
    History.saveFileWithPatch(file)
    return None

'''
获取指定版本的文件
    /file/private/getHistoryFile POST
        + token String token
        + id  文件id
        + version   版本号

    =
        + code [4001|4002|4003]  成功|失败|token改变
        + msg   string  信息
        {} payload   负载
            + currentFile   当前文件
            + historyFile   历史文件

'''
@app.route('/file/private/getHistoryFile', methods=['POST'])
@errorHandle()
@requireAuth()
def getHistoryFileHandler(**kwargs):
    user = kwargs['userInfo']
    fid = int(request.form['id'])
    version = int(request.form['version'])
    file = MdFile(id=fid)
    historyFile,currentFile = History.viewFileWithVersion(version=version,file=file)
    return {'currentFile':currentFile.__dict__,'historyFile':historyFile.__dict__}

'''
恢复文件到某个指定版本
    /file/private/restoreFile POST
        + token String token
        + id  文件id
        + version   版本号

    =
        + code [4001|4002|4003]  成功|失败|token改变
        + msg   string  信息
        {} payload   负载

'''
@app.route('/file/private/restoreFile', methods=['POST'])
@errorHandle()
@requireAuth()
def restoreFileHandler(**kwargs):
    user = kwargs['userInfo']
    fid = int(request.form['id'])
    version = int(request.form['version'])
    History.restoreFile(version,MdFile(id=fid))
    return None

'''
删除文件
    /file/private/deleteFile POST
        + token String token
        + id  文件id

    =
        + code [4001|4002|4003]  成功|失败|token改变
        + msg   string  信息
        {} payload   负载
            None

'''


@app.route('/file/private/deleteFile', methods=['POST'])
@errorHandle()
@requireAuth()
def deleteFileHanler(**kwargs):
    user = kwargs['userInfo']
    fid = int(request.form['id'])
    file = FileDao.getFileById(fid)
    if str(file.ownerId) != str(user.userId):
        raise MdmException(4002, "Permission Denied")
    FileDao.removeFile(fid)
    return None


'''
上传图片
    /file/private/uploadImg POST
        + token String token
        + data  文件数据

    =
        + code [4001|4002|4003]  成功|失败|token改变
        + msg   string  信息
        {} payload   负载
            + url   String 图片url

'''


@app.route('/file/private/uploadImg', methods=['POST'])
@errorHandle()
@requireAuth()
def uploadImgHandler(**kwargs):
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'bmp']
    user = kwargs['userInfo']
    f = request.files['data']
    fnameOrigin = f.filename
    fileType = fnameOrigin.rsplit('.', 1)[1]
    if '.' in fnameOrigin and fileType in ALLOWED_EXTENSIONS:
        fname = str(int(time.time() * 10000)) + str(random.randint(0, 9)) + '.' + str(fileType)
        try:
            img = Image.open(f)
        except:
            raise MdmException(4002, "Image content broken")
        f.save(pwd() + '/static/img/' + fname)

        return {"url": "/static/img/" + fname}
    else:
        raise MdmException(4002, 'Unsupported file type')


'''
用户登录
    /auth POST
        + opr   [login|logout]  操作
        + userName string   用户名
        + password string   密码|token
        
    =
        + code [4001|4002|4003]  认证成功|失败|token改变
        + msg   string  信息
        {} payload   负载
            + token string  token信息
'''


@app.route('/auth', methods=['POST'])
@errorHandle()
def authenticate():
    if request.method == 'POST':
        opr = request.form['opr']

        # print(str(opr)+"\t"+str(userName)+"\t"+str(password))
        auth = Auth.Autentication()
        if opr == "login":
            userName = request.form['userName']
            password = request.form['password']
            token = auth.verifyUser(userName, password)
            if token:
                return [{"token": token}, 4001, "login success"]
            else:
                raise MdmException(4002, "login failed")
        else:
            auth.deleteToken(request.form['password'])
            return [{"token": "None"}, 4003, "token change"]


'''
用户注册
    /regist POST
        +userName   String
        +password   String
    
    =
        + code [4001|4002]  成功|失败
        + msg   string  信息
        {} payload   负载
            + token string  token信息
'''


@app.route('/regist', methods=['POST'])
@errorHandle()
def registHandler():
    userName = request.form['userName']
    password = request.form['password']
    if len(userName) > 0 and len(password) > 0:
        auth = Auth.Autentication()
        token = auth.addUser(userName, password)
        return {"token": token}
    else:
        raise MdmException(4002, '用户名或密码不能为空')




if __name__ == '__main__':
    app.run()

