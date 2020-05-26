#!/usr/bin/env python3
# coding: utf-8

"""Extract one-to-one relations in Estonian WordNet."""

import re
import sys
import xml.etree.ElementTree as ET


tree = ET.ElementTree(ET.parse(sys.argv[1]))

rels = set()  # because of polysemy
pos_dict = {'n': 'N', 'v': 'V', 'a': 'A', 'r': 'D'}

for descendant in tree.getroot().iter('LexicalEntry'):
    for entry in descendant.iter():
        if entry.tag == 'Lemma':
            child = entry.attrib['writtenForm'].replace('_', ' ')
            c_pos = pos_dict[entry.attrib['partOfSpeech']]

        if entry.tag == 'Sense':
            for s in entry.iter('SenseRelation'):
                if s.attrib['relType'] == 'derivation':
                    _, parent, p_pos = s.attrib['target'].split('-')
                    parent = parent.replace('_', ' ')
                    p_pos = pos_dict[re.sub(r'[0-9]*', '', p_pos)]

                    if (parent + '_' + p_pos, child + '_' + c_pos) not in rels:
                        rels.add((parent + '_' + p_pos, child + '_' + c_pos))

                        print(parent + '_' + p_pos,
                              child + '_' + c_pos,
                              sep='\t')
