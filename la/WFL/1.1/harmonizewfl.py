from derinet import Block, Lexicon
import argparse
import logging

import pickle


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logger = logging.getLogger(__name__)


class HarmonizeWFL(Block):
    """Upload relations of Latin WFL to format of Derinet."""

    def __init__(self, fname):
        """Need name of .tsv with relations."""
        self.fname = fname

    def process(self, lexicon: Lexicon):
        """Build Latin WFL to DeriNet format."""
        def parse_lemmas(l_lem, l_pos):
            gend_parse = {'m': 'Masc',
                          'f': 'Fem',
                          'n': 'Neut'}
            type, gend, tag, pos, wid = l_pos.split('_')

            feat = {}
            if pos == 'NOUN':
                if gend in ('m', 'f', 'n'):
                    feat['Gender'] = gend_parse[gend]
                if len(tag) > 1:
                    feat['Declension'] = tag[1]
            elif pos == 'ADJ' and len(tag) > 1:
                feat['AdjClass'] = tag[1]
            elif pos == 'VERB':
                if len(tag) <= 1:
                    pass
                elif tag[1] in ('1', '2', '3', '4', '5'):
                    feat['Conjugation'] = tag[1]
                elif tag[1] == 'A':
                    tag = 'U'

            lid = l_lem + '#' + pos + '#' + wid
            return pos, feat, lid

        # load data
        harm = pickle.load(open(self.fname, 'rb'))

        # add lemmas, morphological features and segmentation
        for entry in harm:
            pos, feat, lid = parse_lemmas(entry['form'], entry['pos'])

            # check presence in the lexicon (due to compounds)
            present = lexicon.get_lexemes(lemma=entry['form'], pos=pos,
                                          lemid=lid)

            if len(present) == 0:
                lexicon.create_lexeme(lemma=entry['form'],
                                      pos=pos,
                                      feats=feat,
                                      lemid=lid)

        # add main relations and used afix,
        # add other derivational relations and used afix,
        # add references to splitted families,
        # add compounding
        for entry in harm:
            c_pos, _, c_lid = parse_lemmas(entry['form'], entry['pos'])
            chi_node = lexicon.get_lexemes(lemma=entry['form'], pos=c_pos,
                                           lemid=c_lid)[0]

            if entry['parent']:
                parse = entry['parent'][0][0].split('_')
                p_form = parse[0]
                p_pos, _, p_lid = parse_lemmas(p_form, '_'.join(parse[1:]))

                par_node = lexicon.get_lexemes(lemma=p_form, pos=p_pos,
                                               lemid=p_lid)[0]

                afix = entry['parent'][1][2]
                typ = entry['parent'][1][1].replace('Derivation_', '')
                if typ in ('Prefix', 'Suffix'):
                    lexicon.add_derivation(source=par_node, target=chi_node)
                    chi_node.parent_relation.feats[typ] = afix
                elif typ == 'Conversion':
                    lexicon.add_conversion(source=par_node, target=chi_node)

            if entry['others']:  # TODO: change place to 9th colummn;conversion
                parents = list()
                for other in entry['others']:
                    parse = other[0][0].split('_')
                    p_form = parse[0]
                    p_pos, _, p_lid = parse_lemmas(p_form, '_'.join(parse[1:]))

                    afix = other[1][2]
                    typ = other[1][1].replace('Derivation_', '')

                    par_node = lexicon.get_lexemes(lemma=p_form, pos=p_pos,
                                                   lemid=p_lid)[0]

                    rl_par = chi_node.parent_relation
                    if (rl_par and par_node.lemid != rl_par.sources[0].lemid) \
                       or not rl_par:
                        if typ in ('Prefix', 'Suffix'):
                            p = par_node.lemid + '&' + typ + '=' + afix
                            p += '&Type=Derivation'
                            parents.append(p)
                        else:
                            parents.append(par_node.lemid + '&Type=' + typ)

                if parents:
                    chi_node.misc['other_parents'] = '|'.join(parents)

            if entry['ref_roots']:
                roots = list()
                for ref in entry['ref_roots']:
                    parse = ref.split('_')
                    p_form = parse[0]
                    p_pos, _, p_lid = parse_lemmas(p_form, '_'.join(parse[1:]))

                    par_node = lexicon.get_lexemes(lemma=p_form, pos=p_pos,
                                                   lemid=p_lid)[0]

                    if par_node.lemid != chi_node.lemid:
                        roots.append(par_node.lemid)

                if roots:
                    chi_node.misc['was_in_family_with'] = '&'.join(roots)

            if entry['compounding']:
                p1_parse = entry['compounding'][0][0].split('_')
                p1_form = p1_parse[0]
                p1_attr = '_'.join(p1_parse[1:])
                p1_pos, p1_feat, p1_lid = parse_lemmas(p1_form, p1_attr)

                p1_node = lexicon.get_lexemes(lemma=p1_form, pos=p1_pos,
                                              lemid=p1_lid)
                if len(p1_node) == 0:
                    lexicon.create_lexeme(lemma=p1_form,
                                          pos=p1_pos,
                                          feats=p1_feat,
                                          lemid=p1_lid)

                p1_node = lexicon.get_lexemes(lemma=p1_form, pos=p1_pos,
                                              lemid=p1_lid)[0]

                p2_parse = entry['compounding'][1][0].split('_')
                p2_form = p2_parse[0]
                p2_attr = '_'.join(p2_parse[1:])
                p2_pos, p2_feat, p2_lid = parse_lemmas(p2_form, p2_attr)
                p2_node = lexicon.get_lexemes(lemma=p2_form, pos=p2_pos,
                                              lemid=p2_lid)
                if len(p2_node) == 0:
                    lexicon.create_lexeme(lemma=p2_form,
                                          pos=p2_pos,
                                          feats=p2_feat,
                                          lemid=p2_lid)

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
