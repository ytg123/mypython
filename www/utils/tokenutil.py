'''
Created on 2019年1月23日

@author: 杨腾广

token管理
'''
from flask import jsonify,make_response,Flask,g
#管理token
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#HTTP  认证
from flask_httpauth import HTTPTokenAuth
from www.sqlUtils import bseSql
import operator as op
#注册flask
app = Flask(__name__)
#HTTP  认证
auth = HTTPTokenAuth(scheme='Bearer')

#设置token信息
app.config['SECRET_KEY'] = 'abc;;.,.,k'
serializer = Serializer(app.config['SECRET_KEY'], expires_in=1800)

#生成token
def proToken(obj):
    return serializer.dumps(obj)

#验证token  
@auth.verify_token
def verify_token(token):
    if op.eq(token, 'null'):
        return False
    else:
        g.data = {}    
        try:
            g.data = serializer.loads(token)
        except:
            pass
        finally:
            if 'account' in g.data:
                return True
            else:
                return False 
#验证不通过时
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'token认证失败！'}), 401)

#根据token拿用户信息
def getAcount(token):
    try:
        data = serializer.loads(token)
        if 'account' in data:
            listcount = bseSql.sqlUitl('select * from account where id="%s"' % data['account'])
            return listcount
        else:
            return None
    except:
        return None