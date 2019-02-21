# coding:utf-8

#admin.py
'''
Created on 2019年1月21日

@author: 杨腾广
    后台管理
'''
import logging; logging.basicConfig(level=logging.INFO)
from . import admin
from flask import jsonify,request
from www.sqlUtils import bseSql
#引入token
from www.utils import tokenutil
#引入上传图片
from www.utils import uploadsfile
from datetime import datetime
import uuid

#获取所有账号信息
@admin.route('/getAllAcnt',methods=['POST'])
@tokenutil.auth.login_required
def home():
    pageNum = request.form.get('pageNum')
    pageSize = request.form.get('pageSize')
    if pageNum == None:
        return jsonify({'result':'参数为空'})
    elif pageSize == None:
        return jsonify({'result':'参数为空'})
    else:
        allCount = bseSql.sqlUitl('select a.id as aid,a.account,a.authority,u.username from account a,user u where a.id = u.accountId and a.cancle <> "%s" order by a.id desc limit %s,%s' % (1,(int(pageNum)-1)*int(pageSize),int(pageSize)))
        if allCount:
            return jsonify({'result':allCount})
        else:
            return jsonify({'result':0})

#所有账号数  checkUserCount
@admin.route('/checkUserCount',methods=['POST'])
@tokenutil.auth.login_required
def checkUserCount():
    ucount = bseSql.sqlUitl('select count(id) from account')
    if ucount[0]['count(id)'] > 0:
        return jsonify({'result':ucount[0]['count(id)']})    
    else:
        return jsonify({'result':0})
    
    
#授权
@admin.route('/accredit',methods=['POST'])
@tokenutil.auth.login_required
def accredit():
    acountId = request.form.get('acountId')
    authorty = request.form.get('authorty')
    if acountId == None:
        return jsonify({'result':'账号id为空！'})
    elif authorty == None:
        return jsonify({'result':'授权标识为空！'})
    else:
        rownum = bseSql.sqlUitl('update account set authority="%s" where id="%s"' %(authorty,acountId))
        if rownum > 0:
            return jsonify({'result':1})
        else:
            return jsonify({'result':0})
        
#删除  
@admin.route('/deleteAcot',methods=['POST'])
@tokenutil.auth.login_required
def deleteAcot():
    acountId = request.form.get('acountId') 
    if acountId == None:
        return jsonify({'result':'账号id为空！'})  
    else:
        rownum = bseSql.sqlUitl('update account set cancle="%s" where id="%s"' %(1,acountId)) 
        if rownum > 0:
            return jsonify({'result':1})
        else:
            return jsonify({'result':0}) 
        
#文章审核查询
@admin.route('/checkArt',methods=["POST"])
@tokenutil.auth.login_required
def checkArt():
    pageNum = request.form.get('pageNum')
    pageSize = request.form.get('pageSize')
    if pageNum == None:
        return jsonify({'result':'参数为空'})
    elif pageSize == None:
        return jsonify({'result':'参数为空'})
    else:
        artArr = bseSql.sqlUitl('select a.id as aid, a.title,a.content,a.auditcon,a.auditathor,a.isAudit,u.id as uid,u.username from article a left join user u on u.accountId = a.auditathor order by a.pushtime desc limit %s,%s' % ((int(pageNum)-1)*int(pageSize),int(pageSize)))
        if artArr:
            return jsonify({'result':artArr})
        else:
            return jsonify({'result':0})    
#文章数量
@admin.route('/checkArtCount',methods=["POST"])
@tokenutil.auth.login_required   
def checkArtCount():
    count = bseSql.sqlUitl('select count(id) from article')
    if count[0]['count(id)']:
        return jsonify({'result':count[0]['count(id)']})
    else:
        return jsonify({'result':0})


#审核操作   
@admin.route('/auditeArt',methods=["POST"])
@tokenutil.auth.login_required 
def auditeArt():
    artid = request.form.get('artid')
    nopass = request.form.get('nopass')
    isaudit= request.form.get('isAudit')
    if artid == None:
        return jsonify({'result':'文章id为空'})
    elif isaudit == None:
        return jsonify({'result':'审核标识为空'})
    elif isaudit == 0:
        if nopass == None:
            return jsonify({'result':'不通过原因为空'})
    else:
        infoList =  getToken()
        if infoList:
            rownum = bseSql.sqlUitl('update article set auditathor="%s",auditcon="%s",isAudit="%s" where id="%s"' % (infoList[0]['id'],nopass,isaudit,artid))
            if rownum > 0:
                return jsonify({'result':1})
            else:
                return jsonify({'result':0})
        else:
            return jsonify({'result':-1})
        
#banner 上传
@admin.route('/bannerUpload',methods=['POST'])
@tokenutil.auth.login_required
def bannerUpload():
    if request.method == 'POST':
        file = request.files['file']   
        if file and uploadsfile.allowed_file(file.filename):
            filename = uploadsfile.secure_filename(file.filename)
            index = filename.find('.')
            fname = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')) + "." +filename[index:]
            url = uploadsfile.os.path.join(uploadsfile.app.config['UPLOAD_FOLDER'], fname)
            logging.info('url is : %s' % uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org'))
            file.save(url)
            return jsonify({'result':url})
        else:
            return jsonify({'result':0})       

#保存banner  
@admin.route('/saveBanner',methods=['POST'])
@tokenutil.auth.login_required  
def saveBanner():
    img = request.form.get('img')
    if img == None:
        return jsonify({'result':'参数为空'})
    else:
        rownum = bseSql.sqlUitl('insert into banner (bannerUrl,isDelete) values("%s",%s)' % (img,1))
        if rownum > 0:
            return jsonify({'result':1})
        else:
            return jsonify({'result':0})

#查询banner
@admin.route('/lookBanner',methods=['POST'])
@tokenutil.auth.login_required  
def lookBanner():
    pageNum = request.form.get('pageNum')
    pageSize =request.form.get('pageSize')
    if pageNum == None:
        return jsonify({'result':'参数为空'})
    elif pageSize == None:
        return jsonify({'result':'参数为空'})
    else:
        bannerList = bseSql.sqlUitl('select id, bannerUrl from banner  where isDelete=%s order by id desc limit %s,%s' % (1,(int(pageNum)-1)*int(pageSize),int(pageSize)))
        if len(bannerList) > 0:
            count = bseSql.sqlUitl('select count(id) as count from banner  where isDelete=%s' % 1)
            if count[0]['count'] > 0:
                return jsonify({'result':bannerList,'count':count[0]['count']})
            else:
                raise ValueError('查询出错')
        else:
            return jsonify({'result':0})

#删除banner  
@admin.route('/deleteBanner',methods=['POST'])
@tokenutil.auth.login_required  
def deleteBanner():
    bnid = request.form.get('bannerId')
    if bnid == None:
        return jsonify({'result':'参数为空'})
    else:
        rownum = bseSql.sqlUitl('update banner set isDelete="%s" where id="%s"' % (0,bnid))
        if rownum > 0:
            return jsonify({'result':1})
        else:
            return jsonify({'result':0})
    
    
    
#获取token
def getToken():
    token = bytes(request.form.get('token'),encoding='utf-8')
    return tokenutil.getAcount(token)