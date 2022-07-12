from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)

# 테스트 시에는 팀원분들 주소, 아이디, 패스워드로 써주세요
client = MongoClient('mongodb+srv://sparta:woowa@cluster0.lqx8f.mongodb.net/?retryWrites=true&w=majority', 27017, username="sparta", password="woowa")
db = client.dbcooking_recipe

# 메인 레시피 페이지
@app.route('/')
def main():
    return render_template("main.html")

@app.route('/recipes', methods=["GET"])
def get_recipes():
    # 맛집 목록을 반환하는 API
    recipes_list = list(db.recipes.find({}, {'_id': False}))
    # recipes_list 라는 키 값에 맛집 목록을 담아 클라이언트에게 반환합니다.
    return jsonify({'result': 'success', 'recipes_list': recipes_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)