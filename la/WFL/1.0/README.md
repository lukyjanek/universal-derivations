# Summary

Universal Derivations version of Word Formation Latin (https://wflblog.wordpress.com/) extracted from LEMLAT v3.0 (https://github.com/CIRCSE/LEMLAT3).


# Introduction

Word Formation Latin (WFL) is a derivational morphology resource for Classical Latin, where lemmas are analysed into their formative components, and relationships between them are established on the basis of Word Formation Rules. For example 'amo' (to love) and 'amator' (lover) are connected with a relationship that describes a change from a verb to a noun through the addition of a suffix (-a-tor) that in itself bears semantic information (in this case it characterises agentive and instrumental nouns, i.e. someone or something performing an action). WFL has been included in Morphological analyzer and lemmatizer for Latin, LEMLAT.

Word Formation Latin has been harmonized manually.


# Acknowledgments

We wish to thank all the developers and annotators of the Word Formation Latin, including Eleonora Litta, Marco Passarotti, and Chris Culy.


## References

As a citation for the resource in articles, please use this:

* Litta, Eleonora; Passarotti, Marco; and Culy, Chris. 2016. Formatio Formosa est. Building a Word Formation Lexicon for Latin. In Proceedings of the 3rd Italian Conference on Computational Linguistics, pages 185–189. http://ceur-ws.org/Vol-1749/paper32.pdf.


```
@INPROCEEDINGS{WordFormationLatin,
    title       = {{Formatio formosa est. Building a Word Formation Lexicon for Latin}},
    author      = {Litta, Eleonora and Passarotti, Marco and Culy, Chris},
    booktitle   = {{Proceedings of the third italian conference on computational linguistics (clic--it 2016)}},
    pages       = {185--189},
    year        = {2016},
    url         = {http://ceur-ws.org/Vol-1749/paper32.pdf}
}
```


# License

The resource is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).
License text is available in the file `LICENSE.txt`.


# Changelog

* 2020-05 UDer v1.0
    * Updating WFL v2019.
    * Replacing LEMIDs to IDs in the tenth JSON-encoded column.
* 2019-09 UDer v0.5
    * Including WFL v2017 to the UDer collection.
    * Manual harmonization.


<pre>
=== Machine-readable metadata =================================================
Resource: Word Formation Latin
Language: Latin
Authors: Litta, Eleonora; Passarotti, Marco; Culy, Chris
License: CC BY-NC-SA 4.0
Contact: https://progetti.unicatt.it/progetti-milan-wfl-home
===============================================================================
</pre>

<pre>
=== Machine-readable metadata =================================================
Harmonized resource: Word Formation Latin
Harmonized version: 2019
Data source: https://raw.githubusercontent.com/CIRCSE/LEMLAT3/master/lemlat_db_26-07-2019.sql
Data available since: UDer v0.5
Harmonization: manual
Lemmas: 36417
Relations: 32414
Families: 4003
Singletons: 121
Avarage tree size: 9.1
Avarage tree depth: 1.7
Avarage tree out-degree: 4.3
Maximum tree size: 524
Maximum tree depth: 6
Maximum tree out-degree: 236
Part-of-speech: ADJ, 29.0; AUX, 0.4; NOUN, 46.1; PRON, 0.3; VERB, 21.2; X, 3.0
Derivational relations: 25212
Conversion relations: 4929
Compounding relations: 2273
Common features: Morphological categories; Compounding; Conversion
JSON features: was_in_family_with; other_parents
===============================================================================
</pre>
