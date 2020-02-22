from app.utils import rsa_utils, jwt_utils, password_utils, mongo_backup
from flask import render_template, request, jsonify, session, send_from_directory, make_response, json
from app.controller import bp
from app.model import User, Questionnair, Organization
from app.model.report import Report
from app.auth import token_auth, role_auth
import os
from public import config


@bp.route("/")
def index():
    return render_template('index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    response = {'code': 40001}
    data = request.get_json()
    user_info = data['user_info']
    password = data['password']
    pwraw = rsa_utils.decrypt(password)
    if pwraw is None:
        return jsonify(response)
    res = User.get_user_by_username(user_info['username'])
    if res is None:
        return jsonify(response)
    pwdb = res.get('password')
    userid = res.get('_id')
    check = password_utils.check_hash(pwdb, pwraw)
    if check is False:
        return jsonify(response)
    token = jwt_utils.create_token(userid)
    response = {
        'code': 20000,
        'token': token
    }
    return jsonify(response)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    user_info = data['user_info']
    password = data['password']
    password = rsa_utils.decrypt(password)
    if password is None:
        return jsonify({'code': 40001})
    if User.has_username(user_info['username']):
        return jsonify({'code': 40101})
    if not user_info.get('role'):
        user_info['role'] = 1
    userid = User.add(user_info, password_utils.generate_hash(password))
    token = jwt_utils.create_token(userid)
    response = {
        'code': 20000,
        'token': token
    }
    return jsonify(response)


@bp.route('/user/add', methods=['GET', 'POST'])
@token_auth.auth.login_required
def add_user():
    userid = session['userid']
    data = request.get_json()
    user_info = data['user_info']
    password = data['password']
    password = password_utils.generate_hash(password)
    if User.has_username(user_info['username']):
        return jsonify({'code': 40101})
    res = User.add_user(userid, user_info, password)
    if not res:
        return jsonify({'code': 44000})
    return jsonify(({'code': 20000}))


@bp.route('/user/resetPwd', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
def reset_pwd():
    data = request.get_json()
    userid = data.get('userid') or session['userid']
    pwd_new = data['pwd_new']
    pwd_new = rsa_utils.decrypt(pwd_new)
    if not data.get('userid'):
        pwd_old = data['pwd_old']
        pwd_old = rsa_utils.decrypt(pwd_old)
        if pwd_old is None or pwd_new is None:
            return jsonify({'code': 40001})
        res = User.get_user_by_userid(userid)
        if res is None:
            return jsonify({'code': 40001})
        pwdb = res.get('password')
        check = password_utils.check_hash(pwdb, pwd_old)
        if check is False:
            return jsonify({'code': 40001})
    res = User.set_password(userid, password_utils.generate_hash(pwd_new))
    if not res:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/user/setUserInfo', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
@role_auth.check_auth_role
def set_user_info():
    data = request.get_json()
    userids = data.get('userids') or [session['userid']]
    user_infos = data.get('user_infos')
    res = User.set_user_info(userids, user_infos)
    if res is None:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/user/setSubOrgs', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
def set_sub_orgs():
    data = request.get_json()
    userids = data.get('userids')
    sub_org = data.get('sub_org')
    org = data.get('org')
    res = User.set_sub_orgs(userids, org, sub_org)
    if res is None:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/user/getUserInfo', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
def get_user_info():
    data = request.get_json() or {}
    userid = data.get('userid') or session['userid']
    res = User.get_user_by_userid(userid)
    if res is None:
        return jsonify({'code': 44000})
    response = {
        'code': 20000,
        'data': {
            'user_info': res.get('user_info')
        }
    }
    return jsonify(response)


@bp.route('/qu/list', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
def qu_list():
    data = request.get_json() or {}
    userid = data.get('userid') or session['userid']
    res = User.get_qus(userid)
    response = {
        'code': 20000,
        'list': res
    }
    return jsonify(response)


@bp.route('/qu/getQuInfo', methods=['GET', 'POST'])
@token_auth.auth.login_required
def qu_get_info():
    userid = session['userid']
    data = request.get_json()
    qu_id = data['qu_id']
    res = Questionnair.get_qu(qu_id, {'_id': 0, 'qu_name': 1, 'qu_info': 1, 'qu_text': 1})
    if res is None:
        return jsonify({'code': 40002})
    response = {
        'code': 20000,
        'data': {
            'qu': res
        }
    }
    return jsonify(response)


@bp.route('/qu/setQuData', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
@role_auth.check_auth_qu
def qu_set_data():
    data = request.get_json() or {}
    userid = data.get('userid') or session['userid']
    qu_id = data['qu_id']
    qu_data = data['qu_data']
    res = User.set_qu_data(userid, qu_id, qu_data)
    if not res:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/user/setUserQuInfo', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
@role_auth.check_auth_qu
def set_user_qu_info():
    data = request.get_json() or {}
    userid = data.get('userid') or session['userid']
    qu_id = data['qu_id']
    info = data['info']
    res = User.set_user_qu_info(userid, qu_id, info)
    if not res:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/qu/getQuData', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
def qu_get_data():
    data = request.get_json() or {}
    userid = data.get('userid') or session['userid']
    qu_id = data['qu_id']
    res = User.get_qu_data(userid, qu_id)
    response = {
        'code': 20000,
        'data': {
            'qu_data': res
        }
    }
    return jsonify(response)


@bp.route('/user/getQu', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
def user_qu_get():
    data = request.get_json() or {}
    userid = data.get('userid') or session['userid']
    qu_id = data['qu_id']
    res = User.get_qu(userid, qu_id)
    response = {
        'code': 20000,
        'data': {
            'qu': res
        }
    }
    return jsonify(response)


@bp.route('/qu/setQuInfo', methods=['GET', 'POST'])
@token_auth.auth.login_required
def qu_set_info():
    userid = session['userid']
    data = request.get_json()
    qu_id = data.get('qu_id')
    qu = data.get('qu')
    res = Questionnair.set_qu_info(qu_id, qu)
    if res is None:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/qu/delQu', methods=['GET', 'POST'])
@token_auth.auth.login_required
def qu_del():
    data = request.get_json()
    qu_id = data['qu_id']
    res = Questionnair.del_qu(qu_id)
    if res is None:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/user/list', methods=['GET', 'POST'])
@token_auth.auth.login_required
def user_list():
    userid = session['userid']
    data = request.get_json()
    data_filter_dict = data['data_filter']  # dict {'role':1, 'org':o1, 'sub_org':so1}
    data_filter = {}
    for k, v in data_filter_dict['user_info'].items():
        if v:
            data_filter['user_info.' + k] = v
    users = User.get_users(userid, data_filter)
    if users is None:
        return jsonify({'code': 44000})
    response = {
        'code': 20000,
        'data': {
            'users': users
        }
    }
    return jsonify(response)


@bp.route('/user/listSel', methods=['GET', 'POST'])
@token_auth.auth.login_required
def user_list_sel():
    userid = session['userid']
    data = request.get_json()
    data_filter = {}
    data_filter_dict = data.get('data_filter')
    if data_filter_dict and data_filter_dict.get('user_info'):
        for k, v in data_filter_dict['user_info'].items():
            if v:
                data_filter['user_info.' + k] = v
    data_sel = data['data_sel'] or None
    users = User.get_users_sel(userid, data_filter, data_sel)
    if users is None:
        return jsonify({'code': 44000})
    response = {
        'code': 20000,
        'data': {
            'users': users
        }
    }
    return jsonify(response)


@bp.route('/user/getSel', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
def user_get_sel():
    data = request.get_json()
    userid = data.get('userid') or session['userid']
    data_sel = data['data_sel'] or None
    user = User.get_user_by_userid(userid, data_sel)
    if user is None:
        return jsonify({'code': 44000})
    response = {
        'code': 20000,
        'data': {
            'user': user
        }
    }
    return jsonify(response)


@bp.route('/user/setSel', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_role
def user_set_sel():
    data = request.get_json()
    userids = data.get('userids')
    data_set = data.get('data_set')
    res = User.set_users_sel(userids, data_set)
    if res is None:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/user/delUser', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
def user_del():
    userid = session['userid']
    data = request.get_json()
    userids = data['userids']  # dict {1: '1', 2: '0', 3: ''}
    res = User.delete(userids)
    if not res:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/user/auth/qu', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
def user_auth_qu():
    data = request.get_json()
    userids = data['userids']
    qu_ids = data['qu_ids']
    is_add = data['is_add']
    res = User.set_auth_qu_use(userids, qu_ids, is_add)
    if not res:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/qu/uploadData', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
@role_auth.check_auth_qu
def qu_upload_data():
    data = request.get_json()
    qu_id = data['qu_id']
    usernames = data['usernames']
    qu_datas = data['qu_datas']
    res = User.upload(qu_id, usernames, qu_datas)
    if res is None:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/qu/set', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_admin
def qu_set():
    data = request.get_json()
    qu_id = data['qu_id']
    data_set = data.get('data_set')
    res = Questionnair.set_qu(qu_id, data_set)
    if res is None:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/qu/get', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_admin
def qu_get():
    data = request.get_json()
    qu_id = data['qu_id']
    data_sel = data.get('data_sel')
    res = Questionnair.get_qu(qu_id, data_sel)
    if res is None:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000, 'data': {'qu': res}})


@bp.route('/system/backup/list', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_admin
def system_backup_list():
    res = mongo_backup.list_file()
    if res is None:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000, 'data': {'dumps': res}})


@bp.route('/system/backup/delete', methods=['GET', 'POST'])
@token_auth.auth.login_required
def system_backup_delete():
    userid = session['userid']
    user_info = User.get_user_by_userid(userid).get('user_info')
    role = user_info.get('role') or 1
    if role < 101:
        return jsonify({'code': 20000, 'msg': '没有权限'})

    data = request.get_json()
    dump_name = data.get('dump_name')
    if not dump_name:
        return jsonify({'code': 44000})
    res = mongo_backup.delete(dump_name)
    if not res:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/system/backup/dump', methods=['GET', 'POST'])
@token_auth.auth.login_required
def system_backup_dump():
    action = '备份'
    userid = session['userid']
    user_info = User.get_user_by_userid(userid).get('user_info')
    role = user_info.get('role') or 1
    if role < 100:
        return jsonify({'code': 20000, 'msg': '没有权限'})
    elif role == 100:
        auth = user_info.get('auth') or []
        if action not in auth:
            return jsonify({'code': 20000, 'msg': '没有权限'})
        auth.remove(action)
        user_info['auth'] = auth
        User.set_user_info([userid], [user_info])

    res = mongo_backup.dump()
    if not res:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/system/backup/restore', methods=['GET', 'POST'])
@token_auth.auth.login_required
def system_backup_restore():
    action = '回滚'
    userid = session['userid']
    user_info = User.get_user_by_userid(userid).get('user_info')
    role = user_info.get('role') or 1
    auth = user_info.get('auth') or []
    if role < 100:
        return jsonify({'code': 20000, 'msg': '没有权限'})
    elif role == 100:
        if action not in auth:
            return jsonify({'code': 20000, 'msg': '没有权限'})

    data = request.get_json()
    dump_name = data.get('dump_name')
    if not dump_name:
        return jsonify({'code': 44000})
    res = mongo_backup.restore(dump_name)
    if not res:
        return jsonify({'code': 44000})

    if role == 100:
        auth.remove(action)
        user_info['auth'] = auth
        User.set_user_info([userid], [user_info])

    return jsonify({'code': 20000})


@bp.route('/org/list', methods=['GET', 'POST'])
@token_auth.auth.login_required
def org_list():
    userid = session['userid']
    res = Organization.get_ogs(userid)
    for e in res:
        if not e.get('sub_orgs'):
            e['sub_orgs'] = []
        if not e.get('subjects'):
            e['subjects'] = []
    orgs_map = dict(zip([e['org_name'] for e in res], [e['sub_orgs'] for e in res]))
    return jsonify({'code': 20000, 'data': {'orgs': res, 'orgs_map': orgs_map}})


@bp.route('/org/list/name', methods=['GET', 'POST'])
def org_list_name():
    res = Organization.get_ogs_name()
    for e in res:
        if not e.get('sub_orgs'):
            e['sub_orgs'] = []
    orgs_map = dict(zip([e['org_name'] for e in res], [e['sub_orgs'] for e in res]))
    return jsonify({'code': 20000, 'data': {'orgs': res, 'orgs_map': orgs_map}})


@bp.route('/org/add', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_org
def org_add():
    data = request.get_json()
    org = data.get('org')
    res = Organization.add_org(org)
    if res is False:
        return jsonify({'code': 20000, 'msg': '机构已存在'})
    if not res:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/org/set', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_org
def org_set():
    data = request.get_json()
    org_id = data.get('org_id')
    org = data.get('org')
    res = Organization.set_org(org_id, org)
    if not res:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/org/del', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_org
def org_del():
    data = request.get_json()
    org_id = data.get('org_id')
    res = Organization.del_org(org_id)
    if not res:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000})


@bp.route('/org/getSubOrgs', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_org
def org_get_sub_orgs():
    userid = session['userid']
    data = request.get_json()
    data_filter = data.get('data_filter') or {}
    res = Organization.get_sub_orgs(userid, data_filter)
    if not res:
        return jsonify({'code': 44000})
    return jsonify({'code': 20000, 'list': res})


@bp.route('/user/downloadReport', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
def user_download_report():
    data = request.get_json() or {}
    userid = session['userid']
    qu_id = data.get('qu_id')
    download_info = data.get('download_info')
    res = Report.download_report(userid, qu_id, download_info)
    if not res:
        return jsonify({'code': 40002})
    return res


@bp.route('/user/getReportText', methods=['GET', 'POST'])
@token_auth.auth.login_required
@role_auth.check_auth_user
def user_get_report_text():
    data = request.get_json() or {}
    userid = session['userid']
    qu_id = data.get('qu_id')
    download_info = data.get('download_info')
    res = Report.get_report_text(userid, qu_id, download_info)
    if not res:
        return jsonify({'code': 20000})
    return jsonify({'code': 20000, 'data': res})


@bp.route('/showFiles', methods=['GET'])
@token_auth.auth.login_required
@role_auth.check_auth_user
def show_photo():
    userid = request.values.get('userid') or session['userid']
    if request.method == 'GET':
        filename = request.values.get('filename')
        if filename:
            try:
                image_data = open(os.path.join(config.USER_FILE_PATH, userid, '%s' % filename), "rb").read()
                response = make_response(image_data)
                response.headers['Content-Type'] = 'image/png'
                return response
            except:
                return jsonify({'code': 20000})
    return jsonify({'code': 20000})


@bp.route('/showFilesCustom', methods=['GET'])
def show_photo_custom():
    if request.method == 'GET':
        filename = request.values.get('filename')
        if filename:
            try:
                image_data = open(os.path.join(config.SYSTEM_FILE_PATH, '%s' % filename), "rb").read()
                response = make_response(image_data)
                response.headers['Content-Type'] = 'image/png'
                return response
            except:
                return jsonify({'code': 20000})
    return jsonify({'code': 20000})


@bp.route('/uploadFiles', methods=['POST'], strict_slashes=False)
@token_auth.auth.login_required
@role_auth.check_auth_user
def api_upload():
    userid = request.form.get('userid') or session['userid']
    filename = request.form.get('filename')
    filename = os.path.join(config.USER_FILE_PATH, userid, filename)
    file_dir = os.path.dirname(filename)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    request.files['file'].save(filename)
    return jsonify({'code': 20000})


@bp.route('/uploadFilesAdmin', methods=['POST'], strict_slashes=False)
@token_auth.auth.login_required
@role_auth.check_auth_admin
def api_upload_admin():
    filename = request.form.get('filename')
    filename = os.path.join(config.SYSTEM_FILE_PATH, filename)
    file_dir = os.path.dirname(filename)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    request.files['file'].save(filename)
    return jsonify({'code': 20000})
