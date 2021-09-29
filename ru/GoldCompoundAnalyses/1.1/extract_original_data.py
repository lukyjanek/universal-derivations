#!/usr/bin/env python3
# coding: utf-8

"""Extract original annotation of comopounds from Gold Compound Analyses."""

import csv
import argparse
from collections import defaultdict


# initial parameters
parser = argparse.ArgumentParser()
parser.add_argument('--input_train', action='store', type=str, help='path to train.csv')
parser.add_argument('--input_test', action='store', type=str, help='path to test.csv')
parser.add_argument('--input_val', action='store', type=str, help='path to val.csv')
parser.add_argument('--output_relations', action='store', type=str, help='path to output list of relation')


# load input data
def load_input_data(path):
    with open(path, mode='r', encoding='U8') as file:
        content = csv.reader(file, delimiter=',')
        return list(content)


# extract relevant data
def extract_relevant_annotations_from_input_data(data):
    relations = defaultdict()
    for rule, compound, c_pos, first_component, fc_pos, second_component, sc_pos in data[1:]:
        relations['_'.join([compound, c_pos])] = \
            ('_'.join([first_component, fc_pos]), '_'.join([second_component, sc_pos]), rule)
    return relations


# store the resulting data
def save_resulting_relations(path, data):
    with open(path, mode='w', encoding='U8') as file:
        for compound, relations in data.items():
            first_component, second_component, rule, dataset = relations
            print(compound, first_component, second_component, rule, dataset, sep='\t', file=file)


# main
def main(args):
    relations = defaultdict()
    for path, dataset in [(args.input_train, 'train'), (args.input_test, 'test'), (args.input_val, 'val')]:
        # extract original data
        extracted_data = load_input_data(path)
        relevant_relations = extract_relevant_annotations_from_input_data(extracted_data)
        # add relevant_relations into relations
        for compound, relation in relevant_relations.items():
            relation = [relation[0], relation[1], relation[2], dataset]
            for idx in (0, 1):
                if ';' in relation[idx]:
                    lemmas, poses = relation[idx].split('_')
                    components = list()
                    for lemma, pos in zip(lemmas.split(';'), poses.split(';')):
                        components.append('_'.join([lemma, pos]))
                    relation[idx] = tuple(components)
                else:
                    relation[idx] = (relation[idx],)
            relations[compound] = tuple(relation)
    save_resulting_relations(args.output_relations, relations)


# run script
if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
