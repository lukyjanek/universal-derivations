#!/usr/bin/env python3
# coding: utf-8

"""Create annotat. data with without: infrequent lexemes, already annotated."""

import sys
import json
import networkx as nx
from collections import defaultdict


# load frequency list of lexemes
frequencies = defaultdict(int)
with open(sys.argv[2], mode='r', encoding='U8') as f:
    for line in f:
        line = line.strip().split()
        freq, lexeme = line[0], ''.join(line[1:])
        frequencies[lexeme] = int(freq)


# load already annotated families
annotated = set()
with open(sys.argv[3], mode='r', encoding='U8') as f:
    content = json.loads(f.read())
    for family in content:
        lexemes = set([lexeme['data']['id'] for lexeme in family['nodes']])
        annotated.update(lexemes)


# load relations
rels = defaultdict(list)
relations = list()
with open(sys.argv[1], mode='r', encoding='U8') as f:
    for line in f:
        line = line.rstrip('\n').split('\t')
        relations.append((line[0], line[1]))
        rels[line[1]].append(line[0])


# build graphs
G = nx.DiGraph()
G.add_edges_from(relations)


# go through components, positive filter of non-tree families
graphs = list()
for family in nx.weakly_connected_components(G):
    fam = {'nodes': [], 'edges': []}
    # build individual family separately
    F = nx.DiGraph()
    for lemma in family:
        for parent in rels[lemma]:
            F.add_edge(parent, lemma)
    # check treenes of family, print non-tree graphs
    if not nx.is_tree(F) or not nx.is_arborescence(F):
        # filter our already annotated families
        if any([True for l in F.nodes if l in annotated]):
            continue
        for node in F.nodes:
            fam['nodes'].append({'data': {'id': node}})
        for target, source in F.edges:
            fam['edges'].append({'data': {'source': source,
                                          'target': target,
                                          'intoTree': 'solid'}})
        graphs.append(fam)


# sorting according to sum of frequencies
graph_with_frequencies = defaultdict(list)
for family in graphs:
    freq = 0
    for lexeme in family['nodes']:
        f = frequencies[lexeme['data']['id'].split('_')[0]]
        freq += f if f != 1 else 0
    graph_with_frequencies[freq].append(family)


# print families sorted according to frequencies of lexemes
output_families = list()
for key in sorted(graph_with_frequencies, reverse=True):
    for family in graph_with_frequencies[key]:
        output_families.append(family)

with open(sys.argv[4], mode='w', encoding='U8') as f:
    f.write(json.dumps(output_families, ensure_ascii=False))
