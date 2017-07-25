
# -*- coding:utf8 -*-
'''
Created on 2017年7月20日

@author: ning.lin
'''
from os import path
import os

import paramiko


#下载文件
def sftp_down_file(server_path, local_path):
    try:
        t = paramiko.Transport(('192.168.153.135', 22))
        t.connect(username='root', password='root')
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path)
        t.close()
    except Exception as e:
        print (str(e))

#上传文件
def sftp_up_file():
    t = paramiko.Transport(("某IP地址",22))
    t.connect(username = "用户名", password = "口令")
    sftp = paramiko.SFTPClient.from_transport(t)
    remotepath='/tmp/test.txt'
    localpath='/tmp/test.txt'
    sftp.put(localpath,remotepath)
    t.close()


def exec_command(ip, port, username, password, cmd):  
    """远程执行命令 
    """  
  
    paramiko.util.log_to_file("paramiko.log")  
  
    ssh = paramiko.SSHClient()  
    ssh.load_system_host_keys()  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    ssh.connect(hostname=ip, port=int(  
        port), username=username, password=password, timeout=5)  
    stdin, stdout, stderr = ssh.exec_command('cmd.exe /C "%s"' % cmd)  
  
    ssh.close()  
  
  
def upload_file(ip, port, username, password, local_file_path, remote_file_path):  
    """上传文件 
    """  
  
    paramiko.util.log_to_file("paramiko.log")  
    trans = paramiko.Transport((ip, int(port)))  
    trans.connect(username=username, password=password)  
    sftp = paramiko.SFTPClient.from_transport(trans)  
    sftp.put(local_file_path, remote_file_path)  
    trans.close()  
  
  
def download_file(ip, port, username, password, local_file_path, remote_file_path):  
    """下载文件 
    """  
    print("开始下载")
    try:
        paramiko.util.log_to_file("/logs/paramiko.log")  
        trans = paramiko.Transport((ip, int(port)))  
        trans.connect(username=username, password=password)  
        sftp = paramiko.SFTPClient.from_transport(trans)  
        sftp.get(remote_file_path, local_file_path)
    except Exception as e:
        print (str(e))
        trans.close()  
  
def upload_dir(ip, port, username, password, local_dir, remote_dir):  
    """上传目录(从windows上传) 
        上传到remote_dir目录中(sftp无法一次创建多级目录，只能使用ssh command创建)
    """  
    paramiko.util.log_to_file("paramiko.log")  
    trans = paramiko.Transport((ip, int(port)))  
    trans.connect(username=username, password=password)  
    sftp = paramiko.SFTPClient.from_transport(trans)  
    try:  
        #sftp不能创建多级目录，如果需要创建则要使用ssh，执行command命令来创建mkdir -p
        sftp.mkdir(remote_dir)
    except Exception as e:  
        print("sftp.mkdir:\t"+str(e))
    for root, dirs, files in os.walk(local_dir):  
        for file_name in files:  
            print("file_name",file_name)
            print("root",root)
            print("dirs",dirs)
            local_file_path = os.path.join(root, file_name)
            print("local_file_path",local_file_path)
            remote_file_path = os.path.join(  
                remote_dir, local_file_path[3:])    # 切片：windows路径去掉盘符  
            print("remote_file_path1",remote_file_path)
            #remote_file_path = remote_file_path.replace("\\", "\\")
            #remote_file_path = remote_file_path.replace(" ", "_")
            remote_file_path =remote_file_path = os.path.join(remote_dir,remote_file_path.split("/")[-1])
            print("remote_file_path2",remote_file_path)
  
            try:  
                sftp.put(local_file_path, remote_file_path)  
            except Exception as e:  
                sftp.mkdir(os.path.dirname(remote_file_path))  
                sftp.put(local_file_path, remote_file_path)  
  
        for dir_name in dirs:  
            local_dir = os.path.join(root, dir_name)  
            remote_path = os.path.join(remote_dir, local_dir[3:])  
            remote_path = remote_path.replace("\\", "/")  
  
            try:  
                sftp.mkdir(os.path.dirname(remote_path))  
                sftp.mkdir(remote_path)  
            except Exception as e:  
                print("upload_dir:\t"+str(e))
    trans.close()  

if __name__ == '__main__':
    ip='192.168.153.135'
    port='22'
    username='root'
    password='root'
    
    local_dir='D:/Program Files/Python_Workspace/devpos_simple2.7/download_files/'
    dest_file=os.path.join(local_dir,'a.txt')
    #文件传入/soft/ELK/dir/目录中
    remote_dir='/soft/ELK/dir/'
    #download_file(ip,port,username,password,dest_file,remote_file)
    #upload_file(ip,port,username,password,dest_file,remote_file)
    upload_dir(ip,port,username,password,local_dir,remote_dir)