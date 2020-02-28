# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 16:20:19 2020

@author: hejiew
"""

import numpy as np
import pandas as pd



df = pd.read_csv('sc50.csv', index_col=0)

X = df.values
y = df.index

y1 = np.asarray([i.split('-')[-1] for i in y])
y2 = np.asarray([i.split('-')[-2] for i in y])

Y = np.concatenate([y1[:,None], y2[:, None]], axis=1)



from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import RidgeClassifierCV
from sklearn.svm import SVC


# Split dataset to 8:2
X_train, X_test, Y_train ,Y_test = train_test_split(X, y1, test_size=0.2)

clf_rf = RandomForestClassifier().fit(X_train, Y_train)
print('====  RandomForest  ====')
print(clf_rf.score(X_train, Y_train) )
print(clf_rf.score(X_test, Y_test) )
print('-' * 30)

clf_et = ExtraTreesClassifier().fit(X_train, Y_train)
print('====  ExtraTrees  ====')
print(clf_et.score(X_train, Y_train) )
print(clf_et.score(X_test, Y_test) )
print('-' * 30)

clf_rl = RidgeClassifierCV(alphas=[1e-3, 1e-2, 1e-1, 1]).fit(X_train, Y_train)
print('====  Ridge  ====')
print(clf_rl.score(X_train, Y_train) )
print(clf_rl.score(X_test, Y_test) )
print('-' * 30)

clf_svm = SVC().fit(X_train, Y_train)
print('====  SVC  ====')
print(clf_svm.score(X_train, Y_train) )
print(clf_svm.score(X_test, Y_test) )
print('-' * 30)

Y_pred = clf_rl.predict(X_test)


wrong_case = []
for i, (y_test, y_pred) in enumerate(zip(Y_test, Y_pred)):
    if y_test != y_pred:
       wrong_case.append(i) 