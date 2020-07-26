# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MaoyanmoviePipeline:
    def process_item(self, item, spider):
        title = item['title']
        date = item['date']
        genre = item['genre']
        output = f'|{title}|\t|{date}|\t|{genre}|\n\n'
        with open('./doubanmovie.txt', 'a+', encoding='utf-8') as article:
            article.write(output)
        return item

