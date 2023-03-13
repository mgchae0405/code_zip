# -*- coding: utf-8 -*-


import pandas as pd
import pymysql
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import DBSave
import connInfo
import random

########## 추후 데이터베이스를 DataScience에서 DS로 변경

# 문제 풀이시간 긴 애들 아웃라이어 제거
def sent_solved(curriculum, lecture_id):
    conn = pymysql.connect( user = 'data',   passwd = '!1qaz@2wsx',  host= '110.10.129.177', db = 'AI',  charset = 'utf8')
    try:
        with conn.cursor() as cursor:
            # 쿼리문은 비공개
            # sql1 = """ query """ %(curriculum, lecture_id)
            cursor.execute(sql1)
            res1 = cursor.fetchall()

            src_cursor = conn.cursor()
            sql_col = "SHOW FULL COLUMNS FROM ``"
            src_cursor.execute(sql_col)
            col_df1 = pd.DataFrame(src_cursor.fetchall())

            conn.commit()

            # sql2 = """ query """ %(curriculum, lecture_id)
            cursor.execute(sql2)
            res2 = cursor.fetchall()

            src_cursor = conn.cursor()
            sql_col = "SHOW FULL COLUMNS FROM ``"
            src_cursor.execute(sql_col)
            col_df2 = pd.DataFrame(src_cursor.fetchall())

            conn.commit()

    finally:
        conn.close()

    conn = pymysql.connect( user = 'mct',   passwd = '1234',  host= '192.168.0.86', db = 'DS',  charset = 'utf8')
    try:
        with conn.cursor() as cursor:

            # sql3 = """ query """ %(curriculum, lecture_id)

            cursor.execute(sql3)
            res3 = cursor.fetchall()

            src_cursor = conn.cursor()
            sql_col = "SHOW FULL COLUMNS FROM ``"
            src_cursor.execute(sql_col)
            col_df3 = pd.DataFrame(src_cursor.fetchall())

            conn.commit()

    finally:
        conn.close()

    prob_set = pd.DataFrame(res1)
    prob_set.columns=col_df1[0]
    prob_set.drop(['limit_time', 'feature_id', 'problem_id', 'insert_date'], axis=1, inplace=True)
    prob_set.rename(columns={'updated' : 'set_date', 'no' : 'set_id'}, inplace=True)

    send = pd.DataFrame(res2)
    send.columns=col_df2[0]
    send = send[['curriculum', 'user_id', 'lecture_id', 'date', 'updated', 'isquizsend']]
    send.rename(columns={'updated' : 'alarm_sent', 'isquizsend' : 'set_id'}, inplace=True)

    quiz = pd.DataFrame(res3)
    quiz.columns=col_df3[0]
    quiz.rename(columns={'insert_date' : 'solved_date'}, inplace=True)

    # 'alarm_sent' : 카톡 알림이 발송된 시간
    df1 = send[send['date'] != send['alarm_sent']].drop('date', axis=1)

    # SyntaxAnswers 테이블
    # 'updated' : 문제 푼 시간
    prob_set = prob_set.drop(['user_id', 'lecture_id', 'curriculum', 'mode'], axis=1)

    # SyntaxAnwers 테이블의 'set_id'와 SyntaxProblemSets 테이블의 'no' columns으로 merge
    df2 = pd.merge(prob_set, quiz, on='set_id')

    duration = pd.merge(df1, df2, on = ['user_id', 'lecture_id', 'set_id'])
    duration['lecture_id'] = pd.to_numeric(duration['lecture_id'])
    duration['duration'] = duration['solved_date'] - duration['alarm_sent']

    Q3 = duration['duration'].quantile(0.75)

    group4 = duration[duration["duration"] > Q3].reset_index(drop=True)
    quiz = quiz[~quiz['set_id'].isin(group4['set_id'])]

    return quiz


def make_Pivot():
    conn = pymysql.connect(host='192.168.0.86', user='mct', password='1234', db='DS', charset='utf8')
    try:
        with conn.cursor() as cursor:
            sql_score = "select * from ``;"
            cursor.execute(sql_score)
            score_table = cursor.fetchall()
            conn.commit()

            sql_score2 = "show columns from ``;"
            cursor.execute(sql_score2)
            score_col = cursor.fetchall()
            conn.commit()
    finally:
        conn.close()
    score_table = pd.DataFrame(score_table, columns=pd.DataFrame(score_col)[0]) # 학생 점수 테이블

    curriculum_list = ['startup','buildup','essential']
    for x in curriculum_list:
        for i in range(1,41):
            res_table = sent_solved(x, i)
            res_table2 = res_table.sort_values(['no','solved_date']).reset_index(drop=True)

            if len(res_table2)>0: # 해당 커리큘럼과 강의에 해당하는 문제풀이 데이터가 존재한다면
                res_table2 = res_table2.groupby(['user_id','parent'])['choice_result'].first().reset_index() # 유저 별 첫 문제풀이만 선택
                res_table2 = res_table2.pivot_table(index='user_id', columns='parent', values='choice_result', dropna=True).replace(-1,0) # 피벗테이블로 만들기
                res_table2.columns.name = None # 컬럼 이름 제거
                res_table2 = res_table2.reset_index()

                # 임의의 y값 제거 후 score 있는 학생 데이터로 테이블 생성
                res_table2 = res_table2.merge(score_table, left_on='user_id', right_on='user_id').set_index('user_id')

                DBSave.DB_save(connInfo.PIVOT_source, res_table2, table_name=f"{x}_{i}_pivot")
                DBSave.DB_save(connInfo.web_PIVOT_source, res_table2, table_name=f"{x}_{i}_pivot")


                # DB에 저장하는 함수 넣을 것!!!


                print(f"{x}_{i}_pivot"+' complete')

