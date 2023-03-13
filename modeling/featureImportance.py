# -*- coding: utf-8 -*-


# FEATURE IMPORTANCE
import pandas as pd
from eli5 import show_weights
from eli5.sklearn import PermutationImportance


def FeatureImportance(xgbr, X, y):
    perm = PermutationImportance(xgbr, scoring='r2', random_state=42).fit(X, y)
    w = show_weights(perm, feature_names=X.columns.astype(str).tolist(), top=len(X.columns) + 1)
    result = pd.read_html(w.data)[0]

    result['Weight'] = result['Weight'].apply(lambda x: float(x.split('±')[0].strip()))
    result = result[result['Weight'] > 0]

    return result

