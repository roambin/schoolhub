from app.dao import Questionnair


def get_qu(qu_id, dict_r=None):
    qu = Questionnair.get_by_id(qu_id, dict_r)
    if qu.get('_id'):
        qu['_id'] = str(qu['_id'])
    return qu


def set_qu(qu_id, dic=None):
    qu = Questionnair.update(qu_id, dic)
    return qu


def set_qu_info(qu_id, dic):
    if qu_id:
        return Questionnair.update(qu_id, dic)
    else:
        return Questionnair.add(dic)


def del_qu(qu_id):
    Questionnair.delete(qu_id)
    return True
