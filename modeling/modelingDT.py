# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.impute import KNNImputer


# DecisionTree Modeling

def MakeDecisionTree(Tree_table):
    # 문제풀이 피벗테이블과 모의고사 점수 테이블 merge
    # Tree_table = table1.merge(table2, left_on='user_id', right_on='user_id').set_index('user_id')

    # 등급과 학년 컬럼 drop
    Tree_table = Tree_table.iloc[:, :-2]

    # KNN_impute
    KNN_imputer = KNNImputer(n_neighbors=1, weights='uniform')

    imputing_table = pd.DataFrame(KNN_imputer.fit_transform(Tree_table),
                                  columns=Tree_table.columns[~Tree_table.columns.isin(
                                      Tree_table.isnull().sum()[Tree_table.isnull().sum() == len(Tree_table)].index)])

    X = imputing_table.iloc[:, 0:-1]  # 독립변수
    y = imputing_table[['jumsu1']]  # 종속변수

    # 모델 선언
    dtr = DecisionTreeRegressor(ccp_alpha=0.0,
                                criterion='mse',
                                max_depth=None,
                                max_features=None,
                                max_leaf_nodes=None,
                                min_impurity_decrease=0.0,
                               # min_impurity_split=None,
                                min_samples_leaf=1,
                                min_samples_split=2,
                                min_weight_fraction_leaf=0.0,
                                random_state=42,
                                splitter='best')

    dtr.fit(X, y)  # 모델 학습


    return dtr, X, y