from app.dao import Organization, User


def get_ogs(userid):
    user_info = User.get_by_id(userid).get('user_info') or {}
    role = user_info.get('role') or 1
    if role >= 100:
        res = Organization.get_iter()
        res = list(res)
        for e in res:
            e['_id'] = str(e['_id'])
        return res
    else:
        res = Organization.get_by_name(user_info.get('org'))
        if not res:
            return []
        res['_id'] = str(res['_id'])
        return [res]


def get_ogs_name():
    res = Organization.get_iter(None, {'_id': 0, 'org_name': 1, 'sub_orgs': 1})
    res = list(res)
    return res


def add_org(org):
    has_org = Organization.get_by_name(org.get('org_name')) is not None
    if has_org:
        return False
    return Organization.add(org)


def set_org(org_id, org):
    del org['_id']
    old_org = Organization.get_by_id(org_id)
    if old_org.get('org_name') != org.get('org_name'):
        User.update({'user_info.org': old_org.get('org_name')}, {'$set': {'user_info.org': org.get('org_name')}})
    return Organization.update_by_id(org_id, org)


def del_org(org_id):
    Organization.delete_by_id(org_id)
    return True


def get_sub_orgs(userid, data_filter):
    user_info = User.get_by_id(userid, ['user_info']).get('user_info')
    role = user_info.get('role') or 1
    if role >= 100:
        org = data_filter.get('user_info').get('org')
        if org:
            res = Organization.get_by_name(org).get('sub_orgs') or []
            return res
        list = []
        res = Organization.get_iter()
        for e in res:
            cur_list = e.get('sub_orgs') or []
            list.extend(cur_list)
        return list
    elif 4 <= role < 100:
        res = Organization.get_by_name(user_info.get('org')).get('sub_orgs') or []
        return res
    else:
        return []
