# 1. 데이터 수집 및 저장

from bs4 import BeautifulSoup
from PIL import Image

import requests
import pandas as pd
import requests

url = 'https://tickets.interpark.com/contents/ranking?genre=MUSICAL'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)


# 공연 이름
#contents > article:nth-child(3) > section > div > div > div.responsive-ranking-list_rankingListWrap__GM0yK.responsive-ranking-list_topRated__axfTY > div:nth-child(1) > div.responsive-ranking-list_rankingItemInner__mMLxe > ul > div.responsive-ranking-list_rankingContentsInner__8FuZE > li
#contents > article:nth-child(3) > section > div > div > div.responsive-ranking-list_rankingListWrap__GM0yK.responsive-ranking-list_topRated__axfTY > div:nth-child(2) > div.responsive-ranking-list_rankingItemInner__mMLxe > ul > div.responsive-ranking-list_rankingContentsInner__8FuZE > li
#contents > article:nth-child(3) > section > div > div > div:nth-child(2) > div:nth-child(1) > div.responsive-ranking-list_rankingItemInner__mMLxe > ul > div.responsive-ranking-list_rankingContentsInner__8FuZE > li

titles = soup.select("#contents > article:nth-child(3) > section > div > div")

for i in titles:
    title = i.select("div.responsive-ranking-list_rankingItemInner__mMLxe > ul > div.responsive-ranking-list_rankingContentsInner__8FuZE > li")
    for title_name in title:
        musical_title = title_name.text
        print(musical_title)

# 공연장
#contents > article:nth-child(3) > section > div > div > div.responsive-ranking-list_rankingListWrap__GM0yK.responsive-ranking-list_topRated__axfTY > div:nth-child(1) > div.responsive-ranking-list_rankingItemInner__mMLxe > ul > div.responsive-ranking-list_rankingContentsInner__8FuZE > div > li
#contents > article:nth-child(3) > section > div > div > div:nth-child(2) > div:nth-child(1) > div.responsive-ranking-list_rankingItemInner__mMLxe > ul > div.responsive-ranking-list_rankingContentsInner__8FuZE > div > li

places = soup.select("#contents > article:nth-child(3) > section > div > div")

for i in places:
    place = i.select("div.responsive-ranking-list_rankingItemInner__mMLxe > ul > div.responsive-ranking-list_rankingContentsInner__8FuZE > div > li")
    for place_name in place:
        musical_place = place_name.text
        print(musical_place)

# 공연기간
#contents > article:nth-child(3) > section > div > div > div.responsive-ranking-list_rankingListWrap__GM0yK.responsive-ranking-list_topRated__axfTY > div:nth-child(1) > div.responsive-ranking-list_rankingItemInner__mMLxe > ul > div.responsive-ranking-list_rankingContentsInner__8FuZE > div > div > div > li:nth-child(1)
#contents > article:nth-child(3) > section > div > div > div:nth-child(2) > div:nth-child(1) > div.responsive-ranking-list_rankingItemInner__mMLxe > ul > div.responsive-ranking-list_rankingContentsInner__8FuZE > div > div > div > li:nth-child(1)

running_dates = soup.select("#contents > article:nth-child(3) > section > div > div")

for i in running_dates:
    running_date = i.select("div.responsive-ranking-list_rankingItemInner__mMLxe > ul > div.responsive-ranking-list_rankingContentsInner__8FuZE > div > div > div")
    for date in running_date:
        musical_date = date.text
        print(musical_date)



titles = soup.select("#contents > article:nth-child(3) > section > div > div")

musical_list = []
index = 1

for i, container in enumerate(titles, start=1):  # 인덱스를 1부터 시작
    title_elements = container.select("div.responsive-ranking-list_rankingItemInner__mMLxe > ul > div.responsive-ranking-list_rankingContentsInner__8FuZE > li")
    place_elements = container.select("div.responsive-ranking-list_rankingItemInner__mMLxe > ul > div.responsive-ranking-list_rankingContentsInner__8FuZE > div > li")
    date_elements = container.select("div.responsive-ranking-list_rankingItemInner__mMLxe > ul > div.responsive-ranking-list_rankingContentsInner__8FuZE > div > div > div")
    
    for title, place, date in zip(title_elements, place_elements, date_elements):
        musical_list.append([
            index,
            title.text.strip(),
            place.text.strip(),
            date.text.strip()
        ])
        index += 1

print(musical_list)

# 2. 데이터프레임 생성 및 저장

#  1) 데이터프레임 생성
import pandas as pd
df_musicals = pd.DataFrame(musical_list, columns=['Rank', 'Title', 'Place', 'Period'])

#  2) 데이터프레임 저장
df_musicals.to_csv('musical_list.csv', index=False, encoding='utf-8')

#  3) csv 파일 읽기
df = pd.read_csv('musical_list.csv')
print(df.head)


# 3. MySQL 연결 및 데이터 삽입

#  1) MySQL 연결
import csv
import pymysql

config = {
    'user' : 'root',
    'password' : 'admin',
    'host' : 'localhost',
    'database' : 'my_musical_db'
}

conn = pymysql.connect(**config)
cursor = conn.cursor()
conn.commit()

#  2) 테이블 생성
cursor.execute('''
    CREATE TABLE IF NOT EXISTS musical_list (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ranking INT,
        title VARCHAR(255),
        place VARCHAR(255),
        period VARCHAR(255)
    )
''')
conn.commit()

#  3) 데이터 삽입

insert_query = '''
    INSERT INTO musical_list (ranking, title, place, period)
    VALUES (%s, %s, %s, %s)
'''

data = list(df.itertuples(index=False, name=None))
cursor.executemany(insert_query, data)
conn.commit()

#  4) 데이터 확인
cursor.execute("SELECT * FROM musical_list")
for row in cursor.fetchall(): 
    print(row)


# 5) 연결 종료
cursor.close()
conn.close()




