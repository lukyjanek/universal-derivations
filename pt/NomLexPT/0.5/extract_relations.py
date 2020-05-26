#!/usr/bin/env python3
# coding: utf-8

"""Extract one-to-one relations in Portuguese Nomlex-PT."""

import re
import sys


with open(sys.argv[1], mode='r', encoding='utf-8') as f:
    data = ''.join(f.readlines()).replace('\n', '')

rels = set()  # because of multiple occurence (due to more origins)
for entry in re.findall(r'(<Description .*?)(</Description>)', data):
    parent = re.search(r'(nomlex:verb.*?)"/', entry[0])
    child = re.search(r'(nomlex:noun.*?)"/', entry[0])

    if parent and child:
        parent = parent.group(1).split('-')[-1] + '_V'
        child = child.group(1).split('-')[-1] + '_N'

        if (parent, child) not in rels:
            rels.add((parent, child))
            print(parent, child, sep='\t')
