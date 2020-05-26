#!/usr/bin/env python3
# coding: utf-8

"""Extract one-to-one relations in Finnish WordNet."""

import sys

relations = set()  # because of polysemy
with open(sys.argv[1], mode='r', encoding='utf-8') as f:
    for line in f:
        p_id, parent, c_id, child, mark, _ = line.split('\t')

        p_pos = p_id.split(':')[1][0].upper()
        c_pos = c_id.split(':')[1][0].upper()

        parent = parent + '_' + p_pos
        child = child + '_' + c_pos

        if mark == '+':
            if (parent, child) not in relations:
                relations.add((parent, child))
                print(parent, child, sep='\t')
