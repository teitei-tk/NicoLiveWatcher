#!/usr/bin/env python
# coding:UTF-8

import sys
import urllib2
import chardet
from db import mongo

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
        request = urllib2.Request(url)
        request.add_header('User-agent', self.watchUserAgent)

        data = ''.join( urllib2.urlopen(request).read() )
        guess = chardet.detect( data )
        result = dict(url=url,data=data,**guess)

        return result

    def getBeautifulSoupObject( self, html ):
        from bs4 import BeautifulSoup
        return BeautifulSoup( html )


class LiveScrapingObject(object):
    def __init__(self, data):
        if data is None:
            return None
        self.title          = data.get('title') or ''
        self.openDatetime   = data.get('openDatetime') or ''

        self.__validation()

    def to_dict(self):
        return {
            'title'         :   self.title,
            'openDatetime'  :   self.openDatetime
            }

    def __validation(self):
        pass


class NicoAnimeSpLiveWatcher(ScraapingBase):
    url = 'http://ch.nicovideo.jp/anime-sp'

    def getNicoLiveAnimeData(self):
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

def run():
    wather = NicoAnimeSpLiveWatcher()
    results = wather.getNicoLiveAnimeData()

    from pprint import pprint
    for result in results:
        pprint(result.to_dict())

if __name__ == "__main__":
    run()
    
