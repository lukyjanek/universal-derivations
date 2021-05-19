#!/usr/bin/env python3
# coding: utf-8

"""Edit JSON-encoded column in the harmonised dataset."""

import sys
import json
from collections import defaultdict


# load IDs from the harmonised data
lexeme_id = defaultdict()
with open(sys.argv[1], mode='r', encoding='U8') as f:
    for line in f:
        line = line.rstrip('\n').split('\t')
        if len(line) > 1:
            lexeme_id[line[1]] = line[0]


# edit JSON-encoded column adn save the data
with open(sys.argv[1], mode='r', encoding='U8') as f:
    for line in f:
        line = line.rstrip('\n').split('\t')
        if len(line) > 1:
            original = json.loads(line[9])
            if original.get('was_in_family_with'):
                keys = [lexeme_id[lex]
                        for lex in original['was_in_family_with'].split('&')]
                original['was_in_family_with'] = ','.join(keys)
            if original.get('other_parents'):
                keys = [lexeme_id[lex.split('&')[0]]
                        for lex in original['other_parents'].replace('&Type=Derivation', '').split('|')]
                original['other_parents'] = '|'.join(keys)
            line[9] = json.dumps(original)
            print('\t'.join(line))
        else:
            print()
