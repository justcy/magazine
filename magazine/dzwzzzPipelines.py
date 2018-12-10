import pymysql
import redis

from scrapy.conf import settings
class MagazinePipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host=settings['MYSQL_HOST'],user=settings['MYSQL_USER'],passwd=settings['MYSQL_PASSWORD'],db =settings['MYSQL_DATABASE'])
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        magazine_id = item['magazine_id']
        book_name = item['book_name'].strip()
        book_cover = item['book_cover']
        book_year = item['book_year']
        book_sno = item['book_sno']
        book_url = item['book_url']
        book_url_md5 = item['book_url_md5']
        sql ="insert into mg_book(magazine_id,book_name,book_cover,book_year,book_sno,book_url,book_url_md5) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql,(magazine_id,book_name,book_cover,book_year,book_sno,book_url,book_url_md5))
        self.conn.commit()

        r = redis.Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'])
        r.set(book_url_md5,self.cursor.lastrowid,7200)
        r.lpush("redis_dzwzzz_details:start_urls",book_url)
        return item
    def close_spider(self,spider):
        self.conn.close()
class TagPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host=settings['MYSQL_HOST'],user=settings['MYSQL_USER'],passwd=settings['MYSQL_PASSWORD'],db =settings['MYSQL_DATABASE'])
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        magazine_id = item['magazine_id']
        tag_name = item['tag_name']
        tag_name_md5 = item['tag_name_md5']
        sql = "insert into mg_tag(magazine_id,tag_name,tag_name_md5) VALUES(%s,%s,%s)"
        self.cursor.execute(sql, (magazine_id,tag_name,tag_name_md5))
        self.conn.commit()
        return item
    def close_spider(self,spider):
        self.conn.close()
class ContentPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host=settings['MYSQL_HOST'],user=settings['MYSQL_USER'],passwd=settings['MYSQL_PASSWORD'],db =settings['MYSQL_DATABASE'])
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        r = redis.Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'])
        book_id = r.get(item['book_id'])
        tag = {"magazine_id": item['magazine_id'],"tag_name": item['tag_id'],"tag_name_md5": item['tag_name_md5']}
        tag_id = self.getTagId(tag)
        cont_url = item['cont_url']
        cont_title = item['cont_title'].strip()
        cont_sno = item['cont_sno']
        cont_author = item['cont_author'].strip()
        cont_source = item['cont_source'].strip()
        cont_detail = ' '.join(item['cont_detail'])
        cont_url_md5 = item['cont_url_md5']

        sql ="insert into mg_content(book_id,tag_id,cont_url,cont_title,cont_sno,cont_author,cont_source,cont_detail,cont_url_md5) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql,(book_id,tag_id,cont_url,cont_title,cont_sno,cont_author,cont_source,cont_detail,cont_url_md5))
        self.conn.commit()
        return item
    def close_spider(self,spider):
        self.conn.close()
    def getTagId(self,tag):
        magazine_id = tag['magazine_id']
        tag_name = tag['tag_name']
        tag_name_md5 = tag['tag_name_md5']
        sql = "SELECT * FROM mg_tag WHERE tag_name_md5 = %s"
        self.cursor.execute(sql,tag_name_md5)
        oldTag = self.cursor.fetchone()
        if oldTag:
            return oldTag[0]
        else:
            sql = "insert into mg_tag(magazine_id,tag_name,tag_name_md5) VALUES(%s,%s,%s)"
            self.cursor.execute(sql, (magazine_id, tag_name, tag_name_md5))
            self.conn.commit()
            return self.cursor.lastrowid
