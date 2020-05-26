#!/usr/bin/env python3
# coding: utf-8

"""Extract one-to-one relations in DerIvaTario."""

import sys
import itertools as it
from collections import defaultdict


annotation = defaultdict()
families = defaultdict(set)

# load data
translate = {'S': 'N', 'V': 'V', 'G': 'A', 'B': 'D',
             'E': 'E', 'N': 'N', 'NU': 'X', 'V@': 'V'}
with open(sys.argv[1], mode='r', encoding='utf-8') as f:
    for line in f:
        entry, pos = line.rstrip('\n').split('\t')

        pos = translate[pos]
        lemma = entry.split(';')[1] + '_' + pos

        families[entry.split(';')[2]].add(lemma)
        annotation[lemma] = tuple(entry.split(';') + [pos])


# save singletons
with open(sys.argv[3], mode='w', encoding='U8') as f:
    for lemma in families['BASELESS:unrec']:
        f.write(lemma + '\t' + ';'.join(annotation[lemma]) + '\n')
del families['BASELESS:unrec']

# save relations
with open(sys.argv[2], mode='w', encoding='U8') as f:
    for root, lemmas in families.items():
        for parent, child in it.permutations(lemmas, 2):
            f.write(parent + '\t' + child + '\t' +
                    ';'.join(annotation[parent]) + '\t' +
                    ';'.join(annotation[child]) + '\n')
