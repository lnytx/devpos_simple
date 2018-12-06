'''
Created on 2017年7月31日

@author: ning.lin
远程服务器上的文件备份，简单一点，先打包再拉下来
'''
import os
import time

from tool_paramiko.ssh_login import return_paramiko_connect, return_ssh_connect, \
    exec_ssh_command


from tool_paramiko.一次执行多个命令 import python_ssh


ip = '192.168.153.135'
port = 22
username = 'root'  
password = 'root'

def backup_dir(ip, port, username, password, local_dir, remote_dir,logfile='../logs/bakcup.log'):
    sftp = return_paramiko_connect(ip,port,username,password,logfile=logfile)
    ssh = return_ssh_connect(ip,port,username,password,logfile=logfile)
    #执行打包命令
    current_time=time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))
    #如果最好有/则去掉，没有则不作处理
    if local_dir[-1] == '/':
        local_dir = local_dir[0:-1]
    
    dir_name = os.path.basename(remote_dir)
    backup_file = ip +'_' + dir_name+'tar.gz_'+current_time
    print("backup_file",backup_file)
    #这里有问题，需要改进
    local_dir_file = local_dir+'/'+'backup_file'+'.tar.gz'
    print("local_dir_file",local_dir_file)
    command = 'cd ' + remote_dir +'  ,tar -czvf /tmp/dir_name.tar.gz ' + remote_dir
    print("command",command)
    #批量执行命令
    python_ssh(ip, port, username, password,shell1='cd'+remote_dir,shell2='tar -czvf /tmp/dir_name.tar.gz '+ remote_dir)
    sftp.get('/tmp/dir_name.tar.gz',local_dir_file)
    #下载文件到本地
if __name__=='__main__':
    local_dir ='D:/Program Files/Python_Workspace/devpos_simple/download_files/'
    remote_dir ='/soft/ELK/dir'
    backup_dir(ip, port, username, password, local_dir, remote_dir)
    print("basename",os.path.basename(remote_dir))
