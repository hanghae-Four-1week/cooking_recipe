# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
# from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests

# 테스트 시에는 팀원분들 주소, 아이디, 패스워드로 써주세요
client = MongoClient('mongodb+srv://test:sparta@cluster0.xaxuh.mongodb.net/?retryWrites=true&w=majority')
db = client.dbcooking_recipe

# 구글 드라이브 절대경로입니다 이 부분도 바꿔주세요
# s = Service('/Users/amigo/Downloads/chromedriver')
# driver = webdriver.Chrome(service=s)

url = "https://www.10000recipe.com/recipe/list.html"

# driver.get(url)
# time.sleep(5)

#더보기 버튼
# for i in range(10):
#     try:
#         btn_more = driver.find_element_by_css_selector("#foodstar-front-location-curation-more-self > div > button")
#         btn_more.click()
#         time.sleep(5)
#     except NoSuchElementException:
#         break

# req = driver.page_source
# driver.quit()

soup = BeautifulSoup(url, 'html.parser')

places = soup.select("#contents_area_full > ul > ul >li ")
print(len(places))

for place in places:
    title = place.select_one('div.common_sp_caption > div.common_sp_caption_tit.line2').text
    img = place.select_one('div.common_sp_thumb > a > img')['src']

    print(title, img)
    doc = {
        "title": title,
        "img": img,
        }
    db.recipes.insert_one(doc)