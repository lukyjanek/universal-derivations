# Summary

Universal Derivations version of D-CELEX (https://catalog.ldc.upenn.edu/LDC96L14).


# Introduction

D-CELEX is one part of CELEX, the large manually created resource providing orthographic, phonetic, morphological, and syntactic annotations. The set of lexemes come from various dictionaries and corpora. The data provides three types of morphological segmentation: (a) an immediate segmentation of lexemes into bases and affixes, (b) a hierarchical segmentation of lexemes into morphemes organised into a tree structure, and (c) a flat segmentation of lexemes into morphemes obtainable from the last tree level.

D-CELEX has been harmonized automatically using Machine Learning method.
Since its original license is restrictive, users have to obtain the original data on their own. Then tha harmonisation can be done using attached Makefile.


# Acknowledgments

We wish to thank all the developers and annotators of (D-)CELEX, including Harald R. Baayen, Richard Piepenbrock, Leon Gulikers.


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
    * Including D-CELEX v2.0 to the UDer collection.
    * Automatic harmonization using Machine Learning.


<pre>
=== Machine-readable metadata =================================================
Resource: D-CELEX
Language: Dutch
Authors: Baayen, Harald R.; Piepenbrock, Richard; Gulikers, Leon
License: GPL-3.0 (for scripts)
Contact: https://catalog.ldc.upenn.edu/LDC96L14
===============================================================================
</pre>

<pre>
=== Machine-readable metadata =================================================
Harmonized resource: D-CELEX
Harmonized version: 2.0
Data source: internal
Data available since: UDer v1.0
Harmonization: automatic
Common features: none
JSON features: was_in_family_with; other_parents; segmentation_hierarch; segmentation; morpheme_order
