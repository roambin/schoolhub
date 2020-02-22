from flask import request, session, jsonify
import functools
from app.dao import User, Organization


def check_auth_user(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        check = __check_auth_user()
        if check:
            return func(*args, **kwargs)
        else:
            return jsonify({'code': 40002})
    return wrapper


def check_auth_role(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        check = __check_auth_role()
        if check:
            return func(*args, **kwargs)
        else:
            return jsonify({'code': 40002})
    return wrapper


def check_auth_qu(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        check = __check_auth_qu()
        if check:
            return func(*args, **kwargs)
        else:
            return jsonify({'code': 40002})
    return wrapper


def check_auth_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        check = __check_auth_admin()
        if check:
            return func(*args, **kwargs)
        else:
            return jsonify({'code': 40002})
    return wrapper


def check_auth_org(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        check = __check_auth_org()
        if check:
            return func(*args, **kwargs)
        else:
            return jsonify({'code': 40002})
    return wrapper


def __check_auth_user():
    userid = session['userid']
    data = request.get_json() or {}
    userids = data.get('userids') or []
    usernames = []
    if not userids:
        userid_get = data.get('userid')
        if userid_get:
            userids = [userid_get]
    if not userids:
        usernames = data.get('usernames') or []
        if not usernames:
            return True
    user_info = User.get_by_id(userid, ['user_info']).get('user_info')
    role = user_info.get('role') or 1
    if role == 101:
        return True
    if userids:
        for userid_get in userids:
            user_info_get = User.get_by_id(userid_get, ['user_info']).get('user_info')
            if not __inner_check_auth_user(user_info, role, user_info_get):
                return False
    else:
        for username in usernames:
            user_info_get = User.get({'user_info.username': username}, ['user_info']).get('user_info')
            if not __inner_check_auth_user(user_info, role, user_info_get):
                return False
    return True


def __inner_check_auth_user(user_info, role, user_info_get):
    role_get = user_info_get.get('role') or 1
    if role < role_get:
        return False
    if role == 100:
        return True
    elif 4 <= role < 100:
        return user_info.get('org') == user_info_get.get('org')
    elif role >= 2:
        check = user_info.get('org') == user_info_get.get('org')
        if not check:
            return False
        sub_org = user_info.get('sub_org')
        sub_org_get = user_info_get.get('sub_org')
        for e in sub_org_get:
            if e not in sub_org:
                return False
        return True
    else:
        return False


def __check_auth_role():
    userid = session['userid']
    data = request.get_json() or {}
    user_infos = data.get('user_infos') or []
    if not user_infos:
        user_info_set = data.get('user_info')
        if not user_info_set:
            return True
        else:
            user_infos = [user_info_set]
    user_info = User.get_by_id(userid, ['user_info']).get('user_info')
    role = user_info.get('role') or 1
    for e in user_infos:
        role_set = e.get('role') or 1
        if role < role_set:
            return False
    return True


def __check_auth_qu():
    userid = session['userid']
    data = request.get_json() or {}
    qu_id_get = data.get('qu_id')
    qu_ids_get = data.get('qu_ids') or []
    if not qu_ids_get:
        if not qu_id_get:
            return True
        else:
            qu_ids_get = [qu_id_get]
    user = User.get_by_id(userid, ['user_info', 'qus.qu_id'])
    role = user.get('user_info').get('role') or 1
    if role >= 100:
        return True
    else:
        qu_ids = list(map(lambda x: str(x['qu_id']), user.get('qus') or []))
        for qu_id in qu_ids_get:
            if qu_id not in qu_ids:
                return False
    return True


def __check_auth_admin():
    userid = session['userid']
    user_info = User.get_by_id(userid, ['user_info']).get('user_info')
    role = user_info.get('role') or 1
    return role >= 100


def __check_auth_org():
    userid = session['userid']
    user_info = User.get_by_id(userid, ['user_info']).get('user_info')
    role = user_info.get('role') or 1
    if role >= 100:
        return True
    data = request.get_json() or {}
    org_name = Organization.get_by_id(data.get('org_id'), ['org_name']).get('org_name')
    if 4 <= role < 100:
        return org_name == user_info.get('org')
    return False
