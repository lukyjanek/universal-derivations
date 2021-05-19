#!/usr/bin/env python3
# coding: utf-8

"""Baseline for harmonising word-formation resources. For evaluation only."""

import argparse
from split_data import split_data
from sklearn.metrics import f1_score
from collections import defaultdict


# parse input parameters
parser = argparse.ArgumentParser()
parser.add_argument('-a', action='store', dest='a', required=True,
                    help='path to the anotated data')
parser.add_argument('-n', action='store', dest='n', required=True,
                    help='name of the resource')
parser.add_argument('-p', action='store', dest='p', required=True,
                    help='path to the data to predict weights')
parser.add_argument('-w', action='store', dest='w', required=True,
                    help='path to the file for returning weighted relations')
parser.add_argument('-fs', action='store', dest='f', required=True,
                    help='path to the file for returning F-score')
par = parser.parse_args()


# load annotated data
annot_data = list()
relations = list()
with open(par.a, mode='r', encoding='U8') as f:
    for line in f:
        lab, parent, child = line.rstrip('\n').split('\t')
        relations.append((parent, child))
        child = child.split('_')
        parent = parent.split('_')
        lab = True if lab == '+' else False
        annot_data.append({**{'parent': parent[0], 'parentPos': parent[1],
                              'child': child[0], 'childPos': child[1]},
                           **{'result': lab}})


# split annotated data on train/validation/holdout
divided = split_data(relations, train=0.65, validation=0.15, holdout=0.2,
                     random_seed=24)
for item in annot_data:
    parent = item['parent'] + '_' + item['parentPos']
    child = item['child'] + '_' + item['childPos']
    item['data'] = divided[(parent, child)]


# baseline
def train_baseline(train_dataset):
    """Return trained simple probabilistic model."""
    model = defaultdict(float)
    all_items = 0
    for item in train_dataset:
        model[item['parentPos']+'-'+item['childPos']] += 1
        all_items += 1
    for key in model:
        model[key] /= all_items
    return model


def baseline(entry, model):
    """Return weight for given relation."""
    return model.get(item['parentPos']+'-'+item['childPos'], 0)


# train simple probabilistic model
for_train = [item for item in annot_data if item['data'] == 'T']
trained = train_baseline(train_dataset=for_train)


# evaluate F-score on validation dataset
y_real_validation = list()
y_pred_validation = list()
for item in annot_data:
    if item['data'] == 'V':
        y_real_validation.append(item['result'])
        res = baseline(entry=item, model=trained)
        r = True if res > 0.5 else False
        y_pred_validation.append(r)
F1_validation = f1_score(y_real_validation, y_pred_validation, average='macro')


# evaluate F-score on holdhout dataset
y_real_holdout = list()
y_pred_holdout = list()
for item in annot_data:
    if item['data'] == 'H':
        y_real_holdout.append(item['result'])
        res = baseline(entry=item, model=trained)
        r = True if res > 0.5 else False
        y_pred_holdout.append(r)
F1_holdout = f1_score(y_real_holdout, y_pred_holdout, average='macro')


# save results
with open(par.f, mode='w', encoding='U8') as f:
    f.write('Resource:' + '\t' + par.n + '\n')
    f.write('F1-validation:' + '\t' + str(F1_validation) + '\n')
    f.write('F1-holdout:' + '\t' + str(F1_holdout) + '\n')
    f.write('\n')


# load predicted data
predicted_data = list()
with open(par.p, mode='r', encoding='U8') as f:
    for line in f:
        line = line.rstrip('\n').split('\t')
        child = line[1].split('_')
        parent = line[0].split('_')
        predicted_data.append({**{'parent': parent[0], 'parentPos': parent[1],
                                  'child': child[0], 'childPos': child[1]}})


# predict data
with open(par.w, mode='w', encoding='U8') as f:
    for item in predicted_data:
        f.write(item['parent'] + '_' + item['parentPos'] + '\t' +
                item['child'] + '_' + item['childPos'] + '\t' +
                str(baseline(item, model=trained)) + '\n')
