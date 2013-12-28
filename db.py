# coding:UTF-8

from pymongo import MongoClient

class mongo:
    db = None

    def __init__(self, host, dbName, port=27017):
        self.connect(host, dbName, port)

    def connect(self, host, dbname, port=27017):
        client = MongoClient( host, port )
        self.db = client[dbname]

    def find( self, collectionName, findType = 'findAll', key={}):
        return self[findType]( collectionName, key=key )

    def findAll( self, collectionName, key={} ):
        return self.db[collectionName].find( key )

    def insert( self, collectionName, key ):
        return self.db[collectionName].insert( key )
