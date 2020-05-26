# Summary

Universal Derivations version of G-CELEX (https://catalog.ldc.upenn.edu/LDC96L14).


# Introduction

G-CELEX is one part of CELEX, the large manually created resource providing orthographic, phonetic, morphological, and syntactic annotations. The set of lexemes come from various dictionaries and corpora. The data provides three types of morphological segmentation: (a) an immediate segmentation of lexemes into bases and affixes, (b) a hierarchical segmentation of lexemes into morphemes organised into a tree structure, and (c) a flat segmentation of lexemes into morphemes obtainable from the last tree level.

G-CELEX has been harmonized automatically using Machine Learning method.
Since its original license is restrictive, users have to obtain the original data on their own. Then tha harmonisation can be done using attached Makefile.


# Acknowledgments

We wish to thank all the developers and annotators of (G-)CELEX, including Harald R. Baayen, Richard Piepenbrock, Leon Gulikers.


## References

As a citation for the resource in articles, please use this:

* Baayen, R. H., Piepenbrock, R., and Gulikers, L. (1995). The CELEX lexical database (release 2). Distributed by the Linguistic Data Consortium, University of Pennsylvania.

```
@MISC{CELEX,
  title         = {{CELEX2}},
  author        = {Baayen, Harald R. and Piepenbrock, Richard and Gulikers, Leon},
  address       = {Philadelphia},
  year          = {1995},
  note          = {{Linguistic Data Consortium, Catalogue No. LDC96L14}},
  copyright     = {{CELEX Agreement}}
}
```


# License

The original resource is licensed under the CELEX Agreement.
The harmonisation scripts are licensed under the GNU General Public License v3.0.
License text is available in the file `LICENSE.txt`.


# Changelog

* 2020-05 UDer v1.0
    * Including G-CELEX v2.0 to the UDer collection.
    * Automatic harmonization using Machine Learning.


<pre>
=== Machine-readable metadata =================================================
Resource: G-CELEX
Language: German
Authors: Baayen, Harald R.; Piepenbrock, Richard; Gulikers, Leon
License: GPL-3.0 (for scripts)
Contact: https://catalog.ldc.upenn.edu/LDC96L14
===============================================================================
</pre>

<pre>
=== Machine-readable metadata =================================================
Harmonized resource: G-CELEX
Harmonized version: 2.0
Data source: internal
Data available since: UDer v1.0
Harmonization: automatic
Lemmas: 53282
Relations: 13553
Families: 39729
Singletons: 34156
Avarage tree size: 1.3
Avarage tree depth: 0.2
Avarage tree out-degree: 0.3
Maximum tree size: 39
Maximum tree depth: 11
Maximum tree out-degree: 35
Part-of-speech: A, 0.2; ADJ, 17.2; ADP, 0.4; ADV, 2.3; C, 0.0; D, 0.1; N, 2.0; NOUN, 51.7; NUM, 0.4; P, 0.0; V, 0.6; VERB, 17.2; X, 7.8
Derivational relations: 10990
Conversion relations: 0
Compounding relations: 2563
Common features: none
JSON features: was_in_family_with; other_parents; segmentation_hierarch; segmentation; morpheme_order
===============================================================================
</pre>
