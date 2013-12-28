#!/usr/bin/env python
# coding:UTF-8

import sys
import urllib2
import chardet
from db import mongo

class ScraapingBase:
    @property
    def watchUserAgent(self):
        ua = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
        return ua

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

class NicoAnimeSpLiveWatcher(object):
    pass
