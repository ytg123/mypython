'''
Created on 2019年1月24日

@author: 杨腾广

上传文件
'''
import os
from flask import Flask
from werkzeug import secure_filename

UPLOAD_FOLDER = 'static\\upload'
ALLOWED_EXTENSIONS = set(['pdf','PDF', 'png','PNG', 'jpg','JPG', 'jpeg','JPEG', 'gif','GIF'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

