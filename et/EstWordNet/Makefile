SHELL=/bin/bash

../../py3env/:
	cd ../../ && $(MAKE) py3env

../../derinet2/:
	cd ../../ && $(MAKE) derinet2

get-data-v05: ../../py3env/
	# 1. download data
	wget -O ../../@input-data/estwn-et-2.1.0.wip.xml https://gitlab.keeleressursid.ee/avalik/data/raw/master/estwn/estwn-et-2.1.0.wip.xml
	../../py3env/bin/python3 0.5/extract_relations.py ../../@input-data/estwn-et-2.1.0.wip.xml > 0.5/relations.tsv


UDer-0.5-et-EstWordNet.tsv: ../../derinet2/ ../../py3env/ get-data-v05
	# 1. get-data-v05
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 0.5/01-harm-annotated/annotation-data-1.json -o 0.5/01-harm-annotated/all-annotations.tsv -j2c
	# 3. harmonise
	../../py3env/bin/python3 0.5/spanning_trees.py -r 0.5/relations.tsv -w 0.5/01-harm-annotated/all-annotations.tsv -o 0.5/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 0.5/harmonizeestwordnet.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeEstWordNet 0.5/harmonized.pickle \
		Save UDer-0.5-et-EstWordNet.tsv

UDer-1.0-et-EstWordNet.tsv: UDer-0.5-et-EstWordNet.tsv
	cp UDer-0.5-et-EstWordNet.tsv UDer-1.0-et-EstWordNet.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.0-et-EstWordNet.tsv > UDer-1.0-et-EstWordNet-v2.tsv
	mv UDer-1.0-et-EstWordNet-v2.tsv UDer-1.0-et-EstWordNet.tsv

UDer-1.1-et-EstWordNet.tsv: UDer-1.0-et-EstWordNet.tsv
	cp UDer-1.0-et-EstWordNet.tsv UDer-1.1-et-EstWordNet.tsv


01-harm-annotation: ../../py3env/ get-data-v05
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 0.5/relations.tsv -o 0.5/01-harm-annotated/annotation-data.json -j


clean:
	rm -rf 0.5/relations.tsv 0.5/01-harm-annotated/all-annotations.tsv 0.5/harmonized.pickle UDer-0.5-et-EstWordNet.tsv
	rm -rf UDer-1.0-et-EstWordNet.tsv UDer-1.1-et-EstWordNet.tsv
