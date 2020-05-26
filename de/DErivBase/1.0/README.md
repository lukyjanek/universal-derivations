# Summary

Universal Derivations version of DErivBase (https://www.ims.uni-stuttgart.de/forschung/ressourcen/lexika/DErivBase.html).


# Introduction

DErivBase is a large-coverage derivational lexicon for German. It consists of derivational families connecting lemmas which are derivationally related among each other. Such derivational families are automatically split into semantically consistent clusters. The lexicon was extracted from SDeWAC, a large German web corpus, with HOFM, a rule-based framework written in Haskell.

DErivBase has been harmonized automatically using Machine Learning method.


# Acknowledgments

We wish to thank all the developers and annotators of DErivBase, including Sebastian Padó, Britta D. Zeller, and Jan Šnajder.


## References

As a citation for the resource in articles, please use this:

* Zeller, Brita; Šnajder, Jan; and Padó, Sebastian. 2013. DErivBase: Inducing and Evaluating a Deriva-tional Morphology Resource for German. In Proceedings of ACL 2013. Sofia, Bulgaria, pages 1201–1211. http://www.aclweb.org/anthology/P13-1118.pdf.
* Zeller, Brita; Padó, Sebastian; and Šnajder, Jan. 2014. Towards Semantic Validation of a Derivational Lexicon. In Proceedings of COLING 2014, the 25th International Conference on Computational Linguistics: Technical Papers. Dublin City University and Association for Computational Linguistics, Dublin, Ireland, pages 1728–1739. http://www.aclweb.org/anthology/C14-1163.

```
@INPROCEEDINGS{DErivBase,
    author      = {Zeller, Britta and \v{S}najder, Jan and Pad{\'o}, Sebastian},
    title       = {{DErivBase: Inducing and Evaluating a Derivational Morphology Resource for German}},
    booktitle   = {{Proceedings of ACL 2013}},
    year        = {2013},                  
    address     = {Sofia, Bulgaria},
    pages       = {1201--1211},
    url         = {http://www.aclweb.org/anthology/P13-1118.pdf}
}

@INPROCEEDINGS{DErivBaseClusters,
  author        = {Zeller, Britta  and  Pad\'{o}, Sebastian  and  \v{S}najder, Jan},
  title         = {{Towards Semantic Validation of a Derivational Lexicon}},
  booktitle     = {Proceedings of COLING 2014, the 25th International Conference on Computational Linguistics: Technical Papers},
  month         = {August},
  year          = {2014},
  address       = {Dublin, Ireland},
  publisher     = {Dublin City University and Association for Computational Linguistics},
  pages         = {1728--1739},
  url           = {http://www.aclweb.org/anthology/C14-1163}
}
```


# License

The resource is licensed under the Creative Commons Attribution-ShareAlike 3.0 License (CC BY-SA 3.0).
License text is available in the file `LICENSE.txt`.


# Changelog

* 2020-05 UDer v1.0
    * Automatic reharmonization of DErivBase v2.0 using Machine Learning.
    * Fixing the original manual annotations.
    * Adding new manual annotations.
    * Replacing LEMIDs to IDs in the tenth JSON-encoded column.
* 2019-09 UDer v0.5
    * Including DErivBase v2.0 to the UDer collection.
    * Automatic harmonization using Machine Learning.


<pre>
=== Machine-readable metadata =================================================
Resource: DErivBase
Language: German
Authors: Padó, Sebastian; Zeller, Britta; Šnajder, Jan
License: CC BY-SA 3.0
Contact: https://www.ims.uni-stuttgart.de/forschung/ressourcen/lexika/DErivBase.html
===============================================================================
</pre>

<pre>
=== Machine-readable metadata =================================================
Harmonized version: DErivBase
Harmonized version: 2.0
Data source: http://www.ims.uni-stuttgart.de/forschung/ressourcen/lexika/DErivBase/DErivBase-v2.0.zip
Data available since: UDer v0.5
Harmonization: automatic
Lemmas: 280775
Relations: 43368
Families: 237407
Singletons: 216982
Avarage tree size: 1.2
Avarage tree depth: 0.1
Avarage tree out-degree: 0.1
Maximum tree size: 46
Maximum tree depth: 5
Maximum tree out-degree: 13
Part-of-speech: ADJ, 9.9; NOUN, 85.5; VERB, 4.6
Derivational relations: 43368
Conversion relations: 0
Compounding relations: 0
Common features: Morphological categories; Derivational rules
JSON features: was_in_family_with; other_parents
===============================================================================
</pre>