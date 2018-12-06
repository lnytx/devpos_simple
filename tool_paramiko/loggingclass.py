# -*- coding: utf-8 -*-

'''
主要用途：
    对程序中所使用的loggong模式做一般性配置
     日志处理
'''

import logging

import logging.handlers

import os

# base_dir='D:\Program Files\Python_Workspace\devpos_simple\logs'
# logs_dir = os.path.join(base_dir, "logs")
# file_name=logs_dir+'\log.txt'

def log(log_file):
#     LEVELS = {'NOSET': logging.NOTSET,
#               'DEBUG': logging.DEBUG,
#               'INFO': logging.INFO,
#               'WARNING': logging.WARNING,
#               'ERROR': logging.ERROR,
#               'CRITICAL': logging.CRITICAL}
    
    #set up logging to file
    
    #logging.basicConfig(level = logging.NOTSET,
    #                    format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    #                    )
    
    ##                    filename = "./log.txt",
    
    ##                    filemode = "w")
    
    # create logs file folder
    logs_dir=os.path.dirname(log_file)
    if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
        pass
    else:
        os.mkdir(logs_dir)
      
    # define a rotating file handler
    #滚动时写入，按大小写入，每个50M
    #rotatingFileHandler = logging.handlers.RotatingFileHandler(filename =file_name,maxBytes = 1024 * 1024 * 50,backupCount = 5)
    #按日期写入
    '''  filename    日志文件名前缀
        when        日志名变更时间单位
            'S' Seconds
            'M' Minutes
            'H' Hours
            'D' Days
            'W0'-'W6' Weekday (0=Monday)
            'midnight' Roll over at midnight
        interval    间隔时间，是指等待N个when单位的时间后，自动重建文件
        backupCount 保留日志最大文件数，超过限制，删除最先创建的文件；默认值0，表示不限制。
        delay       延迟文件创建，直到第一次调用emit()方法创建日志文件
        atTime      在指定的时间（datetime.time格式）创建日志文件。
    '''
    rotatingFileHandler = logging.handlers.TimedRotatingFileHandler(log_file,when='D',interval=1,backupCount=40)
    
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)-8s %(filename)8s %(funcName)8s %(lineno)8d")
    
    rotatingFileHandler.setFormatter(formatter)
    rotatingFileHandler.setLevel(logging.INFO)
    
    logging.getLogger("").addHandler(rotatingFileHandler)
    
    #define a handler whitch writes messages to sys
    #控制台输出
    console = logging.StreamHandler()
    
    console.setLevel(logging.INFO)
    
    #set a format which is simple for console use
    
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)-8s %(filename)8s %(funcName)8s %(lineno)8d")
    #formatter = logging.Formatter("%(name)s: %(levelname)s %(message)s")
    
    #tell the handler to use this format
    
    console.setFormatter(formatter)
    
    #add the handler to the root logger
    
    logging.getLogger("").addHandler(console)
    
    # set initial log level
    logger = logging.getLogger("")
    logger.setLevel(logging.NOTSET)  
    return logger


# if __name__ == "__main__":
#     msg = "this is just a test"
#     log=log()
#     log.info(msg)
#     log.error(msg)
#     log.debug(msg)
#     #log.WARNING(msg)
#     #log.NOTSET(msg)