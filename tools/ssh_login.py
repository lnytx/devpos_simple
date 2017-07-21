#远程服务器  
import paramiko



hostname = '192.168.153.135'
port = 22
username = 'root'  
password = 'root'  
def ssh_login():

    #创建SSH连接日志文件（只保留前一次连接的详细日志，以前的日志会自动被覆盖）  
    paramiko.util.log_to_file('syslog')  
    s = paramiko.SSHClient()  
    #读取know_host  
    s.load_system_host_keys()  
    #建立SSH连接  
    s.connect(hostname,port,username,password,allow_agent=False,look_for_keys=False,timeout=5)  
    stdin,stdout,stderr = s.exec_command('top',timeout=5)  
    #打印标准输出  
    print (stdout.read())
    s.close()
    
def ssh_connect():  
    ssh = paramiko.SSHClient()  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    ssh.connect(hostname, port,username, password,timeout=5)
    try:
        stdin,stdout,stderr = ssh.exec_command('top -n 1')
        #print (stdout.read()) 
        channel = stdout.channel
        status = channel.recv_exit_status()
        print ("status",status)
        print("top",stdout.read())
        print ("stdout",str(stdout.read(),"utf-8"))
        text=str(stdout.read(),"utf-8")
    except Exception as e:
        print(str(e))
        print ("stderr",stderr.read(),str(e))
    #return ssh  
    
def chan_connect():
    #设置ssh连接的远程主机地址和端口
    t=paramiko.Transport((hostname,port))
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
    chan.send('pwd')
    str1=str(chan.recv(65535),'utf-8')
    print(str1)
if __name__=='__main__':
    chan_connect()