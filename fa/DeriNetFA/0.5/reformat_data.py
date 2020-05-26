#!/usr/bin/env python3
# coding: utf-8

"""Change format of the original data to DERINET_V1 format."""

import sys


# load the data and reorganize columns
with open(sys.argv[1], mode='r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\n').split(' ')

        if len(line) == 3:
            line.append('')

        print('\t'.join(line[:2]), '', '', line[3], sep='\t')
