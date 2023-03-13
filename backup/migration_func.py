# -*- coding: utf-8 -*-


import pandas as pd
import pymysql


# 행 길이 구하기
def row_num(source,table_name):
    conn = pymysql.connect(host=source['host'], user=source['user'], password=source['passwd'], db=source['db'], charset='utf8')

    try:
        with conn.cursor() as cursor:
            sql = """SELECT max(no) FROM `%s`;""" % table_name
            cursor.execute("set names utf8")
            cursor.execute(sql)
            count = cursor.fetchall()
            conn.commit()
    except:
        count = [[0]]  # table이 존재하지 않을 때
    finally:
        conn.close()

    max_row = count[0][0]
    return max_row


# table column명 불러오기
def call_col(source, table_name):
    conn = pymysql.connect(host=source['host'], user=source['user'], password=source['passwd'], db=source['db'], charset='utf8')
    try:
        with conn.cursor() as cursor:
            sql = """show columns from %s;""" % table_name
            cursor.execute("set names utf8")
            cursor.execute(sql)
            col = cursor.fetchall()
            conn.commit()
    finally:
        conn.close()

    columns = pd.DataFrame(col)[0]
    return columns