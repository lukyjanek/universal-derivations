#!/usr/bin/env python3
# coding: utf-8

"""Extract one-to-one relations in Slovenian Sloleks."""

import sys
import xml.etree.ElementTree as ET


parser = ET.iterparse(sys.argv[1])

pos_dict = {'samostalnik': 'N', 'pridevnik': 'A', 'zaimek': 'R', 'medmet': 'I',
            'števnik': 'U', 'glagol': 'V', 'prislov': 'D', 'predlog': 'P',
            'veznik': 'C', 'členek': 'K', 'okrajšava': 'L', 'A5e2a': 'E',
            'večbesedna_enota': 'E'}

rels = set()  # because of repeating relations
for _, element in parser:
    if element.tag == 'LexicalEntry':
        parent = ''
        child = ''

        for entry in element.iter():
            if entry.tag == 'Lemma':
                parent = entry[0].attrib['val']
                p_pos = pos_dict[element[0].attrib['val']]
                parent += '_' + p_pos

            if entry.tag == 'RelatedForm':
                child = entry[2].attrib['val']
                c_pos = pos_dict[entry[1].attrib['val']]
                child += '_' + c_pos

                if parent != child and (parent, child) not in rels:
                    print(parent, child, sep='\t')
                    rels.add((parent, child))

        element.clear()
