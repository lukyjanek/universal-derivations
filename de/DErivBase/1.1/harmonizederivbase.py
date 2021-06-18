from derinet import Block, Lexicon
import argparse
import logging

import pickle


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logger = logging.getLogger(__name__)


class HarmonizeDerivBase(Block):
    """Upload harmonized trees of DerivBase to format of Derinet."""

    def __init__(self, fname):
        """Need name of .pickle with harmonized trees."""
        self.fname = fname

    def process(self, lexicon: Lexicon):
        """Build DerivBase to DeriNet format."""
        # load data
        harm = pickle.load(open(self.fname, 'rb'))
        parse_pos = {'V': ('VERB', None),
                     'Nn': ('NOUN', 'Gender:Neut'),
                     'Nf': ('NOUN', 'Gender:Fem'),
                     'Nm': ('NOUN', 'Gender:Masc'),
                     'N': ('NOUN', None),
                     'A': ('ADJ', None)}

        # add lemmas and morphological features
        for entry in harm:
            feat = {}
            if parse_pos[entry['pos']][1] is not None:
                for f in parse_pos[entry['pos']][1:]:
                    key, value = f.split(':')
                    feat[key] = value

            lid = entry['form'] + '#' + parse_pos[entry['pos']][0]
            if parse_pos[entry['pos']][1]:
                lid += '#' + parse_pos[entry['pos']][1].replace('Gender:', '')

            lexicon.create_lexeme(lemma=entry['form'],
                                  pos=parse_pos[entry['pos']][0],
                                  feats=feat, lemid=lid)

        # add main relations and rules,
        # add other derivational relations and rules,
        # add references to splitted families
        for entry in harm:
            c_pos = parse_pos[entry['pos']]
            c_lid = entry['form'] + '#' + c_pos[0]
            if c_pos[1]:
                c_lid += '#' + c_pos[1].replace('Gender:', '')

            chi_node = lexicon.get_lexemes(lemma=entry['form'], pos=c_pos[0],
                                           lemid=c_lid)[0]

            if entry['parent']:
                p_form, p_pos = entry['parent'][0][0].split('_')
                p_pos = parse_pos[p_pos]
                p_lid = p_form + '#' + p_pos[0]
                if p_pos[1]:
                    p_lid += '#' + p_pos[1].replace('Gender:', '')

                par_node = lexicon.get_lexemes(lemma=p_form, pos=p_pos[0],
                                               lemid=p_lid)[0]

                lexicon.add_derivation(source=par_node, target=chi_node)

                rule = entry['parent'][1].replace('>', '')
                chi_node.parent_relation.feats['Rule'] = rule

            if entry['others']:  # TODO: change place to 9th colummn
                parents = list()
                for other in entry['others']:
                    p_form, p_pos = other[0][0].split('_')
                    rule = other[1].replace('>', '')
                    p_pos = parse_pos[p_pos]
                    p_lid = p_form + '#' + p_pos[0]
                    if p_pos[1]:
                        p_lid += '#' + p_pos[1].replace('Gender:', '')

                    par_node = lexicon.get_lexemes(lemma=p_form, pos=p_pos[0],
                                                   lemid=p_lid)[0]

                    rl_par = chi_node.parent_relation
                    if (rl_par and par_node.lemid != rl_par.sources[0].lemid) \
                       or not rl_par:
                        p = par_node.lemid + '&Rule=' + rule
                        p += '&Type=Derivation'
                        parents.append(p)

                if parents:
                    chi_node.misc['other_parents'] = '|'.join(parents)

            if entry['ref_roots']:
                roots = list()
                for ref in entry['ref_roots']:
                    p_form, p_pos = ref.split('_')
                    p_pos = parse_pos[p_pos]
                    p_lid = p_form + '#' + p_pos[0]
                    if p_pos[1]:
                        p_lid += '#' + p_pos[1].replace('Gender:', '')

                    par_node = lexicon.get_lexemes(lemma=p_form, pos=p_pos[0],
                                                   lemid=p_lid)[0]

                    if par_node.lemid != chi_node.lemid:
                        roots.append(par_node.lemid)

                if roots:
                    chi_node.misc['was_in_family_with'] = '&'.join(roots)

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
