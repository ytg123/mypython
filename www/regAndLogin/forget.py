'''
Created on 2019年1月24日

@author: 杨腾广
忘记密码
'''
import logging; logging.basicConfig(level=logging.INFO)
from flask import jsonify,request
from www.utils import utils
from . import forget
from www.sqlUtils import bseSql

@forget.route('',methods=['POST'])
def home():
    name = request.form.get('account')
    pwd = request.form.get('pwd')
    if name == None or pwd == None:
        return jsonify({'result':'参数为空'})
    else:
        newpwd = utils.hmac_md5(pwd)
        rownum = bseSql.sqlUitl('update account set password = "%s" where account="%s"' % (newpwd,name))
        if rownum > 0:
            return jsonify({'result':1})
        else:
            return jsonify({'result':-1})