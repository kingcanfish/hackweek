# -*- coding: utf-8 -*-

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql
from sqlalchemy import or_, and_

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:keyu0102@localhost/hackweek?charset=utf8"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)



@app.before_request
def app_before_request():
    print("HTTP {}  {}".format(request.method, request.url))


@app.after_request
def app_after_request(response):
    response.headers["From"] = "Ncuhome"
    return response


class Lost(db.Model):
    __tablename__ = "lost"

    goods_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(10))  # 用户名
    goods = db.Column(db.String(100))
    location = db.Column(db.String(100))
    desc = db.Column(db.String(512))
    date = db.Column(db.String(25))
    qq = db.Column(db.String(10))
    telephone = db.Column(db.String(11))
    isget = db.Column(db.String(10))
    name = db.Column(db.String(50))
    commit_name = db.Column(db.String(50))





class Find(db.Model):
    __tablename__ = "find"#一般物品的寻物启事表

    goods_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(10))#学号
    name = db.Column(db.String(50))
    goods = db.Column(db.String(100))
    location = db.Column(db.String(100))
    desc = db.Column(db.String(512))
    date = db.Column(db.String(25))
    qq = db.Column(db.String(10))
    telephone = db.Column(db.String(11))
    isget = db.Column(db.String(10))
    



class Offical(db.Model):#官方社团表
    __tablename__ = "offical"

    offical_id = db.Column(db.Integer, primary_key=True)
    offical_name = db.Column(db.String(30))
    telephone = db.Column(db.String(11))
    passwd = db.Column(db.String(20))
    qq = db.Column(db.String(10))
    location = db.Column(db.String(30))





class Safe_info(db.Model):
    __tablename__ = "safe_info"

    goods_id =db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(10))#发布失物招领的人
    id = db.Column(db.String(10))#发布失物招领的人的学号
    get_name = db.Column(db.String(10))#已领取的人的名字
    get_id = db.Column(db.String(10))#已领取的人的学号

        












db.create_all()



@app.route("/lost_add", methods=['POST'])#添加一般物品的失物招领
def add_lost():
    commit_name = request.json.get("commit_name")
    name = request.json.get("name")
    id = request.json.get("id")
    goods = request.json.get("goods")
    location = request.json.get("location")
    desc = request.json.get("desc")
    date = request.json.get("date")
    qq = request.json.get("qq")
    telephone = request.json.get("telephone")
    isget = "未找回"

    if not qq and not telephone:
        return jsonify({
                "status": 0,
                "message": "请联系方式填写完整！"
             }), 400

    lost = Lost(name=name, goods=goods, location=location, desc=desc, date=date, qq=qq, telephone=telephone, isget=isget, id=id, commit_name = commit_name)
    db.session.add(lost)
    db.session.commit()
    return jsonify({
        "status": 1,
        "message": "失物招领发布成功！",
    }), 200



@app.route("/lost_get", methods=['GET'])#筛选一般物品的失物招领
def get_lost():
    """
    查询发布的失误招领
    :return:
    """
    goods = request.args.get("goods")
    location = request.args.get("location")
    date = request.args.get("date")
    isget = request.args.get("isget")


    if not goods:
        abort(400)
    elif not location and not date:
        losts = Lost.query.filter_by(goods=goods, isget=isget).all()
        data = []
        for lost in losts:
            data.append({
                "name": lost.name,#
                "goods": lost.goods,
                "location": lost.location,
                "desc":lost.desc,
                "qq":lost.qq,
                "telephone":lost.telephone,
                "date":lost.date,
                "isget":lost.isget,
                "goods_id":lost.goods_id,
                "commit_name":lost.commit_name
            })  
        return jsonify(data)
    elif not location:
        losts = Lost.query.filter_by(goods=goods, date=date, isget=isget).all()
        data = []
        for lost in losts:
            data.append({
                "name": lost.name,
                "goods": lost.goods,
                "location": lost.location,
                "desc": lost.desc,
                "qq": lost.qq,
                "telephone": lost.telephone,
                "date": lost.date,
                "isget": lost.isget,
                "goods_id":lost.goods_id,
                "commit_name":lost.commit_name
            })
        return jsonify(data)
    elif not date:
        losts = Lost.query.filter_by(goods=goods, location=location, isget=isget).all()
        data = []
        for lost in losts:
            data.append({
                "name": lost.name,
                "goods": lost.goods,
                "location": lost.location,
                "desc": lost.desc,
                "qq": lost.qq,
                "telephone": lost.telephone,
                "date": lost.date,
                "isget":lost.isget,
                "goods_id":lost.goods_id,
                "commit_name":lost.commit_name
            })  
        return jsonify(data)
    else:
        losts = Lost.query.filter_by(goods=goods, location=location, date=date, isget=isget).all()
        data = []
        for lost in losts:
            data.append({
                "name": lost.name,
                "goods": lost.goods,
                "location": lost.location,
                "desc": lost.desc,
                "qq": lost.qq,
                "telephone": lost.telephone,
                "date": lost.date,
                "isget": lost.isget,
                "goods_id": lost.goods_id,
                "commit_name":lost.commit_name
            })  
        return jsonify(data)#筛选失物招领



@app.route("/lost_search", methods=['GET'])#搜索一般物品的失物招领
def search_lost():
    search = request.args.get("search")
    isget = request.args.get("isget")

    if not search:
        return jsonify({
        "status": 0,
        "message": "请输入搜索关键词",
    }), 200
    else:
        search0 ='%'+search+'%'
        data = []
        losts = Lost.query.filter(Lost.isget==isget, or_(Lost.desc.like(search0), Lost.goods.like(search0), Lost.location.like(search0), Lost.date.like(search0))).all()
        for lost in losts:
            data.append({
                "name": lost.name,
                "goods": lost.goods,
                "location": lost.location,
                "desc": lost.desc,
                "qq": lost.qq,
                "telephone": lost.telephone,
                "date": lost.date,
                "isget": lost.isget,
                "goods_id": lost.goods_id,
                "commit_name":lost.commit_name

        })

        return jsonify(data)#失物招领搜索



















@app.route("/find_get", methods=['GET'])#筛选一般物品的寻物启事
def get_find():
    """
    查询发布的寻物启事
    :return:
    """
    goods = request.args.get("goods")
    location = request.args.get("location")
    date = request.args.get("date")


    if not goods:
        abort(400)
    elif not location and not date:
        finds = Find.query.filter_by(goods=goods).all()
        data = []
        for find in finds:
            data.append({
                "name": find.name,
                "goods": find.goods,
                "location": find.location,
                "desc": find.desc,
                "qq": find.qq,
                "telephone": find.telephone,
                "date": find.date,
                "goods_id": find.goods_id
            })  
        return jsonify(data)
    elif not location:
        finds = Find.query.filter_by(goods=goods, date=date).all()
        data = []
        for find in finds:
            data.append({
                "name": find.name,
                "goods": find.goods,
                "location": find.location,
                "desc": find.desc,
                "qq": find.qq,
                "telephone": find.telephone,
                "date": find.date,
                "goods_id": find.goods_id
            }) 
        return jsonify(data)
    elif not date:
        finds = Find.query.filter_by(goods=goods, location=location).all()
        data = []
        for find in finds:
            data.append({
                "name": find.name,
                "goods": find.goods,
                "location": find.location,
                "desc": find.desc,
                "qq": find.qq,
                "telephone": find.telephone,
                "date": find.date,
                "goods_id": find.goods_id
            }) 
        return jsonify(data)
    else:
        finds = Find.query.filter_by(goods=goods, location=location, date=date).all()
        data = []
        for find in finds:
            data.append({
                "name": find.name,
                "goods": find.goods,
                "location": find.location,
                "desc": find.desc,
                "qq": find.qq,
                "telephone": find.telephone,
                "date": find.date,
                "goods_id": find.goods_id
            }) 
        return jsonify(data)#筛选寻物启事





@app.route("/find_add", methods=['POST'])#发布一般物品的寻物启事
def add_find():

    name = request.json.get("name")
    id = request.json.get("id")
    goods = request.json.get("goods")
    location = request.json.get("location")
    desc = request.json.get("desc")
    date = request.json.get("date")
    qq = request.json.get("qq")
    telephone = request.json.get("telephone")
    isget = "未归还"

    if not qq and not telephone:
        return jsonify({
                "status": 0,
                "message": "请联系方式填写完整！"
             }), 400

    find = Find(name=name, goods=goods, location=location, desc=desc, date=date, qq=qq, telephone=telephone, isget=isget, id=id)
    db.session.add(find)
    db.session.commit()
    return jsonify({
        "status": 1,
        "message": "寻物启事发布成功！",
    }), 200#添加寻物启事




@app.route("/find_search", methods=['GET'])#搜索一般物品的寻物启事
def search_find():
    search = request.args.get("search")
    if not search:
        return jsonify({
        "status": 0,
        "message": "请输入搜索关键词",
    }), 200
    else:
        search0 ='%'+search+'%'
        data = []
        losts = Find.query.filter(or_(Find.desc.like(search0), Find.goods.like(search0), Find.location.like(search0), Find.date.like(search0))).all()
        for lost in losts:
            data.append({
                "name": lost.name,
                "goods": lost.goods,
                "location": lost.location,
                "desc": lost.desc,
                "qq": lost.qq,
                "telephone": lost.telephone,
                "date": lost.date,
                "isget": lost.isget,
                "goods_id": lost.goods_id

        })

        return jsonify(data)#失物招领搜索





















@app.route("/my_lost", methods=['GET'])#我的失物招领
def lost_my():
    id = request.args.get("id")
    losts = Lost.query.filter_by(id=id).all()
    data=[]
    for lost in losts:
        data.append({
                "name": lost.name,
                "goods": lost.goods,
                "location": lost.location,
                "desc": lost.desc,
                "qq": lost.qq,
                "telephone": lost.telephone,
                "date": lost.date,
                "isget": lost.isget,
                "goods_id": lost.goods_id
            }) 
    return jsonify(data)







@app.route("/my_find", methods=['GET'])#我的寻物启事
def find_my():
    id = request.args.get("id")
    finds = Find.query.filter_by(id=id).all()
    data=[]
    for find in finds:
        data.append({
                "name": find.name,
                "goods": find.goods,
                "location": find.location,
                "desc": find.desc,
                "qq": find.qq,
                "telephone": find.telephone,
                "date": find.date,
                "isget": find.isget,
                "goods_id": find.goods_id
            }) 
    return jsonify(data)









@app.route("/lost_isget", methods=['PUT'])#改变失物招领的状态
def isget_lost():
    goods_id = request.json.get("goods_id")
    isget = request.json.get("isget")
    lost = Lost.query.filter_by(goods_id=goods_id).first()
    lost.isget = isget
    db.session.commit()
    return jsonify({
            "message":"提交成功！"
        })








@app.route("/find_isget", methods=['DELETE'])#寻物启事已经找回并删除
def isget_find():
    goods_id = request.json.get("goods_id")
    find = Find.query.filter_by(goods_id=goods_id).first()
    db.session.delete(find)
    db.session.commit()
    return jsonify({
            "message":"提交成功！"
        })












@app.route("/add_offical", methods=['POST'])
def add_offical():
    offical_id = request.json.get("offical_id")
    offical_name = request.json.get("offical_name")
    telephone = request.json.get("telephone")
    passwd = request.json.get("passwd")
    qq = request.json.get("qq")
    location = request.json.get("location")
    offical = Offical(name=name, goods=goods, location=location, desc=desc, date=date, qq=qq, telephone=telephone, isget=isget, id=id, commit_name = commit_name)
    db.session.add(offical)
    db.session.commit()
    return jsonify({
        "status": 1,
        "message": "官方账号添加成功！",
    }), 200


@app.route("/get_offical", methods=['GET'])
def get_offical():
    offical_id = request.args.get("offical_id")
    passwd = request.args.get("passwd")
    offical = Offical.query.filter_by(offical_id=offical_id).first()
    if offical.passwd != passwd:
        return jsonify({
                "message":"账号或密码错误!"
            })
    else:
        return jsonify({
                "offical_id": offical.offical_id,
                "offical_name": offical.offical_name,
                "telephone": offical.telephone,
                "qq": offical.qq,
                "location": offical.location
            })






@app.route("/safe", methods=['POST'])
def safe():
    goods_id = request.json.get("goods_id")
    name = request.json.get("name")
    id = request.json.get("id")
    get_name = request.json.get("get_name")
    get_id = request.json.get("get_id")
    safe = Safe_info(goods_id=goods_id, name=name, id=id, get_name=get_name,get_id=get_id)
    db.session.add(safe)
    db.session.commit()
    return jsonify({
            "message":"安全信息保存成功！"
        })








if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)










    



