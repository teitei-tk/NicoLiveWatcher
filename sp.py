# coding:UTF-8
from app import app
from lib import (ScraapingBase, Mongo, LiveScrapingObject)

class SpLiveWatchWrapper(object):
    def __init__(self):
        self.spDb      = AnimeSpWatch()
        self.spWatcher = NicoAnimeSpLiveWatcher()

    def getSpData(self, key):
        return self.spDb.get(key)

    def getAllSpData(self):
        return self.spDb.all()

    def updateSpData(self):
        watchList = self.spWatcher.all()
        for watch in watchList:
            self.spDb.update(watch.to_dict())

class AnimeSpWatch(Mongo):
    colname = "sp_lives"

    def __init__(self):
        self.db = app.db

    def get(self, key):
        return self.db.findOne(self.colname, {'vid' : key})

    def all(self):
        return self.db.findAll( self.colname ) 

    def update(self, data):
        self.db.insert(self.colname, data)

class NicoAnimeSpLiveWatcher(ScraapingBase):
    url = 'http://ch.nicovideo.jp/anime-sp'

    def all(self):
        return self.getLiveAnimeObjects()

    def getLiveAnimeObjects(self):
        siteData = self.siteDecode(self.url)
        pageHtml = siteData['data'].decode(siteData['encoding'])

        bs = self.getBeautifulSoupObject(pageHtml)
        if bs is None:
            return None
        liveDatas = self.scrapingNicoLiveAnimeData(bs)
        return liveDatas
    
    def scrapingNicoLiveAnimeData(self, html):
        import datetime
        liveAnimeDataList = []
        for animeData in html.body.find('div', {'class' : 'p-live_list'}).findAll('form'):
            vidObj = animeData.find('input', {'name' : 'vid'})
            if vidObj.has_key('value'):
                vid = vidObj['value']

            titleObj = animeData.find('input', {'name' : 'title'})
            if titleObj.has_key('value'):
                title = titleObj['value']

            openTimeObj = animeData.find('input', {'name' : 'open_time'})
            if openTimeObj.has_key('value'):
                value = int(openTimeObj['value'])
                openTime = datetime.datetime.fromtimestamp(value)

            startTimeObj = animeData.find('input', {'name' : 'start_time'})
            if startTimeObj.has_key('value'):
                value = int(startTimeObj['value'])
                startTime = datetime.datetime.fromtimestamp(value)

            endTimeObj = animeData.find('input', {'name' : 'end_time'})
            if endTimeObj.has_key('value'):
                value = int(endTimeObj['value'])
                endTime = datetime.datetime.fromtimestamp(value)

            data = dict(
                vid   = vid,
                title = title,
                openDatetime = openTime,
                startDatetime = startTime,
                endDatetime = endTime,
                )
            obj = LiveScrapingObject(data)
            if obj is None:
                continue
            liveAnimeDataList += [obj]
        return liveAnimeDataList
