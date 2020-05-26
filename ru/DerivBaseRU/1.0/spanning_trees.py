#!/usr/bin/env python3
# coding: utf-8

"""Harmonize DerivBaseRU."""

import pickle
import argparse
import networkx as nx
from math import log2
from collections import defaultdict


# parse input parameters
parser = argparse.ArgumentParser()
parser.add_argument('-s', action='store', dest='s', required=False,
                    help='path to the list of singletons')
parser.add_argument('-r', action='store', dest='r', required=True,
                    help='path to the list of all relations')
parser.add_argument('-w', action='store', dest='w', required=True,
                    help='path to the list of weighted relations')
parser.add_argument('-v', action='store', dest='v', required=True,
                    help='default weight of edges ending with virtual root')
parser.add_argument('-o', action='store', dest='o', required=False,
                    help='path to the output file')
parser.add_argument('-ev', action='store', dest='ev', required=False,
                    help='path to the output file')
par = parser.parse_args()


# list of harmonized lexicon
harmonized = list()


# load singletons
if par.s:
    singletons = list()
    with open(par.s, mode='r', encoding='U8') as f:
        for line in f:
            form, pos = line.rstrip('\n').split('_')
            harmonized.append({'form': form, 'pos': pos, 'parent': '',
                               'ref_roots': '', 'others': ''})


# load all relations
rules = dict()
relat_short = defaultdict(list)
with open(par.r, mode='r', encoding='U8') as f:
    for line in f:
        parent, child, rule = line.rstrip('\n').split('\t')
        rules[(parent, child)] = rule
        relat_short[child].append(parent)


# load weighted relations of lemmas with more parents
weighted = dict()
with open(par.w, mode='r', encoding='U8') as f:
    for line in f:
        parent, child, weight = line.rstrip('\n').split('\t')
        if float(weight) != 0:
            weighted[(parent, child)] = log2(float(weight))
        else:
            weighted[(parent, child)] = -100


# make rooted tree from families
G = nx.DiGraph()
G.add_edges_from(list(rules))

for family in nx.weakly_connected_components(G):
    # build family and add virtual root
    F = nx.DiGraph()
    for lemma in family:
        if float(par.v) == 0:
            w = -1000
        elif float(par.v) < 0:
            w = -10**51
        else:
            w = log2(float(par.v))
        F.add_edge('#VIRTUAL#', lemma, weight=w)
        for parent in relat_short[lemma]:
            F.add_edge(parent, lemma, weight=weighted.get((parent, lemma), 1))
            F.add_edge('#VIRTUAL#', parent, weight=w)

    # backup before filtering
    B = F.copy()

    # filter out incorrect negatives
    neg = [n for n in F.nodes if n.startswith('не')]
    for node in neg:
        inputs = [e for e in list(F.in_edges(node)) if e[0] != '#VIRTUAL#']
        if len(inputs) > 1:
            found = None
            # go through all incoming edges to the negative
            for edge in inputs:
                parent, child = edge
                if parent in child.lstrip('не'):
                    found = (parent, child)
                    break
            # delete all edges except the right one
            if found:
                inputs.remove(found)
                F.remove_edges_from(inputs)

    # filter out incorrect reflexives
    refl = [n for n in F.nodes if n.endswith('ся_V')]
    for node in refl:
        inputs = [e for e in list(F.in_edges(node)) if e[0] != '#VIRTUAL#']
        if len(inputs) > 1:
            found = None
            # go through all incoming edges to the reflexive
            for edge in inputs:
                parent, child = edge
                if parent == child.rstrip('ся_V') + '_V':
                    found = (parent, child)
                    break
            # delete all edges except the right one
            if found:
                inputs.remove(found)
                F.remove_edges_from(inputs)

    # find maximum spanning tree
    if len(F.nodes) > 20000:
        # greedy approach for extremely big graphs
        gre = nx.algorithms.tree.greedy_branching(F, attr='weight', kind='max',
                                                  default=par.v)
        E = nx.DiGraph()
        E.add_edges_from(gre.edges)
    else:
        # traditional spanning
        edm = nx.algorithms.tree.branchings.Edmonds(F, seed=24)
        E = edm.find_optimum(attr='weight', default=par.v, kind='max',
                             style='arborescence')

    # save family
    roots = [edge[1] for edge in E.edges if edge[0] == '#VIRTUAL#']
    for node in E.nodes:
        if node == '#VIRTUAL#':
            continue
        form, pos = node.split('_')
        n = {'form': form, 'pos': pos}
        obli = [(edge, rules[edge]) for edge in E.in_edges(node)
                if edge[0] != '#VIRTUAL#']
        facu = [(edge, rules[edge]) for edge in B.in_edges(node)
                if edge[0] != '#VIRTUAL#']
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
if par.o:
    pickle.dump(harmonized, open(par.o, 'wb'))

if par.ev:
    with open(par.ev, mode='w', encoding='U8') as f:
        for entry in harmonized:
            if entry['parent']:
                f.write('+\t' + entry['parent'][0][0] + '\t' + entry['form'] +
                        '_' + entry['pos'] + '\n')
