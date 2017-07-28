
# -*- coding:utf8 -*-
'''
Created on 2017年7月20日

@author: ning.lin
'''
from os import path
import os

import paramiko
from _stat import S_ISDIR
from loggingclass import log
log_file=os.path.join('./file_err.log')
log=log(log_file)


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
        #paramiko.util.log_to_file("/logs/paramiko.log")  
        trans = paramiko.Transport((ip, int(port)))  
        trans.connect(username=username, password=password)  
        sftp = paramiko.SFTPClient.from_transport(trans)  
        sftp.get(remote_file_path, local_file_path)
    except Exception as e:
        print (str(e))
        trans.close()  
#下载一个目录中的所有文件        
def download_dir(ip, port, username, password, local_dir, remote_dir):  
    """下载远程服务器的目录中所有文件 
    """  
    print("log_file",log_file)
    print("开始下载")
    try:
        #paramiko.util.log_to_file("/logs/paramiko.log")  
        trans = paramiko.Transport((ip, int(port)))  
        trans.connect(username=username, password=password)  
        sftp = paramiko.SFTPClient.from_transport(trans)
        try:
            print(__get_all_files_in_remote_dir(sftp, remote_dir))
                        #print("sss",os.path.join(remote_dir,file))
                    #print("dirs",dirs)
                    #print("root",files)
        except Exception as e:
            print("files err",log.error(str(e)))
#             for f in files:
#                 print ('Downloading file:',os.path.join(remote_dir,f))
            #sftp.get(os.path.join(remote_dir,f),os.path.join(local_dir,f))    
    except Exception as e:
        print (log.error(str(e)))
        trans.close() 
#获取目录下所有的文件及目录
def catch_dir_file(path):
    dirs = os.path.dirname(path)
    for dir in os.listdir(dirs):                             # 遍历当前目录所有问价和目录
        child = os.path.join('.', dir)                    # 加上路径，否则找不到
        print("child",child)
        if os.path.isdir(child):                            # 如果是目录，则继续遍历子目录的文件
            for file in os.listdir(child):                    
                if os.path.splitext(file)[1] == '.meta':    # 分割文件名和文件扩展名，并且扩展名为'meta'        
                    file = os.path.join(child, file)        # 同样要加上路径
                    f = open(file, 'r')
                    guid = f.readlines()[1].split(': ')[1]  # 获取文件第二行以': '分割的后者
                    #outfile.write(guid)                     # 写入输出文件
                    f.close()                        
        elif os.path.isfile(child):                         # 如果是文件，则直接判断扩展名
            if os.path.splitext(child)[1] == '.meta':
                f = open(child, 'r')
                guid = f.readlines()[1].split(': ')[1]
                #outfile.write(guid)
                f.close()
# ------获取远端linux主机上指定目录及其子目录下的所有文件------
def __get_all_files_in_remote_dir(sftp, remote_dir):
    # 保存所有文件的列表
    all_files = list()
    # 去掉路径字符串最后的字符'/'，如果有的话
    if remote_dir[-1] == '/':
        remote_dir = remote_dir[0:-1]
    # 获取当前指定目录下的所有目录及文件，包含属性值
    files = sftp.listdir_attr(remote_dir)
    for file in files:
        # remote_dir目录中每一个文件或目录的完整路径
        filename = remote_dir + '/' + file.filename
        # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
        if S_ISDIR(file.st_mode):
            all_files.extend(__get_all_files_in_remote_dir(sftp, filename))
        else:
            all_files.append(filename)
    return all_files
#在当前目录下创建子目录
def mkdir_path(dir):
    #判断是否是个目录
    if os.path.isdir(dir):
         #判断目录是否存在
        if not os.path.exists(dir): 
            try:
                os.mkdir(dir)
            except Exception as e:
                print (log.error(str(e)))
        else:
            print("%s已存在该目录" % dir)
    else:
        print("s%这不是一个目录" % dir)
     
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
#             print("file_name",file_name)
#             print("root",root)
#             print("dirs",dirs)
            local_file_path = os.path.join(root, file_name)
            #print("local_file_path",local_file_path)
            remote_file_path = os.path.join(  
                remote_dir, local_file_path[3:])    # 切片：windows路径去掉盘符  
            #print("remote_file_path1",remote_file_path)
            #remote_file_path = remote_file_path.replace("\\", "\\")
            #remote_file_path = remote_file_path.replace(" ", "_")
            remote_file_path =remote_file_path = os.path.join(remote_dir,remote_file_path.split("/")[-1])
            #print("remote_file_path2",remote_file_path)
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
    
    local_dir='D:/Program Files/Python_Workspace/devpos_simple/download_files/'
    dest_file=os.path.join(local_dir,'a.txt')
    #文件传入/soft/ELK/dir/目录中
    remote_dir='/soft/ELK/dir/'
    remote_file='/soft/ELK/dir/OMS数据库sql.txt'
    #download_file(ip,port,username,password,dest_file,remote_file)
    #download_file(ip, port, username, password, dest_file, remote_file)
    #upload_dir(ip,port,username,password,local_dir,remote_dir)
    download_dir(ip, port, username, password, local_dir, remote_dir)
