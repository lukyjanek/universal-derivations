#!/usr/bin/env python3
# coding: utf-8

"""Extract one-to-one relations in DerivBase."""

import sys


with open(sys.argv[1], mode='r', encoding='utf-8') as f:
    for line in f:
        rel = line.rstrip('\n').split(' ')[3:]

        rule_i = 1
        while rule_i < len(rel):
            # clean verbs according to documntation
            if '_V' in rel[rule_i - 1]:
                lemma, _ = rel[rule_i - 1].split('_')
                rel[rule_i - 1] = lemma + '_V'
            if '_V' in rel[rule_i + 1]:
                lemma, _ = rel[rule_i + 1].split('_')
                rel[rule_i + 1] = lemma + '_V'
            # print relations
            if '*' in rel[rule_i]:
                rel[rule_i] = rel[rule_i].replace('*', '')
                print(rel[rule_i + 1], rel[rule_i - 1], rel[rule_i], sep='\t')
            else:
                print(rel[rule_i - 1], rel[rule_i + 1], rel[rule_i], sep='\t')
            rule_i += 2
