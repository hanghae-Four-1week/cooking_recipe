from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests



# 테스트 시에는 팀원분들 주소, 아이디, 패스워드로 써주세요
#류현님주소
# client = MongoClient('mongodb+srv://test:sparta@cluster0.xaxuh.mongodb.net/?retryWrites=true&w=majority')
#민희
client = MongoClient('mongodb+srv://sparta:woowa@cluster0.lqx8f.mongodb.net/?retryWrites=true&w=majority', 27017, username="sparta", password="woowa")
db = client.dbcooking_recipe

def get_menu_urls():
    # headers = 유저 정보를 넣어서 해당 사이트의 서버에게 봇으로 인식되어 크롤링이 차단되는 것을 제지함.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # 버튼 이름을 params로 줄 때
    param = {'q': '편스토랑'}
    r = requests.get("https://www.10000recipe.com/recipe/list.html", params=param, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    lis = soup.select('#contents_area_full > ul > ul > li')
    for li in lis:
        image = li.select_one('div.common_sp_thumb > a > img')['src']
        title = li.select_one('div.common_sp_caption > div.common_sp_caption_tit.line2').text
        address_name = li.select_one('div.common_sp_thumb > a')['href']
        id= address_name[-7:]

        print(title, image, id,param)
        doc = {
            "title": title,
            "image": image,
            'id': id,
            'q':'편스토랑'
        }

        db.menuPyeon.insert_one(doc)

    return

get_menu_urls()



