# coding:UTF-8
import unittest, random
from pymongo import MongoClient

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from app import ( app, )
from lib import ( Mongo, )
from nico import NicoLiveWatcher

class TestWatcher(unittest.TestCase):
    def setUp(self):
        app.db = Mongo('localhost', 'test_db')
        self.initialize()

    def initialize(self):
        self.wather = NicoLiveWatcher()
        self.wather.updateSpData()

    def tearDown(self):
        client = MongoClient('localhost')
        client.drop_database('test_db')
        pass

    def testWatch(self):
        assert self.wather.getAllSpData()
