from derinet import Block, Lexicon
import argparse
import logging

import pickle


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logger = logging.getLogger(__name__)


class HarmonizeEtymWordNetCA(Block):
    """Upload harmonized trees of Etymological WordNet to format of Derinet."""

    def __init__(self, fname):
        """Need name of .pickle with harmonized trees."""
        self.fname = fname

    def process(self, lexicon: Lexicon):
        """Build Catalan Etymological WordNet to DeriNet format."""
        # load data
        harm = pickle.load(open(self.fname, 'rb'))

        # add lemmas and morphological features
        for entry in harm:
            lexicon.create_lexeme(lemma=entry['form'], pos='')

        # add main derivational relations,
        # add other derivational relations,
        # add references to splitted families
        for entry in harm:
            chi_node = lexicon.get_lexemes(lemma=entry['form'])[0]

            if entry['parent']:
                par_node = lexicon.get_lexemes(lemma=entry['parent'][0])[0]
                lexicon.add_derivation(source=par_node, target=chi_node)

            if entry['others']:  # TODO: change place to 9th colummn
                parents = list()
                for other in entry['others']:
                    par_node = lexicon.get_lexemes(lemma=other[0])[0]

                    rl_par = chi_node.parent_relation
                    if (rl_par and par_node.lemid != rl_par.sources[0].lemid) \
                       or not rl_par:
                        parents.append(par_node.lemid + '&Type=Derivation')

                if parents:
                    chi_node.misc['other_parents'] = '|'.join(parents)

            if entry['ref_roots']:
                roots = list()
                for ref in entry['ref_roots']:
                    par_node = lexicon.get_lexemes(lemma=ref)[0]
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
