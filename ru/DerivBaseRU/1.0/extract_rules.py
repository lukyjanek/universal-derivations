#!/usr/bin/env python3
# coding: utf-8

"""Extract rules and their meaning from DerivBase.Ru."""

import re
import sys
from collections import defaultdict


data = defaultdict()
with open(sys.argv[1], mode='r', encoding='U8') as f:
    for line in f:
        feats = line.rstrip('\n').split('\t')[2]
        for item in feats.split('#'):
            rule, rule_process = item.split('&')
            rule_num = re.search(r'rule([0-9]*)', rule).group(1)
            rule_men = re.search(r'(.*?)(\(.*?\))', rule).group(2)
            if rule_num:
                data[rule_num] = (rule_men, rule_process)

with open(sys.argv[2], mode='w', encoding='U8') as f:
    for key in sorted(list(data), key=lambda x: int(x)):
        f.write('rule' + key + '\t' + data[key][0] + '\t' + data[key][1] + '\n')
