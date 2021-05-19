#!/usr/bin/env python3
# coding: utf-8

"""Input statistics for technical report."""

import sys
import re
import xlrd
import networkx as nx
import xml.etree.ElementTree as ET
from collections import defaultdict


def morpholexen(data=None):
    """Return statistics for MorphoLex-en."""
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    families = defaultdict(set)
    wb = xlrd.open_workbook(sys.argv[5])
    for sheet in ('0-1-0', '0-1-1', '0-1-2', '0-1-3', '0-1-4', '0-2-0',
                  '0-2-1', '0-2-2', '0-2-3', '0-3-0', '0-3-1', '0-3-2',
                  '0-4-0', '1-1-0', '1-1-2', '1-1-3', '1-1-4', '1-2-0',
                  '1-2-1', '1-2-2', '1-3-0', '2-1-0', '2-1-1', '2-1-2',
                  '2-1-3', '2-2-0', '3-1-0'):
        sh = wb.sheet_by_name(sheet)
        tr_pos = {'NN': 'N', 'JJ': 'A', 'RB': 'D', 'VB': 'V'}
        for rownum in range(sh.nrows):
            row = sh.row_values(rownum)  # 4 = form, 5 = pos, 8 = segment
            for p in row[5].split('|'):
                if not tr_pos.get(p, False):
                    continue

                word = str(row[4]) + '_' + str(tr_pos[p])
                if word not in lem:
                    pos[tr_pos.get(p, 'X')] += 1
                lem.add(word)

                roots = re.findall(r'\(.*?\)', row[8])
                if len(roots) == 0:
                    sing += 1
                    continue
                for root in roots:
                    families[root].add(word)

        for key, lemmas in families.items():
            if len(lemmas) == 1:
                sing += 1
            else:
                fam += 1

    return len(lem), 0, fam, sing, pos


def morpholexfr(data=None):
    """Return statistics for MorphoLex-en."""
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    families = defaultdict(set)
    wb = xlrd.open_workbook(sys.argv[5])
    for sheet in ('0-1-0', '0-1-1', '0-1-2', '0-1-3', '0-2-0', '0-2-2',
                  '0-3-0', '1-1-0', '1-1-1', '1-1-2', '1-1-3', '1-2-0',
                  '1-2-1', '2-1-0', '2-1-1', '2-1-2'):
        sh = wb.sheet_by_name(sheet)
        for rownum in range(sh.nrows):
            row = sh.row_values(rownum)  # 1 = form, 3 = segment
            lem.add(str(row[1]))

            roots = re.findall(r'\(.*?\)', row[3])
            if len(roots) == 0:
                sing += 1
                continue
            for root in roots:
                families[root].add(str(row[1]))

        for key, lemmas in families.items():
            if len(lemmas) == 1:
                sing += 1
            else:
                fam += 1

    return len(lem), 0, fam, sing, pos


def derivbaseru(data):
    """Return statistics for DerivBase.Ru."""
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    lem = set()
    for path in sys.argv[1].split('\n'):
        with open(sys.argv[5], mode='r', encoding='U8') as f:
            lem.update(f.read().split('\n'))

    for l in lem:
        pos[l.split('_')[1]] += 1

    relations = defaultdict(list)
    tr_pos = {'adj': 'A', 'noun': 'N', 'verb': 'V', 'adv': 'D', 'num': 'C'}
    for line in data:
        line = line.strip().split('\t')
        line[0] = line[0] + '_' + tr_pos[line[1]]
        line[2] = line[2] + '_' + tr_pos[line[3]]
        relations[(line[0], line[2])].append('&'.join(line[-2:]))

    related_lexemes = set()
    for parent, child in relations:
        related_lexemes.add(parent)
        related_lexemes.add(child)

    for l in lem:
        if l not in related_lexemes:
            sing += 1

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    return len(lem), len(relations), fam, sing, pos


def derivbasehr(data):
    """Return statistics for DerivBase.hr."""
    rel = 0
    sing = 0
    lem = set()
    fam = len(data)
    pos = defaultdict(int)

    for line in data:
        for word in line.strip().split():
            if word not in lem:
                pos[word.split('_')[1]] += 1
                lem.add(word)

        if len(line.strip().split()) == 1:
            sing += 1
        else:
            n = len(line.strip().split())
            rel += (n * (n - 1))

    return len(lem), int(rel), fam - sing, sing, pos


def derinet(data):
    """Return statistics for DeriNet."""
    rel = 0
    sing = 0
    fam = 0
    lem = set()
    pos = defaultdict(int)

    prev_line = None
    for line in data:
        if line != '\n':
            lem.add(line)
            pos[line.split('\t')[3]] += 1
            relid = line.split('\t')[6]
            if relid:
                typerel = line.split('\t')[7]
                if 'Type=Compounding' not in typerel:
                    rel += 1
                else:
                    sources = re.search(r'Sources=(.*?)&', typerel).group(1)
                    rel += len(sources.split(','))
        else:
            fam += 1
            if prev_line.split('\t')[0].endswith('.0'):
                sing += 1
        prev_line = line
    fam += 1

    return len(lem), int(rel), fam - sing, sing, pos


def polishwfn(data):
    """Return statistics for Polish Word-Formation Network."""
    rel = 0
    sing = 0
    fam = 0
    lem = list()
    pos = defaultdict(int)

    idS = set()
    for line in data:
        entry = line.rstrip('\n').split('\t')
        if entry[4] != '':
            idS.add(entry[4])

    for line in data:
        entry = line.rstrip('\n').split('\t')
        # if entry[2] not in lem:
        pos[entry[3]] += 1
        lem.append(entry[2])

        if entry[4] != '':
            rel += 1
        else:
            if entry[0] not in idS:
                sing += 1
            fam += 1

    return len(lem), int(rel), fam - sing, sing, pos


def derinetes(data):
    """Returns statistics for Spanish DeriNet.ES."""
    return polishwfn(data)


def derinetfa(data):
    """Returns statistics for Persian DeriNet.FA."""
    df = list()
    for line in data:
        line = line.rstrip('\n').split(' ')

        if len(line) == 3:
            line.append('')

        df.append((line[0], line[1], '', '', line[3]))

    rel = 0
    sing = 0
    fam = 0
    lem = set()
    pos = defaultdict(int)

    idS = set()
    for entry in df:
        if entry[4] != '':
            idS.add(entry[4])

    for entry in df:
        if entry[0:2] not in lem:
            pos[entry[3]] += 1
            lem.add(tuple(entry[0:2]))

        if entry[4] != '':
            rel += 1
        else:
            if entry[0] not in idS:
                sing += 1
            fam += 1

    return len(lem), int(rel), fam - sing, sing, pos


def spanishwfn(data):
    """Return statistics for Spanish Word-Formation Network."""
    return polishwfn(data)


def catvar(data):
    """Return statistics for CatVar."""
    rel = 0
    sing = 0
    lem = set()
    fam = len(data)
    pos = defaultdict(int)

    translate = {'N': 'N', 'V': 'V', 'AJ': 'A', 'AV': 'D'}
    for line in data:
        for word in line.strip().split('#'):
            if word not in lem:
                pos[translate[word.split('_')[1].split('%')[0]]] += 1
                lem.add(word)

        if len(line.strip().split('#')) == 1:
            sing += 1
        else:
            n = len(line.strip().split('#'))
            rel += (n * (n - 1))

    return len(lem), int(rel), fam - sing, sing, pos


def demonette(data, tag='morphologicalRelation', i=1):
    """Return statistics for Démonette."""
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    data_string = ''.join(data)

    tree = ET.ElementTree(ET.fromstring(data_string))
    root = tree.getroot()

    translate = {'N': 'N', 'A': 'A', 'V': 'V', 'D': 'D', 'R': 'D'}
    relations = list()
    for entry in root.iter(tag):
        lm1 = entry[0][0].text + '_' + entry[0][i].text
        lm2 = entry[1][0].text + '_' + entry[1][i].text

        if lm1 not in lem:
            pos[translate[lm1.split('_')[1][0]]] += 1
            lem.add(lm1)
        if lm2 not in lem:
            pos[translate[lm2.split('_')[1][0]]] += 1
            lem.add(lm2)

        relations.append((lm1, lm2))

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    return len(lem), len(relations), fam, sing, pos


def verbaction(data):
    """Return statistics for Verbaction."""
    return demonette(data, tag='couple')


def morphonette(data):
    """Return statistics for Morphonette."""
    return demonette(data, tag='filament', i=2)


def derivbase(data):
    """Return statistics for DErivBase."""
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    relations = set()
    for line in data:
        line = line.rstrip('\n').split(' ')
        for i in range(3, len(line)-2, 2):
            if line[i].endswith('_Ven'):
                line[i] = line[i][:-2]
            if line[i+2].endswith('_Ven'):
                line[i+2] = line[i+2][:-2]

            if '*' in line[i+1]:
                relations.add((line[i+2], line[i]))
            else:
                relations.add((line[i], line[i+2]))

            if line[i] not in lem:
                lem.add(line[i])
                pos[line[i].split('_')[1][0]] += 1
            if line[i+2] not in lem:
                lem.add(line[i+2])
                pos[line[i+2].split('_')[1][0]] += 1

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    with open(sys.argv[5], mode='r', encoding='U8') as f:
        for line in f:
            line = line.rstrip('\n').split(' ')
            if len(line) == 1:
                if line[0] not in lem:
                    lem.add(line[0])
                    pos[line[0].split('_')[1][0]] += 1
                sing += 1

    return len(lem), len(relations), fam, sing, pos


def derivcelex(data):
    """Return statistics for DErivCELEX."""
    return derivbasehr(data)


def derivatario(data):
    """Return statistics for derIvaTario."""
    rel = 0
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    translate = {'S': 'N', 'V': 'V', 'G': 'A', 'B': 'D', 'E': 'E', 'N': 'N'}
    families = defaultdict(list)
    for line in data:
        lemma = line.split('\t')[0].split(';')[1] + '_' \
                + line.strip().split('\t')[1]

        if lemma not in lem:
            pos[translate[line.strip().split('\t')[1][0]]] += 1
            lem.add(lemma)

        if line.split('\t')[0].split(';')[2] != 'BASELESS:unrec':
            families[line.split('\t')[0].split(';')[2]].append(lemma)
        else:
            sing += 1

    fam += len(families)

    for base, words in families.items():
        n = len(words)
        rel += (n * (n - 1))

    return len(lem), 0, fam, sing, pos


def gcelex(data, i=13):
    """Return statistics for G-CELEX2."""
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    relations = list()
    empty = set()
    for line in data:
        entry = line.rstrip('\n').split('\\')

        lemma = entry[1]
        struclab = entry[i]

        if struclab == '':
            empty.add(lemma)
            continue

        lemma = entry[1] + '_' + entry[i][-2]
        imm = entry[8].split('+')
        immclass = list(entry[9])

        if lemma not in lem:
            if lemma[-1] == 'B':
                pos['D'] += 1
            elif lemma[-1] == 'D':
                pos['B'] += 1
            else:
                pos[lemma[-1]] += 1
            lem.add(lemma)

        added = False
        for struct in zip(immclass, imm):
            if struct[0] in ('N', 'V', 'A', 'B', 'F', 'Q', 'O', 'R'):
                if struct[1] + '_' + struct[0] != lemma:
                    relations.append((struct[1] + '_' + struct[0], lemma))
                added = True

        if not added:
            sing += 1

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    edited_lem = [key[:-2] for key in lem]
    for word in empty:
        if word not in edited_lem:
            pos['?'] += 1
            lem.add(word)
            sing += 1

    return len(lem), 0, fam, sing, pos


def dcelex(data):
    """Return statistics for D-CELEX2."""
    return gcelex(data, i=12)


def ecelex(data):
    """Return statistics for E-CELEX2."""
    rel = 0
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    families = defaultdict(list)
    empty = set()
    for line in data:
        entry = line.rstrip('\n').split('\\')

        lemma = entry[1]
        flatsa = list(entry[20])
        struclab = entry[21]

        if struclab == '':
            empty.add('(' + lemma + ')')
            continue

        lemma = entry[1] + '_' + entry[21][-2]
        struclab = re.findall(r'\([^\(].*?\]', struclab)

        if lemma not in lem:
            if lemma[-1] == 'B':
                pos['D'] += 1
            elif lemma[-1] == 'D':
                pos['B'] += 1
            else:
                pos[lemma[-1]] += 1
            lem.add(lemma)

        added = False
        for struct in zip(flatsa, struclab):
            if struct[0] in ('S', 'F') and struct[1][-2] in ('N', 'V', 'A',
                                                             'B', 'Q', 'O'):
                families[struct[1]].append(lemma)
                rel += 1
                added = True

        if not added:
            if len(flatsa) == 1:
                families[struclab[0]].append(lemma)
            else:
                for struct in zip(flatsa, struclab):
                    families[struct[1]].append(lemma)
                    rel += 1

    found = False
    for word in empty:
        for key in list(families):
            if word in key:
                found = True
                continue
        if not found:
            families[word]
            if word not in lem:
                pos['?'] += 1
                lem.add(word)

    for root, children in families.items():
        if len(children) == 0:
            sing += 1
        elif len(children) == 1:
            root = root.replace(')[', '_')[1:-1]
            if root in children[0]:
                sing += 1

    fam = len(families) - sing
    return len(lem), 0, fam, sing, pos


def princetonwn(data):
    """Return statistics for Princeton WordNet."""
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    translate = {'1': 'N', '2': 'V'}
    relations = list()
    for line in data:
        entry = line.lstrip('"').rstrip('\n"').split('","')

        if len(entry) != 7:
            continue

        lm1 = entry[0].split('%')[0] + '_' + entry[1][0]
        lm2 = entry[3].split('%')[0] + '_' + entry[4][0]

        if lm1 not in lem:
            pos[translate[entry[1][0]]] += 1
            lem.add(lm1)
        if lm2 not in lem:
            pos[translate[entry[4][0]]] += 1
            lem.add(lm2)

        relations.append((lm1, lm2))

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    return len(lem), len(relations), fam, sing, pos


def estwn(data):
    """Return statistics for Estonian WordNet."""
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    data_string = ''.join(data)

    tree = ET.ElementTree(ET.fromstring(data_string))
    root = tree.getroot()

    translate = {'n': 'N', 'a': 'A', 'v': 'V', 'r': 'D'}
    relations = list()
    for descendant in root.iter('LexicalEntry'):
        for child in descendant.iter():
            if child.tag == 'Lemma':
                lm1 = child.attrib['writtenForm'] + '$' \
                      + child.attrib['partOfSpeech']
            if child.tag == 'Sense':
                for ch in child.iter():
                    if 'relType' in ch.attrib:
                        if ch.attrib['relType'] == 'derivation':
                            lm2 = ch.attrib['target'].split('-')[1] + '$' \
                                  + re.sub(r'[0-9]*', '',
                                           ch.attrib['target'].split('-')[2])

                            if lm1 not in lem:
                                pos[translate[lm1.split('$')[1]]] += 1
                                lem.add(lm1)
                            if lm2 not in lem:
                                pos[translate[lm2.split('$')[1]]] += 1
                                lem.add(lm2)

                            relations.append([lm1, lm2])

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    return len(lem), len(relations), fam, sing, pos


def finnwn(data):
    """Return statistics for Finnish WordNet."""
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    relations = list()
    for line in data:
        entry = line.strip().split('\t')

        if '+' in entry[4]:
            lm1 = entry[1] + '_' + entry[0].split(':')[1][0]
            lm2 = entry[3] + '_' + entry[2].split(':')[1][0]

            if lm1 not in lem:
                pos[lm1.split('_')[1].upper()] += 1
                lem.add(lm1)
            if lm2 not in lem:
                pos[lm2.split('_')[1].upper()] += 1
                lem.add(lm2)

            relations.append((lm1, lm2))

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    return len(lem), len(relations), fam, sing, pos


def sloleks(data=None):
    """Return statistics for Sloleks."""
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    parser = ET.iterparse(sys.argv[5])

    translate = {'samostalnik': 'N', 'pridevnik': 'A', 'A5e2a': 'A5e2a',
                 'prislov': 'D', 'večbesedna': 'večbesedna', 'glagol': 'V',
                 'števnik': 'števnik', 'predlog': 'predlog',
                 'okrajšava': 'okrajšava', 'členek': 'členek',
                 'medmet': 'medmet', 'veznik': 'veznik', 'zaimek': 'zaimek'}
    relations = list()
    for event, element in parser:
        if element.tag == 'LexicalEntry':
            lm1 = ''
            lm2s = list()

            for i in element.iter():
                if i.tag == 'Lemma':
                    lm1 = i[0].attrib['val'] + '_' + element[1].attrib['val']
                    if lm1 not in lem:
                        pos[translate[lm1.split('_')[1]]] += 1
                        lem.add(lm1)

                if i.tag == 'RelatedForm':
                    lm2s.append(i[2].attrib['val'] + '_' + i[1].attrib['val'])
                    if lm2s[-1] not in lem:
                        pos[translate[lm2s[-1].split('_')[1]]] += 1
                        lem.add(lm2s[-1])

                    relations.append([lm1, lm2s[-1]])

            element.clear()

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    return len(lem), len(relations), fam, sing, pos


def finudpud(data):
    """Return statistics for Finnish UD PUD."""
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    translate = {'NOUN': 'N', 'ADJ': 'A', 'ADV': 'D', 'PROPN': 'R',
                 'VERB': 'V'}
    rel_mem = set()
    for line in data:
        if line != '\n' and line[0] != '#':
            entry = line.rstrip('\n').split('\t')
            if 'Derivation' in entry[5]:

                lm1 = entry[2] + '_' + entry[3]
                if lm1 not in lem:
                    pos[translate[entry[3]]] += 1
                    lem.add(lm1)

                for feature in entry[5].split('|'):
                    if 'Derivation' in feature:
                        rel_mem.add((lm1, feature.split('=')[1]))
                        break

    return len(lem), 0, fam, sing, pos


def finudtdt(data):
    """Return statistics for Finnish UD TDT."""
    return finudpud(data)


def kozyudkpv(data):
    """Return statistics for Komi-Zyrian UD Lattice."""
    return finudpud(data)


def wfl(data):
    """Return statistics for Word-Formation Latin."""
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    # database of lemmas
    lemmas = defaultdict()
    with open(sys.argv[5], mode='r', encoding='U8') as f:
        for line in f:
            entry = line.lstrip('(').rstrip(')\n').replace("'", '').split(',')

            if entry[2] == 'N2/1':
                entry[2] = 'A1'
            elif entry[2] == 'N3A':
                entry[2] = 'A2'
            elif entry[2] == 'N3B':
                entry[2] = 'N3'

            lemmas[entry[0]] = entry[1:]

    # deriv relations
    relations = list()
    for line in data:
        entry = line.lstrip('(').rstrip(')\n').replace("'", '').split(',')

        lm1 = lemmas[str(entry[1])][0] + '_' + lemmas[str(entry[1])][1]
        lm2 = lemmas[str(entry[2])][0] + '_' + lemmas[str(entry[2])][1]

        if lm1 not in lem:
            pos[lm1.split('_')[1][0]] += 1
            lem.add(lm1)
        if lm2 not in lem:
            pos[lm2.split('_')[1][0]] += 1
            lem.add(lm2)

        relations.append((lm1, lm2))

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    return len(lem), len(relations), fam, sing, pos


def plwn(data):
    """Return statistics for Polish WordNet."""
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    data_string = ''.join(data)

    tree = ET.ElementTree(ET.fromstring(data_string))
    root = tree.getroot()

    # create wordlist (all WN lemmas)
    all_lem = defaultdict()
    for d in root.iter('lexical-unit'):
        all_lem[d.attrib['id']] = d.attrib['name'] + '_' + d.attrib['pos']

    # extract relevant relations
    relevant = ('62', '169', '158', '244', '3425', '3426', '148', '19', '56',
                '57', '143', '39', '165', '149', '44', '151', '160', '63',
                '41', '42', '43', '156', '55', '152', '34', '38', '108', '59',
                '164', '35', '142', '53', '50', '111', '166', '155', '52',
                '157', '48', '242', '47', '110', '141', '144', '51', '168',
                '154', '40', '46', '161', '37', '36', '49', '163', '45')

    translate = {'czasownik': 'V', 'rzeczownik': 'N', 'przymiotnik': 'A',
                 'przysłówek': 'D', 'CZYNNOŚĆ': 'CZYNNOŚĆ', '': '',
                 'rzeczownik pwn': 'N', 'czasownik pwn': 'V'}
    relations = set()
    for d in root.iter('lexicalrelations'):
        if d.attrib['relation'] in relevant:
            lm1 = all_lem[d.attrib['parent']]
            lm2 = all_lem[d.attrib['child']]

            if lm1 not in lem:
                pos[translate[lm1.split('_')[1]]] += 1
                lem.add(lm1)
            if lm2 not in lem:
                pos[translate[lm2.split('_')[1]]] += 1
                lem.add(lm2)

            if lm1 != lm2:
                relations.add((lm1, lm2))

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    return len(lem), len(relations), fam, sing, pos


def elex(data):
    """Return statistics for E-Lex."""
    rel = 0
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    translate = {'N': 'N', 'V': 'V', 'A': 'A', 'Q': 'Q', 'B': 'D', 'X': 'X',
                 'O': 'O', 'I': 'I'}
    families = defaultdict(list)
    for line in data:
        line = line.rstrip('\r\n').split('\\')

        lm = line[1] + '_'
        struct = line[2]

        if struct == '':  # if derivation is not present
            continue

        lm += struct[-2]

        if lm not in lem:
            pos[translate[lm.split('_')[1]]] += 1
            lem.add(lm)

            struclab = re.findall(r'\([^\(].*?\]', struct)
            lexmorph = [re.search(r'\((.*)\)\[.\]', s).group(1)
                        for s in struclab
                        if re.search(r'\((.*)\)\[.\]', s)]

            for morph in lexmorph:
                families[morph].append(lm)
                rel += 1

            if len(lexmorph) == 0:
                sing += 1

    fam = len(families)
    return len(lem), 0, fam, sing, pos


def wikti(data):
    """Return statistics for given Wiktionary."""
    rel = 0
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    for line in data:
        line = line.rstrip('\n').split('\t')

        if line[0] not in lem:
            lem.add(line[0])
            pos[line[0].split('_')[1]] += 1
        if line[1] not in lem:
            lem.add(line[1])
            pos[line[1].split('_')[1]] += 1
        rel += 1

    with open(sys.argv[5], mode='r', encoding='U8') as f:
        for line in f:
            line = line.rstrip('\n').split('\t')
            if len(line) == 1:
                sing += 1
            fam += 1

    return len(lem), int(rel), fam - sing, sing, pos


def famorphoFR(data):
    """Return statistics for Famorpho-FR."""
    rel = 0
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    data_string = ''.join(data)

    tree = ET.ElementTree(ET.fromstring(data_string))
    root = tree.getroot()

    translate = {'noun': 'N', 'adjective': 'A', 'verb': 'V', 'adverb': 'D',
                 'interjection': 'I'}
    families = list()
    for descendant in root.iter('family'):
        f = list()
        for child in descendant.iter():
            lm = None
            if child.tag == 'entry':
                for entry in child:
                    if entry.tag == 'written_form':
                        lm = entry.text
                    if entry.tag == 'cat':
                        lm += '_' + entry.text

                if lm not in lem:
                    lem.add(lm)
                    pos[translate[lm.split('_')[1]]] += 1
                f.append(lm)
        families.append(f)

    for f in families:
        n = len(f)
        rel += (n * (n - 1))

        if n == 1:
            sing += 1
        else:
            fam += 1

    return len(lem), int(rel), fam, sing, pos


def nomage(data):
    """Return statistics for Nomage."""
    rel = 0
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    data = ''.join(data)
    data = data.replace('\t', '')
    data = data.replace('\r', '')
    data = data.replace('\n', '')
    data = data.replace('\ufeff', '')

    entries = re.findall(r'\<LexicalEntry\>(.*?)\<\/LexicalEntry\>', data)

    translate = {'noun': 'N', 'verb': 'V'}
    relations = list()
    for entry in entries:
        p = re.search(r'att="POS" val="(.*?)"', entry).group(1)

        if p == 'noun':
            lm = re.findall(r'Sense id="(.*?)"', entry)
            rl = re.findall(r'SenseRelation target="(.*?)"', entry)

            # singletons
            if len(lm) == 0 or len(rl) == 0:
                sing += 1
                pos[translate[p]] += 1
                continue

            # lemmas and relations
            if len(lm) == len(rl):
                for r in zip(lm, rl):
                    relations.append(r)
                    if r[0][:-1] + '_' + p not in lem:
                        lem.add(r[0][:-1] + '_' + p)
                        pos[translate[p]] += 1
                    if r[1][:-1] + '_' + 'verb' not in lem:
                        lem.add(r[1][:-1] + '_' + 'verb')
                        pos['V'] += 1

            elif len(lm) > len(rl):
                res = list()
                for rlid in rl:
                    res += [l for l in lm if rlid[-1] in l]

                for r in zip(res, rl):
                    relations.append(r)
                    if r[0][:-1] + '_' + p not in lem:
                        lem.add(r[0][:-1] + '_' + p)
                        pos[translate[p]] += 1
                    if r[1][:-1] + '_' + 'verb' not in lem:
                        lem.add(r[1][:-1] + '_' + 'verb')
                        pos['V'] += 1

        elif p == 'verb':
            lm = re.findall(r'Sense id="(.*?)"', entry)
            for l in lm:
                if l[:-1] + '_' + p not in lem:
                    lem.add(l[:-1] + '_' + p)
                    pos[translate[p]] += 1

    rel = len(relations)

    # build families
    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    return len(lem) + sing, int(rel), fam, sing, pos


def nomlex(data):
    """Return statistics for NOMLEX."""
    data = ''.join(data)
    data = data.replace('\n', '')
    data = data.replace('  ', '')

    entries = re.findall(r'\:(ORTH\s*.*?)(\)\(NOM\s|$)', data)

    lem = set()
    relations = list()
    pos = defaultdict(int)
    for entry in entries:
        lm1 = re.search(r'ORTH "(.*?)"', entry[0]).group(1) + '_' + 'N'
        lm2 = re.search(r'VERB "(.*?)"', entry[0]).group(1) + '_' + 'V'

        if lm1 not in lem:
            lem.add(lm1)
            pos['N'] += 1

        if lm2 not in lem:
            lem.add(lm2)
            pos['V'] += 1

        relations.append((lm1, lm2))

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    sing = 0
    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    return len(lem) + sing, len(relations), fam, sing, pos


def adjadv(data):
    """Return statistics for ADJADV."""
    data = ''.join(data)
    data = data.replace('\n', '')
    data = data.replace('  ', '')

    entries = re.findall(r'ADJADV \:(ORTH\s*.*?)(\)\(|$)', data)
    entries += re.findall(r'ADJVERB \:(ORTH\s*.*?)(\)\(|$)', data)

    lem = set()
    sing = 0
    relations = list()
    pos = defaultdict(int)
    for entry in entries:
        lm1 = re.search(r'ORTH "(.*?)"', entry[0]).group(1) + '_' + 'A'
        lm2 = re.search(r'VERB "(.*?)"', entry[0])
        lm3 = re.search(r'ADV "(.*?)"', entry[0])

        if lm2:
            lm2 = lm2.group(1) + '_' + 'V'
            if lm2 not in lem:
                lem.add(lm2)
                pos['V'] += 1
            relations.append((lm1, lm2))

        elif lm3:
            lm3 = lm3.group(1) + '_' + 'D'
            if lm3 not in lem:
                lem.add(lm3)
                pos['D'] += 1
            relations.append((lm1, lm3))

        else:
            sing += 1
            pos['A'] += 1

        if lm1 not in lem:
            lem.add(lm1)
            pos['A'] += 1

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    return len(lem) + sing, len(relations), fam, sing, pos


def nomadv(data):
    """Return statistics for NOMADV."""
    data = ''.join(data)
    data = data.replace('\n', '')
    data = data.replace('  ', '')

    entries = re.findall(r'NOMADV \:(ORTH\s*.*?)(\)\(|$)', data)

    lem = set()
    sing = 0
    relations = list()
    pos = defaultdict(int)
    for entry in entries:
        lm1 = re.search(r'ORTH "(.*?)"', entry[0]).group(1) + '_' + 'N'
        lm2 = re.search(r'ADV "(.*?)"', entry[0])

        if lm2:
            lm2 = lm2.group(1) + '_' + 'D'
            if lm2 not in lem:
                lem.add(lm2)
                pos['D'] += 1
            relations.append((lm1, lm2))

        else:
            sing += 1
            pos['N'] += 1

        if lm1 not in lem:
            lem.add(lm1)
            pos['N'] += 1

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    return len(lem) + sing, len(relations), fam, sing, pos


def nomlexplus(data):
    """Return statistics for NOMLEX-plus."""
    data = ''.join(data)
    data = data.replace('\n', '')
    data = data.replace('  ', '')

    entries = re.findall(r'NOM \:(ORTH\s*.*?)(\)\(|$)', data)
    entries += re.findall(r'NOMADJ \:(ORTH\s*.*?)(\)\(|$)', data)

    lem = set()
    sing = 0
    relations = list()
    pos = defaultdict(int)
    for entry in entries:
        lm1 = re.search(r'ORTH "(.*?)"', entry[0]).group(1) + '_' + 'N'
        lm2 = re.search(r'VERB "(.*?)"', entry[0])
        lm3 = re.search(r'ADJ "(.*?)"', entry[0])

        if lm2:
            lm2 = lm2.group(1) + '_' + 'V'
            if lm2 not in lem:
                lem.add(lm2)
                pos['V'] += 1
            relations.append((lm1, lm2))

        elif lm3:
            lm3 = lm3.group(1) + '_' + 'A'
            if lm3 not in lem:
                lem.add(lm3)
                pos['A'] += 1
            relations.append((lm1, lm3))

        else:
            sing += 1
            pos['N'] += 1

        if lm1 not in lem:
            lem.add(lm1)
            pos['N'] += 1

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    return len(lem) + sing, len(relations), fam, sing, pos


def nomlexpt(data):
    """Return statistics for NOMLEX-PT."""
    data = ''.join(data)
    data = data.replace('\n', '')
    data = data.replace('  ', '')

    entries = re.findall(r'(<Description .*?)(</Description>)', data)

    lem = set()
    relations = list()
    pos = defaultdict(int)
    for entry in entries:
        lm1 = re.search(r'(nomlex:verb.*?)"/', entry[0])
        lm2 = re.search(r'(nomlex:noun.*?)"/', entry[0])

        if lm1 and lm2:
            lm1 = lm1.group(1).split('-')[2] + '_' + 'V'
            lm2 = lm2.group(1).split('-')[2] + '_' + 'N'

            if lm1 not in lem:
                lem.add(lm1)
                pos['V'] += 1

            if lm2 not in lem:
                lem.add(lm2)
                pos['N'] += 1

            relations.append((lm1, lm2))

    G = nx.Graph()
    G.add_edges_from(relations)
    fam = nx.number_connected_components(G)

    sing = 0
    for family in nx.connected_components(G):
        if len(family) == 1:
            sing += 1

    return len(lem) + sing, len(relations), fam, sing, pos


def etymwn(data):
    """Return statistics for given Etymological WordNet."""
    rel = 0
    sing = 0
    lem = set()
    fam = 0
    pos = defaultdict(int)

    relations = list()
    for line in data:
        line = line.rstrip('\n').split('\t')

        if line[0] not in lem:
            lem.add(line[0])
            pos[''] += 1
        if line[1] not in lem:
            lem.add(line[1])
            pos[''] += 1
        relations.append((line[0], line[1]))
        rel += 1

    G = nx.Graph()
    G.add_edges_from(relations)
    for family in sorted(nx.connected_components(G)):
        if len(family) == 1:
            sing += 1
        else:
            fam += 1

    return len(lem), int(rel), fam, sing, pos


if __name__ == '__main__':
    lem, rel, fam, sing, pos = eval(sys.argv[1])(data=sys.stdin.readlines())
    print(sys.argv[2],
          sys.argv[3] + ' ' + sys.argv[4],
          format(lem, ',d'),
          format(rel, ',d'),
          format(fam, ',d'),
          format(sing, ',d'),
          str(round(pos['N']/lem*100)) + ' / ' +
          str(round(pos['A']/lem*100)) + ' / ' +
          str(round(pos['V']/lem*100)) + ' / ' +
          str(round(pos['D']/lem*100)) + ' / ' +
          str(round(sum([n for p, n in pos.items()
                         if p not in 'NAVD'])/lem*100)),
          sep=' & ')
