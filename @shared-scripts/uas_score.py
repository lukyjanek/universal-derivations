#!/usr/bin/env python3
# coding: utf-8

"""Calculate Unlabelled Attachement Score (UAS; F-measure) of the spannning."""

import argparse
from collections import defaultdict
from sklearn.metrics import f1_score


# parse input parameters
parser = argparse.ArgumentParser()
parser.add_argument('-a', action='store', dest='a', required=True,
                    help='path to the anotated data')
parser.add_argument('-pred', action='store', dest='p', required=True,
                    help='path to the predicted data')
parser.add_argument('-v', action='store', dest='v', required=False,
                    help='weight set for spanning')
parser.add_argument('-o', action='store', dest='o', required=False,
                    help='path to the file for returning UAS')
par = parser.parse_args()


# load data
def load_data(path):
    """Load annotated and predicted data."""
    data = defaultdict()
    with open(path, mode='r', encoding='U8') as f:
        for line in f:
            mark, parent, child = line.rstrip('\n').split('\t')
            data[(parent, child)] = True if mark == '+' else False
    return data


# load annotated and predicted data
annotated = load_data(par.a)
predicted = load_data(par.p)


# create lists
y_right, y_pred = list(), list()
for relation, mark in annotated.items():
    y_right.append(mark)
    y_pred.append(predicted.get((relation), False))


# evaluate UAS
F1 = f1_score(y_right, y_pred, average='macro')

# save result
with open(par.o, mode='a', encoding='U8') as f:
    f.write('Weight: ' + par.v + '\t' + 'UAS: ' + str(F1) + '\n')
