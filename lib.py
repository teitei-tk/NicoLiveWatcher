# coding:UTF-8
from pymongo import MongoClient

class ScraapingBase:
    url = None
    ua = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'

    @property
    def watchUserAgent(self):
        return self.ua

    def sitesDecode( self, urls ):
        siteDect = []
        for url in urls:
            result = self.siteDecode( url )
            siteDect.append(result)

        return siteDect

    def siteDecode( self, url ):
        import urllib2
        import chardet
        request = urllib2.Request(url)
        request.add_header('User-agent', self.watchUserAgent)

        data = ''.join( urllib2.urlopen(request).read() )
        guess = chardet.detect( data )
        result = dict(url=url,data=data,**guess)

        return result

    def getBeautifulSoupObject( self, html ):
        from bs4 import BeautifulSoup
        return BeautifulSoup( html )


class Mongo:
    db = None

    def __init__(self, host, dbName, port=27017):
        self.connect(host, dbName, port)

    def connect(self, host, dbname, port=27017):
        client = MongoClient( host, port )
        self.db = client[dbname]

    def find(self, collectionName, findType = 'findAll', key={}):
        return self[findType](collectionName, key=key)

    def findOne(self, collectionName, key={}):
        return self.db[collectionName].find(key).limit(1)

    def findAll(self, collectionName, key={}):
        return self.db[collectionName].find(key)

    def insert(self, collectionName, key):
        return self.db[collectionName].insert(key)


class LiveScrapingObject(object):
    def __init__(self, data):
        if data is None:
            return None
        self.vid            = data.get('vid') or ''
        self.title          = data.get('title') or ''
        self.openDatetime   = data.get('openDatetime') or ''
        self.startDatetime  = data.get('startDatetime') or ''
        self.endDatetime    = data.get('endDatetime') or ''

        self.__validation()

    def to_dict(self):
        return {
            'vid'           :   self.vid,
            'title'         :   self.title,
            'openDatetime'  :   self.openDatetime,
            'startDatetime' :   self.startDatetime,
            'endDatetime'   :   self.endDatetime,
            }

    def __validation(self):
        pass


