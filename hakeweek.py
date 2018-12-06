from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:keyu0102@localhost/hackweek?charset=utf8"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

db = SQLAlchemy(app)



@app.before_request
def app_before_request():
    print("HTTP {}  {}".format(request.method, request.url))


@app.after_request
def app_after_request(response):
    response.headers["From"] = "Ncuhome"
    return response


class Lost(db.Model):
    __tablename__ = "shi_test"



    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))  # 用户名
    goods = db.Column(db.String(100))
    location = db.Column(db.String(100))
    desc = db.Column(db.String(256))
    date = db.Column(db.String(50))
    qq = db.Column(db.String(10))
    telephone = db.Column(db.String(256))




db.create_all()



@app.route("/lost_add", methods=['POST'])
def add():

    name = request.json.get("name")
    goods = request.json.get("goods")
    location = request.json.get("location")
    desc = request.json.get("desc")
    date = request.json.get("date")
    qq = request.json.get("qq")
    telephone = request.json.get("telephone")



    if not qq or not telephone:
        return jsonify({
                "status": 0,
                "message": "请联系方式填写完整！"
             }), 400

    lost = Lost(name=name, goods=goods, location=location, desc=desc, date=date, qq=qq, telephone=telephone)
    db.session.add(lost)
    db.session.commit()
    return jsonify({
        "status": 1,
        "message": "失物招领发布成功！",
    }), 200





@app.route("/lost_get", methods=['POST'])
def get_user():
    """
    查询发布的失误招领
    :return:
    """
    goods = request.json.get("goods")
    location = request.json.get("location")
    date = request.json.get("date")

    if not goods:
        abort(400)
    elif  not location and not date:
        losts = Lost.query.filter_by(goods=goods).all()
        data = []
        for lost in losts:
            data.append({
                "name": lost.name,
                "goods": lost.goods,
                "location": lost.location,
                "desc":lost.desc,
                "qq":lost.qq,
                "telephone":lost.telephone,
                "date":lost.date
            })  
        return jsonify(data)
    elif not location:
        losts = Lost.query.filter_by(goods=goods,date=date).all()
        data = []
        for lost in losts:
            data.append({
                "name": lost.name,
                "goods": lost.goods,
                "location": lost.location,
                "desc":lost.desc,
                "qq":lost.qq,
                "telephone":lost.telephone,
                "date":lost.date
            })  
        return jsonify(data)
    elif not date:
        losts = Lost.query.filter_by(goods=goods,location=location).all()
        data = []
        for lost in losts:
            data.append({
                "name": lost.name,
                "goods": lost.goods,
                "location": lost.location,
                "desc":lost.desc,
                "qq":lost.qq,
                "telephone":lost.telephone,
                "date":lost.date
            })  
        return jsonify(data)
    else:
        losts = Lost.query.filter_by(goods=goods,location=location,date=date).all()
        data = []
        for lost in losts:
            data.append({
                "name": lost.name,
                "goods": lost.goods,
                "location": lost.location,
                "desc":lost.desc,
                "qq":lost.qq,
                "telephone":lost.telephone,
                "date":lost.date
            })  
        return jsonify(data)





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True,debug=True)










    



