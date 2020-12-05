#!/usr/bin/env python
# encoding: utf-8
from jieba.analyse import extract_tags
import string
import YiQIng
from flask import Flask, request, render_template, jsonify
import utils


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ajax/', methods=['POST', 'GET'])
def ajax():
    if request.method == 'POST':
        name = request.values.get('name')
        age = request.values.get('age')
        print(name, age)
    return render_template('test.html')


@app.route('/get_time/', methods=['POST', 'GET'])
def get_time():
    dt = utils.get_time()
    return dt


@app.route('/get_center1/', methods=['POST', 'GET'])
def get_center1():
    # 获取数据库中想要的数据
    res = utils.get_center1()

    return jsonify({"confirm" : str(res[0]), "suspect" : str(res[1]), "heal": str(res[2]), "dead" : str(res[3])})


@app.route('/get_center2/', methods=['POST', 'GET'])
def get_center2():
    data = []
    res = utils.get_center2()
    for i in res:
        data.append({"name":str(i[0]),"value": int(i[1])})
    return jsonify({"data":data})

@app.route('/get_left1/', methods=['POST', 'GET'])
def get_left1():
    data = utils.get_left1()
    day, confirm, suspect, heal, dead = [], [], [], [], []
    for a, b, c, d, e in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day": day, "confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})


@app.route('/get_left2/', methods=['POST', 'GET'])
def get_left2():
    data = utils.get_left2()
    day, confirm_add, suspect_add = [], [], []
    for a, b, c in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add})


@app.route('/get_right1/', methods=['POST', 'GET'])
def get_right1():
    data = utils.get_right1()
    city = []
    confirm = []
    for k,v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({"city": city, "confirm": confirm})


@app.route('/get_right2/', methods=['POST', 'GET'])
def get_right2():
    data = utils.get_right2()
    d = []
    for i in data:
        k = i[0].rstrip(string.digits)
        v = i[0][len(k):]
        ks = extract_tags(k)
        for j in ks:
            if not j.isdigit():
                d.append({"name": j, "value": v})
    return jsonify({"kws": d})


@app.route('/update/', methods=['POST', 'GET'])
def update():
    print('正在更新')
    YiQIng.insert_history()
    YiQIng.insert_details()

    return {"code" : 200}


if __name__ == '__main__':
    app.run(port=8888)

