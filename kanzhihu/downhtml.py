# -*- coding:utf-8 -*-
# IDE encding 和project encoding都是utf-8

import cPickle
import requests
import cookielib
try:
    from bs4 import BeautifulSoup
except:
    import BeautifulSoup


# 获取cookies
requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')
requests.cookies.load(ignore_discard=True)



class downHtml:

    def __init__(self): #定义初始参数
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64)'
        self.headers = {'User-Agent':self.user_agent}   #浏览器header信息
        self.listNum = 1
        self.EOFerror = 0
        self.connectError = 0
        self.errorList = []

    def loadList(self):
        while True:
            pageNum = self.listNum
            num = str(pageNum)

            errorFile = open('Error.txt','w')
            errorFile.write(num)


            list = 'E:/code/kanzhihu/cPinkle/'+num+'.text'
            listFile =file(list,'rb')
            list = []
            urlList = cPickle.load(listFile)
            listNum = len(urlList)

            print u'正在下载第%s页' %pageNum

            for url in urlList:
                try:
                    request = requests.get(url)
                    content = request.content
                    soup = BeautifulSoup(content,'lxml')
                    #将页面内容传入得到soup对象
                    title = soup.title.string.replace(' ','').replace('-知乎'.decode('utf-8'),'')
                    #以utf-8进行编码输出
                    fileName = 'E:/code/kanzhihu/test/'+title+'.html'
                    print fileName
                except:
                    print u"链接错误"
                    self.connectError +=1
                    print u"已有%s个链接错误" %self.connectError

                try:
                    urlFile = open(fileName,'w')
                    urlFile.write(content)
                    urlFile.close()
                    listNum = listNum-1
                    print listNum
                except:
                    listNum = listNum-1
                    self.EOFerror += 1
                    print u"这是EOF错误%s\n" %self.EOFerror


            self.listNum += 1


hg = downHtml()
hg.loadList()

