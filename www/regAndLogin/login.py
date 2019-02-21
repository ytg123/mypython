'''
Created on 2019年1月21日

@author: 杨腾广

    登录功能
'''
import logging; logging.basicConfig(level=logging.INFO)
from flask import jsonify,request
from www.utils import utils
from . import login
import operator as op
from www.sqlUtils import bseSql
#引入token
from www.utils import tokenutil

@login.route('',methods=['POST'])
def home():
    name = request.form.get("act")
    pwd = request.form.get("pwd")
    if  name == None:
        return jsonify({'result':'账号为空'})
    elif pwd == None:
        return jsonify({'result':'密码为空'})
    else:
        newpwd = utils.hmac_md5(pwd)
        spwd = bseSql.sqlUitl('select id,password from account where account="%s" and cancle="%s"' % (name,0))
        if spwd:
            if  op.eq(newpwd,spwd[0]['password']):
                #生成token
                token = tokenutil.proToken({'account': spwd[0]['id']})
                logging.info('token：  %s' % str(token, encoding = "utf8"))
                return jsonify({'result':str(token, encoding = "utf8")})
            else:
                return jsonify({'result':0}) #密码不正确
        else:
            return jsonify({'result':-1}) #用户不存在
        
























