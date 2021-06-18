#!/usr/bin/env python3
# coding: utf-8

"""Extract one-to-one relations in French Démonette."""

import sys
import xml.etree.ElementTree as ET
from collections import defaultdict


def construction(tag, entry):
    """Return construction of lemma."""
    pro = ''
    seg = ''
    rot = ''
    for i in entry.iter(tag):
        for j in i.iter():
            if j.tag == 'constructionalProcess':
                pro = j.text
            elif j.tag == 'constructionalExponent':
                seg = j.text
            elif j.tag == 'constructionalTheme':
                rot = j.text
    return (pro, seg, rot)


tree = ET.ElementTree(ET.parse(sys.argv[1]))
root = tree.getroot()

semantic_labels = defaultdict(set)
segmentations = defaultdict(set)
indirect = defaultdict(set)
directless = defaultdict(set)
relations = set()

for entry in root.iter('morphologicalRelation'):

    if entry[2][0].text == 'descendant':
        parent = entry[1][0].text
        p_pos = entry[1][1].text
        p_sem = entry[1][2].text
        p_pro, p_seg, p_rot = construction(tag='sourceFormConstruction',
                                           entry=entry)
        child = entry[0][0].text
        c_pos = entry[0][1].text
        c_sem = entry[0][2].text
        c_pro, c_seg, c_rot = construction(tag='targetFormConstruction',
                                           entry=entry)

    elif entry[2][0].text == 'ascendant':
        parent = entry[0][0].text
        p_pos = entry[0][1].text
        p_sem = entry[0][2].text
        p_pro, p_seg, p_rot = construction(tag='targetFormConstruction',
                                           entry=entry)
        child = entry[1][0].text
        c_pos = entry[1][1].text
        c_sem = entry[1][2].text
        c_pro, c_seg, c_rot = construction(tag='sourceFormConstruction',
                                           entry=entry)

    elif entry[2][0].text == 'indirect':
        p = entry[0][0].text + '_' + entry[0][1].text
        c = entry[1][0].text + '_' + entry[1][1].text
        indirect[p].add(c)
        indirect[c].add(p)

    else:
        p = entry[0][0].text + '_' + entry[0][1].text
        c = entry[1][0].text + '_' + entry[1][1].text
        directless[p].add(c)
        directless[c].add(p)

    semantic_labels[parent + '_' + p_pos].add(p_sem)
    semantic_labels[child + '_' + c_pos].add(c_sem)

    if p_pro != '' and p_seg != '' and p_rot != '':
        segmentations[parent + '_' + p_pos].add((p_pro, p_seg, p_rot))
    if c_pro != '' and c_seg != '' and c_rot != '':
        segmentations[child + '_' + c_pos].add((c_pro, c_seg, c_rot))

    relations.add((parent + '_' + p_pos, child + '_' + c_pos))


for rel in relations:
    p_sems = '|'.join(semantic_labels[rel[0]])
    c_sems = '|'.join(semantic_labels[rel[1]])

    p_segs = ['|'.join(i) for i in segmentations[rel[0]]]
    c_segs = ['|'.join(i) for i in segmentations[rel[1]]]

    p_inds = '|'.join(indirect[rel[0]])
    c_inds = '|'.join(indirect[rel[1]])

    p_dless = '|'.join(directless[rel[0]])
    c_dless = '|'.join(directless[rel[1]])

    print(*rel, p_sems, c_sems, '#'.join(p_segs), '#'.join(c_segs),
          p_inds, c_inds, p_dless, c_dless, sep='\t')
