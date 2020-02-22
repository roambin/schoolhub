from app.myoperator.mongo_operator import db
from bson import ObjectId
user = db['user']


def add(dic):
    res = user.insert_one(dic)
    return res.inserted_id


def get(dic, dic_r=None):
    if dic_r:
        res = user.find_one(dic, dic_r)
    else:
        res = user.find_one(dic)
    return res


def get_by_id(userid, dic_r=None):
    res = get({'_id': ObjectId(userid)}, dic_r)
    return res


def get_iter(dic_f, dic_r):
    res = user.find(dic_f, dic_r)
    return res


def update(dic_s, dic):
    user.update_many(dic_s, dic)
    return True


def update_one(dic_s, dic):
    user.update_one(dic_s, dic)
    return True


def update_by_id_set(userid, dic):
    user.update_one({'_id': ObjectId(userid)}, {"$set": dic})
    return True


def update_by_id_add(userid, dic):
    user.update_one({'_id': ObjectId(userid)}, {"$addToSet": dic})
    return True


def delete(userid):
    user.delete_one({'_id': ObjectId(userid)})


def get_user_iter(dic_f, dic_r):
    res = user.find(dic_f, dic_r)
    return res


def get_qu(userid):
    res = user.find_one({'_id': ObjectId(userid)}, {'_id': 0, 'qu': 1})
    return res


def add_qu(userid, qu_id):
    user.update_one({'_id': ObjectId(userid)}, {"$set": {'qu.'+qu_id+'.qu_data': 1}})
    return True
