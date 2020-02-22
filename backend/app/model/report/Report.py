from app.model.report.qus import Mbti

obj_map = {
    '5e495cc421a85ca33b638d94': Mbti
}


def generate_report(qu_id, qu_data):
    obj = obj_map.get(qu_id)
    if not obj:
        return {}
    return obj.generate_report(qu_id, qu_data)


def download_report(userid, qu_id, download_info):
    obj = obj_map.get(qu_id)
    if not obj:
        return {}
    return obj.download_report(userid, qu_id, download_info)


def get_report_text(userid, qu_id, download_info):
    obj = obj_map.get(qu_id)
    if not obj:
        return {}
    return obj.get_report_text(userid, qu_id, download_info)
