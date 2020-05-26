#!/usr/bin/env python3
# coding: utf-8

"""Extract one-to-one relations from DerivBase.Ru."""

import sys
from collections import defaultdict


# load lemma set
lemmas = set()
for path in sys.argv[1].split('\n'):
    with open(path, mode='r', encoding='U8') as f:
        lemmas.update(f.read().split('\n'))

# load connections
relations = defaultdict(list)
pos = {'adj': 'A', 'noun': 'N', 'verb': 'V', 'adv': 'D', 'num': 'C'}
for path in sys.argv[2].split('\n'):
    with open(path, mode='r', encoding='U8') as f:
        for line in f:
            line = line.strip().split('\t')
            line[0] = line[0] + '_' + pos[line[1]]
            line[2] = line[2] + '_' + pos[line[3]]
            relations[(line[0], line[2])].append('&'.join(line[-2:]))

# print relations
with open(sys.argv[3], mode='w', encoding='U8') as f:
    for rel, info in relations.items():
        parent, child = rel
        info = '#'.join(info)
        lemmas.discard(parent)
        lemmas.discard(child)
        f.write('\t'.join([parent, child, info]) + '\n')

# print singletons
with open(sys.argv[4], mode='w', encoding='U8') as f:
    for singleton in lemmas:
        f.write(singleton + '\n')
