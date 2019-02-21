'''
Created on 2019年1月21日

@author: 杨腾广
    
    前台功能
'''
import logging; logging.basicConfig(level=logging.INFO)
from flask import jsonify,request
from datetime import datetime
import uuid
from . import index
from www.sqlUtils import bseSql
#引入token
from www.utils import tokenutil
#引入上传图片
from www.utils import uploadsfile

#登录成功后，判断账号有没用户信息，，如果没有就去维护用户信息，否则就去首页
@index.route('/isIndex',methods=['POST'])
def home():
    infoList = getToken()
    uinfo = bseSql.sqlUitl('select count(u.id),a.authority from user u,account a where a.id = "%s" and accountId = "%s"' % (infoList[0]['id'],infoList[0]['id']))
    #如果有结果修改否则新增
    if uinfo[0]['count(u.id)'] <= 0:
        return jsonify({'result':0})
    elif uinfo[0]['authority'] == 0:
        return jsonify({'result':-1})
    elif uinfo[0]['authority'] == 1:
        return jsonify({'result':1})
    else:
        return jsonify({'result':1})
    
#获取banner
@index.route('/banner',methods=['POST'])
def banner():
    banners= bseSql.sqlUitl('select id,bannerUrl from banner  where isDelete="%s" order by id' % 1)
    print(banners)
    if len(banners)> 0:
        return jsonify({'result':banners})
    else:
        return jsonify({'result':'banner'})

#获取用户信息
@index.route('/getSelfInfo',methods=['POST'])
@tokenutil.auth.login_required
def getSelf():
    infoList =  getToken()
    if infoList:
        selfInfo = bseSql.sqlUitl('select u.username,u.age,u.six,u.img,ac.account,ac.authority from user u , account ac where u.accountId="%s"' % infoList[0]['id'])
        if selfInfo:
            return jsonify({'result':selfInfo})
        else:
            return jsonify({'result':-1})
    else:
        return jsonify({'result':0})

#获取账号
@index.route('/getAccount',methods=['POST'])
@tokenutil.auth.login_required
def getAccount():
    infoList =  getToken()
    if infoList:
        acountInfo = bseSql.sqlUitl('select account from account where id="%s"' % infoList[0]['id'])
        if acountInfo:
            return jsonify({'result':acountInfo})
        else:
            return jsonify({'result':0})

#获取文章信息
@index.route('/getArticle',methods=['POST'])
def getAtcile():
    page = request.form.get('page')
    pageNum = request.form.get('pageNum')
    searchText = request.form.get('searchTxt')
    artcileList = bseSql.sqlUitl('select a.id,a.title,a.pubauthor,a.pushtime,a.content,t.tnum from article a left join (select count(thumbnum) as tnum,articleId from thumb group by articleId) t on a.id = t.articleId where a.isAudit="%s" and a.title like "%s"  order by a.pushtime desc limit %s,%s' % (1,'%'+searchText+'%',(int(page)-1)*int(pageNum),int(pageNum)))
    if artcileList:
        artcount = bseSql.sqlUitl('select count(id) from article where isAudit="%s"  and title like "%s"' % (1,'%'+searchText+'%'))
        if artcount[0]['count(id)'] > 0: 
            return jsonify({'result':artcileList,'count':artcount[0]['count(id)']})
        else:
            pass                                                   
    else:
        return jsonify({'result':0})

#我的收藏
@index.route('/mycollec',methods=['POST'])
@tokenutil.auth.login_required
def  getMycollec():
    page = request.form.get('page')
    pageNum = request.form.get('pageNum')
    infoList =  getToken()
    if infoList:
        artcileList = bseSql.sqlUitl('select j.id,j.title,j.content,j.pubauthor,j.pushtime,j.accountId,j.articleId,t.tnum from (select a.id,a.title,a.content,a.pubauthor,a.pushtime,o.accountId,o.articleId from article a right join (select articleId,accountId from collec where accountId = "%s" and iscollec = "%s") o on o.articleId = a.id where a.isAudit = "%s") j left join (select count(thumbnum) as tnum,articleId from thumb group by articleId) t on t.articleId = j.articleId  order by j.pushtime  limit %s,%s' % (infoList[0]['id'],1,1,(int(page)-1)*int(pageNum),int(pageNum)))
        if artcileList:
            artcount = bseSql.sqlUitl('select count(ct.id) from (select j.id,j.title,j.content,j.pubauthor,j.pushtime,j.accountId,j.articleId,t.tnum from (select a.id,a.title,a.content,a.pubauthor,a.pushtime,o.accountId,o.articleId from article a right join (select articleId,accountId from collec where accountId = "%s" and iscollec = "%s") o on o.articleId = a.id where a.isAudit = "%s") j left join (select count(thumbnum) as tnum,articleId from thumb group by articleId) t on t.articleId = j.articleId  order by j.pushtime) ct' % (infoList[0]['id'],1,1))
            if artcount[0]['count(ct.id)'] > 0: 
                return jsonify({'result':artcileList,'count':artcount[0]['count(ct.id)']})
            else:
                pass                                                 
        else:
            return jsonify({'result':0})
    else:
        return jsonify({'result':-1})

#评论
@index.route('/sendDiscuss',methods=['POST'])
@tokenutil.auth.login_required
def sendDiscuss():
    artid = request.form.get('artid')
    discon = request.form.get('discon')
    sendTime = datetime.now()
    infoList =  getToken()
    if infoList:
        rownum = bseSql.sqlUitl('insert into discuss (accountId,articleId,dsicusscon,discusstime) values ("%s","%s","%s","%s")' % (infoList[0]['id'],artid,discon,sendTime))
        if rownum > 0:
            return jsonify({'result':1})
        else:
            return jsonify({'result':0})
    else:
        return jsonify({'result':-1})
    

#回复评论
@index.route('/replayDiscuss',methods=['POST'])
@tokenutil.auth.login_required
def replayDis():
    replaycon = request.form.get('discon')  
    discusssid = request.form.get('discussId')
    pid = request.form.get('pid')
    replayTime = datetime.now()
    infoList =  getToken()
    if infoList:
        accountId = bseSql.sqlUitl('select accountId from discuss where id="%s"' % discusssid)
        print(accountId)
        print(infoList[0]['id'])
        if accountId:
            if infoList[0]['id'] == accountId[0]['accountId']:
                return jsonify({'result':'same'})
            else:
                rownum = bseSql.sqlUitl('insert into replay (discussId,accountId,replaycon,replaytime,articleId) values ("%s","%s","%s","%s","%s")' % (discusssid,infoList[0]['id'],replaycon,replayTime,pid))
                if rownum > 0:
                    return jsonify({'result':1})
                else:
                    return jsonify({'result':0})
        else:
            return jsonify({'result':'none'})
    else:
        return jsonify({'result':-1})

#查看评论及回复
@index.route('/lookDiscussAndReplay',methods=['POST'])
@tokenutil.auth.login_required
def lookDiscussAndReplay():
    artid = request.form.get('artid')
    #评论信息
    discussscon = bseSql.sqlUitl('select d.articleId,d.id as did,d.discusstime,d.dsicusscon,d.accountId,u.img,u.username from discuss d left join user u on u.accountId = d.accountId  where d.articleId="%s" order by did'  % artid)
    if discussscon:
        replayyycon = bseSql.sqlUitl('select ry.articleId,ry.discussId,ry.id,ry.replaycon,ry.replaytime,ry.accountId,ru.img,ru.username from replay ry left join user ru on ru.accountId = ry.accountId where ry.articleId = "%s" order by ry.discussId' % artid)
        if replayyycon:
            return jsonify({'result':{'drcon':discussscon,'rpcon':replayyycon}})
        else:
            return jsonify({'result':0})
    else:
        return jsonify({'result':0})
    
#访客量
@index.route('/victornum',methods=['POST'])
@tokenutil.auth.login_required
def getVictorNum():
    artid = request.form.get('artid')
    startTime = request.form.get('startTime')
    endTime = request.form.get('endTime')
    insertTime = datetime.now()
    infoList =  getToken()
    if infoList:
        num = bseSql.sqlUitl('select count(id) from victor where accountId = "%s" and articleId = "%s" and  victime BETWEEN "%s" AND "%s"' % (infoList[0]['id'],artid,startTime,endTime))
        print(num)
        if num[0]['count(id)'] == 0:
            #增加访客
            rownum = bseSql.sqlUitl('insert into victor (accountId,articleId,victime,vicnum) values ("%s","%s","%s","%s")' % (infoList[0]['id'],artid,insertTime,1))
            if rownum > 0:
                vicNum = bseSql.sqlUitl('select count(accountId) from victor where articleId = "%s" and victime BETWEEN "%s" AND "%s" group by accountId;' % (artid,startTime,endTime))
                print(vicNum)
                if vicNum[0]['count(accountId)'] > 0:
                    return jsonify({'result':len(vicNum)})
        else:
            vicNumm = bseSql.sqlUitl('select count(accountId) from victor where articleId = "%s" and victime BETWEEN "%s" AND "%s" group by accountId;' % (artid,startTime,endTime))
            print(vicNumm)
            if vicNumm[0]['count(accountId)'] > 0:
                return jsonify({'result':len(vicNumm)})
    else:
        return jsonify({'result':-1})
#根据文章id获取内容
@index.route('/getArticleById',methods=['POST'])
def getArtById():
    artid = request.form.get('artid')
    if artid == None:
        return jsonify({'result','none'})
    else:
        #infoList =  getToken()
        #if infoList:    
        artcon = bseSql.sqlUitl('select a.id,a.title,a.pubauthor,a.pushtime,a.content,a.pageview from article a left join collec c on c.articleId = a.id where a.id = "%s"' % artid)
        if artcon:
            return jsonify({'result':artcon})
        else:
            return jsonify({'result':0})
        #else:
            #return jsonify({'result':-1})

#根据账号id和文章id查是否收藏文章
@index.route('/isCollec',methods=['POST'])
@tokenutil.auth.login_required
def isCollec():
    artid = request.form.get('artid')
    infoList =  getToken()
    if infoList:
        quey = bseSql.sqlUitl('select iscollec from collec where articleId="%s" and accountId="%s"' % (artid,infoList[0]['id']))
        if quey:
            return jsonify({'result':quey})
        else:
            return jsonify({'result':0})
    else:
        return jsonify({'result':-1})   
        
#点赞
@index.route('/thumbupadd',methods=['POST'])
@tokenutil.auth.login_required
def thumb():
    tid = request.form.get('id')
    infoList =  getToken()
    if infoList:
        thumbn = bseSql.sqlUitl('select count(id),thumbnum from thumb where accountId = "%s" and articleId = "%s"' % (infoList[0]['id'],tid))
        if thumbn[0]['count(id)'] == 0:
            #点赞量
            rownum = bseSql.sqlUitl('insert into thumb (accountId,articleId,thumbnum) values ("%s","%s","%s")' % (infoList[0]['id'],tid,1))
            if rownum > 0:
                thumbupm = bseSql.sqlUitl('select count(thumbnum) as tnum from thumb  where articleId="%s" group by articleId' % tid)
                return jsonify({'result':thumbupm[0]['tnum']})
            else:
                return jsonify({'result':0})
        else:
            return jsonify({'result':'thumbed'}) 
    else:
        return jsonify({'result':-1}) 
    
#收藏
@index.route('/opcollec',methods=['POST'])
@tokenutil.auth.login_required
def collecArt():
    artid = request.form.get('artid')    
    infoList =  getToken()
    if infoList:
        collec = bseSql.sqlUitl('select id,iscollec from collec where accountId="%s" and articleId="%s"' % (infoList[0]['id'],artid))
        if len(collec) == 0:
            #还没有收藏，可以收藏
            rownum = bseSql.sqlUitl('insert into collec (accountId,articleId,iscollec) values ("%s","%s","%s")' % (infoList[0]['id'],artid,1))
            if rownum > 0:
                return jsonify({'result':1}) #收藏成功
            else:
                return jsonify({'result':0})
        else:
            return jsonify({'result':'colleced'})
    else:
        return jsonify({'result':-1})
#修改个人信息
@index.route('/upselfInfo',methods=['POST'])
@tokenutil.auth.login_required
def updateSelfInfo():
    #获取前台过来的参数
    nickname = request.form.get('nickname')
    age = request.form.get('age')
    six = request.form.get('six')
    img = request.form.get('img')
    infoList =  getToken()
    if infoList:
        uinfo = bseSql.sqlUitl('select count(id) from user where accountId="%s"' % infoList[0]['id'])
        #如果有结果修改否则新增
        if uinfo[0]['count(id)'] == 0:
            rownum = bseSql.sqlUitl('insert into user (username,age,six,img,accountId) values ("%s","%s","%s","%s","%s")' % (nickname,age,six,img,infoList[0]['id']))
            if rownum > 0:
                return jsonify({'result':'新增成功！'})
            else:
                return jsonify({'result':'新增失败！'})
        else:
            rownums =  bseSql.sqlUitl('update user set username="%s",age="%s",six="%s",img="%s" where accountId="%s"' % (nickname,age,six,img,infoList[0]['id']))
            if rownums > 0:
                return jsonify({'result':'修改成功！'})
            else:
                return jsonify({'result':'修改失败！'})
    else:
        return jsonify({'result':0}) 

#上传头像
@index.route('/fupload',methods=['POST'])
@tokenutil.auth.login_required
def uploadF():
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

#文章发布
@index.route('/publishArticle',methods=['POST'])
@tokenutil.auth.login_required
def articelPublish():
    title = request.form.get('title')
    author = request.form.get('author')
    content = request.form.get('content')
    pubtime = datetime.now()
    infoList =  getToken()
    if title == None:
        return jsonify({'result':'标题不能为空'})
    elif author == None:
        return jsonify({'result':'发布者不能空'})
    elif content == None:
        return jsonify({'result':'内容不能空'})
    else:
        rownum = bseSql.sqlUitl('insert into article (title,content,pubauthor,pushtime,accountId,isAudit) values ("%s","%s","%s","%s","%s","%d")' % (title,content,author,pubtime,infoList[0]['id'],0))
        if rownum > 0:
            return jsonify({'result':1})
        else:
            return jsonify({'result':0}) 

   
#获取token
def getToken():
    token = bytes(request.form.get('token'),encoding='utf-8')
    return tokenutil.getAcount(token)
    