#!/usr/bin/env python3
# coding: utf-8

"""Make feature vector (in dict) for given relation."""

import numpy as np
import textdistance as txd


def make_vector(parent, child, parent_pos=None, child_pos=None, custom=dict()):
    """Build feature vector (in dict) for given child+pos and parent+pos.

    Features included:
    child. child lemma (str)
    parent. parent lemma (str)
    childPos. child part-of-speech (str)
    parentPos. parent part-of-speech (str)
    levDist. Levenshtein distance (num)
    levSim. Levenshtein similarity (num)
    jar_winDist. Jaro-Winkler distance (float)
    jar_winSim. Jaro-Winkler similarity (float)
    jacDist. Jaccard distance (float)
    jacSim. Jaccard similarity (float)
    lcsseq. Length of the longest common substring (num)
    stOne. same 1 start letters of lemmas (bool: 0/1)
    stTwo. same 2 start letters of lemmas (bool: 0/1)
    enOne. same 1 end letters of lemmas (bool: 0/1)
    enTwo. same 2 end letters of lemmas (bool: 0/1)
    stOnChi. 1-gram (starting) of child (str, unknown: NA)
    stTwChi. 2-gram (starting) of child (str, unknown: NA)
    stThChi. 3-gram (starting) of child (str, unknown: NA)
    stFoChi. 4-gram (starting) of child (str, unknown: NA)
    stFiChi. 5-gram (starting) of child (str, unknown: NA)
    stOnPar. 1-gram (starting) of parent (str, unknown: NA)
    stTwPar. 2-gram (starting) of parent (str, unknown: NA)
    stThPar. 3-gram (starting) of parent (str, unknown: NA)
    stFoPar. 4-gram (starting) of parent (str, unknown: NA)
    stFiPar. 5-gram (starting) of parent (str, unknown: NA)
    enOnChi. 1-gram (ending) of child (str, unknown: NA)
    enTwChi. 2-gram (ending) of child (str, unknown: NA)
    enThChi. 3-gram (ending) of child (str, unknown: NA)
    enFoChi. 4-gram (ending) of child (str, unknown: NA)
    enFiChi. 5-gram (ending) of child (str, unknown: NA)
    enOnPar. 1-gram (ending) of parent (str, unknown: NA)
    enTwPar. 2-gram (ending) of parent (str, unknown: NA)
    enThPar. 3-gram (ending) of parent (str, unknown: NA)
    enFoPar. 4-gram (ending) of parent (str, unknown: NA)
    enFiPar. 5-gram (ending) of parent (str, unknown: NA)
    """
    # resulted vector
    vect = {**dict(), **custom}
    vect['child'] = child
    vect['parent'] = parent
    vect['childPos'] = child_pos
    vect['parentPos'] = parent_pos

    # Levenshtein, Jaro-Winkler, Jaccard distances and longest common subs.
    p, c = parent.lower(), child.lower()
    vect['levDist'] = txd.levenshtein.distance(p, c)
    vect['levSim'] = txd.levenshtein.similarity(p, c)
    vect['jar_winDist'] = txd.jaro_winkler.distance(p, c)
    vect['jar_winSim'] = txd.jaro_winkler.similarity(p, c)
    vect['jacDist'] = txd.jaccard.distance(p, c)
    vect['jacSim'] = txd.jaccard.similarity(p, c)
    vect['lcsseq'] = txd.lcsstr.similarity(p, c)

    # length difference
    length = round(((len(parent) - len(child))**2)**(1/2))
    vect['lengthDif'] = length

    # same starts
    start_one = True if parent[0].lower() == child[0].lower() else False
    start_two = True if parent[:2].lower() == child[:2].lower() else False
    vect['stOne'] = start_one
    vect['stTwo'] = start_two

    # same ends
    end_one = True if parent[-1].lower() == child[-1].lower() else False
    end_two = True if parent[-2:].lower() == child[-2:].lower() else False
    vect['enOne'] = end_one
    vect['enTwo'] = end_two

    # starting n-gram
    s_name = ('stOn', 'stTw', 'stTh', 'stFo', 'stFi')
    s_par = [parent[:i] if len(parent) >= i else np.nan for i in range(1, 6)]
    s_chi = [child[:i] if len(child) >= i else np.nan for i in range(1, 6)]
    vect = {**vect, **{name+'Par': gram for name, gram in zip(s_name, s_par)}}
    vect = {**vect, **{name+'Chi': gram for name, gram in zip(s_name, s_chi)}}

    # ending n-gram
    e_name = ('enOn', 'enTw', 'enTh', 'enFo', 'enFi')
    e_par = [parent[-i:] if len(parent) >= i else np.nan for i in range(1, 6)]
    e_chi = [child[-i:] if len(child) >= i else np.nan for i in range(1, 6)]
    vect = {**vect, **{name+'Par': gram for name, gram in zip(e_name, e_par)}}
    vect = {**vect, **{name+'Chi': gram for name, gram in zip(e_name, e_chi)}}

    return vect
