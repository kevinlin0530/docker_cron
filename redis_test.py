from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup as bs
import requests as req
import mysql.connector
import redis

class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def get(self, value):
        return self.redis_client.get(value)

    def set(self, key,vaule, expire_time):
        self.redis_client.setex(key,expire_time,vaule)
        
    def keys(self,pattern="*"):
        return self.redis_client.scan_iter(match=pattern)

def get_sql_connect():
    conn = mysql.connector.connect(
        host='35.201.205.128',
        user='root',
        password='d]a)Qf8=moJ"YiOU',
        database = 'gitaction',
    )
    return conn

def check_data(cursor,title):
    cursor.execute("SELECT * FROM test WHERE title = %s",(title,))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False
    
def insert_data(conn,cursor,title, timestamp):
    cursor.execute('INSERT INTO test (title, timestamp) VALUES (%s, %s)', (title, timestamp))
    conn.commit()
    
def update_data(conn,cursor,title, timestamp):
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('UPDATE test SET update_time = %s WHERE title = %s', (timestamp_str, title))
    conn.commit()

def convert_utc_to_taiwan(utc_time):
    taiwan_timezone = timezone(timedelta(hours=8))
    return utc_time.astimezone(taiwan_timezone)

def getData(url):
    cache = RedisCache()
    conn = get_sql_connect()
    cursor = conn.cursor()
    request=req.get(url, headers={
        "cookie":"over18=1",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    })
    root=bs(request.text,"html.parser")
    titles=root.find_all("div",class_="title")
    for title in titles:
        if title.a != None:
            title_string = title.a.string
            current_time = convert_utc_to_taiwan(datetime.now())
            name = cache.get(title_string)
            if name:
                update_data(conn,cursor,title_string, current_time)
                print(f"update_data:{title_string},update_time:{current_time}")
            else:
                insert_data(conn,cursor,title_string, current_time)
                print(f"insert_data:{title_string},insert_time:{current_time}")
            timestamp_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            cache.set(title_string,timestamp_str,70)
    nextLink=root.find("a", string="‹ 上頁")
    conn.close()
    return nextLink["href"]

pageURL="https://www.ptt.cc/bbs/movie/index.html"
count=0
getData(pageURL)
while count<2:
    pageURL="https://www.ptt.cc"+getData(pageURL)
    count+=1
result = "Finished"
print(result)