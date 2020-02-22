from pymysql import escape_string as pymysql_escape_string


def escape_string(value, mapping=None):
    return pymysql_escape_string(value, mapping)
