.PHONY: clean get-data-v05 UDer-0.5-en-WordNet.tsv 01-harm-annotation
SHELL=/bin/bash

../../py3env/:
	cd ../../ && $(MAKE) py3env/

../../derinet2/:
	cd ../../ && $(MAKE) derinet2/

get-data-v05: ../../py3env/
	mkdir original-data/
	# 1. download data
	wget -O ../../@input-data/morphosemantic-database.xls http://wordnetcode.princeton.edu/standoff-files/morphosemantic-links.xls
	# 2. preproces data
	../../py3env/bin/python3 0.5/convert_xlsx2csv.py -i ../../@input-data/morphosemantic-database.xls -o original-data/morphosemantic-links.csv
	../../py3env/bin/python3 0.5/extract_relations.py original-data/morphosemantic-links.csv > 0.5/relations.tsv


UDer-0.5-en-WordNet.tsv: ../../derinet2/ ../../py3env/ get-data-v05
	# 1. get-data-v05
	# 2. proces annotations
	../../py3env/bin/python3 ../../annot_data.py -i 0.5/01-harm-annotated/annotation-data-1.json -o 0.5/01-harm-annotated/all-annotations.tsv -j2c
	# 3. harmonise
	../../py3env/bin/python3 -B 0.5/spanning_trees.py -r 0.5/relations.tsv -w 0.5/01-harm-annotated/all-annotations.tsv -o 0.5/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 0.5/harmonizewordnet.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeWordNet 0.5/harmonized.pickle \
		Save UDer-0.5-en-WordNet.tsv

UDer-1.0-en-WordNet.tsv: UDer-0.5-en-WordNet.tsv
	cp UDer-0.5-en-WordNet.tsv UDer-1.0-en-WordNet.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.0-en-WordNet.tsv > UDer-1.0-en-WordNet-v2.tsv
	mv UDer-1.0-en-WordNet-v2.tsv UDer-1.0-en-WordNet.tsv

UDer-1.1-en-WordNet.tsv: UDer-1.0-en-WordNet.tsv
	cp UDer-1.0-en-WordNet.tsv UDer-1.1-en-WordNet.tsv


01-harm-annotation: ../../py3env/ get-data-v05
	../../py3env/bin/python3 ../../annot_data.py -i 0.5/relations.tsv -o 0.5/01-harm-annotated/annotation-data.json -j


clean:
	rm -rf original-data/ 0.5/relations.tsv 0.5/01-harm-annotated/all-annotations.tsv 0.5/harmonized.pickle UDer-0.5-en-WordNet.tsv
	rm -rf UDer-1.0-en-WordNet.tsv UDer-1.1-en-WordNet.tsv
