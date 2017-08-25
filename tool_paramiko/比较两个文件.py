'''
Created on 2017年7月24日

@author: ning.lin
'''
#coding:utf-8
import codecs
import difflib
import sys





def readfile(filename):
    try:
        with codecs.open(filename,"r",encoding="utf-8") as f:#以utf-8的编码打开文件，原文件也是utf-8类型的
            text=f.readlines()
            #print(text)
            return text
    except IOError as error:
       print('Read file Error:'+str(error))
       sys.exit()


    
    
#保存两个文件的比较结果
def save_tempHtml(html):
    with codecs.open('diff.html', 'wb', 'utf-8') as f:
        f.write(html)

#计算字符串出现的次数
def conut_str(string):
    count=0
    with codecs.open(tempfile,"r",encoding="utf-8") as f:
        lines = f.readlines() 
        for line in lines:
            if string in line:
                count += 1
        print("要替换的字符串%s\t出现%s次" % (string,count))
        
#替换文件中的字符串
def replace_tempHtml(oldstr,newstr):
    count=0
    with codecs.open(tempfile,"r",encoding="utf-8") as f:
        lines = f.readlines() 
    with codecs.open(tempfile,"w",encoding="utf-8") as f_w:
        for line in lines:
            if oldstr in line:
                count += 1
                #替换
                line = line.replace(oldstr,newstr)
                #line = line.replace('''content=\"text/html; charset=ISO-8859-1"''','''content="text/html; charset=UTF-8"''')
            f_w.write(line)

def compare_two_files(textfile1,textfile2):
    text1_lines = readfile(textfile1) 
    text2_lines = readfile(textfile2)
    if textfile1=="" or textfile2=="":
        print ("有文件不存在")
    #输出html格式
    d = difflib.HtmlDiff()
    html=d.make_file(text1_lines, text2_lines)
    
    #直接输出结果
    d2 = difflib.Differ()
    diff = d2.compare(text1_lines, text2_lines)
    compare_line='\n'.join(list(diff))
    #print(compare_line)
    print ('type(html)')
    #保存到html文件中
    save_tempHtml(html)
    #替换文件中的charset=ISO-8859-1为charset=UTF-8
    
    replace_tempHtml(''' content=\"text/html; charset=ISO-8859-1"''','''content="text/html; charset=UTF-8"''')
    conut_str('''td''')
if __name__=='__main__':
    tempfile='diff.html'
    textfile1='D:\\Program Files\\Python_Workspace\\devpos_simple\\a.txt'
    textfile2='D:\\Program Files\\Python_Workspace\\devpos_simple\\b.txt'
    compare_two_files(textfile1,textfile2)
