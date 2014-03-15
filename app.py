# coding:UTF-8
from lib import ( Mongo, )
from config import ( DB_HOST, DB_NAME, )

class Nico(object):
    def __init__(self):
        self.db = Mongo( DB_HOST, DB_NAME )
app = Nico()
