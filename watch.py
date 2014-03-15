#!/usr/bin/env python
# coding:UTF-8

import sys
from nico import NicoLiveWatcher

def run():
    wather = NicoLiveWatcher()
    wather.updateSpData()

if __name__ == "__main__":
    run()
    
