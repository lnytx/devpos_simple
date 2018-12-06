'''
Created on 2017年8月10日

@author: ning.lin
'''


from 一次执行多个命令 import python_ssh_command


ip='192.168.216.128'
port=22
username='root'
password='root'
def get_info():
    list=[]
    result=python_ssh_command(ip,port,username,password,
                              disk='fdisk -l | grep Disk',mem='cat /proc/meminfo | grep MemTotal',
                              Product='dmidecode | grep "Product Name"',)
    for i in result['disk']:
       list=i.split('\n')
       if len(list)>1:
           print("硬盘容量",list[0])
    for i in result['mem']:
       list=i.split('\n')
       if len(list)>1:
           print("内存大小",list[0])
    for i in result['Product']:
       list=i.split('\n')
       if len(list)>1:
           print("Product",list[0])
if __name__ == '__main__':
    get_info()
