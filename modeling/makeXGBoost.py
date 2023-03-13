# -*- coding: utf-8 -*-


import pandas as pd
from xgboost import XGBRegressor
from sklearn.impute import KNNImputer


# XGBoost Modeling

def MakeXGBoost(PivotTable):
    # z_score를 이용해 점수의 이상치 처리 ( 평균-2*표준편차 < x < 평균+2*표준편차 )
    mean_rank = PivotTable['jumsu1'].mean()
    std_rank = PivotTable['jumsu1'].std()
    df_com_pivot_label = PivotTable[
        ((mean_rank - (2 * std_rank)) < PivotTable['jumsu1']) & (PivotTable['jumsu1'] < (mean_rank + (2 * std_rank)))]

    # immputation 오류 때문에 user_id를 index로 설정
    df_com_pivot_label = df_com_pivot_label.set_index('user_id')

    # KNN_impute (k=30)
    KNN_imputer = KNNImputer(n_neighbors=30, weights='uniform')

    imputing_table = pd.DataFrame(KNN_imputer.fit_transform(df_com_pivot_label),
                                  columns=df_com_pivot_label.columns[~df_com_pivot_label.columns.isin(
                                      df_com_pivot_label.isnull().sum()[
                                          df_com_pivot_label.isnull().sum() == len(df_com_pivot_label)].index)])

    # 식별하기 위해 인덱스 유저ID로 설정
    imputing_table['user_id'] = df_com_pivot_label.index
    imputing_table = imputing_table.set_index('user_id')

    X = imputing_table.drop('jumsu1', axis=1)  # 독립변수
    y = imputing_table[['jumsu1']]  # 종속변수

    # XGBoost 모델 선언
    xgbr = XGBRegressor(booster='gbtree',
                        n_estimators=100,
                        learning_rate=0.1,
                        objective='reg:squarederror',
                        random_state=42
                        )

    xgbr.fit(X, y)  # 모델 학습

    return xgbr, X, y

