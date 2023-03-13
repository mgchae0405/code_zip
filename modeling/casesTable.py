# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from copy import deepcopy
import ast

# db 내 트리 전위탐색 코드
def pre_order(node, child, solve, value, dct, TreeTable):

    if not TreeTable[TreeTable['node_id'] == node]['child'].isna().values:
        child = ast.literal_eval(str(child))
        dct[TreeTable[TreeTable['node_id'] == node]['problem_id'].iloc[0]] = 0

        copy_dct = deepcopy(dct)

        pre_order(child[0], TreeTable[TreeTable['node_id'] == child[0]]['child'].iloc[0], solve, value, copy_dct, TreeTable)

        dct[TreeTable[TreeTable['node_id'] == node]['problem_id'].iloc[0]] = 1
        copy_dct = deepcopy(dct)
        pre_order(child[1], TreeTable[TreeTable['node_id'] == child[1]]['child'].iloc[0], solve, value, copy_dct, TreeTable)

    else:
        solve.append(dct)
        value.append(TreeTable[TreeTable['node_id'] == node]['score'].iloc[0])



    ### 경우의 수 테이블
def CreateCasesTable(TreeTable, X): #####################################

    # 전위순회 탐색을 통해 트리 경우의 수 저장
    solve = []  # 각 문제풀이 결과가 들어갈 리스트
    value = []  # 리프노드의 value가 들어갈 리스트
    dct = {}

    # 첫번째 노드 0은 default로 추후 설정, child로 변수명으로 저장 후 실행 ,dct 는 비어있는 dict
    pre_order(0, TreeTable[TreeTable['node_id'] == 0]['child'].iloc[0], solve, value, dct, TreeTable)

    # Cases Table 생성
    CasesTable = pd.DataFrame(solve)
    col_list = X.astype(str)[~X.astype(str).isin(CasesTable.columns.astype(str).tolist())]

    for x in col_list:
        CasesTable[f'{x}'] = np.nan
    CasesTable['y'] = value
    return CasesTable
