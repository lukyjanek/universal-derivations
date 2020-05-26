#!/usr/bin/env python3
# coding: utf-8

"""Train and test machine learning model to weight WF relations."""

import re
import os
import sys
import pickle
import argparse
from collections import defaultdict
from collections import OrderedDict

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import Perceptron
from sklearn.calibration import CalibratedClassifierCV
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import make_scorer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score

sys.path.append(os.path.realpath('../..'))
from feature_vector import make_vector  # noqa: E402


# parse input parameters
parser = argparse.ArgumentParser()
parser.add_argument('-a', action='store', dest='a', required=True,
                    help='path to the anotated data')
parser.add_argument('-l', action='store', dest='l', required=True,
                    help='frequency limit for n-grams')
parser.add_argument('-p', action='store', dest='p', required=False,
                    help='path to the data to predict weights')
parser.add_argument('-m', action='store', dest='m', required=False,
                    help='name of model to predict weights')
parser.add_argument('-perf', action='store', dest='perf', required=False,
                    help='path to save performance of the model')
parser.add_argument('-w', action='store', dest='w', required=False,
                    help='path to save file with weigted relations')
par = parser.parse_args()


# data
df = pd.DataFrame()
included_features = ('child', 'parent', 'childPos', 'parentPos', 'levDist',
                     'lengthDif', 'stOne', 'stTwo', 'enOne', 'enTwo',
                     'stTwChi', 'stThChi', 'stFoChi', 'stFiChi', 'stTwPar',
                     'stThPar', 'stFoPar', 'stFiPar', 'enTwPar', 'enThPar',
                     'enFoPar', 'enFiPar', 'enTwChi', 'enThChi', 'enFoChi',
                     'enFiChi')


# load manually annotated data
rows_list = list()
with open(par.a, mode='r', encoding='utf-8') as f:
    for line in f:
        lab, child, parent = line.rstrip('\n').split('\t')

        child = child.split('_')
        parent = parent.split('_')
        lab = 1 if lab == '+' else 0

        features = make_vector(parent=parent[0], parent_pos=parent[1],
                               child=child[0], child_pos=child[1])
        vector = OrderedDict()
        for key in included_features:
            vector[key] = features[key]
        vector = {**vector, **{'result': lab}}

        rows_list.append(vector)


# load data to predict (if given)
if par.p:
    with open(par.p, mode='r', encoding='utf-8') as f:
        for line in f:
            child, parent = line.rstrip('\n').split('\t')

            child = child.split('_')
            parent = parent.split('_')

            features = make_vector(parent=parent[0], parent_pos=parent[1],
                                   child=child[0], child_pos=child[1])
            vector = OrderedDict()
            for key in included_features:
                vector[key] = features[key]
            vector = {**vector, **{'result': np.nan}}

            rows_list.append(vector)

df = pd.DataFrame(rows_list)
df = df.reset_index(drop=True)


# convert types to bool
df['stOne'] = df['stOne'].astype('bool')
df['stTwo'] = df['stTwo'].astype('bool')
df['enOne'] = df['enOne'].astype('bool')
df['enTwo'] = df['enTwo'].astype('bool')


# one-hot n-grams
names_affixes = ('stTwChi', 'stThChi', 'stFoChi', 'stFiChi', 'stTwPar',
                 'stThPar', 'stFoPar', 'stFiPar', 'enTwPar', 'enThPar',
                 'enFoPar', 'enFiPar', 'enTwChi', 'enThChi', 'enFoChi',
                 'enFiChi')
for name in names_affixes:
    # make frequency list
    freq_list = defaultdict(int)
    for value in df[df['result'].isin([0, 1])][name]:
        freq_list[value] += 1

    # make list of high-frequency n-grams (with freq > limit l)
    allowed_grams = list()
    for gram, freq in freq_list.items():
        if freq > int(par.l) and gram != np.nan:
            allowed_grams.append(gram)

    # replace low-frequency grams to NaN
    new = df[name].apply(lambda i: i if i in allowed_grams else np.nan)

    # binarize new feature
    dummy = pd.get_dummies(new)
    for dum_name in dummy:
        df[name + '_' + dum_name] = dummy[dum_name].astype('bool')

    # remove input column
    df = df.drop(columns=name)


# binarize part-of-speech tags
for name in ('childPos', 'parentPos'):
    # binarize
    dummy = pd.get_dummies(df[name])
    for dum_name in dummy:
        df[name + '_' + dum_name] = dummy[dum_name].astype('bool')

    # remove input column
    df = df.drop(columns=name)


# remove child and parent strings
df = df.drop(columns='child')
df = df.drop(columns='parent')


# set evaluating metrics for cross-validations
scoring = {'f1': make_scorer(f1_score, average='macro'),
           'precision': make_scorer(precision_score, average='macro'),
           'recall': make_scorer(recall_score, average='macro'),
           'accuracy': make_scorer(accuracy_score)}


def print_evaluation(cros_val, model, right, name):
    """Print results of models."""
    with open(par.perf, mode='a', encoding='utf-8') as f:
        f.write('RESULTS: ' + name + '\n')
        # cross-validation
        f.write('c-v acc: ' + str(cros_val['test_accuracy']) +
                ' ' + str(np.mean(cros_val['test_accuracy'])) + '\n')
        f.write('c-v pre: ' + str(cros_val['test_precision']) +
                ' ' + str(np.mean(cros_val['test_precision'])) + '\n')
        f.write('c-v rec: ' + str(cros_val['test_recall']) +
                ' ' + str(np.mean(cros_val['test_recall'])) + '\n')
        f.write('c-v f1m: ' + str(cros_val['test_f1']) +
                ' ' + str(np.mean(cros_val['test_f1'])) + '\n')
        # standard output model
        f.write('model CMX:\n')
        f.write(str(confusion_matrix(right, model)) + '\n')
        f.write('model acc: ' + str(accuracy_score(right, model)) + '\n')
        f.write('model pre: ' + str(precision_score(right, model,
                                                    average='macro')) + '\n')
        f.write('model rec: ' + str(recall_score(right, model,
                                                 average='macro')) + '\n')
        f.write('model f1m: ' + str(f1_score(right, model,
                                             average='macro')) + '\n')
        f.write('\n')


# split data to predict
dataset_to_predict = df[df['result'].isnull()]
del dataset_to_predict['result']
x_predict = np.array(dataset_to_predict)


# split data (test evaluate = 0.1 ; train = 0.9)
df = df[df['result'].isin([0, 1])]
df['result'] = df['result'].astype('bool')

x = np.array(df[[col for col in df if col != 'result']])
y = np.array(df.result)

x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                    test_size=0.1,
                                                    random_state=24)
y_train = y_train.ravel()
y_test = y_test.ravel()


# define models
classif = [
    ('Gaussian Naive Bayes', GaussianNB()),
    ('LOGistic Regression', LogisticRegression(solver='liblinear',
                                               multi_class='ovr',
                                               penalty='l1',
                                               random_state=24)),
    ('Multi-Layer Perc', MLPClassifier(alpha=1,
                                       max_iter=10000,
                                       solver='sgd',
                                       random_state=24)),
    ('Perceptr', CalibratedClassifierCV(Perceptron(max_iter=5,
                                                   tol=-np.infty,
                                                   random_state=24),
                                        cv=10, method='isotonic')),
    ('Decision Tree', DecisionTreeClassifier(min_samples_split=5,
                                             random_state=24))
]


# machine learning
models = dict()
for name, model in classif:
    name = ''.join(re.findall(r'[A-Z]', name))
    # selected model
    if par.m and par.m != name:
        continue

    # train and test 5-fold cross-validations
    cv = cross_validate(model, x, y.ravel(), scoring=scoring, cv=5,
                        return_train_score=False)

    # train and test output model
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    # evaluate all
    if par.perf:
        print_evaluation(cv, y_pred, y_test, name)

    # local save of model
    models[name] = model


# predict weights
if par.p and par.m and par.w:
    if par.m in models:
        # predict
        y_prob = models[par.m].predict_proba(x_predict)
        # save weights
        with open(par.p, mode='r', encoding='utf-8') as f, \
                open(par.w, mode='w', encoding='utf-8') as g:
            for line, weight in zip(f, y_prob):
                relation = line.rstrip('\n').split('\t')
                relation.append(str(weight[1]))
                g.write('\t'.join(relation) + '\n')
