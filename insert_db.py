# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from url import get_urls
# import time
# from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests


# 테스트 시에는 팀원분들 주소, 아이디, 패스워드로 써주세요
#류현님주소
client = MongoClient('mongodb+srv://test:sparta@cluster0.xaxuh.mongodb.net/?retryWrites=true&w=majority')
#민희
# client = MongoClient('mongodb+srv://sparta:woowa@cluster0.lqx8f.mongodb.net/?retryWrites=true&w=majority', 27017, username="sparta", password="woowa")
db = client.dbcooking_recipe




get_urls()

def insert_recipe(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # html태그의 text를 음식 이름을 얻기 위해 select_one으로 뽑아준다.
    name = soup.select_one('#contents_area > div.view2_summary.st3 > h3').text

    # 마찬가지로 이미지 태그의 속성 src를 가져온다.
    img_url = soup.select_one('#main_thumbs')['src']
    id = url[-7:]

    # 재료 항목 추출
    def get_ingredients():
        ings = soup.select('#divConfirmedMaterialArea > ul > a')
        # 사이트에 사용될 때 용이하도록 배열에 담음
        lis = []
        for ing in ings:
            # text를 출력했을때 줄바꿈으로 인해 생긴 \n를 .replace를 이용해 공백문자로 바꿔줌
            li = ing.select_one('li').text.replace('\n', '')
            # 리스트에 공백문자가 대량 발생하여 .join을 이용해 하나로 합침
            li2 = ' '.join(li.split())
            lis.append(li2)
        return (lis)

    ingredients = get_ingredients()

    # 순서 추출
    def get_steps():
        steps = soup.select('#contents_area > div:nth-child(11) > .view_step_cont')
        divs = []
        for step in steps:
            div = step.select_one('.media-body').text.replace('\n', '')
            divs.append(div)
        return (divs)

    steps = get_steps()

    # doc이라는 객체에 키: 값을 명시하여 담음
    doc = {
        'type': '기타',
        'title': name,
        'image': img_url,
        'ingredient': ingredients,
        'step': steps,
        'id': id
    }

    # db에 doc를 넣는다.
    db.recipes.insert_one(doc)
    print('완료!', name)

def insert_all():
    # db.recipe.drop()
    # urls 변수에 get_urls 함수를 담아서 반복문을 돌려 모든 페이지에서 추출한 객체들을 뽑아 담는다.
    urls = get_urls()
    for url in urls:
        insert_recipe(url)

# 함수 실행
insert_all()