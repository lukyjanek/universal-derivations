from derinet import Block, Lexicon
import argparse
import logging

import pickle


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logger = logging.getLogger(__name__)


class HarmonizeDCelex(Block):
    """Upload harmonized trees of DCelex to format of Derinet."""

    def __init__(self, fname):
        """Need name of .pickle with harmonized trees."""
        self.fname = fname

    def process(self, lexicon: Lexicon):
        """Build DCelex to DeriNet format."""
        # load data
        harm = pickle.load(open(self.fname, 'rb'))
        parse_pos = {'N': 'NOUN', 'V': 'VERB', 'A': 'ADJ', 'D': 'ADV',
                     'X': 'X', 'C': 'NUM', 'P': 'ADP'}

        # add lemmas and morphological features
        for entry in harm:
            oid, form = entry['form'].split('_')
            lid = form + '#' + parse_pos[entry['pos']] + '#' + oid
            lexicon.create_lexeme(lemma=form,
                                  pos=parse_pos[entry['pos']], lemid=lid)

        # add main relations,
        # add original features,
        # add compounds
        for entry in harm:
            c_pos = parse_pos[entry['pos']]
            oid, form = entry['form'].split('_')
            c_lid = form + '#' + c_pos + '#' + oid
            chi_node = lexicon.get_lexemes(lemma=form, pos=c_pos,
                                           lemid=c_lid)[0]

            if entry['parent']:
                p_oid, p_form, p_pos = entry['parent'][0].split('_')
                p_pos = parse_pos[p_pos]
                p_lid = p_form + '#' + p_pos + '#' + p_oid

                par_node = lexicon.get_lexemes(lemma=p_form, pos=p_pos,
                                               lemid=p_lid)[0]
                lexicon.add_derivation(source=par_node, target=chi_node)

            # features
            orig = entry['orig'].split('#')
            if len(orig) > 0 and orig != ['']:
                orig_hierarch = orig[0]
                chi_node.misc['segmentation_hierarch'] = orig_hierarch
            if len(orig) > 1:
                orig_flat = orig[1]
                chi_node.misc['segmentation'] = orig_flat
            if len(orig) > 2:
                orig_morphs = orig[2]
                chi_node.misc['morpheme_order'] = orig_morphs

            # compounds
            if entry['compounding']:
                # parent 1
                p1_oid, p1_form, p1_pos = entry['compounding'][0][0].split('_')
                p1_pos = parse_pos[p1_pos]
                p1_lid = '#'.join([p1_form, p1_pos, p1_oid])
                p1_node = lexicon.get_lexemes(lemma=p1_form, pos=p1_pos,
                                              lemid=p1_lid)
                if len(p1_node) == 0:
                    lexicon.create_lexeme(lemma=p1_form, pos=p1_pos,
                                          lemid=p1_lid)
                    # features
                    p1_node = lexicon.get_lexemes(lemma=p1_form, pos=p1_pos,
                                                  lemid=p1_lid)[0]
                    orig = entry['compounding'][0][1].split('#')
                    if len(orig) > 0 and orig != ['']:
                        orig_hierarch = orig[0]
                        p1_node.misc['segmentation_hierarch'] = orig_hierarch
                    if len(orig) > 1:
                        orig_flat = orig[1]
                        p1_node.misc['segmentation'] = orig_flat
                    if len(orig) > 2:
                        orig_morphs = orig[2]
                        p1_node.misc['morpheme_order'] = orig_morphs

                p1_node = lexicon.get_lexemes(lemma=p1_form, pos=p1_pos,
                                              lemid=p1_lid)[0]

                # parent 2
                p2_oid, p2_form, p2_pos = entry['compounding'][1][0].split('_')
                p2_pos = parse_pos[p2_pos]
                p2_lid = '#'.join([p2_form, p2_pos, p2_oid])
                p2_node = lexicon.get_lexemes(lemma=p2_form, pos=p2_pos,
                                              lemid=p2_lid)
                if len(p2_node) == 0:
                    lexicon.create_lexeme(lemma=p2_form, pos=p2_pos,
                                          lemid=p2_lid)
                    # features
                    p2_node = lexicon.get_lexemes(lemma=p1_form, pos=p1_pos,
                                                  lemid=p1_lid)[0]
                    orig = entry['compounding'][1][1].split('#')
                    if len(orig) > 0 and orig != ['']:
                        orig_hierarch = orig[0]
                        p2_node.misc['segmentation_hierarch'] = orig_hierarch
                    if len(orig) > 1:
                        orig_flat = orig[1]
                        p2_node.misc['segmentation'] = orig_flat
                    if len(orig) > 2:
                        orig_morphs = orig[2]
                        p2_node.misc['morpheme_order'] = orig_morphs

                p2_node = lexicon.get_lexemes(lemma=p2_form, pos=p2_pos,
                                              lemid=p2_lid)[0]

                if p1_node == p2_node or not p1_node or not p2_node:
                    continue
                lexicon.add_composition([p1_node, p2_node], p1_node, chi_node)

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
