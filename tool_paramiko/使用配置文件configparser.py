'''
Created on 2017年7月24日

@author: ning.lin
'''
# -*- coding: utf-8 -*-
'''
-read(filename) 直接读取ini文件内容
-sections() 得到所有的section，并以列表的形式返回
-options(section) 得到该section的所有option
-items(section) 得到该section的所有键值对 type <class 'list'>
-get(section,option) 得到section中option的值，返回为string类型
-getint(section,option) 得到section中option的值，返回为int类型
'''
#定义日志写入路径log

from _codecs import decode
import code
import configparser
from email._header_value_parser import Section
import inspect

from loggingclass import log

'''
1，不能区分大小写。
2，重新写入的ini文件不能保留原有INI文件的注释。
3，重新写入的ini文件不能保持原有的顺序。
4，不支持嵌套。
5，不支持格式校验。
'''
logfile='D:\\Program Files\\Python_Workspace\\devpos_simple\\logs\\config.log'
log=log(logfile)

def config_test():
    cf = configparser.ConfigParser()
    cf.read('./property.config',encoding='utf-8')
    #获取所有的sections,返回一个列表
    sections = cf.sections()
    print("section",sections)
    #得到该section的所有键值对,type <class 'list'>
    items=cf.items('concurrent')
    print("items",items)
    print("type",type(items))
    #得到最终的配置值，string类型.getint取int类型的数据，比如端口什么的
    value = cf.get('db','db_host')
    value2 = cf.get('db','db_port')
    print("type(value)",type(value2),value2)
    
    #获取options内容
    #options = cf.options(sections[1])
    for k in sections:
        options = cf.options(k)
        items = cf.items(k)
        print("items",k,items)
        print("options",k,":",options)
    

  
def read_config_file(logfile):  
    '''''Read_config_file(filename) 
 
        this function is used for parse the config file'''      
    #定义一个方法
    cofile = './property.config' 
    data = {}  
    config = configparser.ConfigParser()
    try:  
        with open(cofile,'r') as confile:  
            config.readfp(confile)  
        #config.read(filename)  
            for i in config.sections():  
                for (key, value) in config.items(i):  
                    data[key] = value
                print(log.info(str(value)))
            return data      
    except Exception as e:  
        print ("Open file error." ,log.error(str(e))) 


def config_write(sections='default',ip='127.0.0.1',port=22,user='root',passwd='root',**key):
    '''
                    生成配置文件, 字典的形式添加数据
    '''
    print("函数参数个数",inspect.getargspec(config_write))
    try:
        config = configparser.ConfigParser()
        config[sections]={
                        'ip':ip,
                        'port':port,
                        'user':user,
                        'passwd':passwd,
                        }
        #for k,v in key.items():
            #config[sections][k]=v
            #print("value",v)
#         config['web']={}
#         config['web']['ip']='192.168.0.1'
#         config["mysql"]={}
#         topsecret=config['myssql']#这种操作还是在操作mysql这个sections
#         topsecret['ip']='127.0.0.1'
#         topsecret['user']='root'
    except Exception as e:
        print("config初始化异常",str(e),log.error(str(e)))
    try:
        with open('config.ini', 'w') as configfile:
            print("添加sections",sections)
            config.add_section(sections)
            config.set(sections,"ip",ip)
            config.set(sections,"port",str(port))
            config.set(sections,"user",user)
            config.set(sections,"passwd",passwd)
            print("写入配置文件")
            config.add_section('ass')
            config.write(configfile)
    except Exception as e:
        print("打开文件异常",str(e),log.error(str(e)))
if __name__=='__main__':
    #read_config_file(logfile)
    #config_write('db','192.168.153.135',22,'root','root')
    config_write('web2','192.168.153.135',22,'root','root',key1='asss',key2='bbb',s="ssss")
    config_write('web3','192.168.153.135',22,'root','root',key1='asss',key2='bbb',s="ssss")
