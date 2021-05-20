#!/usr/bin/env python3
# coding: utf-8

"""Extract relations in Latin WFL; for UDer v1.1."""

import argparse
from collections import defaultdict


# initialise arguments
parser = argparse.ArgumentParser()
parser.add_argument('--lemmario', type=str)
parser.add_argument('--wfr', type=str)
parser.add_argument('--wfr_rel', type=str)
parser.add_argument('--output', type=str)


# load lemmario into dictionary {id_of_lemma : [info_about_lemma]}
def load_lemmario(path):
    lemmario = defaultdict()
    with open(path, mode='r', encoding='U8') as f:
        for line in f:
            entry = line.rstrip('\n').split('\t')
            lemmario[entry[0]] = entry[1:]
    return lemmario


# load word-formation types into dictionary {id_of_type : [info_about_type]}
def load_wordformation_type(path):
    wfr = defaultdict()
    with open(path, mode='r', encoding='U8') as f:
        for line in f:
            entry = line.rstrip('\n').split('\t')
            wfr[entry[2]] = entry[:2] + entry[3:]
    return wfr


# main
def main(args):
    # load input database
    lemmario = load_lemmario(args.lemmario)
    wfr = load_wordformation_type(args.wfr)

    # load input relations
    with open(args.wfr_rel, mode='r', encoding='U8') as f, \
         open(args.output, mode='w', encoding='U8') as g:
        for line in f:
            id_par, _, id_chi, id_wfr, _, _ = line.rstrip('\n').split('\t')

            # parent
            parent = lemmario[id_par]
            parent = '_'.join(parent[:4] + [parent[6], str(id_par)])

            # child
            child = lemmario[id_chi]
            child = '_'.join(child[:4] + [child[6], str(id_chi)])

            # relation type
            category = wfr[id_wfr][0]
            process = wfr[id_wfr][1]
            affix = ''
            if wfr[id_wfr][2] and wfr[id_wfr][2] != 'NULL':
                affix = wfr[id_wfr][2]
            elif wfr[id_wfr][5] and wfr[id_wfr][5] != 'NULL':
                affix = wfr[id_wfr][5]

            print(parent, child, category, process, affix, sep='\t', file=g)


# run main
if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
