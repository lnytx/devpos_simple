#远程服务器
from _sqlite3 import connect
from distutils import command
import os
import shutil

import paramiko

from loggingclass import log


from tool_paramiko.使用配置文件configobj import read_all
from tool_paramiko.使用配置文件configobj import read_theSames
from tool_paramiko.使用配置文件configobj import add_config


ip = '192.168.153.135'
port = '9202'
username = 'root'  
password = 'root'  

logfile='D:\\Program Files\\Python_Workspace\\devpos_simple\\logs\\ssh_loggin.log'
log=log(logfile)
conf_ini = "./text.ini"  

def return_paramiko_connect(ip,port,username,password,logfile=logfile):
    #创建paramiko连接，用于传输文件
    try:
        paramiko.util.log_to_file("../logs/paramiko.log")  
        trans = paramiko.Transport((ip, int(port)))  
        trans.connect(username=username, password=password)  
        sftp = paramiko.SFTPClient.from_transport(trans)  
    except Exception as e:
        print ("连接%s:%s时报错，请查看日志%s" % (ip,port,logfile),str(e),'\n',log.error(str(e)))
        #记录IP加端口，将其写入未连接成功的配置文件中
    return sftp

def return_ssh_connect(ip,port,username,password,logfile=logfile):
    #创建SSH连接用于执行命令
    try:
        ssh = paramiko.SSHClient()
        paramiko.util.log_to_file('../logs/ssh.log')
        #允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("ip+端口",ip,port)
        ssh.connect(ip, int(port),username, password,timeout=1)
    except Exception as e:
        print ("连接%s:%s时报错，请查看日志%s" % (ip,port,logfile),str(e),'\n',log.error(str(e)))
        #记录IP加端口，将其写入未连接成功的配置文件中
        #将连接异常的IP写入到数据库，这里是写入到一个配置文件中
    return ssh

def exec_ssh_command(ssh,command):
    try:
        stdin,stdout,stderr = ssh.exec_command(command)
        channel = stdout.channel
        status = channel.recv_exit_status()
        print("status",status)
        if status==0:
            print("已经连接到该主机%s:%s,mkdir -p命令执行成功" %(ip,port))
        else:
            print("执行命令%s报错,请查看日志"% (status))
            log.error(str(stderr.read()))
            print (stderr.read().decode('utf-8'))
    except Exception as e:
        print (stderr.read().decode('utf-8'),log.error(str(e)))

#根据提供的参数使用ssh连接到对应机器   
def ssh_connect_command(logfile,ip,port,username,password,command):
    no_con_server=[]
    try:
        ssh = paramiko.SSHClient()
        paramiko.util.log_to_file('../logs/ssh.log')
        #允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("ip+端口",ip,port)
        ssh.connect(ip, int(port),username, password,timeout=1)
        try:
            stdin,stdout,stderr = ssh.exec_command(command)
            channel = stdout.channel
            status = channel.recv_exit_status()
            print("status",status)
            if status==0:
                print("已经连接到该主机%s:%s，%s命令执行成功" %(ip,port,command))
                #打印执行的命令
                #print (stdout.read().decode('utf-8'))
            else:
                print("执行命令%s报错,请查看日志"% (status,logfile))
                log.error(str(stderr.read()))
                print (stderr.read().decode('utf-8'))
                sessions=ip+":"+port
                #执行命令异常的IP写入到数据库，这里是写入到一个配置文件中
                add_config(logfile,sessions,ip,port,username,password)
        except Exception as e:
            print ("执行命令%s时报错，请看日志" % command,logfile,'\n',stderr.read().decode('utf-8'),log(str(e)))
            sessions=ip+":"+port
            #执行命令异常的IP写入到数据库，这里是写入到一个配置文件中
            add_config(logfile,sessions,ip,port,username,password)
    except Exception as e:
        print ("连接%s:%s时报错，请查看日志%s" % (ip,port,logfile),str(e),'\n',log.error(str(e)))
        #记录IP加端口，将其写入未连接成功的配置文件中
        sessions=ip+":"+port
        #将连接异常的IP写入到数据库，这里是写入到一个配置文件中
        add_config(logfile,sessions,ip,port,username,password)
        
    
    #return ssh  
    


    
    
def chan_connect(ip,port,command):
    #设置ssh连接的远程主机地址和端口
    t=paramiko.Transport((ip,port))
    #设置登录名和密码
    t.connect(username=username,password=password)
    #连接成功后打开一个channel
    chan=t.open_session()
    #设置会话超时时间
    chan.settimeout(3)
    #打开远程的terminal
    chan.get_pty()
    #激活terminal
    chan.invoke_shell()
    #然后就可以通过chan.send('command')和chan.recv(recv_buffer)来远程执行命令以及本地获取反馈。
    chan.send('df -h')
    str1=str(chan.recv(65535),'utf-8')
    print(str1)

def test_ssh_config(conf_ini,sames):
    no_connect_ini="../configs/no_conn.ini"
    dict_server={}
    dict_server=read_theSames(conf_ini,sames)
    print("dict_server",dict_server)
    #print("type",type(dict_server),dict_server)
    #print(dict_server['ssh_01']['ip'])
    #print(type(read_theSames(conf_ini,'ssh')))
    #print("dict_server",dict_server)
    for key in dict_server:
        #print("value type",value)#class 'configobj.Section'
        #print("key",dict_server[key])
        #测试配置文件中的IP是否可能使用ssh连接上
        ssh_connect_command(no_connect_ini,dict_server[key]['ip'], dict_server[key]['port'], dict_server[key]['user'], dict_server[key]['passwd'], 'pings www.baidu.com -W 1 -c 1')
def test_ssh_fail_config():
    conf_ini='../configs/no_conn.ini'
    temp_ini='../configs/for_fail_con.ini'
    shutil.copyfile(conf_ini, temp_ini)
    dict_server={}
    dict_server=read_all(conf_ini)
    print("dict_server",dict_server)
    if os.path.exists(temp_ini):
        os.remove(temp_ini)
    for key in dict_server:
        #测试配置文件中的IP是否可能使用ssh连接上
        ssh_connect_command(temp_ini,dict_server[key]['ip'], dict_server[key]['port'], dict_server[key]['user'], dict_server[key]['passwd'], 'ping www.baidu.com -W 1 -c 1')
if __name__=='__main__':
    #ssh_connect(ip,port,username,password,'pwd')
    #test_ssh_config(conf_ini,'ssh')
    test_ssh_fail_config()
    
    