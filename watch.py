#!/usr/bin/env python
# coding:UTF-8

import sys
from sp import SpLiveWatchWrapper

class NicoLiveWatcher(SpLiveWatchWrapper):
    def __init__(self):
        super(NicoLiveWatcher, self).__init__()

    def run(self):
        pass

def run():
    wather = NicoLiveWatcher()
    wather.spWatcher.all()
    for result in wather.spWatcher.all():
        from pprint import pprint
        pprint( result.to_dict() )

if __name__ == "__main__":
    run()
    
