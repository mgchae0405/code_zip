# -*- coding: utf-8 -*-

import migration_func
import DBSave

import pymysql
import pandas as pd
import time


def backup_table(max_row, my_max_row, table_name, flg, origin_source ,ds_source):

    for i in range(my_max_row // flg, (max_row // flg) + 1):
        conn = pymysql.connect(host=origin_source['host'], user=origin_source['user'], password=origin_source['passwd'], db=origin_source['db'],
                               charset='utf8')
        try:
            with conn.cursor() as cursor:
                # insert, create 모든 경우를 대비한 쿼리
                sql = """SELECT * FROM `%s` where no > %d and no < %d ;""" % (table_name, i * flg if i * flg >= my_max_row else my_max_row,  (i + 1) * flg + 1)
                print(sql)
                cursor.execute("set names utf8")
                cursor.execute(sql)
                table = cursor.fetchall()
                conn.commit()
        finally:
            conn.close()

        df_test = pd.DataFrame(table)
        df_test.columns = migration_func.call_col(origin_source, table_name)

        #workstation에 저장
        DBSave.DB_save(ds_source, df_test, "backup_"+table_name)

        #30분 단위로 실행
        time.sleep(1800)
