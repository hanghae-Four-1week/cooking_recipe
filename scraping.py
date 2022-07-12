import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient



client = MongoClient('mongodb+srv://sparta:woowa@cluster0.lqx8f.mongodb.net/?retryWrites=true&w=majority', 27017, username="sparta", password="woowa")
db = client.dbcooking_recipe

# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.10000recipe.com/recipe/list.html',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
dishes = soup.select('#contents_area_full > ul > ul >li ')


for dish in dishes:
    # dishes 안에 dish 가 있으면,
    dish_img = dish.select_one('div.common_sp_thumb > a > img')['src']
    dish_title = dish.select_one('div.common_sp_caption > div.common_sp_caption_tit.line2').text
    dish_star_tag = dish.select_one('div.common_sp_caption > div.common_sp_caption_rv > span.common_sp_caption_rv_star')

    # print(dish_star) 별점 크롤링 문제
    doc = {
        'dish_img': dish_img,
        'dish_title': dish_title,
        # 'dish_star': dish_star
    }
    db.dishes.insert_one(doc)



