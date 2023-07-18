# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import os
import sqlite3


class MongoDBPipeline:
    collection_name = 'transcripts'
    password = os.environ.get('MongoDB Pass')

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(f"mongodb+srv://avisheksaha123:{self.password}@cluster0.abfbmt5.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['Transcripts']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item
    
class SQLitePipeline:

    def open_spider(self, spider):
        # create database file
        self.connection = sqlite3.connect('transcripts.db')
        # we need a cursor object to execute SQL queries
        self.c = self.connection.cursor()
        #  try/except will help when running this for the +2nd time (we can't create the same table twice)
        try:
            # query: create table with columns
            self.c.execute('''
                CREATE TABLE transcripts(
                    title TEXT,
                    transcript TEXT,
                    url TEXT
                )
            ''')
            # save changes
            self.connection.commit()
        except sqlite3.OperationalError:
            pass


    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        # query: insert data into table
        self.c.execute('''
            INSERT INTO transcripts (title,transcript,url) VALUES(?,?,?)
        ''', (
            item.get('title'),
            item.get('transcript'),
            item.get('url'),
        ))
        # save changes
        self.connection.commit()
        return item
