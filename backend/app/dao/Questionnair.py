from app.myoperator.mongo_operator import db
from bson import ObjectId
qu = db['qu']


def add(dic):
    res = qu.insert_one(dic)
    return res.inserted_id


def get(dic, dic_r=None):
    if dic_r:
        res = qu.find_one(dic, dic_r)
    else:
        res = qu.find_one(dic)
    return res


def get_by_id(qu_id, dic_r=None):
    res = get({'_id': ObjectId(qu_id)}, dic_r)
    return res


def get_iter(dic, dic_r=None):
    if dic_r:
        res = qu.find(dic, dic_r)
    else:
        res = qu.find(dic)
    return res


def update(qu_id, dic):
    qu.update_one({'_id': ObjectId(qu_id)}, {"$set": dic})
    return True


def delete(qu_id):
    qu.delete_one({'_id': ObjectId(qu_id)})