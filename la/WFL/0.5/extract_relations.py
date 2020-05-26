#!/usr/bin/env python3
# coding: utf-8

"""Extract relations in Latin WFL."""

import sys
from collections import defaultdict


# load lemmario
lemmario = defaultdict()
with open(sys.argv[1], mode='r', encoding='utf-8') as f:
    for line in f:
        entry = line.rstrip('\n').split('\t')
        lemmario[entry[0]] = entry[1:]


# load and extract relations
pos = {'I': 'I', 'N': 'N', 'N1': 'N1', 'N2': 'N2', 'N4': 'N4', 'N5': 'N5',
       'V1': 'V1', 'V2': 'V2', 'V3': 'V3', 'V4': 'V4', 'V5': 'V5', 'VA': 'VA',
       'VP': 'VP', 'N3A': 'A2', 'N3B': 'N3', 'N2/1': 'A1', 'PR': 'PR',
       'NY': 'A', 'V': 'V'}
with open(sys.argv[2], mode='r', encoding='utf-8') as f:
    for line in f:
        entry = line.rstrip('\n').split('\t')
        wfr, chi_id, par_id, order, category, process, affix = entry

        # parent
        parent = lemmario[par_id][0] + '_' + pos[lemmario[par_id][1]] + '_'
        parent += '_'.join(lemmario[par_id][2:4]) + '_' + par_id
        parent = parent.replace('\\', '')

        # child
        child = lemmario[chi_id][0] + '_' + pos[lemmario[chi_id][1]] + '_'
        child += '_'.join(lemmario[chi_id][2:4]) + '_' + chi_id
        child = child.replace('\\', '')

        print(parent, child, order, category, process, affix, sep='\t')
