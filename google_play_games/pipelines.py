# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from cmath import e
from itemadapter import ItemAdapter
import psycopg2
import pymongo


class GooglePlayGamesPipeline:
    def __init__(self):
        # self.conn = psycopg2.connect(database='test_database', user='postgres', password='binshao123', host='127.0.0.1', port='5432')
        self.conn = psycopg2.connect(database='google_play', user='postgres', password='binshao123', host='127.0.0.1', port='5432')
        self.cur = self.conn.cursor()
        print('connect success')

    def process_item(self, item, spider):
        print(item)
        try:
            # insert_sql = 'insert into test_table (name, genre, rating_value) values (%s, %s, %s)' % (str(item['name']), str(item['genre']), str(item['rating_value']))
            # self.cur.execute(insert_sql)
            # self.cur.execute('insert into test_table (name, genre, rating_value) values (%s, %s, %s)', (item['name'], item['genre'], item['rating_value']))
            self.cur.execute('insert into google_play_games (name, author, star_rating, download_times, content_rating, introduction, update_time, genre, url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (item['name'], item['author'], item['star_rating'], item['download_times'], item['content_rating'], item['introduction'], item['update_time'], item['genre'], item['url']))
            self.conn.commit()
            print('success')
        except Exception as e:
            print(e)
            self.conn.rollback()
            print("failed")
        # finally:
        #     if self.conn:
        #         self.cur.close()
        #         self.conn.close()

class GooglePlayGamesPipeline_mongodb:
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['test_database']
        self.post = self.db['test_collection']

    def process_item(self, item, spider):
        game = dict(item)
        self.post.insert_one(game)
        return item

        
        
