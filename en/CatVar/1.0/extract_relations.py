#!/usr/bin/env python3
# coding: utf-8

"""Extract one-to-one relations in CatVar."""

import sys
import itertools as it


with open(sys.argv[1], mode='r', encoding='utf-8') as f:
    for line in f:
        entry = line.rstrip('\n').split('#')
        entry = [e.split('%')[0] for e in entry]
        [print(*relation, sep='\t') for relation in it.permutations(entry, 2)]
