# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/1 17:38
@Auth ： DingKun
@File ：log.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import logging
import os.path

'''
功能描述：实现控制台和文件同时记录日志的功能
编写人：超哥
编写日期：
步骤分析：
  1-配置日志记录器名称
  2-配置日志级别
  3-配置日志格式（可以分别设置，也可以统一设置）
  4-创建并添加handler-控制台
  5-创建并添加handler-文件
  6-提供对外获取logger
'''


def log_create():
    logger = logging.getLogger('EQMX Mqtt Bridge Informations')
    logger.setLevel(level=logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    # if os.path.exists("/home/MosuitToMysql/log.txt"):
    #     pass
    # else:
    txt_file = open("log.txt", 'w')
    txt_file.close()
    file_handler = logging.FileHandler("log.txt")
    file_handler.setLevel(level=logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


log_create = log_create()

if __name__ == '__main__':
    logger = log_create
    logger.info('使用函数定义的log方法')
