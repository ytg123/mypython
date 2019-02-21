import mysql.connector
import logging; logging.basicConfig(level=logging.INFO)
#引入SQL信息
from conf.ggsql.config import sqlConfig
def __init__():
    pass
    
def sqlUitl(sql):
    logging.info(sql)
    if not isinstance(sql, str):
        raise TypeError('参数必须是字符串类型')
    else:
        try:    
            conn = mysql.connector.connect(host=sqlConfig['h'],user=sqlConfig['u'],password=sqlConfig['p'],database=sqlConfig['db'])
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            #增删改需要提交
            if sql.lower().find('select') == -1:
                try:
                    conn.commit()
                    return cursor.rowcount
                finally:
                    conn.rollback()
            else:
                #获取所有数据
                results = cursor.fetchall()
                return results
        except:
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()
        finally:
            cursor.close()
            conn.close()   
def __del__():
    pass
