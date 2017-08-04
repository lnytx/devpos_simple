'''
Created on 2017年7月24日

@author: ning.lin
'''
# -*- coding: utf-8 -*-
import time

from configobj import ConfigObj

from loggingclass import log


print("123")



#定义日志写入路径log
logfile='D:\\Program Files\\Python_Workspace\\devpos_simple\\logs\\config.log'
log=log(logfile)

#  
conf_ini = 'test.ini'
c1 = ConfigObj(conf_ini)
print("conf_ini",c1)

print(time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time())))
#  
# 读配置文件  
#  
# print (c1['server'])
# print (c1['server']['servername'])
L=[1,2,3,4]
print("L[10:]",L[10:])

v='a:b:c'
print(v.split(':')[1])


    

#if __name__=='__main__':
#    pass
    #read_config_file(logfile)
    #config_write('db','192.168.153.135',22,'root','root')
    #config_write('web2','192.168.153.135',22,'root','root',key1='asss',key2='bbb',s="ssss")
    #config_write('web3','192.168.153.135',22,'root','root',key1='asss',key2='bbb',s="ssss")
