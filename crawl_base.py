#!/home/ubuntu/anaconda2/bin/python

from abc import * 
import configparser
import db

class CrawBase():
    def __init__(self):
        self.dbHost = self.config["DB"]["DB_HOST"]
        self.dbHost = self.config["DB"]["DB_HOST"]

    ### 실제 crawl 함수. 
    @abstractmethod
    def crawlData(self, **kwargs):

    def parsingDoc()
    ### 파라메터 추가 필요시에 호출할 수 있도록
    def addParams()
    #### 차후 DB에서 불러서 쓸 수 있도록
    def getTargetSiteInfo(self,siteName):

    def loadConf(self):
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')
        
     main():

