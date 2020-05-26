.PHONY: all ../py3env/
SHELL=/bin/bash

# install virtual environment (base)
../py3env/:
	@cd ../ && $(MAKE) -s py3env/

# statistics for each available datasets
# before running scripts, the downloading and potentially renaming of
# datasets are required for some resources
# add datasets manually for: Derinet.FA, CELEX, E-Lex, PlWordNet
all: ../py3env/
	$(MAKE) -s morpholexen >> input-data-statistics.txt
	$(MAKE) -s morpholexfr >> input-data-statistics.txt
	$(MAKE) -s derivbaseru >> input-data-statistics.txt
	$(MAKE) -s derivbasehr >> input-data-statistics.txt
	$(MAKE) -s derinet >> input-data-statistics.txt
	$(MAKE) -s polishwfn >> input-data-statistics.txt
	$(MAKE) -s spanishwfn >> input-data-statistics.txt
	$(MAKE) -s derinetes >> input-data-statistics.txt
	$(MAKE) -s derinetfa >> input-data-statistics.txt
	$(MAKE) -s catvar >> input-data-statistics.txt
	$(MAKE) -s demonette >> input-data-statistics.txt
	$(MAKE) -s verbaction >> input-data-statistics.txt
	$(MAKE) -s morphonette >> input-data-statistics.txt
	$(MAKE) -s derivbase >> input-data-statistics.txt
	$(MAKE) -s derivcelex >> input-data-statistics.txt
	$(MAKE) -s derivatario >> input-data-statistics.txt
	$(MAKE) -s celex >> input-data-statistics.txt
	$(MAKE) -s princetonwn >> input-data-statistics.txt
	$(MAKE) -s estwn >> input-data-statistics.txt
	$(MAKE) -s finnwn >> input-data-statistics.txt
	$(MAKE) -s sloleks >> input-data-statistics.txt
	$(MAKE) -s finudpud >> input-data-statistics.txt
	$(MAKE) -s finudtdt >> input-data-statistics.txt
	$(MAKE) -s kozyudkpv >> input-data-statistics.txt
	$(MAKE) -s wfl >> input-data-statistics.txt
	$(MAKE) -s plwn >> input-data-statistics.txt
	$(MAKE) -s elex >> input-data-statistics.txt
	$(MAKE) -s enwikti >> input-data-statistics.txt
	$(MAKE) -s cswikti >> input-data-statistics.txt
	$(MAKE) -s dewikti >> input-data-statistics.txt
	$(MAKE) -s plwikti >> input-data-statistics.txt
	$(MAKE) -s frwikti >> input-data-statistics.txt
	$(MAKE) -s famorphoFR >> input-data-statistics.txt
	$(MAKE) -s nomage >> input-data-statistics.txt
	$(MAKE) -s nomlex >> input-data-statistics.txt
	$(MAKE) -s nombank >> input-data-statistics.txt
	$(MAKE) -s nomlexpt >> input-data-statistics.txt
	$(MAKE) -s etymwn >> input-data-statistics.txt
	cat input-data-statistics.txt | sort > sorted-statistics.txt
	mv sorted-statistics.txt input-data-statistics.txt

# English MorphoLex-en
../@input-data/MorphoLEX_en.xlsx:
	@wget https://github.com/hugomailhot/MorphoLex-en/raw/master/MorphoLEX_en.xlsx -P ../@input-data/

morpholexen: ../@input-data/MorphoLEX_en.xlsx ../py3env/
	@echo '' | ../py3env/bin/python3 input-statistics.py 'morpholexen' English 'MorphoLex-en' 1.0 '../@input-data/MorphoLEX_en.xlsx'

# French MorphoLex-fr
../@input-data/Morpholex_FR.xlsx:
	@wget https://github.com/hugomailhot/morpholex-fr/raw/master/xlsx/Morpholex_FR.xlsx -P ../@input-data/

morpholexfr: ../@input-data/Morpholex_FR.xlsx ../py3env/
	@echo '' | ../py3env/bin/python3 input-statistics.py 'morpholexfr' French 'MorphoLex-fr' 1.0 '../@input-data/Morpholex_FR.xlsx'

# Russian DerivBase.Ru
../@input-data/derivbaseRU-noun.txt:
	@wget -O ../@input-data/derivbaseRU-connections.zip https://github.com/s231644/DerivBaseRu/raw/master/data/wiktionary/v001.00-connections.zip
	@wget -O ../@input-data/derivbaseRU-noun.txt https://github.com/s231644/DerivBaseRu/raw/master/data/wiktionary/noun.txt
	@wget -O ../@input-data/derivbaseRU-verb.txt https://raw.githubusercontent.com/s231644/DerivBaseRu/master/data/wiktionary/verb.txt
	@wget -O ../@input-data/derivbaseRU-adj.txt https://github.com/s231644/DerivBaseRu/raw/master/data/wiktionary/adj.txt
	@wget -O ../@input-data/derivbaseRU-adv.txt https://raw.githubusercontent.com/s231644/DerivBaseRu/master/data/wiktionary/adv.txt

derivbaseru: #../@input-data/derivbaseRU-noun.txt ../py3env/
	@mkdir -p original-data/
	@cat ../@input-data/derivbaseRU-noun.txt | sed -e 's/$$/_N/g' >> original-data/tagged.txt
	@cat ../@input-data/derivbaseRU-adj.txt | sed -e 's/$$/_A/g' >> original-data/tagged.txt
	@cat ../@input-data/derivbaseRU-verb.txt | sed -e 's/$$/_V/g' >> original-data/tagged.txt
	@cat ../@input-data/derivbaseRU-adv.txt | sed -e 's/$$/_D/g' >> original-data/tagged.txt
	@unzip -d original-data/ ../@input-data/derivbaseRU-connections.zip
	@for file in $$(ls original-data/connections_*.csv) ; do \
		sed '1d' $$file >> original-data/connections.csv ;\
	done
	@cat 'original-data/connections.csv' | ../py3env/bin/python3 input-statistics.py 'derivbaseru' Russian DerivBase.Ru 1.0 'original-data/tagged.txt'
	@rm -rf 'original-data/'

# Croatian DerivBase.hr
../@input-data/DerivBase.hr.v1.tar.gz:
	@wget 'http://takelab.fer.hr/data/derivbasehr/DerivBase.hr.v1.tar.gz' -P ../@input-data/

derivbasehr: ../@input-data/DerivBase.hr.v1.tar.gz ../py3env/
	@tar -xzf '../@input-data/DerivBase.hr.v1.tar.gz'
	@cat 'DerivBase.hr.v1/DerivBase.hr.K.v1.0' | ../py3env/bin/python3 input-statistics.py 'derivbasehr' Croatian DerivBase.Hr 1.0
	@rm -rf 'DerivBase.hr.v1'

# Czech DeriNet
../@input-data/derinet-2-0.tsv:
	@curl --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2995{/derinet-2-0.tsv} -o ../@input-data/derinet-2-0.tsv

derinet: ../@input-data/derinet-2-0.tsv ../py3env/
	@cat '../@input-data/derinet-2-0.tsv' | ../py3env/bin/python3 input-statistics.py 'derinet' Czech DeriNet 2.0

# Polish Word-Formation Network
../@input-data/polish-wfn-0.5.zip:
	@wget 'https://ufal.mff.cuni.cz/~vidra/derinet/polish-wfn-0.5.zip' -P ../@input-data/

polishwfn: ../@input-data/polish-wfn-0.5.zip ../py3env/
	@unzip -q ../@input-data/polish-wfn-0.5.zip
	@cat 'polish-wfn-0.5/polish-wfn.tsv' | ../py3env/bin/python3 input-statistics.py 'polishwfn' Polish 'The Polish WFN' 0.5
	@rm -rf 'polish-wfn-0.5.zip' 'polish-wfn-0.5/'

# Spanish Word-Formation Network
../@input-data/spanish-wfn-0.5.zip:
	@wget 'http://ufal.mff.cuni.cz/~zabokrtsky/derinet/spanish-wfn-0.5.zip' -P ../@input-data/

spanishwfn: ../@input-data/spanish-wfn-0.5.zip ../py3env/
	@unzip -q ../@input-data/spanish-wfn-0.5.zip
	@cat 'spanish-wfn-0.5/spanish-wfn.tsv' | ../py3env/bin/python3 input-statistics.py 'spanishwfn' Spanish 'The Spanish WFN' 0.5
	@rm -rf 'spanish-wfn-0.5.zip' 'spanish-wfn-0.5/'

# Spanish DeriNet.ES
../@input-data/derinet-es-2019-05-10.tsv:
	@wget 'https://ufal.mff.cuni.cz/~vidra/derinet/derinet-es-2019-05-10.tsv' -P ../@input-data/

derinetes: ../@input-data/derinet-es-2019-05-10.tsv ../py3env/
	@cat '../@input-data/derinet-es-2019-05-10.tsv' | ../py3env/bin/python3 input-statistics.py 'derinetes' Spanish 'DeriNet.ES' 0.5

# Persian DeriNet.FA
../@input-data/DeriNetFA-UfalFormat.tsv:
	@echo -e 'You need "DeriNetFA-UfalFormat.tsv". Try to contact Ebrahim Ansari.'

derinetfa: ../@input-data/DeriNetFA-UfalFormat.tsv ../py3env/
	@cat '../@input-data/DeriNetFA-UfalFormat.tsv' | ../py3env/bin/python3 input-statistics.py 'derinetfa' Persian 'DeriNet.FA' 0.5

# English CatVar
../@input-data/catvar21.signed:
	@wget 'https://raw.githubusercontent.com/nizarhabash1/catvar/master/catvar21.signed' -P ../@input-data/

catvar: ../@input-data/catvar21.signed ../py3env/
	@cat '../@input-data/catvar21.signed' | ../py3env/bin/python3 input-statistics.py 'catvar' English 'CatVar' 2.1

# French Démonette
../@input-data/demonette-1.2.zip:
	@wget 'http://redac.univ-tlse2.fr/lexiques/demonette/demonette-1.2.zip' -P ../@input-data/

demonette: ../@input-data/demonette-1.2.zip ../py3env/
	@unzip -q '../@input-data/demonette-1.2.zip'
	@cat 'demonette-1.2.xml' | ../py3env/bin/python3 input-statistics.py 'demonette' French 'Démonette' 1.2
	@rm -rf 'demonette-1.2.csv' 'demonette-1.2.ods' 'demonette-1.2.xlsx' 'demonette-1.2.xml' 'manuel-1.2.pdf'

# French Verbaction
../@input-data/Verbaction-1.0.zip:
	@wget 'http://redac.univ-tlse2.fr/lexiques/verbaction/Verbaction-1.0.zip' -P ../@input-data/

verbaction: ../@input-data/Verbaction-1.0.zip ../py3env/
	@unzip -q '../@input-data/Verbaction-1.0.zip'
	@cat 'Verbaction-1.0/Verbaction-1.0.xml' | sed -e '2d' > 'Verbaction-1.0/Verbaction-1.0-cor.xml'
	@iconv -f 'iso-8859-1' -t 'utf-8' 'Verbaction-1.0/Verbaction-1.0-cor.xml' > 'Verbaction-1.0/Verbaction-1.0-cor-utf8.xml'
	@cat 'Verbaction-1.0/Verbaction-1.0-cor-utf8.xml' | ../py3env/bin/python3 input-statistics.py 'verbaction' French 'VerbAction' 1.0
	@rm -rf 'Verbaction-1.0'

# French Morphonette
../@input-data/morphonette-0.1.zip:
	@wget 'http://redac.univ-tlse2.fr/lexiques/morphonette/morphonette-0.1.zip' -P ../@input-data/

morphonette: ../@input-data/morphonette-0.1.zip ../py3env/
	@unzip -q '../@input-data/morphonette-0.1.zip'
	@cat 'morphonette-0.1.xml' | ../py3env/bin/python3 input-statistics.py 'morphonette' French 'Morphonette' 0.1
	@rm -rf 'header.xml' 'morphonette-0.1.xml' 'morphonette-0.1.dtd' 'Licence.txt'

# German DerivBase
../@input-data/derivbase-v2.0.zip:
	wget 'https://www.ims.uni-stuttgart.de/documents/ressourcen/lexika/derivbase/derivbase-v2.0.zip' -P ../@input-data/

derivbase: ../@input-data/derivbase-v2.0.zip ../py3env/
	@unzip -q '../@input-data/derivbase-v2.0.zip'
	@cat 'derivbase/DErivBase-v2.0-rulePaths.txt' | ../py3env/bin/python3 input-statistics.py 'derivbase' German 'DErivBase' 2.0 'derivbase/DErivBase-v2.0-families.txt'
	@rm -rf 'derivbase'

# German DerivCELEX
../@input-data/derivcelex-v2.txt:
	@wget 'https://www.ims.uni-stuttgart.de/documents/ressourcen/lexika/derivbase/derivcelex-v2.txt' -P ../@input-data/

derivcelex: ../@input-data/derivcelex-v2.txt ../py3env/
	@cat '../@input-data/derivcelex-v2.txt' | cut -d ' ' -f 2- > 'DErivCelex-v2-cor.txt'
	@cat 'DErivCelex-v2-cor.txt' | ../py3env/bin/python3 input-statistics.py 'derivcelex' German 'DErivCELEX' 2.0
	@rm -rf 'DErivCelex-v2-cor.txt'

# Italian DerIvaTario
../@input-data/derivatario.csv:
	@wget 'http://derivatario.sns.it/derivatario.csv' -P ../@input-data/

../@input-data/Lemmi_rango_txt.zip:
	@wget 'http://linguistica.sns.it/CoLFIS/files/Lemmi_rango_txt.zip' -P ../@input-data/

derivatario: ../@input-data/derivatario.csv ../@input-data/Lemmi_rango_txt.zip ../py3env/
	@unzip -q '../@input-data/Lemmi_rango_txt.zip'
	@cat 'Lemmi_rango.txt' | sed -e '1d' | sed -e "s/[\'\:\(\)\-\–\/\<\>\.\?\!\+\&]/a/g" -e 's/[\"-]/a/g' -e 's/\,\s[a-zA-Z0-9]*/a/g' -e 's/[a-zA-Z0-9]\s[a-zA-Z0-9]/a/g' -e 's/[a-zA-Z0-9]\s[a-zA-Z0-9]/a/g' -e 's/[a-zA-Z0-9]\s[a-zA-Z0-9]/a/g' | tr -s ' ' | cut -d ' ' -f 1,17  | sed -e 's/VaaC@/VA-IN-TC@/g' | sed -e 's/aaC@/V-IN-TC@/g' | sed -e 's/3407 MINUTO/3407 E@/g' | sed -e 's/88190 W/88190 E/g' > 'derivatario-pos-list.txt'
	@cat '../@input-data/derivatario.csv' | while read -r a; do echo -ne $$a'\t' >> 'derivatario-with-pos.txt'; echo $$a | cut -d ';' -f 1 | tr '\n' ' ' | sed -e 's/^/\^/g' | grep -f - 'derivatario-pos-list.txt' | cut -d ' ' -f 2 >> 'derivatario-with-pos.txt'; done
	@cat 'derivatario-with-pos.txt' | ../py3env/bin/python3 input-statistics.py 'derivatario' Italian 'DerIvaTario' 1.0
	@rm -rf 'derivatario-with-pos.txt' 'derivatario-pos-list.txt' 'Lemmi_rango.txt' 'read me Lemmi_rango txt.txt'

# Dutch, English and German CELEX
../@input-data/celex2.zip:
	@echo -e 'You need "celex2.zip". It is not free. More info here:\n\thttps://catalog.ldc.upenn.edu/LDC96L14'

celex: ../@input-data/celex2.zip ../py3env/
	@unzip -q '../@input-data/celex2.zip'
	@cat 'celex2/dutch/dml/dml.cd' | ../py3env/bin/python3 input-statistics.py 'dcelex' Dutch 'D-CELEX' 2.0
	@cat 'celex2/german/gml/gml.cd' | ../py3env/bin/python3 input-statistics.py 'gcelex' German 'G-CELEX' 2.0
	@cat 'celex2/english/eml/eml.cd' | ../py3env/bin/python3 input-statistics.py 'ecelex' English 'E-CELEX' 2.0
	@rm -rf 'celex2'

# English Princeton WordNet
../@input-data/morphosemantic-links.xls:
	@wget 'http://wordnetcode.princeton.edu/standoff-files/morphosemantic-links.xls' -P ../@input-data/

princetonwn: ../@input-data/morphosemantic-links.xls ../py3env/
	@xls2csv '../@input-data/morphosemantic-links.xls' > 'princetonWordnet.csv'
	@cat 'princetonWordnet.csv' | sed -e '1d' | ../py3env/bin/python3 input-statistics.py 'princetonwn' English 'The Morpho-Semantic Database' 1.0
	@rm -rf 'princetonWordnet.csv'

# Estonian Estonian Wordnet (EstWN)
../@input-data/estwn-et-2.1.0.wip.xml:
	@wget 'https://gitlab.keeleressursid.ee/avalik/data/raw/master/estwn/estwn-et-2.1.0.wip.xml' -P ../@input-data/

estwn: ../@input-data/estwn-et-2.1.0.wip.xml ../py3env/
	@cat '../@input-data/estwn-et-2.1.0.wip.xml' | ../py3env/bin/python3 input-statistics.py 'estwn' Estonian EstWordNet 2.1

# Finnish Finnish Wordnet (FinnWN)
../@input-data/fiwn-lexrels.tsv:
	@wget 'https://github.com/frankier/fiwn/raw/master/data/rels/fiwn-lexrels.tsv' -P ../@input-data/

finnwn: ../@input-data/fiwn-lexrels.tsv ../py3env/
	@cat '../@input-data/fiwn-lexrels.tsv' | ../py3env/bin/python3 input-statistics.py 'finnwn' Finnish 'FinnWordNet' 2.0

# Slovene Sloleks
../@input-data/Sloleks2.0.LMF.zip:
	@curl --remote-name-all https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1230{/Sloleks2.0.LMF.zip} -o ../@input-data/Sloleks2.0.LMF.zip

sloleks: ../@input-data/Sloleks2.0.LMF.zip ../py3env/
	@unzip -q '../@input-data/Sloleks2.0.LMF.zip'
	@echo '' | ../py3env/bin/python3 input-statistics.py 'sloleks' Slovene 'Sloleks' 1.2 'Sloleks2.0.LMF/sloleks_clarin_2.0.xml'
	@rm -rf 'Sloleks_v1.2.xml' 'Sloleks2.0.LMF'

# Finnish PUD
../@input-data/fi_pud-ud-test.conllu:
	@wget 'https://raw.githubusercontent.com/UniversalDependencies/UD_Finnish-PUD/master/fi_pud-ud-test.conllu' -P ../@input-data/

finudpud: ../@input-data/fi_pud-ud-test.conllu ../py3env/
	@cat '../@input-data/fi_pud-ud-test.conllu' | ../py3env/bin/python3 input-statistics.py 'finudpud' Finnish 'PUD UD Treebank' 2.0
	@rm -rf 'fi_pud-ud-test.conllu'

# Finnish TDT
../@input-data/fi_tdt-ud-test.conllu:
	@wget 'https://raw.githubusercontent.com/UniversalDependencies/UD_Finnish-TDT/master/fi_tdt-ud-train.conllu' -P ../@input-data/
	@wget 'https://raw.githubusercontent.com/UniversalDependencies/UD_Finnish-TDT/master/fi_tdt-ud-dev.conllu' -P ../@input-data/
	@wget 'https://raw.githubusercontent.com/UniversalDependencies/UD_Finnish-TDT/master/fi_tdt-ud-test.conllu' -P ../@input-data/

finudtdt: ../@input-data/fi_tdt-ud-test.conllu ../py3env/
	@cat '../@input-data/fi_tdt-ud-train.conllu' >> 'fi_tdt-ud-all.conllu'
	@cat '../@input-data/fi_tdt-ud-dev.conllu' >> 'fi_tdt-ud-all.conllu'
	@cat '../@input-data/fi_tdt-ud-test.conllu' >> 'fi_tdt-ud-all.conllu'
	@cat 'fi_tdt-ud-all.conllu' | ../py3env/bin/python3 input-statistics.py 'finudtdt' Finnish 'TDT UD Treebank' 5.0
	@rm 'fi_tdt-ud-all.conllu'

# Komi-Zyrian Lattice
../@input-data/kpv_lattice-ud-test.conllu:
	@wget 'https://raw.githubusercontent.com/UniversalDependencies/UD_Komi_Zyrian-Lattice/master/kpv_lattice-ud-test.conllu' -P ../@input-data/

kozyudkpv: ../@input-data/kpv_lattice-ud-test.conllu ../py3env/
	@cat '../@input-data/kpv_lattice-ud-test.conllu' | ../py3env/bin/python3 input-statistics.py 'kozyudkpv' Komi-Zyrian 'Lattice UD Treebank' 1.0

# Word-Formation Latin
../@input-data/lemlat_db_26-07-2019.sql:
	@wget 'https://raw.githubusercontent.com/CIRCSE/LEMLAT3/master/lemlat_db_26-07-2019.sql' -P ../@input-data/

wfl: ../@input-data/lemlat_db_26-07-2019.sql ../py3env/
	@grep -e 'INSERT INTO `lemmario`' '../@input-data/lemlat_db_26-07-2019.sql' | sed -e 's/^.*VALUES //g' | sed -e 's/;//g' | sed -e 's/),(/)\n(/g' > 'lemlat3-lemmario.txt'
	@grep -e 'INSERT INTO `lemmas_wfr`' '../@input-data/lemlat_db_26-07-2019.sql' | sed -e 's/^.*VALUES //g' | sed -e 's/;//g' | sed -e 's/),(/)\n(/g' > 'lemlat3-lemmaswfr.txt'
	@cat 'lemlat3-lemmaswfr.txt' | ../py3env/bin/python3 input-statistics.py 'wfl' Latin 'Word Formation Latin' 2019 'lemlat3-lemmario.txt'
	@rm -rf 'lemlat3-lemmaswfr.txt' 'lemlat3-lemmario.txt'

# Polish WordNet
../@input-data/plwordnet_4_0.zip:
	@echo -e 'You need "plwordnet_4_0.zip". Try to fill the license agreement and download data. Both here:\n\thttp://nlp.pwr.wroc.pl/plwordnet/download/?lang=eng'

plwn: ../@input-data/plwordnet_4_0.zip ../py3env/
	@unzip '../@input-data/plwordnet_4_0.zip'
	@cat 'plwordnet_4_0/plwordnet-4.0.xml' | ../py3env/bin/python3 input-statistics.py 'plwn' Polish 'PlWordNet' 4.0
	@rm -rf 'plwordnet_4_0'

# Dutch E-lex
../@input-data/e-Lex_1.1.1.zip:
	@echo -e 'You need "e-Lex_1.1.1.zip". Register, confirm the agreement and download it here:\n\thttps://ivdnt.org/downloads/taalmaterialen/tstc-e-lex'

elex: ../@input-data/e-Lex_1.1.1.zip ../py3env/
	@unzip -q '../@input-data/e-Lex_1.1.1.zip'
	@cat 'Data/e-Lex-1.1.txt' | ../py3env/bin/python3 input-statistics.py 'elex' Dutch 'E-Lex' 1.1.1
	@rm -rf 'Data' 'Doc'

# English Wiktionary
../@input-data/en-wiktiwf-D-1-0.tsv:
	@wget 'https://raw.githubusercontent.com/lukyjanek/wiktionary-wf/master/releases/en/en-wiktiwf-D-1-0.tsv' -P ../@input-data/

../@input-data/en-wiktiwf-C-1-0.tsv:
	@wget 'https://raw.githubusercontent.com/lukyjanek/wiktionary-wf/master/releases/en/en-wiktiwf-C-1-0.tsv' -P ../@input-data/

enwikti: ../@input-data/en-wiktiwf-D-1-0.tsv ../@input-data/en-wiktiwf-C-1-0.tsv ../py3env/
	@cat '../@input-data/en-wiktiwf-D-1-0.tsv' | ../py3env/bin/python3 input-statistics.py 'wikti' English 'En-WiktiWF' 1.0 '../@input-data/en-wiktiwf-C-1-0.tsv'

# Czech Wiktionary
../@input-data/cs-wiktiwf-D-1-0.tsv:
	@wget 'https://raw.githubusercontent.com/lukyjanek/wiktionary-wf/master/releases/cs/cs-wiktiwf-D-1-0.tsv' -P ../@input-data/

../@input-data/cs-wiktiwf-C-1-0.tsv:
	@wget 'https://raw.githubusercontent.com/lukyjanek/wiktionary-wf/master/releases/cs/cs-wiktiwf-C-1-0.tsv' -P ../@input-data/

cswikti: ../@input-data/cs-wiktiwf-D-1-0.tsv ../@input-data/cs-wiktiwf-C-1-0.tsv ../py3env/
	@cat '../@input-data/cs-wiktiwf-D-1-0.tsv' | ../py3env/bin/python3 input-statistics.py 'wikti' Czech 'Cs-WiktiWF' 1.0 '../@input-data/cs-wiktiwf-C-1-0.tsv'

# German Wiktionary
../@input-data/de-wiktiwf-D-1-0.tsv:
	@wget 'https://raw.githubusercontent.com/lukyjanek/wiktionary-wf/master/releases/de/de-wiktiwf-D-1-0.tsv' -P ../@input-data/

../@input-data/de-wiktiwf-C-1-0.tsv:
	@wget 'https://raw.githubusercontent.com/lukyjanek/wiktionary-wf/master/releases/de/de-wiktiwf-C-1-0.tsv' -P ../@input-data/

dewikti: ../@input-data/de-wiktiwf-D-1-0.tsv ../@input-data/de-wiktiwf-C-1-0.tsv ../py3env/
	@cat '../@input-data/de-wiktiwf-D-1-0.tsv' | ../py3env/bin/python3 input-statistics.py 'wikti' German 'De-WiktiWF' 1.0 '../@input-data/de-wiktiwf-C-1-0.tsv'

# Polish Wiktionary
../@input-data/pl-wiktiwf-D-1-0.tsv:
	@wget 'https://raw.githubusercontent.com/lukyjanek/wiktionary-wf/master/releases/pl/pl-wiktiwf-D-1-0.tsv' -P ../@input-data/

../@input-data/pl-wiktiwf-C-1-0.tsv:
	@wget 'https://raw.githubusercontent.com/lukyjanek/wiktionary-wf/master/releases/pl/pl-wiktiwf-C-1-0.tsv' -P ../@input-data/

plwikti: ../@input-data/pl-wiktiwf-D-1-0.tsv ../@input-data/pl-wiktiwf-C-1-0.tsv ../py3env/
	@cat '../@input-data/pl-wiktiwf-D-1-0.tsv' | ../py3env/bin/python3 input-statistics.py 'wikti' Polish 'Pl-WiktiWF' 1.0 '../@input-data/pl-wiktiwf-C-1-0.tsv'

# French Wiktionary
../@input-data/fr-wiktiwf-D-1-0.tsv:
	@wget 'https://raw.githubusercontent.com/lukyjanek/wiktionary-wf/master/releases/fr/fr-wiktiwf-D-1-0.tsv' -P ../@input-data/

../@input-data/fr-wiktiwf-C-1-0.tsv:
	@wget 'https://raw.githubusercontent.com/lukyjanek/wiktionary-wf/master/releases/fr/fr-wiktiwf-C-1-0.tsv' -P ../@input-data/

frwikti: ../@input-data/fr-wiktiwf-D-1-0.tsv ../@input-data/fr-wiktiwf-C-1-0.tsv ../py3env/
	@cat '../@input-data/fr-wiktiwf-D-1-0.tsv' | ../py3env/bin/python3 input-statistics.py 'wikti' French 'Fr-WiktiWF' 1.0 '../@input-data/fr-wiktiwf-C-1-0.tsv'

# French Famorph-FR
../@input-data/famorpho-fr.zip:
	@wget 'http://redac.univ-tlse2.fr/lexiques/famorpho-fr/famorpho-fr.zip' -P ../@input-data/

famorphoFR: ../@input-data/famorpho-fr.zip ../py3env/
	@unzip -q '../@input-data/famorpho-fr.zip'
	@cat 'famorpho-fr.xml' | ../py3env/bin/python3 input-statistics.py 'famorphoFR' French 'Famorpho-FR' 1.0
	@rm -rf 'famorpho-fr.xml' 'famorpho-fr.dtd' 'famorpho-header.xml' 'header.xml' 'Licence.txt'

# French Nomage
../@input-data/LMF_nomage_2011-12-10.gz:
	@wget 'https://github.com/abalvet/nomage/raw/master/XML_LMF_Nomage_Lexicon_v1.0/LMF_nomage_2011-12-10.gz' -P ../@input-data/

nomage: ../@input-data/LMF_nomage_2011-12-10.gz ../py3env/
	@gunzip -qv '../@input-data/LMF_nomage_2011-12-10.gz'
	@cat '../@input-data/LMF_nomage_2011-12-10' | ../py3env/bin/python3 input-statistics.py 'nomage' French 'Nomage' 1.0

# English NOMLEX
../@input-data/NOMLEX-2001.exp:
	@wget 'https://nlp.cs.nyu.edu/nomlex/NOMLEX-2001.exp' -P ../@input-data/

nomlex: ../@input-data/NOMLEX-2001.exp ../py3env/
	@cat '../@input-data/NOMLEX-2001.exp' | ../py3env/bin/python3 input-statistics.py 'nomlex' English 'NOMLEX' 2001

# English NomBank
../@input-data/nombank.1.0.zip:
	@wget 'https://nlp.cs.nyu.edu/meyers/nombank/nombank.1.0.zip' -P ../@input-data/

nombank: ../@input-data/nombank.1.0.zip ../py3env/
	@unzip -q ../@input-data/nombank.1.0.zip
	@cat 'nombank.1.0/ADJADV.1.0' | ../py3env/bin/python3 input-statistics.py 'adjadv' English 'ADJADV' 1.0
	@cat 'nombank.1.0/NOMADV.1.0' | ../py3env/bin/python3 input-statistics.py 'nomadv' English 'NOMADV' 1.0
	@cat 'nombank.1.0/NOMLEX-plus.1.0' | ../py3env/bin/python3 input-statistics.py 'nomlexplus' English 'NOMLEXPlus' 1.0
	@rm -rf 'nombank.1.0'

# Portuguese NOMLEX
../@input-data/nomlex-pt.rdf.gz:
	@wget 'https://github.com/own-pt/nomlex-pt/raw/master/nomlex-pt.rdf.gz' -P ../@input-data/

nomlexpt: ../@input-data/nomlex-pt.rdf.gz ../py3env/
	@gunzip -qv '../@input-data/nomlex-pt.rdf.gz'
	@cat '../@input-data/nomlex-pt.rdf' | ../py3env/bin/python3 input-statistics.py 'nomlexpt' Portuguese 'NomLex-PT' 2016

# Etymological WordNet
../@input-data/etymwn-20130208.zip:
	wget 'https://cs.rutgers.edu/~gd343/downloads/etymwn-20130208.zip' -P ../@input-data/

etymwn: ../@input-data/etymwn-20130208.zip ../py3env/
	@unzip -q ../@input-data/etymwn-20130208.zip
	@mkdir -p etym-data/
	@for lang in 'lat' 'ita' 'eng' 'fra' 'spa' 'epo' 'deu' 'fin' 'nld' 'xcl' 'pol' 'hun' 'dan' 'glg' 'isl' 'gla' 'jpn' 'ces' 'vol' 'tur' 'hbs' 'gle' 'cat' 'swe' 'rus' 'kat' 'por' 'ron' 'cmn' 'glv' 'ast' 'nob' 'tel' 'ido' 'grc' 'vec' 'ang' 'lit' 'ell' 'lav' 'kor' 'bul'; do \
		cat etymwn.tsv | grep -e $$lang':.*'$$lang':' | grep -e 'rel:is_derived_from' | sed -e 's/'$$lang': //g' -e 's/\trel:is_derived_from//g' | awk -F "\t" '{ print $$2 "\t" $$1}' > etym-data/relations-$$lang.tsv ;\
		cat etymwn.tsv | grep -e $$lang':.*'$$lang':' | grep -e 'rel:has_derived_form' | sed -e 's/'$$lang': //g' -e 's/\trel:has_derived_form//g' | awk -F "\t" '{ print $$1 "\t" $$2}' >> etym-data/relations-$$lang.tsv ;\
		cat etym-data/relations-$$lang.tsv | grep -ve '[[:punct:]]' -ve ' ' -ve '[0-9]' | sort | uniq > etym-data/relations-$$lang-copy.tsv ;\
		mv etym-data/relations-$$lang-copy.tsv etym-data/relations-$$lang.tsv ;\
	done
	@cat etym-data/relations-lat.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Latin 'EtymWordNet-lat' 2013
	@cat etym-data/relations-ita.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Italian 'EtymWordNet-ita' 2013
	@cat etym-data/relations-eng.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' English 'EtymWordNet-eng' 2013
	@cat etym-data/relations-fra.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' French 'EtymWordNet-fra' 2013
	@cat etym-data/relations-spa.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Spanish 'EtymWordNet-spa' 2013
	@cat etym-data/relations-epo.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Esperanto 'EtymWordNet-epo' 2013
	@cat etym-data/relations-deu.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' German 'EtymWordNet-deu' 2013
	@cat etym-data/relations-fin.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Finnish 'EtymWordNet-fin' 2013
	@cat etym-data/relations-nld.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Dutch 'EtymWordNet-nld' 2013
	@cat etym-data/relations-xcl.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Armenian 'EtymWordNet-xcl' 2013
	@cat etym-data/relations-pol.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Polish 'EtymWordNet-pol' 2013
	@cat etym-data/relations-hun.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Hungarian 'EtymWordNet-hun' 2013
	@cat etym-data/relations-dan.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Danish 'EtymWordNet-dan' 2013
	@cat etym-data/relations-glg.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Galician 'EtymWordNet-glg' 2013
	@cat etym-data/relations-isl.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Icelandic 'EtymWordNet-isl' 2013
	@cat etym-data/relations-gla.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Gaelic 'EtymWordNet-gla' 2013
	@cat etym-data/relations-jpn.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Japanese 'EtymWordNet-jpn' 2013
	@cat etym-data/relations-ces.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Czech 'EtymWordNet-ces' 2013
	@cat etym-data/relations-vol.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Volapük 'EtymWordNet-vol' 2013
	@cat etym-data/relations-tur.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Turkish 'EtymWordNet-tur' 2013
	@cat etym-data/relations-hbs.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Serbo-Croatian 'EtymWordNet-hbs' 2013
	@cat etym-data/relations-gle.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Irish 'EtymWordNet-gle' 2013
	@cat etym-data/relations-cat.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Catalan 'EtymWordNet-cat' 2013
	@cat etym-data/relations-swe.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Swedish 'EtymWordNet-swe' 2013
	@cat etym-data/relations-rus.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Russian 'EtymWordNet-rus' 2013
	@cat etym-data/relations-kat.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Georgian 'EtymWordNet-kat' 2013
	@cat etym-data/relations-por.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Portuguese 'EtymWordNet-por' 2013
	@cat etym-data/relations-ron.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Romanian 'EtymWordNet-ron' 2013
	@cat etym-data/relations-cmn.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Mandarin 'EtymWordNet-cmn' 2013
	@cat etym-data/relations-glv.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Manx 'EtymWordNet-glv' 2013
	@cat etym-data/relations-ast.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Asturian 'EtymWordNet-ast' 2013
	@cat etym-data/relations-nob.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Norwegian 'EtymWordNet-nob' 2013
	@cat etym-data/relations-tel.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Telugu 'EtymWordNet-tel' 2013
	@cat etym-data/relations-ido.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Ido 'EtymWordNet-ido' 2013
	@cat etym-data/relations-grc.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' 'Greek (ancient)' 'EtymWordNet-grc' 2013
	@cat etym-data/relations-vec.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Venetian 'EtymWordNet-vec' 2013
	@cat etym-data/relations-ang.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' 'English (old)' 'EtymWordNet-ang' 2013
	@cat etym-data/relations-lit.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Lithuanian 'EtymWordNet-lit' 2013
	@cat etym-data/relations-ell.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' 'Greek (modern)' 'EtymWordNet-ell' 2013
	@cat etym-data/relations-lav.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Latvian 'EtymWordNet-lav' 2013
	@cat etym-data/relations-kor.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Korean 'EtymWordNet-kor' 2013
	@cat etym-data/relations-bul.tsv | ../py3env/bin/python3 input-statistics.py 'etymwn' Bulgarian 'EtymWordNet-bul' 2013
	@rm -rf etym-data/ etymwn.tsv readme.txt
