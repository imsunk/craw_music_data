#!/home/ubuntu/anaconda2/bin/python
import MySQLdb
class DBConnect():
    def __iniit__(self,host,user,passwd):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = MySQLdb.connect(host,user,passwd)

    def getConnection(self):
        if self.db==None:
            self.db = MySQLdb.connect(host,user,passwd)
        return self.db

    def query():




