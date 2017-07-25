#远程服务器  
import paramiko

from loggingclass import log


ip = '192.168.153.135'
port = 22
username = 'root'  
password = 'root'  

logfile='D:\\Program Files\\Python_Workspace\\devpos_simple\\logs\\ssh_loggin.log'
log=log(logfile)

def ssh_login():

    #创建SSH连接日志文件（只保留前一次连接的详细日志，以前的日志会自动被覆盖）  
    paramiko.util.log_to_file('syslog')  
    s = paramiko.SSHClient()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    #读取know_host  
    s.load_system_host_keys()  
    #建立SSH连接  
    s.connect(ip,port,username,password,allow_agent=False,look_for_keys=False,timeout=5)  
    stdin,stdout,stderr = s.exec_command('df -h',timeout=5)
    #打印标准输出  
    print (stdout.read().decode('utf-8'))
    s.close()
    
def ssh_connect(ip,port,command):
    try:
        ssh = paramiko.SSHClient()  
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
        ssh.connect(ip, port,username, password,timeout=5)
        try:
            stdin,stdout,stderr = ssh.exec_command(command)
            channel = stdout.channel
            status = channel.recv_exit_status()
            if status==0:
                print (stdout.read().decode('utf-8'))
            else:
                log.error(str(stderr.read()))
                print (stderr.read().decode('utf-8'))
        except Exception as e:
            print (stderr.read().decode('utf-8'))
    except Exception as e:
        print ("stderr",log.error(str(e)))
        #有异常就一直去调用
        #ssh_connect()
        
    
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
if __name__=='__main__':
    ssh_connect(ip,port,'ssa')