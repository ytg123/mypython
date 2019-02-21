'''
Created on 2019年1月22日

@author: 杨腾广
'''
import hmac,random

#d5key = ''.join([chr(random.randint(48, 122)) for i in range(20)])
d5key = b'abc876..??'
#生成密钥
def hmac_md5(s):
    return hmac.new(d5key, s.encode('utf-8'), 'MD5').hexdigest()