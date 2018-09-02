import os

from flask import Flask
from flask import request
import json
import util.Auth as Auth
import util.Install as Install
import util.Config as Config
import time


def resultFormat(code, msg, payload):
    res = {
        "code":code,
        "msg":msg,
        "payload":payload
    }
    # print(json.dumps(res))
    return json.dumps(res)


#受token验证保护的API
def requireAuth(**kwargs):
    def auth(func):
        def wrapper(**kwargs):
            # print(kwargs['params'])
            token = request.form.get('token')
            auth = Auth.Autentication()
            user = auth.verifyToken(token)
            # print(user)
            if user:
                return func(userInfo = user)
            else:
                return resultFormat(4002,"login first",{})
        return wrapper
    return auth

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
        return "<h1>Congradulations!</h1></br>MarkdownManager2 has been suuccessfully installed :)"
    else:
        return "<h1>:(</h1></br>Something bad happend"

@app.route('/protected',methods=['POST'])
@requireAuth()
def hello_world(**kwargs):
    return str(kwargs['userInfo'])

'''
    /auth POST
        + opr   [login|logout]  操作
        + userName string   用户名
        + password string   密码
        
    =
        + code [4001|4002]  认证成功|失败
        + msg   string  信息
        + payload   负载
            + token string  token信息
'''
@app.route('/auth',methods=['POST'])
def authenticate():
    if request.method == 'POST':
        opr = request.form['opr']
        userName = request.form['userName']
        password = request.form['password']
        # print(str(opr)+"\t"+str(userName)+"\t"+str(password))
        if opr == "login":
            auth = Auth.Autentication()
            token=auth.verifyUser(userName,password)
            if token:
                return resultFormat(4001, "success", {"token":token})
            else:
                return resultFormat(4002, "failed", None)
        else:
            return resultFormat(4001,"success",{"token":"None"})


if __name__ == '__main__':
    app.run()
