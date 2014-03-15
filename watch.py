#!/usr/bin/env python
# coding:UTF-8

import sys
from nico import NicoLiveWatcher

def run():
    wather = NicoLiveWatcher()
    wather.update_sp_data()

if __name__ == "__main__":
    run()
    
