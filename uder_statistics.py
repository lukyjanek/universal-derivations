#!/usr/bin/env python3
# coding: utf-8

"""Calculate basic statistics on UDer resource (from DeriNet 2.0 format)."""

import sys
import networkx as nx
from collections import defaultdict


# properties
FAMILIES = 1
SINGLETONS = 0
RELATIONS = 0
LEMMAS = 0
POS = defaultdict(int)
DERIVATIONS = 0
COMPOUNDING = 0
CONVERSION = 0
VARIANTS = 0
DEPTH = 0
WIDTH = 0
MAXSIZE = 0
MAXWIDTH = 0
MAXDEPTH = 0


# load data, calculate properties
families = list()
relations = list()
with open(sys.argv[1], mode='r', encoding='U8') as f:
    lemmas_in_family = 0
    lemmas_before_fam = 0
    for line in f:
        if line == '\n':
            FAMILIES += 1
            if lemmas_in_family == 1:
                SINGLETONS += 1
            lemmas_in_family = 0
            families.append(relations)
            if len(relations) > MAXSIZE:
                MAXSIZE = len(relations)
            relations = list()
        else:
            line = line.rstrip('\n').split('\t')
            LEMMAS += 1
            lemmas_in_family += 1
            POS[line[3]] += 1
            if line[6] != '':
                RELATIONS += 1
                relations.append((line[6], line[0]))
            if 'Type=Derivation' in line[7]:
                DERIVATIONS += 1
            elif 'Type=Compounding' in line[7]:
                COMPOUNDING += 1
            elif 'Type=Conversion' in line[7]:
                CONVERSION += 1
            elif 'Type=Variant' in line[7]:
                VARIANTS += 1

families.append(relations)
if len(relations) > MAXSIZE:
    MAXSIZE = len(relations)


# build families and calculate sum of depths and wides
for fam in families:
    if fam:
        # build
        G = nx.DiGraph()
        G.add_edges_from(fam)
        root = None
        # find source
        for rel in fam:
            if '.0' in rel[0]:
                root = rel[0]
                break
        # depth
        d = max(nx.shortest_path_length(G, root).values())
        DEPTH += d
        if d > MAXDEPTH:
            MAXDEPTH = d
        # out-degree (width)
        w = max([G.out_degree(node) for node in G.nodes])
        WIDTH += w
        if w > MAXWIDTH:
            MAXWIDTH = w


# print results
print('Lemmas:', LEMMAS)
print('Relations:', RELATIONS)
print('Families:', FAMILIES)
print('Singletons:', SINGLETONS)
print('Avarage tree size:', str(round(LEMMAS/FAMILIES, 1)))
print('Avarage tree depth:', str(round(DEPTH/FAMILIES, 1)))
print('Avarage tree out-degree:', str(round(WIDTH/FAMILIES, 1)))
print('Maximum tree size:', MAXSIZE)
print('Maximum tree depth:', MAXDEPTH)
print('Maximum tree out-degree:', MAXWIDTH)

pos_line = ''
for key, freq in sorted(POS.items()):
    pos_line += '; ' + key + ', ' + str(round(freq/LEMMAS*100, 1))
if ' , 100.0' in pos_line:
    print('Part-of-speech:', 'none')
else:
    print('Part-of-speech:', pos_line[2:])

print('Derivational relations:', DERIVATIONS)
print('Conversion relations:', CONVERSION)
print('Compounding relations:', COMPOUNDING)
print('Variant relations:', VARIANTS)

# print('Table:')
# print(format(LEMMAS, ',d'),
#       format(RELATIONS, ',d'),
#       format(FAMILIES, ',d'),
#       format(SINGLETONS, ',d'),
#       str(round(LEMMAS/FAMILIES, 1)) + ' / ' + str(MAXSIZE),
#       str(round(DEPTH/FAMILIES, 1)) + ' / ' + str(MAXDEPTH),
#       str(round(WIDTH/FAMILIES, 1)) + ' / ' + str(MAXWIDTH),
#       str(round(POS['NOUN']/LEMMAS*100)),
#       str(round(POS['ADJ']/LEMMAS*100)),
#       str(round(POS['VERB']/LEMMAS*100)),
#       str(round(POS['ADV']/LEMMAS*100)),
#       str(round(sum([n for p, n in POS.items()
#                      if p not in ('NOUN', 'ADJ', 'VERB', 'ADV', '')])/LEMMAS*100)),
#       sep=' & ')
