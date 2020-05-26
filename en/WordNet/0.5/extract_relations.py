#!/usr/bin/env python3
# coding: utf-8

"""Extract one-to-one relations in Princeton WordNet."""

import sys
import csv


memory_polysemy = set()  # because of polysemy in wordnet
relations = list()

pos_dict = {'1': 'N', '2': 'V'}
with open(sys.argv[1], mode='r', encoding='utf-8') as f:
    csv_reader = csv.reader(f, delimiter=',')
    next(csv_reader)
    for line in csv_reader:
        if len(line) != 7:
            continue

        parent, p_id = line[0].replace('_', ' ').split('%')
        p_pos = pos_dict[p_id[0]]
        parent = parent + '_' + p_pos

        child, ch_id = line[3].replace('_', ' ').split('%')
        ch_pos = pos_dict[ch_id[0]]
        child = child + '_' + ch_pos

        if (parent, child) not in memory_polysemy:  # exclude polysemy
            relations.append((parent, child))
            memory_polysemy.add((parent, child))
            print(parent, child, line[2], sep='\t')
