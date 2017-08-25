'''
Created on 2017年8月3日

@author: ning.lin
'''
import requests
import threading

class downloader:
    def __init__(self,url,process_number=8):
        self.url= url
        self.process_number=process_number
        self.name=self.url.split('/')[-1]
        r = requests.head(self.url)
        self.total = int(r.headers['Content-Length'])
        print ('total is %s' % (self.total))
        print("name",self.name)
    def get_range(self):
        ranges=[]
        offset = int(self.total/self.process_number)
        for i in  range(self.process_number):
            if i==self.process_number-1:
                ranges.append((i*offset,''))
            else:
                ranges.append((i*offset,(i+1)*offset))
        return ranges
    def download(self,start,end):
        headers={'Range':'Bytes=%s-%s' % (start,end),'Accept-Encoding':'*'}
        res = requests.get(self.url,headers=headers)
        print ('%s:%s download success'%(start,end))
        self.fd.seek(start)
        self.fd.write(res.content)
        #self.fd.write(res.text)
        print("res.content",type(res.content))
    def run(self):
        self.fd =  open(self.name,'wb')
        thread_list = []
        n = 0
        for ran in self.get_range():
            start,end = ran
            print ('thread %d start:%s,end:%s'%(n,start,end))
            n+=1
            thread = threading.Thread(target=self.download,args=(start,end))
            thread.start()
            thread_list.append(thread)
        for i in thread_list:
            i.join()
        print ('download %s load success'%(self.name))
        self.fd.close()
if __name__=='__main__':
    down = downloader('http://images.cnitblog.com/blog/407700/201505/041320268929440.png',6)
    down.run()