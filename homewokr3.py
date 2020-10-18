import requests


from bs4 import BeautifulSoup
from pymongo import MongoClient # 몽고db 임폴트...?

client = MongoClient('localhost',27017) #
db = client.dbmusic # client안에 dbmusic이라는 db를 생성

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

genie = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
for tr in genie:
    rank = tr.select_one('td.number').text[0:2].strip()
    title = tr.select_one('td.info > a.title.ellipsis').text.strip()
    artist = tr.select_one('td.info > a.artist.ellipsis').text
    album = tr.select_one('td.info > a.albumtitle.ellipsis').text.center(20,'-')
    # print(rank, title, artist, album)

    doc = {
        'rank': rank,
        'title' : title,
        'artist' : artist,
        'album' : album
    }
    db.genie.insert_one(doc)

