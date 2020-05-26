# Summary

Universal Derivations version of CatVar, the Categorial Variation Database (https://clipdemos.umiacs.umd.edu/catvar/ and https://github.com/nizarhabash1/catvar).


# Introduction

CatVar is an automaticallyconstructed word-formation database of English derivationally related nouns, adjectives, verbs, and adverbs. Word-formation families were based on the morphological segmentation obtained from several morphological segmenters and the English part of CELEX. Some relations were also included from ADJADV (NomBank).

CatVar has been harmonized automatically using Machine Learning method.


# Acknowledgments

We wish to thank all the developers and annotators of CatVar, including Nizar Habash and Bonnie Dorr.


## References

As a citation for the resource in articles, please use this:

* Habash, Nizar and Dorr, Bonnie. A Categorial Variation Database for English. In Proceedings of the North American Association for Computational Linguistics (NAACL'03), Edmonton, Canada, 2003, pp. 17--23.

```
@INPROCEEDINGS{CatVar,
	address     = {Edmonton, Canada},
	author      = {Nizar Habash and Bonnie Dorr},
	booktitle   = {{Proceedings of the North American Association for Computational Linguistics (NAACL'03)}},
	pages       = {17--23},
	title       = {{A Categorial Variation Database for English}},
	year        = {2003}
}
```


# License

The resource is licensed under the Open Software License version 1.1 (OSL-1.1).
License text is available in the file `LICENSE.txt`.


# Changelog

* 2020-05 UDer v1.0
    * Including CatVar v2.1 to the UDer collection.
    * Automatic harmonization using Machine Learning.


<pre>
=== Machine-readable metadata =================================================
Resource: CatVar
Language: English
Authors: Habash, Nizar; Dorr, Bonnie
License: OSL-1.1
Contact: https://clipdemos.umiacs.umd.edu/catvar/
===============================================================================
</pre>

<pre>
=== Machine-readable metadata =================================================
Harmonized resource: CatVar
Harmonized version: 2.1
Data source: https://raw.githubusercontent.com/nizarhabash1/catvar/master/catvar21.signed
Data available since: UDer v1.0
Harmonization: automatic
Lemmas: 82675
Relations: 25096
Families: 57579
Singletons: 45626
Avarage tree size: 1.4
Avarage tree depth: 0.3
Avarage tree out-degree: 0.3
Maximum tree size: 18
Maximum tree depth: 7
Maximum tree out-degree: 10
Part-of-speech: ADJ, 24.4; ADV, 4.6; NOUN, 60.0; VERB, 11.1
Derivational relations: 25096
Conversion relations: 0
Compounding relations: 0
Common features: none
JSON features: was_in_family_with; other_parents
===============================================================================
</pre>