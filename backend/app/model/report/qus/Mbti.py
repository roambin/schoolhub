from flask import json, send_from_directory
from public import config
from app.model import User, Questionnair

__json_map = '[["I", "E"], ["S", "N"], ["E", "I"], ["F", "T"], ["S", "N"], ["J", "P"], ["E", "I"]' \
            ', ["N", "S"], ["F", "T"], ["E", "I"], ["N", "S"], ["T", "F"], ["P", "J"], ["N", "S"]' \
            ', ["N", "S"], ["N", "S"], ["F", "T"], ["P", "J"], ["I", "E"], ["F", "T"], ["F", "T"]' \
            ', ["J", "P"], ["P", "J"], ["S", "N"], ["E", "I"], ["T", "F"], ["J", "P"], ["E", "I"]' \
            ', ["F", "T"], ["P", "J"], ["N", "S"], ["P", "J"], ["I", "E"], ["P", "J"], ["E", "I"]' \
            ', ["F", "T"], ["J", "P"], ["F", "T"], ["E", "I"], ["S", "N"], ["F", "T"], ["J", "P"]' \
            ', ["E", "I"], ["N", "S"]]'
mbti_opt_map = json.loads(__json_map)
report_file_path = config.RESOURCE_PATH + 'report/mbti/'


def generate_report(qu_id, qu_data):
    count = {'E': 0, 'I': 0, 'N': 0, 'S': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
    for i in range(len(qu_data)):
        cur_map = mbti_opt_map[i]
        v = cur_map[qu_data[i] - 1]
        count[v] += 1
    mbti_type = ''
    for k, v in count.items():
        if v > 5:
            mbti_type += k
    qu_report = {
        'report_preview': mbti_type,
        'report_data': {'type': mbti_type, 'count': count}
    }
    return qu_report


def download_report(userid, qu_id, download_info):
    is_admin = User.__is_admin(userid)
    if not is_admin:
        qu = User.get_qu(userid, qu_id) or {}
        info = qu.get('info') or {}
        if info.get('auth') != 2:
            return None
    report_type = download_info.get('type')
    if not report_type:
        return None
    try:
        report_file = send_from_directory('../' + config.RESOURCE_PATH + 'report/mbti/', report_type + '.pdf', as_attachment=True)
    except:
        return None
    return report_file


def get_report_text(userid, qu_id, download_info):
    is_admin = User.__is_admin(userid)
    if not is_admin:
        qu = User.get_qu(userid, qu_id) or {}
        info = qu.get('info') or {}
        if info.get('auth') != 2:
            return None
    report_type = download_info.get('type')
    if not report_type:
        return None
    res = Questionnair.get_qu(qu_id, ['qu_report_map'])
    report_text = res.get('qu_report_map') or {}
    report_text = report_text.get(report_type)
    return report_text
