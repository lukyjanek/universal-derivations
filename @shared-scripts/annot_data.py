#!/usr/bin/env python3
# coding: utf-8

"""Build data for annotation."""

import sys
import json
import math
import random
import argparse
import networkx as nx
from collections import defaultdict


# parse input parameters
parser = argparse.ArgumentParser()
parser.add_argument('-i', action='store', dest='i', required=True, nargs='+',
                    help='path to input file (relations: parent [tab] child)')
parser.add_argument('-j', action='store_true', dest='j', required=False,
                    help='save in .json file (for Annotation Interface)')
parser.add_argument('-c', action='store_true', dest='c', required=False,
                    help='save in classic list')
parser.add_argument('-j2c', action='store_true', dest='jc', required=False,
                    help='convert .json file into classic list')
parser.add_argument('-o', action='store', dest='o', required=False,
                    help='path to output file (json / clasic)')
parser.add_argument('-stat', action='store', dest='stat', required=False,
                    help='path to output statistics')
par = parser.parse_args()


# check options
if par.jc and par.j and par.c:
    sys.exit('ERROR: Cannot use -c, -j and -j2c together.')
elif par.j and par.c:
    sys.exit('ERROR: Cannot use -c and -j together.')
if (par.jc or par.j or par.c) and not par.o:
    sys.exit('ERROR: Cannot use -c or -j or -j2c without -o.')


# annotated json convert to classic format
if par.jc:
    # load all json files
    mark = {'solid': '+', 'dotted': '-'}
    classic = list()
    for path in par.i:
        with open(path, mode='r', encoding='U8') as f:
            content = json.loads(f.read())
            # go through each family in json and convert to classic
            for family in content:
                rels = defaultdict()  # relations in family
                annotated = False  # lock of annotated family
                treenes = False  # lock of tree-shape of the family

                # load relations
                for edge in family['edges']:
                    key = (edge['data']['target'], edge['data']['source'])
                    rels[key] = mark[edge['data']['intoTree']]
                    if edge['data']['intoTree'] == 'dotted':
                        annotated = True

                # check treenes if the family (components) is annotated
                if annotated:
                    positive_edges = [r for r in rels if rels[r] == '+']
                    edg = defaultdict(list)
                    for item in positive_edges:
                        edg[item[1]].append(item[0])

                    G = nx.DiGraph()
                    G.add_edges_from(positive_edges)
                    tree_shaped_components = list()
                    for fam in nx.weakly_connected_components(G):
                        F = nx.DiGraph()
                        F.add_edges_from([(p, l) for l in fam for p in edg[l]])
                        if nx.is_tree(F) and nx.is_arborescence(F):
                            tree_shaped_components.append(True)
                        else:
                            tree_shaped_components.append(False)

                    treenes = all(tree_shaped_components)

                # add to data or continue
                if annotated and treenes:
                    classic.append(rels)
                elif annotated and not treenes:
                    print('ERROR: Family is not tree-shaped:', family)

    # save converted annotated data
    with open(par.o, mode='w', encoding='U8') as f:
        for family in classic:
            for rel, mark in family.items():
                f.write(mark + '\t' + rel[0] + '\t' + rel[1] + '\n')


# create annotated data in json or classic style
elif par.j or par.c or par.stat:
    # statistics
    non_tree_fams = 0
    tree_fams = 0
    non_tree_rels = 0
    tree_rels = 0

    # load all relations
    rels = defaultdict(list)
    relations = list()
    for path in par.i:
        with open(path, mode='r', encoding='U8') as f:
            for line in f:
                line = line.rstrip('\n').split('\t')
                relations.append((line[0], line[1]))
                rels[line[1]].append(line[0])

    # build graphs
    G = nx.DiGraph()
    G.add_edges_from(relations)

    # go through components
    # positive filter of non-tree families
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
            for node in F.nodes:
                fam['nodes'].append({'data': {'id': node}})
            for target, source in F.edges:
                fam['edges'].append({'data': {'source': source,
                                              'target': target,
                                              'intoTree': 'solid'}})
            graphs.append(fam)
            non_tree_rels += len(F.edges)
            non_tree_fams += 1
        else:
            tree_rels += len(F.edges)
            tree_fams += 1
    random.shuffle(graphs)

    # save to file
    if par.j:
        c = 5000
        for i in range(0, math.ceil(len(graphs)/c)):
            name = par.o.replace('.json', '') + '-' + str(i+1) + '.json'
            with open(name, mode='w', encoding='U8') as f:
                f.write(json.dumps(graphs[i*c:(i+1)*c], ensure_ascii=False))
    if par.c:
        with open(par.o, mode='w', encoding='U8') as f:
            for family in graphs:
                for relation in family['edges']:
                    f.write('' + '\t' + relation['data']['target'] + '\t'
                            + relation['data']['source'] + '\n')
                f.write('\n')
    if par.stat:
        with open(par.stat, mode='w', encoding='U8') as f:
            f.write('Tree-shaped families:\t' + str(tree_fams) + '\n')
            f.write('Tree-shaped relations:\t' + str(tree_rels) + '\n')
            f.write('Non-tree-shaped families:\t' + str(non_tree_fams) + '\n')
            f.write('Non-tree-shaped relations:\t' + str(non_tree_rels) + '\n')
