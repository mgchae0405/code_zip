# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from pandas.api.types import is_object_dtype
import numpy as np


def DB_save(source, table, table_name):  # TreeTable, CasesTable

    db_connection_str = """mysql+pymysql://%s:%s@%s/%s?charset=utf8""" % (source['user'],source['passwd'],source['host'],source['db'])

    for i in table:
        if is_object_dtype(table[i]):
            table[i] = table[i].astype('str')
        table[i] = table[i].replace('None', np.nan)

    # DB 연결
    db_connection = create_engine(db_connection_str, echo=False, poolclass=NullPool, encoding='utf8')
    conn = db_connection.connect()

    # 테이블화
    table.to_sql(name='%s' % table_name, con=db_connection, if_exists='replace', index=False)  # replace or append

    # DB 연결해제
    conn.close()
    db_connection.dispose()

    return print('Complete to create %s table' % table_name, source['host'])