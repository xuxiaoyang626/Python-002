# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

dbInfo = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'Xiaowuxiong626.',
    'db' : 'db_maoyan'
}

class MaoyanmoviePipeline:        
    def process_item(self, item, spider):
        print('Processing item')
        conn = pymysql.connect(
            host = dbInfo['host'],
            port = dbInfo['port'],
            user = dbInfo['user'],
            password = dbInfo['password'],
            db = dbInfo['db']
        )

        print('Successfilly connected to DB')

        title = item['title']
        date = item['date']
        genre = item['genre']
        sql = 'INSERT INTO `MOVIES` (`TITLE`,`DATE`,`GENRE`) VALUES (%s, %s, %s)'

        cur = conn.cursor()
        try:
            cur.execute(sql, (title, date, genre))
            cur.close()
            conn.commit()
            print('Successfilly intsert item to DB')
        except Exception as e:
            print(e)
            conn.rollback()
        conn.close()

        return item
