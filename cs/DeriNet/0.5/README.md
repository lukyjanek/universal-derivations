# Summary

Universal Derivations version of DeriNet (http://www.ufal.mff.cuni.cz/derinet).


# Introduction

DeriNet is the lexical network that captures core word-formation relations for Czech. The network focuses on derivational relations because derivation is the most frequent and the most productive word-formation process in Czech.

The network was initialized with a set of lexemes whose existence was supported by corpus evidence. Derivational links were created using three sources of information: links delivered by a tool for morphological analysis, links based on an automatically discovered set of derivation rules, and on a grammar-based set of rules.

The data structure (the rooted tree) and format of DeriNet (2.0 and above) have become the standard format used in Universal Derivations.


# Acknowledgments

We wish to thank all the developers and annotators of the DeriNet, including Jonáš Vidra, Zdeněk Žabokrtský, Magda Ševčíková, Adéla Kalužová, Lukáš Kyjánek, Šárka Dohnalová, Vojtěch Hudeček, Milan Straka, and Nikita Mediankin.


## References

As a citation for the resource in articles, please use this:

* Vidra, Jonáš; Žabokrtský, Zdeněk; Kyjánek, Lukáš; Ševčíková, Magda; Dohnalová, Šárka. 2019. DeriNet 2.0. LINDAT/CLARIN digital library at the Institute of Formal and Applied Linguistics (ÚFAL) Faculty of Mathematics and Physics, Charles University. http://hdl.handle.net/11234/1-2995.

```
@MISC{DeriNet,
    title       = {{DeriNet 2.0}},
    author      = {Vidra, Jon{\'a}{\v s} and {\v Z}abokrtsk{\'y}, Zden{\v e}k and Kyj{\'a}nek, Luk{\'a}{\v s} and {\v S}ev{\v c}{\'{\i}}kov{\'a}, Magda and Dohnalov{\'a}, {\v S}{\'a}rka},
    url         = {http://hdl.handle.net/11234/1-2995},
    note        = {{LINDAT}/{CLARIN} digital library at the Institute of Formal and Applied Linguistics ({{\'U}FAL}), Faculty of Mathematics and Physics, Charles University},
    copyright   = {Attribution-{NonCommercial}-{ShareAlike} 3.0 Unported ({CC} {BY}-{NC}-{SA} 3.0)},
    year        = {2019}
}
```


# License

The resource is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License (CC BY-NC-SA 3.0).
License text is available in the file `LICENSE.txt`.


# Changelog

* 2019-09 UDer v0.5
    * Including DeriNet v2.0 to the UDer collection.
    * Original part-of-speech categories unified.
    * No harmonization of the data structure needed.


<pre>
=== Machine-readable metadata =================================================
Resource: DeriNet
Language: Czech
Authors: Vidra, Jonáš; Žabokrtský, Zdeněk; Ševčíková, Magda; Kalužová, Adéla; Kyjánek, Lukáš; Dohnalová, Šárka; Hudeček, Vojtěch; Straka, Milan; Mediankin, Nikita
License: CC BY-NC-SA 3.0
Contact: http://ufal.mff.cuni.cz/derinet
===============================================================================
</pre>

<pre>
=== Machine-readable metadata =================================================
Harmonized version: DeriNet v2.0
Data source: https://github.com/vidraj/derinet/raw/master/data/releases/cs/derinet-2-0.tsv.gz
Data available since: UDer v0.5
Harmonization: default
Common features: Segmentations; Semantic labels; Morphological categories
JSON features: techlemma; is_compound; segmentation
