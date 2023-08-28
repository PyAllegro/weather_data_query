# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/31 14:13
@Auth ： DingKun
@File ：SaveToMySQL.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import json
import logging
import os
import sys
import pymysql

import log
from log import log_create

accountInfo = {"host": "123.60.171.53",
               "user": "root",
               "passwd": "qazWSX123EDC-",
               "db": "emqx_yiwei",
               "charset": "utf8"
               }


def connectMysql():
    # accountInfo = "accountInfo_meter.json"
    # with open(accountInfo, 'r') as load_f:
    #     load_dict = json.load(load_f)
    info = accountInfo  # load_dict
    host = info['host']  # 主机ip地址
    user = info['user']  # 用户名
    passwd = info['passwd']  # 密码
    db = info['db']  # 数据库名
    charset = info['charset']  # 字符集
    # 建立一个MySQL连接（不使用配置文件，直接填入数据库连接信息）
    try:
        conn = pymysql.connect(host=host, user=user, passwd=passwd, database=db, charset=charset)
        # 创建游标,给数据库发送sql指令,id已经设置为自增
        cursor = conn.cursor()
    except Exception as e:
        log_create.error('数据库连接超时' + str(e))
        except_type, except_value, except_traceback = sys.exc_info()
        except_file = os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
        exc_dict = {"报错类型": except_type,
                    "报错信息": except_value,
                    "报错文件": except_file,
                    "报错行数": except_traceback.tb_lineno}
        log_create.error(str(exc_dict), str(e))
        return False, '服务器连接超时' + str(e)
    else:
        return conn, cursor


def saveToMysql(data):
    conn, cursor = connectMysql()
    try:
        assert conn is not False, '数据库连接失败' + cursor
        sql = "insert into position_weather(positionCounty, temperature, humidity, visibility, windSpeed, " \
              "pressureSurfaceLevel, rainAccumulation, cloudCover, collectionTime) values  (%s, %s, %s, %s, %s, %s," \
              "%s, %s, %s) "
        cursor.executemany(sql, data)
        conn.commit()
    except Exception as e:
        if conn is not False:
            cursor.close()
            conn.close()
        else:
            pass
        except_type, except_value, except_traceback = sys.exc_info()
        except_file = os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
        exc_dict = {"报错类型": except_type,
                    "报错信息": except_value,
                    "报错文件": except_file,
                    "报错行数": except_traceback.tb_lineno}
        log.logger.error(exc_dict)
        return False
    else:
        cursor.close()
        conn.close()
        return True

