#!/usr/bin/env python3
# coding: utf-8

"""Harmonize part-of-speech values."""

import sys


pos = {'N': 'NOUN', 'A': 'ADJ', 'V': 'VERB', 'D': 'ADV'}
with open(sys.argv[1], mode='r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\n').split('\t')

        if len(line) == 1:
            print()
        else:
            line[3] = pos[line[3]]
            print(*line, sep='\t')
