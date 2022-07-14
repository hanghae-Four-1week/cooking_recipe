import requests
from bs4 import BeautifulSoup

# 재료 별 레시피 url을 통해 각 페이지의 레시피 게시물로 들어가는 통로를 만듦
def get_urls():
    # headers = 유저 정보를 넣어서 해당 사이트의 서버에게 봇으로 인식되어 크롤링이 차단되는 것을 제지함.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # 데이터를 가져올 http를 requests의 API get을 이용해 가져온다.
    data = requests.get('https://www.10000recipe.com/recipe/list.html?q=&query=&cat1=&cat2=21&cat3=34&cat4=&fct=&order=reco&lastcate=cat3&dsearch=&copyshot=&scrap=&degree=&portion=&time=&niresource=', headers=headers)

    # data.text = requests의 text 속성을 통해 사이트의 html을 UTF-8로 인코딩된 문자열로 얻을 수 있다.
    # BeautifulSoup을 통해 해당 html 소스를 python 객체로 변환한다.
    # BeautifulSoup은 html 코드를 Python이 이해하는 객체 구조로 변환하는 Parsing을 한다.
    soup = BeautifulSoup(data.text, 'html.parser')

    # 레시피 게시판의 페이지의 url을 얻기 위해서 각 게시판의 html을 가져온다.
    lis = soup.select('#contents_area_full > ul > ul > li')

    # urls라는 빈 배열을 하나 만든다.
    urls = []

    for li in lis:
        # 반복문을 이용하여 게시판 태그 안에 해당 페이지 링크를 가리키는 a 태그 탐색한다.
        a = li.select_one('div.common_sp_thumb > a')
        if a is not None:
            # 사이트의 도메인과 위에서 가져온 a 태그의 href 속성을 이용하여 페이지 링크를 만든다.
            base_url = 'https://www.10000recipe.com/'
            url = base_url + a['href']
            # 만들어놨던 배열에 하나씩 넣는다.
            urls.append(url)
    return urls
