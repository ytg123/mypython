'''
Created on 2019年1月21日

@author: 杨腾广

注册功能
'''
import logging; logging.basicConfig(level=logging.INFO)
from flask import jsonify,request
from www.utils import utils
from . import register
from www.sqlUtils import bseSql



@register.route('',methods=['POST'])
def home():
    name = request.form.get("act")
    password = request.form.get("pwd")
    num = bseSql.sqlUitl(('select count(id) from account where account="%s"' % name))
    if num[0]['count(id)'] > 0:
        return jsonify({'result':'该账号已存在！'})
    else:
        d5pwd = utils.hmac_md5(password)
        logging.info(d5pwd)
        rownum = bseSql.sqlUitl(('insert into account (account,password,authority,cancle) values ("%s","%s",1,0)' % (name,d5pwd)))
        if rownum > 0:
            return jsonify({'result':1})
        else:
            return jsonify({'result':0})
    

