from collections import defaultdict
from derinet import Block, Lexicon
import argparse
import logging

import re
import pickle


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logger = logging.getLogger(__name__)


class HarmonizeGoldCompoundAnalyses(Block):
    """Harmonise list of compounds into UDer format."""

    def __init__(self, fname):
        """Need name of .pickle with harmonized trees."""
        self.fname = fname

    def process(self, lexicon: Lexicon):
        """Build GoldCompoundAnalyses to DeriNet format."""
        # load data
        data = list()
        with open(self.fname, mode='r', encoding='U8') as file:
            for line in file:
                data.append(line.rstrip().split('\t'))

        parse_pos = {
            'verb': 'VERB', 'noun': 'NOUN', 'adv': 'ADV', 'glroot': 'X', 'tgr': 'ADV', 'num': 'NUM', 'prop': 'PROPN',
            'part': 'PART','comp': 'ADJ', 'adj': 'ADJ', 'pron': 'PRON', 'suffixoid': 'Affixoid',
            'prefixoid': 'Affixoid'
        }

        # add lemmas and morphological features
        for entry in data:
            # compound lexeme
            lemma = entry[0].split('_')[0]
            pos = parse_pos[entry[0].split('_')[1]]
            lemid = '#'.join([lemma, pos])
            
            lexeme = lexicon.create_lexeme(lemma=lemma, pos=pos, lemid=lemid)
            lexeme.misc['dataset'] = entry[-1]

            # components
            for idx in (1, 2):
                for item in eval(entry[idx]):
                    lemma = item.split('_')[0]
                    pos = parse_pos[item.split('_')[1]]
                    lemid = '#'.join([lemma, pos])
                    
                    lexeme = lexicon.create_lexeme(lemma=lemma, pos=pos, lemid=lemid)
                    if pos == 'Affixoid':
                        lexeme.add_feature('Fictitious', 'Yes')

        # add relations and rules
        for entry in data:
            # compound lexeme
            lemma = entry[0].split('_')[0]
            pos = parse_pos[entry[0].split('_')[1]]
            lemid = '#'.join([lemma, pos])
            
            compound_lexeme = lexicon.get_lexemes(lemma=lemma, pos=pos, lemid=lemid)[0]

            # components
            components = list()
            for idx in (1, 2):
                for item in eval(entry[idx]):
                    lemma = item.split('_')[0]
                    pos = parse_pos[item.split('_')[1]]
                    lemid = '#'.join([lemma, pos])
                    
                    component = lexicon.get_lexemes(lemma=lemma, pos=pos, lemid=lemid)[0]
                    components.append(component)

            if compound_lexeme in components or len(set(components)) < 2:
                continue

            sources = [components[-1]] + components[:-1]
            lexicon.add_composition(
                sources=sources, main_source=components[-1], target=compound_lexeme, feats={'Rule', 'a'}
            )

        return lexicon

    @staticmethod
    def parse_args(args):
        """
        Parse a list of strings containing the arguments.

        Pick the relevant ones from the beginning and leave the rest be.
        Return the parsed args to this module and the unprocessed rest.
        """
        parser = argparse.ArgumentParser(
            prog=__class__.__name__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        parser.add_argument("file", help="The file to load annotation from.")
        # argparse.REMAINDER tells argparse not to be eager
        # and to process only the start of the args.
        parser.add_argument("rest", nargs=argparse.REMAINDER,
                            help="A list of other modules and their arguments")

        args = parser.parse_args(args)

        fname = args.file

        # Return *args to __init__, **kwargs to init
        # and the unprocessed tail of arguments to other modules.
        return [fname], {}, args.rest
