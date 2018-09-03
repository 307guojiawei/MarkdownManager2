from functools import wraps
import json

'''
统一状态代码：
    4001    操作成功
    4002    操作失败
    4003    token改变

    5000    其他错误
'''
err_code = {
    "4001": "操作成功",
    "4002": "操作失败",
    "4003": "token改变",

    "5000": "其他错误"
}

def resultFormat(code, msg, payload):
    res = {
        "code":code,
        "msg":"",
        "payload":payload
    }
    if str(code) in err_code:
        res["msg"] = str(err_code[str(code)])+" : "+str(msg)
    else:
        res["msg"] = str(msg)
    # print(json.dumps(res))
    return json.dumps(res)

#装饰器 decorater
def errorHandle(**kwargs1):
    def handler(func):
        @wraps(func)
        def wrapper(**kwargs):
            try:
                result = func(**kwargs)
                if not isinstance(result,list):
                    return resultFormat(4001,"",result)
                elif len(result) == 3:
                    return resultFormat(result[1],result[2],result[0])
                else:
                    raise MdmException(5000,"function args err")
            except MdmException as e:
                msg = e.errMsg
                if str(e.errId) in err_code:
                    msg = str(err_code[str(e.errId)])+" : "+str(e.errMsg)
                return resultFormat(e.errId,msg,None)
            except Exception as e:
                msg = str(type(e))+":"+str(e)+":args="+str(e.args)
                return resultFormat(5000,msg,None)
        return wrapper
    return handler


class MdmException(Exception):
    def __init__(self,id ,msg):
        self.errId = id
        self.errMsg = msg

    def __str__(self):
        return "Error("+str(self.errId)+"):\t"+str(self.errMsg)
