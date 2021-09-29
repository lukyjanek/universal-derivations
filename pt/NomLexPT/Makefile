SHELL=/bin/bash

../../py3env/:
	cd ../../ && $(MAKE) py3env

../../derinet2/:
	cd ../../ && $(MAKE) derinet2

get-data-v05: ../../py3env/
	mkdir original-data/
	# 1. donwload data
	wget -O ../../@input-data/nomlex-pt.rdf.gz https://github.com/own-pt/nomlex-pt/raw/master/nomlex-pt.rdf.gz
	gunzip -c ../../@input-data/nomlex-pt.rdf.gz > original-data/nomlex-pt.rdf
	# 2. preproces data
	../../py3env/bin/python3 0.5/extract_relations.py original-data/nomlex-pt.rdf > 0.5/relations.tsv


UDer-0.5-pt-NomLexPT.tsv: ../../derinet2/ ../../py3env/ get-data-v05
	# 1. get-data-v05
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 0.5/01-harm-annotated/annotation-data-1.json -o 0.5/01-harm-annotated/all-annotations.tsv -j2c
	# 3. harmonise
	../../py3env/bin/python3 0.5/spanning_trees.py -r 0.5/relations.tsv -w 0.5/01-harm-annotated/all-annotations.tsv -o 0.5/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 0.5/harmonizenomlexpt.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeNomlexPT 0.5/harmonized.pickle \
		Save UDer-0.5-pt-NomLexPT.tsv

UDer-1.0-pt-NomLexPT.tsv: UDer-0.5-pt-NomLexPT.tsv
	cp UDer-0.5-pt-NomLexPT.tsv UDer-1.0-pt-NomLexPT.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.0-pt-NomLexPT.tsv > UDer-1.0-pt-NomLexPT-v2.tsv
	mv UDer-1.0-pt-NomLexPT-v2.tsv UDer-1.0-pt-NomLexPT.tsv

UDer-1.1-pt-NomLexPT.tsv: UDer-1.0-pt-NomLexPT.tsv
	cp UDer-1.0-pt-NomLexPT.tsv UDer-1.1-pt-NomLexPT.tsv


01-harm-annotation: ../../py3env/ get-data-v05
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 0.5/relations.tsv -o 0.5/01-harm-annotated/annotation-data.json -j


clean:
	rm -rf original-data/ 0.5/relations.tsv 0.5/01-harm-annotated/all-annotations.tsv 0.5/harmonized.pickle UDer-0.5-pt-NomLexPT.tsv
	rm -rf UDer-1.0-pt-NomLexPT.tsv UDer-1.1-pt-NomLexPT.tsv
