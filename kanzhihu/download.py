# -*- coding: utf-8 -*-

import re
import urllib2
import cPickle



class kanzhihu:

    def __init__(self): #定义初始参数
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64)'
        self.headers = {'User-Agent':self.user_agent}   #浏览器header信息
        self.page = 1
        self.listNum = 1

    def getContent(self,pageNumber): #导入页码获得页面代码
        url = 'http://www.kanzhihu.com/page/'+str(pageNumber)
        request = urllib2.Request(url,headers = self.headers)      #发出request请求并获取response
        response = urllib2.urlopen(request)
        content = response.read()    #读取response中的信息
        return content


    def getUrl(self,pageNumber):  #导入页码得到目录网址
        content = self.getContent(pageNumber)  #调用getUrl函数
        pattern = re.compile('<p class="post-date">Post on (.*?):00</p>.*?<a href="(.*?)" rel="bookmark" title="(.*?)">',re.S)
        #item[0]是日期，item[1]是目录网址，[2]是内容
        items = re.findall(pattern,content)   #使用pattern规则来查找符合要求的items
        return items


    def getAnswerUrl(self,pageNumber):   #导入页码获得目录内的答案网址
        while True:
            pageNumber =self.page
            items = self.getUrl(pageNumber)
            answerList = []
            print u"第%s页" %self.page
            for item in items:
                answerList = []
                answerUrl = item[1]
                itemTitle = item[2].replace(' ', '')
                itemDate = item[0].replace(' ', '_')

                answerRequest = urllib2.Request(answerUrl,headers = self.headers)      #发出request请求并获取response
                answerResponse = urllib2.urlopen(answerRequest)
                answerContent = answerResponse.read()
                answerPattern = re.compile('font-weight: bold;">(.*?)</a></h3>.*?<span class="readmore"><a href="(.*?)"',re.S)
                #answer[0]是答案标题，answer[1]是答案网址
                answers = re.findall(answerPattern,answerContent)
                print itemTitle.decode('utf-8')

                for answer in answers:
                    answerList.append(answer[1])

                num = str(self.listNum)
                listFile = 'E:/code/kanzhihu/cPinkle/'+num+'.text'

                f1 =file(listFile,'wb')
                cPickle.dump(answerList,f1,True)
                f1.close()
                f2 =file(listFile, "rb")
                urlList = cPickle.load(f2)
                for url in urlList:
                    print url
                print self.listNum
                self.listNum += 1
                
            self.page += 1


kzh = kanzhihu()
kzh.getAnswerUrl(1)






