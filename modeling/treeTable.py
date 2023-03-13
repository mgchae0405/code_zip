# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

# scikit learn 에서 제공해주는 Tree 정보를 활용하여 탐색할 수 있는 형태로 db화  
def CreateTreeTable(dtr, X):
    n_nodes = dtr.tree_.node_count  # 노드의 개수
    children_left = dtr.tree_.children_left  # 왼쪽으로 뻗는 가지의 순서
    children_right = dtr.tree_.children_right  # 오른쪽으로 뻗는 가지의 순서
    feature = dtr.tree_.feature  # 피쳐의 인덱스값
    threshold = dtr.tree_.threshold  # 임계치
    feature_names = X.columns.astype(str)  # 피쳐 이름

    node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
    is_leaves = np.zeros(shape=n_nodes, dtype=bool)
    stack = [(0, -1)]  # seed is the root node id and its parent depth
    tree_lst = []

    while len(stack) > 0:
        node_id, parent_depth = stack.pop()
        node_depth[node_id] = parent_depth + 1

        # If we have a test node
        if (children_left[node_id] != children_right[node_id]):
            stack.append((children_left[node_id], parent_depth + 1))
            stack.append((children_right[node_id], parent_depth + 1))
        else:
            is_leaves[node_id] = True

    for i in range(n_nodes):
        # 리프노드 일 때
        if is_leaves[i]:
            tree_lst.append([i,  # 노드ID
                             None,  # 문제ID
                             None,  # 자식노드
                             int(dtr.tree_.value.reshape(1, -1)[0][i]),  # 리프노드의 점수
                             node_depth[i],  # 노드 깊이
                             None])  # 중간 점수 (임계치)
        # 리프노드 아닐 때
        else:
            tree_lst.append([i,  # 노드ID
                             feature_names[feature[i]],  # 문제ID
                             [children_left[i], children_right[i]],  # 자식노드
                             None,  # 리프노드의 점수
                             node_depth[i],  # 노드 깊이
                             int(dtr.tree_.value.reshape(1, -1)[0][i])])  # 중간 점수 (임계치)

    TreeTable = pd.DataFrame(tree_lst, columns=['node_id', 'problem_id', 'child', 'score', 'depth', 'middle_score'])

    # 부모노드 찾기
    lst_parent = []
    for i in range(1, len(TreeTable)):
        for j in range(0, i):
            if TreeTable['child'].iloc[j] is None:
                continue
            elif TreeTable['node_id'].iloc[i] in TreeTable['child'].iloc[j]:
                lst_parent.append(TreeTable['node_id'].iloc[j])

    lst_parent.insert(0, None)
    TreeTable['parent'] = lst_parent

    # 컬럼 위치 정렬
    TreeTable = TreeTable[['node_id', 'problem_id', 'parent', 'child', 'depth', 'middle_score', 'score']]

    return TreeTable