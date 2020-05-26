#!/usr/bin/env python3
# coding: utf-8

"""Split annotation data to train, validation and holdout."""

import sys
import math
import random
import argparse
import networkx as nx
from collections import defaultdict


def split_data(relations, train=0.5, validation=0.25, holdout=0.25,
               random_seed=None, stats=False):
    """Return dictionary of relations (parent, child) assigned T/V/H label."""
    def generate_subsets(G):
        # store relations
        parents = defaultdict(list)
        for edge in G.edges:
            parents[edge[1]].append(edge[0])

        # build and list components (in stable order)
        components = list()
        for component in nx.weakly_connected_components(G):
            C = nx.DiGraph()
            for node in component:
                for parent in parents[node]:
                    C.add_edge(parent, node)
            components.append(C)
        fams = {sorted(f)[0]: f for f in components}
        num_fams = len(list(fams))

        # select families
        H_keys = random.sample(sorted(fams), k=math.floor(num_fams*holdout))
        H = [fams[k] for k in H_keys]
        for item in H_keys:
            del fams[item]

        V_keys = random.sample(sorted(fams), k=math.floor(num_fams*validation))
        V = [fams[k] for k in V_keys]
        for item in V_keys:
            del fams[item]

        T = [fams[k] for k in fams if k not in H_keys and k not in V_keys]

        return T, V, H

    # set random seed if present
    if random_seed:
        random.seed(random_seed)

    # control sum
    if train + validation + holdout != 1:
        print('ERROR: Sum of sizes for splitting data is not 1.')
        return None

    # build families
    F = nx.DiGraph()
    F.add_edges_from(relations)

    # split on subsets, check proportion of relations included
    # resample (allowed 1% difference from the given size of subsets)
    TRAIN, VALIDATION, HOLDOUT = generate_subsets(F)
    rels_H = [edge for f in HOLDOUT for edge in f.edges]
    rels_V = [edge for f in VALIDATION for edge in f.edges]
    rels_T = [edge for f in TRAIN for edge in f.edges]
    all_rels = len(rels_H) + len(rels_V) + len(rels_T)

    iteration = 0
    while len(rels_H) < all_rels*(holdout-0.01) or \
            len(rels_V) < all_rels*(validation-0.01) or \
            len(rels_T) < all_rels*(train-0.01) or iteration > 5000:
        TRAIN, VALIDATION, HOLDOUT = generate_subsets(F)
        rels_H = [edge for f in HOLDOUT for edge in f.edges]
        rels_V = [edge for f in VALIDATION for edge in f.edges]
        rels_T = [edge for f in TRAIN for edge in f.edges]
        iteration += 1

    # assigning T/V/H labels
    divided = {rel: 'H' for rel in rels_H}
    divided = {**divided, **{rel: 'V' for rel in rels_V}}
    divided = {**divided, **{rel: 'T' for rel in rels_T}}

    # return statistics
    # print({'train_fams': len(TRAIN), 'validation_fams': len(VALIDATION),
    #        'holdout_fams': len(HOLDOUT), 'train_rels': len(rels_T),
    #        'validation_rels': len(rels_V), 'holdout_rels': len(rels_H)})
    if stats:
        return {'train_fams': len(TRAIN), 'validation_fams': len(VALIDATION),
                'holdout_fams': len(HOLDOUT), 'train_rels': len(rels_T),
                'validation_rels': len(rels_V), 'holdout_rels': len(rels_H)}

    return divided


if __name__ == '__main__':
    # parse input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-T', action='store_true', dest='t', required=False,
                        help='return TRAIN dataset')
    parser.add_argument('-V', action='store_true', dest='v', required=False,
                        help='return VALIDATION dataset')
    parser.add_argument('-H', action='store_true', dest='h', required=False,
                        help='return HOLDOUT dataset')
    parser.add_argument('-a', action='store', dest='a', required=True,
                        help='path to the annotated data')
    parser.add_argument('-stat', action='store', dest='stat', required=False,
                        help='path to the file with statistics')
    par = parser.parse_args()

    # load data
    rels = defaultdict()
    with open(par.a, mode='r', encoding='U8') as f:
        for line in f:
            entry = line.rstrip('\n').split('\t')
            rels[(entry[1], entry[2])] = entry[0]

    # split data
    if par.stat:
        data = split_data(list(rels), train=0.65, validation=0.15, holdout=0.2,
                          random_seed=24, stats=True)
    else:
        data = split_data(list(rels), train=0.65, validation=0.15, holdout=0.2,
                          random_seed=24)

    # return data
    if par.stat:
        with open(par.stat, mode='w', encoding='U8') as f:
            for key, val in data.items():
                f.write(key + '\t' + str(val) + '\n')
        sys.exit()
    if par.t:
        for relation, dataset in data.items():
            if dataset == 'T':
                print(rels[relation], *relation, sep='\t')
    elif par.v:
        for relation, dataset in data.items():
            if dataset == 'V':
                print(rels[relation], *relation, sep='\t')
    elif par.h:
        for relation, dataset in data.items():
            if dataset == 'H':
                print(rels[relation], *relation, sep='\t')
