'''
Created on 2017年7月24日

@author: ning.lin
'''
# -*- coding: utf-8 -*-
from configobj import ConfigObj

from loggingclass import log

'''
一个简单的配置文件定义
[web2]     这是sections
user = root   这一行是options/后面的值就是value
passwd = root
'''


#定义日志写入路径log
logfile='D:\\Program Files\\Python_Workspace\\devpos_simple\\logs\\config.log'
log=log(logfile)


conf_ini = "./text.ini"  
#读取配置文件中的某一个sections
def read_sections(filename,sections):

    dict_value={}
    try:
        config = ConfigObj(filename,encoding='UTF8')
        for k,v in config[sections].items():
            dict_value[k]=v
        return dict_value
    except Exception as e:
        print("config err",log.error(str(e)))
#得到配置文件中的所有配置       
def read_all(filename):
    '''
            常见方法
    ‘items’
    ‘iteritems’
    ‘iterkeys’
    ‘itervalues’
    ‘keys’
    ‘popitem’
    ‘values’
    '''
    dict_value={}
    try:
        config = ConfigObj(filename,encoding='UTF8')
        #items = config.popitem()
        items = config.iteritems()
        for k,v in items:
            dict_value[k]=v
        return dict_value
    except Exception as e:
        print("config err",log.error(str(e)))

#找到集群中的所有机器，以配置文件中的名称为准，
def read_theSames(filename,same):
    '''
    same是同一组机器的共性命名，
    [web1][web2][web4]----same=web
     read_theSames(filename,web)
    '''
    dict_value={}
    count = len(same)
    print("same位数",count)
    try:
        config = ConfigObj(filename,encoding='UTF8')
        #items = config.popitem()
        items = config.iteritems()
        for k,v in items:
            if k[0:count]==same:
                dict_value[k]=v
        return dict_value
    except Exception as e:
        print("config err",log.error(str(e)))
        
#添加新项目
def add_config(filename,sections='default',ip='127.0.0.1',port=22,user='root',passwd='root',**key):
    '''
                    生成配置文件, 字典的形式添加数据
    '''
    try:
        config = ConfigObj(filename,encoding='UTF8')  
        #config.initial_comment(sections)
        config[sections]={}
        config[sections]['ip'] = ip
        config[sections]['port'] = port
        config[sections]['user'] = user
        config[sections]['passwd'] = passwd
    #添加多余的配置字段 
        for k,v in key.items():
            config[sections][k]=v
        print(sections,config[sections])
        config.write()
    except Exception as e:
        print("config初始化异常",str(e),log.error(str(e)))

def update_config(filename,sections,options,value):
    try:
        config = ConfigObj(filename,encoding='UTF8')  
        config[sections][options]=value
        #修改一个sections
        #config.rename(sections, 'sss')
        config.write()
    except Exception as e:
        print("config初始化异常",str(e),log.error(str(e)))
        
def del_config(filename,sections,options):
    try:
        config = ConfigObj(filename,encoding='UTF8')
        if validate_config(filename,sections,options):
            del config[sections][options]
            config.write()
        else:
            print( "ther is no that options")
    except Exception as e:
        print("config err",log.error(str(e)))
#验证是否有这个配置选项上
def validate_config(filename,sections,options):
    try:
        config = ConfigObj(filename,encoding='UTF8')
        #判断是否存在sections
        value1=config.get(sections)
        if value1:
            #判断是否存在options
            value2=config.get(sections).get(options)
            if value2:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print("config err",log.error(str(e)))
    
if __name__=='__main__':
    #print(read_theSames(conf_ini,'db'))
    #clear_clinfig(conf_ini)
    #print(read_all(conf_ini))
    #update_config(conf_ini, 'web2', 'ip', '192.168.0.100')
    #print(validate_config(conf_ini,'web3','sss'))
    #del_config(conf_ini,'web24','ssss')
    #add_config(conf_ini,'web2','192.168.153.135',22,'root','root')
    add_config(conf_ini,'web_01','192.168.153.135',22,'root','root',true='true',Off='Off',s="ssss")
    add_config(conf_ini,'web_02','172.17.0.2',22,'root','root',true='true',Off='Off',s="ssss")
    add_config(conf_ini,'web_03','172.17.0.3',22,'root','root',true='true',Off='Off',s="ssss")
    add_config(conf_ini,'db_store03','172.17.0.4',38022,'root','root',true='true',Off='Off',s="ssss")
    add_config(conf_ini,'db_store02','172.17.0.5',38022,'root','root',true='true',Off='Off',s="ssss")
