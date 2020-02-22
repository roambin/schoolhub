from app.dao import User, Questionnair
from bson import ObjectId
from app.model.report import Report


def __is_admin(userid):
    user_info = User.get_by_id(userid).get('user_info')
    if not user_info:
        return False
    role = user_info.get('role')
    if not role:
        return False
    return role >= 100


def __get_qu_ids(userid):
    if __is_admin(userid):
        qu_ids = Questionnair.get_iter({}, ['_id'])
        return list[qu_ids]
    qu_ids = User.get_by_id(userid, ['qus.qu_id']).get('qus') or []
    qu_ids = list(map(lambda x: x['qu_id'], qu_ids))
    return qu_ids


def __get_auth_users(userid):
    user_info = User.get_by_id(userid, ['user_info']).get('user_info')
    role = user_info.get('role') or 1
    if role == 101:
        userids = User.get_iter({}, None)
    elif role == 100:
        userids = User.get_iter({'user_info.role': {'$lte': role}}, None)
    elif role >= 4:
        org = user_info.get('org')
        if not org:
            userids = []
        else:
            userids = User.get_iter({'user_info.role': {'$lte': role}, 'user_info.org': user_info.get('org')}, None)
    elif role >= 2:
        org = user_info.get('org')
        sub_org = user_info.get('sub_org')
        if not org or not sub_org:
            userids = []
        else:
            userids = User.get_iter({'user_info.role': {'$lte': role}, 'user_info.org': org,
                                     '$or': [{'user_info.sub_org': {'$in': sub_org}}, {'user_info.sub_org': []}]}, None)
    else:
        userids = []
    arr = []
    for e in userids:
        arr.append(e.get('_id'))
    userids = arr
    return userids


def __get_qu(userid, qu_id):
    res = User.get({"_id": ObjectId(userid), "qus": {'$elemMatch': {"qu_id": ObjectId(qu_id)}}}, ['qus'])
    return res


def has_username(username):
    user = User.get({'user_info.username': username})
    return user is not None


def get_user_by_username(username):
    return User.get({'user_info.username': username})


def get_user_by_userid(userid, dic_r=None):
    return User.get({'_id': ObjectId(userid)}, dic_r)


def add(user_info, password):
    userid = User.add({'user_info': user_info, 'password': password})
    return userid


def add_user(user_id, user_info_set, password):
    user_info = User.get_by_id(user_id, ['user_info']).get('user_info') or {}
    user_info_set['role'] = 1
    user_info_set['org'] = user_info.get('org')
    user_info_set['sub_org'] = user_info.get('sub_org')
    add(user_info_set, password)
    return True


def set_password(userid, password):
    return User.update_by_id_set(userid, {'password': password})


def set_user_info(userids, user_infos):
    for userid, user_info in zip(userids, user_infos):
        User.update_by_id_set(userid, {'user_info': user_info})
    return True


def set_sub_orgs(userids, org, sub_org):
    for userid in userids:
        if org:
            User.update_by_id_set(userid, {'user_info.org': org, 'user_info.sub_org': sub_org})
        else:
            User.update_by_id_set(userid, {'user_info.sub_org': sub_org})
    return True


def set_users_sel(userids, data_set):
    for userid, data_set in zip(userids, data_set):
        User.update_by_id_set(userid, data_set)
    return True


def get_qus(userid):
    if __is_admin(userid):
        qu_iter = Questionnair.get_iter({}, ['_id', 'qu_name'])
    else:
        qu_ids = __get_qu_ids(userid)
        qu_iter = Questionnair.get_iter({'_id': {'$in': qu_ids}}, ['_id', 'qu_name'])
    qus = []
    for e in qu_iter:
        qus.append({'qu_id': str(e['_id']), 'qu_name': e['qu_name']})
    return qus


def add_qu(userid, qu_id):
    return User.update_by_id_add(userid, {'qus': {'qu_id': ObjectId(qu_id)}})


def get_qu(userid, qu_id):
    res = User.get({"_id": ObjectId(userid), "qus": {'$elemMatch': {"qu_id": ObjectId(qu_id)}}}, {'_id': 0, 'qus.$': 1})
    if not res:
        return None
    res = res.get('qus')
    if res:
        res = res[0]
        res['qu_id'] = str(res['qu_id'])
    return res


def get_qu_data(userid, qu_id):
    res = User.get({"_id": ObjectId(userid), "qus": {'$elemMatch': {"qu_id": ObjectId(qu_id)}}},
                   {'_id': 0, 'qus.$.qu_data': 1})
    if not res:
        return None
    res = res.get('qus')
    if res:
        res = res[0].get('qu_data')
    return res


def set_qu_data(userid, qu_id, qu_data):
    has_qu = __get_qu(userid, qu_id) is not None
    if not has_qu:
        User.update_by_id_add(userid, {'qus': {'qu_id': ObjectId(qu_id), 'info': {'auth': 1}}})
    qu_report = Report.generate_report(qu_id, qu_data)
    return User.update_one({"_id": ObjectId(userid), "qus": {'$elemMatch': {"qu_id": ObjectId(qu_id)}}},
                           {'$set': {'qus.$.qu_data': qu_data, 'qus.$.qu_report': qu_report}})


def set_user_qu_info(userid, qu_id, info):
    has_qu = __get_qu(userid, qu_id) is not None
    if not has_qu:
        return User.update_by_id_add(userid, {'qus': {'qu_id': ObjectId(qu_id), 'info': info}})
    else:
        return User.update_one({"_id": ObjectId(userid), "qus": {'$elemMatch': {"qu_id": ObjectId(qu_id)}}},
                               {'$set': {'qus.$.info': info}})


def upload(qu_id, usernames, qu_datas):
    for username, qu_data in zip(usernames, qu_datas):
        userid_set = User.get({'user_info.username': username}, ['_id'])
        if not userid_set:
            continue
        userid_set = str(userid_set.get('_id'))
        set_qu_data(userid_set, qu_id, qu_data)
    return True


def get_users(userid, data_filter=None):
    if data_filter is None:
        data_filter = {}
    userids = __get_auth_users(userid)
    data_filter['_id'] = {'$in': userids}
    res = User.get_user_iter(data_filter, ['user_info', 'qus'])
    user_infos = []
    for e in res:
        e['_id'] = str(e['_id'])
        if e.get('qus'):
            user_qu_map = {}
            for qu in e['qus']:
                # if not qu.get('qu_report'):
                #     qu['qu_report'] = {}
                user_qu_map[str(qu['qu_id'])] = {'qu_report': qu.get('qu_report'), 'info': qu.get('info')}
            e['qus'] = user_qu_map
        else:
            e['qus'] = {}
        user_infos.append(e)
    return user_infos


def get_users_sel(userid, data_filter=None, data_sel=None):
    if data_filter is None:
        data_filter = {}
    userids = __get_auth_users(userid)
    data_filter['_id'] = {'$in': userids}
    res = User.get_user_iter(data_filter, data_sel)
    users = []
    for e in res:
        e['_id'] = str(e['_id'])
        users.append(e)
    return users


def delete(userids):
    for userid in userids:
        User.delete(userid)
    return True


def set_auth_qu_use(userids, qu_ids, is_add):
    userids = list(map(lambda x: ObjectId(x), userids))
    qu_ids = list(map(lambda x: ObjectId(x), qu_ids))
    if is_add:
        for userid in userids:
            for qu_id in qu_ids:
                has_qu = __get_qu(userid, qu_id) is not None
                if not has_qu:
                    User.update_by_id_add(userid, {'qus': {'qu_id': ObjectId(qu_id), 'info': {'auth': 1}}})
    else:
        User.update({'_id': {'$in': userids}}, {'$pull': {'qus': {'qu_id': {'$in': qu_ids}}}})
    return True
