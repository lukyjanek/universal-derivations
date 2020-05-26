#!/usr/bin/env python3
# coding: utf-8

"""Extract one-to-one relations in Dutch CELEX."""

import sys
import itertools as it
from collections import defaultdict


# translate pos
translate = {'N': 'N', 'V': 'V', 'A': 'A', 'B': 'D', 'D': 'X', 'F': 'A',
             'Q': 'C', 'O': 'P', 'R': 'N', 'C': 'C', 'X': 'X', 'P': 'P',
             'I': 'X', 'E': 'A'}

base = defaultdict(list)
lemma_full = defaultdict()
lemma_base = defaultdict()
annotation = defaultdict()
comp_base = defaultdict(list)
comp_full = defaultdict(list)
compounds = list()
singletons = set()
# load lemmas and pos from data
with open(sys.argv[1], mode='r', encoding='utf-8') as f:
    for line in f:
        entry = line.rstrip('\n').split('\\')

        lid = entry[0]
        lemma = entry[1]
        tree = entry[12]
        step = entry[8].split('+')
        form = list(entry[9])

        # empty struct
        if tree == '':
            singletons.add(lid + '_' + lemma + '_X')
            continue

        pos = entry[12][-2]
        annotation[lid + '_' + lemma + '_' + translate[pos]] = [tree, step, form]

        if len([True for i in form if i.isupper()]) == 1:
            if 'x' not in form:
                comp_full[''.join(step)].append(lid + '_' + lemma + '_' + pos)
            for abstract, morph in zip(form, step):
                if abstract.isupper():
                    base[morph].append(lid + '_' + lemma + '_' + pos)
                    lemma_full[lid + '_' + lemma + '_' + pos] = ''.join(step)
                    lemma_base[lid + '_' + lemma + '_' + pos] = morph
        elif len([True for i in form if i.isupper()]) > 1:
            compounds.append(lid + '_' + lemma + '_' + pos)
            for abstract, morph in zip(form, step):
                if abstract.isupper():
                    comp_base[lid + '_' + lemma + '_' + pos].append(morph)
        else:
            singletons.add(lid + '_' + lemma + '_' + pos)


# construct derivational families
for b in sorted(list(base), key=lambda x: len(x)):
    if not base.get(b, False):
        continue
    previous_bases = set()
    while True:
        bases = {lemma_full[i] for i in base[b]}
        if b in bases:
            bases.remove(b)
        if len(bases) == 0 or bases == previous_bases:
            break
        for full in bases:
            if full in base:
                base[b] += base[full]
                del base[full]
        previous_bases = bases
    bs = {lemma_full[i] for i in base[b]}

relations = list()
for b, lems in base.items():
    # singleton
    if len(lems) == 1:
        singletons.add(lems[0])
        continue
    else:
        for rel in it.permutations(lems, 2):
            relations.append(rel)


# find compounding relations
compounding = list()
for comp in compounds:
    parents = [comp_full.get(i, False) for i in comp_base[comp]]
    if len(parents) != 2:
        singletons.add(comp)
    elif all(parents) and len(parents[0]) == 1 and len(parents[1]) == 1:
        compounding.append((comp, (parents[0][0], parents[1][0])))
    else:
        singletons.add(comp)


# save singletons
with open(sys.argv[3], mode='w', encoding='U8') as f:
    for lemma in singletons:
        lemma = lemma[:-1] + translate[lemma[-1]]
        if annotation.get(lemma, False):
            info = annotation[lemma]
            info = '#'.join([info[0], ';'.join(info[1]), ';'.join(info[2])])
            f.write(lemma + '\t' + info + '\n')
        else:
            f.write(lemma + '\t' + '' + '\n')


# save relations
with open(sys.argv[2], mode='w', encoding='U8') as f:
    for parent, child in relations:
        parent = parent[:-1] + translate[parent[-1]]
        pinfo, cinfo = '', ''
        if annotation.get(parent, False):
            info = annotation[parent]
            pinfo = '#'.join([info[0], ';'.join(info[1]), ';'.join(info[2])])
        child = child[:-1] + translate[child[-1]]
        if annotation.get(child, False):
            info = annotation[child]
            cinfo = '#'.join([info[0], ';'.join(info[1]), ';'.join(info[2])])
        f.write(parent + '\t' + child + '\t' + pinfo + '\t' + cinfo + '\n')


# save compounds
with open(sys.argv[4], mode='w', encoding='U8') as f:
    for compound, parents in compounding:
        compound = compound[:-1] + translate[compound[-1]]
        parent1 = parents[0][:-1] + translate[parents[0][-1]]
        compoundinfo, p1info, p2info = '', '', ''
        if annotation.get(compound, False):
            info = annotation[compound]
            compoundinfo = '#'.join([info[0], ';'.join(info[1]), ';'.join(info[2])])
        if annotation.get(parent1, False):
            info = annotation[parent1]
            p1info = '#'.join([info[0], ';'.join(info[1]), ';'.join(info[2])])
        parent2 = parents[1][:-1] + translate[parents[1][-1]]
        if annotation.get(parent2, False):
            info = annotation[parent2]
            p2info = '#'.join([info[0], ';'.join(info[1]), ';'.join(info[2])])
        f.write(compound + '\t' + parent1 + '\t' + parent2 +
                '\t' + compoundinfo + '\t' + p1info + '\t' + p2info + '\n')
