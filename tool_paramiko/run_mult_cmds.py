# -*- coding: utf-8 -*-
'''
一次性执行多个linux命令
'''
import paramiko

from loggingclass import log


def python_ssh_command(ip, port, username, password,logfile='../logs/command.log',**shell):
    from loggingclass import log
    log=log(logfile)
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # 用于允许连接不在known_hosts名单中的主机
        ssh.connect(ip, port, username, password)
        result = {}
        for key in shell:
            try:
                stdin,stdout,stderr = ssh.exec_command(shell[key])
                channel = stdout.channel
                status = channel.recv_exit_status()
                print("status",status)
                if status==0:
                    print("已经连接到该主机%s:%s,%s:命令执行成功" %(ip,port,shell[key]))
                    #打印命令输出结果
                    #print (stdout.read().decode('utf-8'))
                else:
                    print("执行命令%s报错,请查看日志"% (shell[key]))
                    log.error(str(stderr.read()))
                    print (stderr.read().decode('utf-8'))
            except Exception as e:
                print (stderr.read().decode('utf-8'),log.error(str(e)))
            #stdin,stdout,stderr = ssh.exec_command(shell[key])
            #print("key",key)
            result[key] = stdout.read().decode('utf-8'),stderr.read().decode('utf-8')
        ssh.close()
        print("result",result,type(result))
        return result
    except Exception as e:
        result = u'无'
        print("异常",str(e))
        return result
#python_ssh_command('192.168.216.128', '22','root', 'root',a='cd /soft',b='ls -l',c='touch 1.log')

