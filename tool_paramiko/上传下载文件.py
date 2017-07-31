
# -*- coding:utf8 -*-
'''
Created on 2017年7月20日

@author: ning.lin
'''
from _stat import S_ISDIR
from os import path
import os

import paramiko

from loggingclass import log
from tool_paramiko.ssh_login import return_paramiko_connect, \
    return_ssh_connect


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
            print(get_all_files_in_remote_dir(sftp, remote_dir))
            list_files=get_all_files_in_remote_dir(sftp, remote_dir)
            print("list_files",list_files)
            for file in list_files:
                #print("DIR",)
                #print("local_dir",local_dir)
                dir = os.path.dirname(file)
                #print("tempdir",dir)
                #如果本地路径最后一个不是/刚加上/
                if local_dir[-1] == '/':
                    local_dir = local_dir[:-1]
                #print("local_dir",local_dir)
                full_path = local_dir + dir + '/'
                #本地对应的文件
                full_file=local_dir + file
                #print("full_file",full_file)
                #远程机器上的文件
                #print("file",file)
                if not os.path.isdir(full_path):
                    try:
                        os.makedirs(full_path)
                        #print("assss",os.path.split(path)[0])
                        print("目录创建成功",full_path)
                    except Exception as err:
                        print("创建目录时报错",str(err),log.error(str(err)))
                else:
                    print("已创建")
                sftp.get(file,full_file)
        except Exception as e:
            print("files err",log.error(str(e)))
#             for f in files:
#                 print ('Downloading file:',os.path.join(remote_dir,f))
            #sftp.get(os.path.join(remote_dir,f),os.path.join(local_dir,f))    
    except Exception as e:
        print (log.error(str(e)))
        trans.close() 

# ------获取远端linux主机上指定目录及其子目录下的所有文件------
def get_all_files_in_remote_dir(sftp, remote_dir):
    #sftp='local'或者remote来区分本地或远程目录
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
            all_files.extend(get_all_files_in_remote_dir(sftp, filename))
        else:
            all_files.append(filename)
    return all_files
#获取本机目录中的所有文件
def get_all_files_in_local_dir(local_dir):
    # 保存所有文件的列表
    all_files = list()
    # 去掉路径字符串最后的字符'/'，如果有的话
    if local_dir[-1] == '/':
        local_dir = local_dir[0:-1]
    if os.path.exists(local_dir):
        files = os.listdir(local_dir)
        for file in files:
            # remote_dir目录中每一个文件或目录的完整路径
            filename = os.path.join(local_dir, file)
            filename = filename.replace("\\", "/")
            # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
            if os.path.isdir(filename):
                all_files.extend(get_all_files_in_local_dir(filename))
            else:
                all_files.append(filename)
    else:
        print("local_dir不存在 ")
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

#上传单个目录    
def upload_single_dir(ip, port, username, password, local_dir, remote_dir):  
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
    
#上传多个目录，包括子目录
def upload_manay_dir(ip, port, username, password, local_dir, remote_dir):  
    """上传多个目录目录(从windows上传) 
        上传到remote_dir目录中(使用ssh command创建多个目录)
    """  
    sftp=return_paramiko_connect(ip, port, username, password)
    ssh=return_ssh_connect(ip, port, username, password)
    
    if remote_dir[-1] != '/':
        remote_dir = remote_dir+'/'
    all_files = get_all_files_in_local_dir(local_dir)
    for x in all_files:
        #os.path.split(x)[-1]取得是文件的名称
        filename = os.path.split(x)[-1]
        #下面的是将远程目录替换掉本地的目录os.path.split(x)[0]取得是文件的目录
        remote_file = os.path.split(x)[0].replace(local_dir, remote_dir)
        path = remote_file.replace('\\', '/')
        print(path.index(remote_dir))
        print("path",path[(path.index('soft'))+len(remote_dir)-2:])
        path = path[(path.index('soft'))+len(remote_dir)-2:]
        print("path",path)
        
        # 创建目录 sftp的mkdir也可以，但是不能创建多级目录所以改用ssh创建。
        try:
            stdin,stdout,stderr = ssh.exec_command('mkdir -p ' + path)
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
            print (stderr.read().decode('utf-8'),log(str(e)))
            
        remote_filename = path + '/' + filename
        print ('Put files...' + filename)
        print ('remote_filename...' + remote_filename)
        print("x",x)
        #上传文件
        try:
            sftp.put(x, remote_filename)
        except Exception as e:
            print (log(str(e)))
    sftp.close()

if __name__ == '__main__':
    ip='192.168.153.135'
    port='22'
    username='root'
    password='root'
    temp_ini='./for_fail_con.ini'
    local_dir='D:/Program Files/Python_Workspace/devpos_simple/download_files/'
    up_local_dir='D:/Program Files/Python_Workspace/devpos_simple/download_files/soft/ELK/dir/'
    dest_file=os.path.join(local_dir,'a.txt')
    #文件传入/soft/ELK/dir/目录中
    remote_dir='/soft'
    remote_file='/soft/ELK/dir/OMS数据库sql.txt'
    #download_file(ip,port,username,password,dest_file,remote_file)
    #download_file(ip, port, username, password, dest_file, remote_file)
    #upload_single_dir(ip,port,username,password,local_dir,remote_dir)
    #download_dir(ip, port, username, password, local_dir, remote_dir)
    upload_manay_dir(ip, port, username, password, local_dir, remote_dir)
    #get_all_files_in_local_dir(local_dir)
    print(up_local_dir.index('soft'))
    #print(up_local_dir[62:])
