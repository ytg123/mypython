'''
Created on 2019年1月21日

@author: 杨腾广

程序入口
'''

from flask import Flask

#解决跨域
from flask_cors import CORS
#引入后台
from admin.admin import admin
#引入前台
from index.index import index
#引入注册 登录
from regAndLogin.login import login
from regAndLogin.register import register
from regAndLogin.forget import forget
#注册flask
app = Flask(__name__)


#解决跨域
CORS(app,resources=r'*')

#注册
app.register_blueprint(login,url_prefix='/login')

#注册登录
app.register_blueprint(register,url_prefix='/register')

#注册忘记密码
app.register_blueprint(forget,url_prefix='/forget')

#注册前台
app.register_blueprint(index,url_prefix='/index')

#注册后台
app.register_blueprint(admin,url_prefix='/admin')



if __name__ == '__main__':
    app.run()
