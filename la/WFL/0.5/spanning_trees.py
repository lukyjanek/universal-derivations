#!/usr/bin/env python3
# coding: utf-8

"""Harmonize WFL."""

import pickle
import argparse
import networkx as nx
from collections import defaultdict


# parse input parameters
parser = argparse.ArgumentParser()
parser.add_argument('-r', action='store', dest='r', required=True,
                    help='path to the list of all relations')
parser.add_argument('-w', action='store', dest='w', required=True,
                    help='path to the list of weighted relations')
parser.add_argument('-o', action='store', dest='o', required=True,
                    help='path to the output file')
par = parser.parse_args()


# list of harmonized lexicon
harmonized = list()


# load all relations
compounds = defaultdict(list)
rel_info = dict()
rels = list()
relat_short = defaultdict(list)
with open(par.r, mode='r', encoding='utf-8') as f:
    for line in f:
        parent, child, order, rule, categ, afix = line.rstrip('\n').split('\t')
        if categ == 'Compounding':
            compounds[child].append((parent, order, rule, categ, afix))
            continue
        rels.append((parent, child))
        relat_short[child].append(parent)
        rel_info[(parent, child)] = (order, rule, categ, afix)


# save compounding
for child, parents in compounds.items():
    parse = child.split('_')
    form = parse[0]
    pos = '_'.join(parse[1:])
    n = {'form': form, 'pos': pos, 'parent': '', 'ref_roots': '',
         'others': '', 'compounding': []}
    for parent in parents:
        n['compounding'].append(parent)
    harmonized.append(n)


# load weighted relations of lemmas with more parents (manually annotated)
# cahnge annotation marks to 0/1 values as weight
weighted = dict()
with open(par.w, mode='r', encoding='utf-8') as f:
    for line in f:
        mark, child, parent = line.rstrip('\n').split('\t')
        weight = 0
        if mark == '+':
            weight = 1
        weighted[(parent, child)] = float(weight)


# make rooted tree from families
G = nx.DiGraph()
G.add_edges_from(rels)

for family in nx.weakly_connected_components(G):
    # build family
    F = nx.DiGraph()
    for lemma in family:
        for parent in relat_short[lemma]:
            F.add_edge(parent, lemma)

    # add virtual root
    for node in [n for n in F.nodes]:
        F.add_edge('VIRTUAL', node)

    # assign weight edges
    for node in F.nodes:
        parents = [edge for edge in F.edges
                   if edge[1] == node and edge[0] != 'VIRTUAL']
        for parent, child in parents:
            if (parent, child) in weighted:
                F.edges[parent, child]['weight'] = weighted[(parent, child)]
            else:
                F.edges[parent, child]['weight'] = 1

    # find maximum spanning tree
    E = nx.algorithms.maximum_spanning_arborescence(F, default=-10**50)

    # save family
    roots = [edge[1] for edge in E.edges if edge[0] == 'VIRTUAL']
    for node in [n for n in E.nodes if n != 'VIRTUAL']:
        parse = node.split('_')
        form = parse[0]
        pos = '_'.join(parse[1:])
        n = {'form': form, 'pos': pos, 'compounding': []}
        obli = [(edge, rel_info[edge]) for edge in E.edges
                if edge[1] == node and edge[0] != 'VIRTUAL']
        facu = [(edge, rel_info[edge]) for edge in F.edges
                if edge[1] == node and edge[0] != 'VIRTUAL']
        if obli:
            n['parent'] = obli[0]
            n['ref_roots'] = ''
            if facu:
                facu.remove(obli[0])
        else:
            n['parent'] = ''
            n['ref_roots'] = roots if len(roots) > 1 else ''
        n['others'] = facu
        harmonized.append(n)


# save harmonized data
pickle.dump(harmonized, open(par.o, 'wb'))
