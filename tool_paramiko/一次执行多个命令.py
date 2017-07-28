# -*- coding: utf-8 -*-
import paramiko

def python_ssh(hostname,username,password,**shell):
    try:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # 用于允许连接不在known_hosts名单中的主机
        s.connect(hostname = hostname,username = username,password = password)
        result = {}
        for key in shell:
            stdin,stdout,stderr = s.exec_command(shell[key])
            print("key",key)
            result[key] = stdout.read().decode('utf-8'),stderr.read().decode('utf-8')
        s.close()
        return result
    except Exception as e:
        result = u'无'
        print("异常",str(e))
        return result
#python_ssh('192.168.153.135', 'root', 'root',a='cd /soft',b='ls -l',c='touch 1.log')
print(python_ssh('192.168.153.135', 'root', 'root',shell1='cd /soft',shell2='ls -al',shell3='mkdir 1.log'))