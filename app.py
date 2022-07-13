from pymongo import MongoClient
import jwt
import datetime
import hashlib
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from markupsafe import escape
from bson.json_util import loads, dumps


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb+srv://test:sparta@cluster0.xaxuh.mongodb.net/?retryWrites=true&w=majority')
db = client.dbcooking_recipe





@app.route('/')
def main_recipe():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userid = (payload["id"])
        user_info = db.users.find_one({"username": userid})
        recipes_list = list(db.recipes.find({}))
        return render_template('index.html', user = user_info, recipes_list = recipes_list)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/recipes', methods=["GET"])
def get_recipes():
    # 맛집 목록을 반환하는 API
    recipes_list = list(db.recipes.find({}, {'_id': False}))
    # print(recipes_list)
    # recipes_list 라는 키 값에 레시피 목록을 담아 클라이언트에게 반환합니다.
    return jsonify({'result': 'success', 'recipes_list': recipes_list})



@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


# @app.route('/user/<username>')
# def user(username):
#     # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         # 내 프로필이면 True, 다른 사람 프로필 페이지면 False
#         status = (username == payload["id"])

#         user_info = db.users.find_one({"username": username}, {"_id": False})
#         return render_template('user.html', user_info=user_info, status=status)
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))


# --------------------로그인----------------------
@app.route('/sign_in', methods=['POST'])
def sign_in():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one(
        {'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



# --------------------회원가입-----------------------
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    password_hash = hashlib.sha256(
        password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "nickname": nickname_receive,                              # 닉네임
        "password": password_hash,                                  # 비밀번호
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

# --------------------아이디 중복확인-----------------------
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))

    return jsonify({'result': 'success', 'exists': exists})


@app.route('/main/type', methods=['GET'])
# db에서 키워드로 db리스트 가져오기
def show_card():
    keyword = request.args.get('type')
    menu_card = list(db.recipes.find({'type': {'$regex': keyword}})) # $regex -> 포함된 문자열을 리스트 가져오기
    return jsonify({'menu_card': dumps(menu_card)}) #dump() -> JSON문자열로 변환, id값이 $oid안에 있어서?

@app.route('/posting', methods=['POST'])
def posting():
    # 클라이언트로부터 'comment_give'받아서 'comment_receive'에 넣어주기
    comment_receive = request.form["comment_give"]
    print(comment_receive, "댓글")
    # 클라이언트로부터 'date_give'받아서 'date_receive'에 넣어주기
    date_receive = request.form["date_give"]
    # 'date_receive'를 문자열로 변환하기
    date_receive = repr(date_receive)
    print(date_receive, "날짜")
    # 클라이언트로부터 'title_give' 받아서 'title_give'에 넣기
    title_give = request.form['title_give']
    print(title_give, "타이틀")
    # 쿠키에서 토큰받기
    token_receive = request.cookies.get('mytoken')
    try:
        # 받은 'token'에서 'id,exp'이 있는 payload 받아오기
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # payload['id']에서 userid 받아오기
        userid = (payload["id"])
        # db의 user에서 userid 받아와서 user_info에 넣기
        user_info = db.users.find_one({"userid": userid})
        print(user_info,"유저인포")
        # user_name, comment, date, title 들을 posts라는 db에 저장
        doc = {
            'user_name':user_info['username'],
            "comment": comment_receive,
            "date": date_receive,
            'title': title_give
        }
        db.posts.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    # jwt에서 exp가 만료되었을 때, "show_menu"로 보내기
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("show_menu"))




@app.route("/detail/<i>")
def post_dishes(i):

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userid = (payload["id"])
        user_info = db.users.find_one({"username": userid})
        recipes_list = list(db.recipes.find({'id': i}))
        print(recipes_list)
        return render_template('detail.html', user = user_info, recipes_list = recipes_list)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
# @app.route("/theme/<theme_name>", methods=["POST"])
# def travel_read(theme_name):
#     travel_list = list(db.travels.find({'theme': theme_name}, {'_id': False}))
#     return jsonify({'travels': travel_list})

# @app.route('/detail', methods=["GET"])
# def get_dishes():
#     # 요리 목록을 반환하는 API
#     # return jsonify({'result': 'success', 'recipe_list': []})
#     return jsonify({'msg': 'GET 연결 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
