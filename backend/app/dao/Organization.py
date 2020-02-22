from app.myoperator.mongo_operator import db
from bson import ObjectId
org = db['org']


def add(dic):
    res = org.insert_one(dic)
    return res.inserted_id


def get(dic, dic_r=None):
    if dic_r:
        res = org.find_one(dic, dic_r)
    else:
        res = org.find_one(dic)
    return res


def get_by_name(org_name, dic_r=None):
    res = get({'org_name': org_name}, dic_r)
    return res


def get_by_id(org_id, dic_r=None):
    res = get({'_id': ObjectId(org_id)}, dic_r)
    return res


def get_iter(dic=None, dic_r=None):
    if dic_r:
        res = org.find(dic, dic_r)
    else:
        res = org.find(dic)
    return res


def update_by_id(org_id, dic):
    org.update_one({'_id': ObjectId(org_id)}, {"$set": dic})
    return True


def delete_by_id(org_id):
    org.delete_one({'_id': ObjectId(org_id)})
