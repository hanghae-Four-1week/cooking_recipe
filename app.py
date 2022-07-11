from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('mongodb+srv://sparta:woowa@Cluster0.lqx8f.mongodb.net/?retryWrites=true&w=majority', 27017, username="sparta", password="woowa")
db = client.dbcooking_recipe


@app.route('/')
def main():
    return render_template("index.html")

@app.route("/detail", methods=["POST"])
def post_dishes():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg':'POST 연결 완료!'})

@app.route('/detail', methods=["GET"])
def get_dishes():
    # 요리 목록을 반환하는 API
    # return jsonify({'result': 'success', 'recipe_list': []})
    return jsonify({'msg': 'GET 연결 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)