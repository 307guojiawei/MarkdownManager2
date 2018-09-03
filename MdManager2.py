import os

from flask import Flask
from flask import request
import json
import util.Auth as Auth
import util.Install as Install
import util.Config as Config
import time
from util.Auth import requireAuth
from util.ErrorHandle import errorHandle, MdmException

app = Flask(__name__)
app.debug = True



@app.route('/')
def pwd():
    return str(os.path.realpath(__file__))

@app.route('/mdm2/install')
def install():
    conf = Config.Config()
    if not conf.properties.has_key("INSTALL"):
        Install.install()
        conf.properties.put("INSTALL",str(time.time()))
        return "<h1>:)</h1></br>MarkdownManager2 has been suuccessfully installed :)"
    else:
        return "<h1>:(</h1></br>You have already installed.<br>To reinstall,remove <strong>INSTALL</strong> from config.properties "

@app.route('/protected',methods=['POST'])
@errorHandle()
@requireAuth()
def hello_world(**kwargs):
    return str(kwargs['userInfo'])

@app.route('/file/privateList',methods=['POST'])
@errorHandle()
@requireAuth()
def privateListHandler(**kwargs):
    user = kwargs["userInfo"]

    return None

'''
    /auth POST
        + opr   [login|logout]  操作
        + userName string   用户名
        + password string   密码|token
        
    =
        + code [4001|4002|4003]  认证成功|失败|token改变
        + msg   string  信息
        + payload   负载
            + token string  token信息
'''
@app.route('/auth',methods=['POST'])
@errorHandle()
def authenticate():
    if request.method == 'POST':
        opr = request.form['opr']
        userName = request.form['userName']
        password = request.form['password']
        # print(str(opr)+"\t"+str(userName)+"\t"+str(password))
        auth = Auth.Autentication()
        if opr == "login":
            token=auth.verifyUser(userName,password)
            if token:
                return [{"token":token},4001,"login success"]
            else:
                raise MdmException(4002,"login failed")
        else:
            auth.deleteToken(request.form['password'])
            return [{"token":"None"},4003,"token change"]




if __name__ == '__main__':
    app.run()
