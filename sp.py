# coding:UTF-8
from lib import (ScraapingBase, Mongo, LiveScrapingObject)

class SpLiveWatchWrapper(object):
    def __init__(self):
        self.spWatch = AnimeSpWatch()
        self.spWatcher = NicoAnimeSpLiveWatcher()

class AnimeSpWatch(Mongo):
    colname = "sp_lives"

    def __init__(self):
        from config import (DB_HOST, DB_NAME)
        self.db = Mongo(DB_HOST, DB_NAME)

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
        liveAnimeDataList = []
        liveAnimeList = html.body.find('div', {'class' : 'p-live_list'})

        # title取得
        for animeData in liveAnimeList.findAll('div', {'class' : 'g-live-title g-live-hq'}):
            title = animeData.find('a').string.strip()
            data = dict(liveTitle = title)
            liveAnimeDataList.append(data)

        liveDatas = []
        for index, data in enumerate(
                liveAnimeList.findAll('p', {'class' : 'g-live-airtime reserved'})):
            # 不要なデータを掃除
            data.find('span', {'class' : 'p-status_lamp'}).extract()

            openDay = data.find('strong').string
            data.find('strong').extract()

            openTime = data.get_text().strip().rstrip(' -').replace(u'\xa0', u' ')
            if index >= len(liveAnimeDataList):
                break

            datetime = dict(time = openTime, day = openDay)
            liveAnimeData = liveAnimeDataList[index] 
            liveData = dict(
                title        = liveAnimeData.get('liveTitle'),
                openDatetime = datetime
                )
            
            obj = LiveScrapingObject(liveData)
            if obj is None:
                continue
            liveDatas += [obj]
        return liveDatas
