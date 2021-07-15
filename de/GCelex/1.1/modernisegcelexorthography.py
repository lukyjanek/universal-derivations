from derinet import Block, Lexicon
import argparse
import logging

from collections import defaultdict


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logger = logging.getLogger(__name__)


class ModerniseGCelexOrthography(Block):
    """Modernise older orthography of GCelex."""

    def __init__(self, fname):
        """Need name of file with moder orthography."""
        self.fname = fname

    def process(self, lexicon: Lexicon):
        """Modernise older orthography of GCelex."""
        # load file with modernised orthography
        corrected_orthography = defaultdict()
        with open(self.fname, mode='r', encoding='U8') as file:
            for line in file:
                line = line.rstrip().split('\\')
                corrected_orthography[line[0]] = line

        # go through lexicon and update orthography; the older one move to misc
        for lexeme in lexicon.iter_lexemes():
            _, _, orig_id = lexeme.lemid.split('#')

            lexeme.misc['older_ortho'] = lexeme.lemma
            lexeme._lemma = corrected_orthography[orig_id][1]

            if 'segmentation' in lexeme.misc.keys():
                lexeme.misc['segmentation'] = \
                    corrected_orthography[orig_id][8].replace('+', ';')

            if 'segmentation_hierarch' in lexeme.misc.keys():
                lexeme.misc['segmentation_hierarch'] = \
                    corrected_orthography[orig_id][13]

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
