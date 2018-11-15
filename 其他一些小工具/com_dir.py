#-*- coding:utf-8 –*-
'''
解压两个war包，并将差异文件提取出来，实现war包的增量更新
'''

import filecmp
import os
import shutil
import time
from asyncio.tasks import sleep


holderlist=[]
def compare_dir(leftDir,rightDir):
    #目录比较 忽略test.py
#     dirObj = filecmp.dircmp(leftDir, rightDir, ['test.py'])
    pathDir =  os.listdir(leftDir)
    dirObj = filecmp.dircmp(leftDir, rightDir)
    only_in_one = dirObj.left_only#只在左边文件夹中存在的文件或文件夹；
    diff_in_one = dirObj.diff_files#获取差异文件
#     dirpath = os.path.abspath(leftDir)#

    [holderlist.append(os.path.abspath(os.path.join(leftDir,x))) for x in only_in_one]
    [ holderlist.append(os.path.abspath(os.path.join(leftDir,x))) for x in diff_in_one ]
    if len(dirObj.common_dirs) > 0:  #判断是否存在相同子目录，以便递归,两边文件夹都存在的子文件夹；
        for item in dirObj.common_dirs:   #递归子目录
            compare_dir(os.path.abspath(os.path.join(leftDir,item)),os.path.abspath(os.path.join(rightDir,item)))
    return holderlist


def unzip_war(war):
    '''
    解压tar包到当前目录的当前名称
    '''
    (filepath,tempfilename) = os.path.split(war)
    (filename,extension) = os.path.splitext(tempfilename)
    tar_dest=os.path.join(filepath,filename)
    if not os.path.exists(tar_dest):
        os.makedirs(tar_dest)
    ar_command = 'tar -zxvf %s -C %s' % (war,tar_dest)
    print("开始解压")
    start=time.time()
    os.system(ar_command)
    end=time.time()
    print("解压时长",end-start)
    time.sleep(2)
    return tar_dest

if __name__=='__main__':
    new='E:\\java\\hb_web_wsbsdt1.war'#第二次打包后的文件
    old='E:\\java\\hb_web_wsbsdt.war'#第一次打包后的文件
    res_dir='E:\\java\\last'#保留差异文件的目录
    
    new_dir=unzip_war(new)
    old_dir=unzip_war(old)
    start=time.time()
    holderlist=compare_dir(new_dir,old_dir)#后打的新包在为new,之前打的旧包为old
    end=time.time()
    print("获取差异文件时间",end-start)
    time.sleep(2)
    for i in holderlist:
        tar_dest=i.replace(new_dir,res_dir)#
        des_dir=os.path.dirname(tar_dest)
        if os.path.isdir(i):
            if not os.path.exists(des_dir):
                os.makedirs(des_dir)
            else:
                shutil.rmtree(des_dir)
            shutil.copytree(i,tar_dest)
        else:
            if not os.path.exists(des_dir):
                os.makedirs(des_dir)
            shutil.copyfile(i,tar_dest)
     
