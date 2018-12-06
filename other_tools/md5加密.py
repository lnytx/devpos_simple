def md5(str1):
    import hashlib  
    if isinstance(str1,str):
        #encode(encoding='gb2312')
        m = hashlib.md5(str1.encode('UTF-8')) 
        md5value=m.hexdigest()
        return md5value
print(md5('我是'))
