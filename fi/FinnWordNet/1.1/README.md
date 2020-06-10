# Summary

Universal Derivations version of derivational relations extracted from FinnWordNet, Finnish WordNet (https://github.com/frankier/fiwn/).


# Introduction

FinnWordNet is a wordnet for Finnish. It was created by having professional translators translate the word senses of the Princeton WordNet (PWN) v3.0 into Finnish and by combining the translations with the PWN structure. It has been updated and extended among others by some derivational relations (Lindén et al., 2012).

FinnWordNet has been harmonized automatically using Machine Learning method.


# Acknowledgments

We wish to thank all the developers and annotators of FinnWordNet, including Krister Lindén, Jyrki Niemi, Mirka Hyvärinen, Lauri Carlson, Ulla Vanhatalo, Hissu Hyvärinen, Juha Kuokkala, Pinja Pennala, Kristiina Muhonen, Paula Pääkkö.


## References

As a citation for the resource in articles, please use this:

* Lindén, Krister; and Carlson; Lauri. 2010. FinnWordNet – Finnish WordNet by Translation. LexicoNordica – Nordic Journal of Lexicography. 17: 119–140. http://www.ling.helsinki.fi/~klinden/pubs/FinnWordnetInLexicoNordica-en.pdf.
* Lindén, Krister; Niemi, Jyrki; and Hyvärinen, Mirka. 2012. Extending and updating the Finnish Wordnet. In Shall We Play the Festschrift Game?, Springer, pages 67–98.


```
@ARTICLE{FinnWordNet,
    title       = {{FinnWordNet--Finnish WordNet by Translation}},
    author      = {Lind{\'e}n, Krister and Carlson, Lauri},
    journal     = {{LexicoNordica -- Nordic Journal of Lexicography}},
    volume      = {17},
    pages       = {119--140},
    year        = {2010},
    url         = {http://www.ling.helsinki.fi/~klinden/pubs/FinnWordnetInLexicoNordica-en.pdf}
}

@INCOLLECTION{FinnWordNetDerivations,
    title       = {{Extending and updating the Finnish Wordnet}},
    author      = {Lind{\'e}n, Krister and Niemi, Jyrki and Hyv{\"a}rinen, Mirka},
    booktitle   = {Shall We Play the Festschrift Game?},
    pages       = {67--98},
    year        = {2012},
    publisher   = {Springer}
}
```


# License

The resource is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0). Sublicense is WordNet 3.0 License.
License and sublicense texts are available in the file `LICENSE.txt`.


# Changelog

* 2020-06 UDer v1.1
    * Without changes.
* 2020-05 UDer v1.0
    * Automatic reharmonization of FinnWordNet v2.0 using Machine Learning.
    * Fixing the original manual annotations.
    * Adding new manual annotations.
    * Replacing LEMIDs to IDs in the tenth JSON-encoded column.
* 2019-09 UDer v0.5
    * Including FinnWordNet v2.0 to the UDer collection.
    * Automatic harmonization using Machine Learning.


<pre>
=== Machine-readable metadata =================================================
Resource: FinnWordNet
Language: Finnish
Authors: Lindén, Krister; Niemi, Jyrki; Hyvärinen, Mirka
License: CC BY-SA 4.0
Contact: http://www.ling.helsinki.fi/en/lt/research/finnwordnet/
===============================================================================
</pre>

<pre>
=== Machine-readable metadata =================================================
Harmonized resource: FinnWordNet
Harmonized version: 2.0
Data source: https://github.com/frankier/fiwn/raw/master/data/rels/fiwn-lexrels.tsv
Data available since: UDer v0.5
Harmonization: automatic
Lemmas: 20035
Relations: 11850
Families: 8185
Singletons: 1560
Avarage tree size: 2.4
Avarage tree depth: 1.0
Avarage tree out-degree: 1.2
Maximum tree size: 18
Maximum tree depth: 5
Maximum tree out-degree: 13
Part-of-speech: ADJ, 29.2; NOUN, 55.3; VERB, 15.5
Derivational relations: 11850
Conversion relations: 0
Compounding relations: 0
Common features: none
JSON features: was_in_family_with; other_parents
===============================================================================
</pre>
