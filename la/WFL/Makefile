.PHONY: clean get-data-v05 UDer-0.5-la-WFL.tsv 01-harm-annotation
SHELL=/bin/bash

../../py3env/:
	cd ../../ && $(MAKE) py3env/

../../derinet2/:
	cd ../../ && $(MAKE) derinet2/

get-data-v05: ../../py3env/
	mkdir -p original-data/
	# 1. download data
	wget -O ../../@input-data/lemlat_db_01-08-2018.sql https://raw.githubusercontent.com/CIRCSE/LEMLAT3/master/lemlat_db_01-08-2018.sql
	# 2. preproces data
	grep -e 'INSERT INTO `lemmario`' ../../@input-data/lemlat_db_01-08-2018.sql | sed -e 's/^.*VALUES //g' | sed -e 's/;//g' | sed -e 's/),(/)\n(/g' | sed -e "s/^('*//g" | sed -e "s/'*)$$//g" | sed "s/'*,'*/\t/g" > original-data/lemlat3-lemmario.txt
	grep -e 'INSERT INTO `lemmas_wfr`' ../../@input-data/lemlat_db_01-08-2018.sql | sed -e 's/^.*VALUES //g' | sed -e 's/;//g' | sed -e 's/),(/)\n(/g' | sed -e "s/^('*//g" | sed "s/'*,'*/\t/g" | sed -e "s/'*)$$//g" > original-data/lemlat3-lemmaswfr.txt
	../../py3env/bin/python3 0.5/extract_relations.py original-data/lemlat3-lemmario.txt original-data/lemlat3-lemmaswfr.txt > 0.5/relations.tsv

get-data-v10: ../../py3env/
	mkdir -p original-data/
	# 1. download data
	# wget -O ../../@input-data/lemlat_db_26-07-2019.sql https://raw.githubusercontent.com/CIRCSE/LEMLAT3/master/lemlat_db_26-07-2019.sql
	# 2. preproces data
	grep -e 'INSERT INTO `lemmario`' ../../@input-data/lemlat_db_26-07-2019.sql | sed -e 's/^.*VALUES //g' | sed -e 's/;//g' | sed -e 's/),(/)\n(/g' | sed -e "s/^('*//g" | sed -e "s/'*)$$//g" | sed "s/'*,'*/\t/g" > original-data/lemlat3-lemmario.txt
	grep -e 'INSERT INTO `lemmas_wfr`' ../../@input-data/lemlat_db_26-07-2019.sql | sed -e 's/^.*VALUES //g' | sed -e 's/;//g' | sed -e 's/),(/)\n(/g' | sed -e "s/^('*//g" | sed "s/'*,'*/\t/g" | sed -e "s/'*)$$//g" > original-data/lemlat3-lemmaswfr.txt
	../../py3env/bin/python3 0.5/extract_relations.py original-data/lemlat3-lemmario.txt original-data/lemlat3-lemmaswfr.txt > 1.0/relations.tsv

get-data-v11: ../../py3env/
	mkdir -p original-data/
	# 1. download data
	wget -O ../../@input-data/wfl_derivational_db.sql https://raw.githubusercontent.com/CIRCSE/WFL/master/derivational_db.sql
	# 2. preproces data
	grep -e 'INSERT INTO `lemmario`' ../../@input-data/wfl_derivational_db.sql | sed -e 's/^.*VALUES //g' | sed -e 's/;//g' | sed -e 's/),(/)\n(/g' | sed -e "s/^('*//g" | sed -e "s/'*)$$//g" | sed "s/'*,'*/\t/g" > original-data/lemmario.txt
	grep -e 'INSERT INTO `wfr`' ../../@input-data/wfl_derivational_db.sql | sed -e 's/^.*VALUES //g' | sed -e "s/),/\n/g" | sed -e "s/^('*//g" | sed -e "s/NULL/'NULL'/g" | sed -e "s/','/\t/g" | sed -e "s/'//g" > original-data/wfr.txt
	grep -e 'INSERT INTO `wfr_rel`' ../../@input-data/wfl_derivational_db.sql | sed -e 's/^.*VALUES //g' | sed -e 's/;//g' | sed -e 's/),(/)\n(/g' | sed -e "s/^('*//g" | sed "s/'*,'*/\t/g" | sed -e "s/'*)$$//g" > original-data/wfr-rel.txt
	../../py3env/bin/python3 1.1/extract_relations.py --lemmario="original-data/lemmario.txt" --wfr="original-data/wfr.txt" --wfr_rel="original-data/wfr-rel.txt" --output="1.1/relations.tsv"


UDer-0.5-la-WFL.tsv: ../../derinet2/ ../../py3env/ get-data-v05
	# 1. get-data-v05
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 0.5/01-harm-annotated/annotation-data-1.json -o 0.5/01-harm-annotated/all-annotations.tsv -j2c
	# 3. harmonize data
	../../py3env/bin/python3 0.5/spanning_trees.py -r 0.5/relations.tsv -w 0.5/01-harm-annotated/all-annotations.tsv -o 0.5/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 0.5/harmonizewfl.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeWFL 0.5/harmonized.pickle \
		Save UDer-0.5-la-WFL.tsv

UDer-1.0-la-WFL.tsv: get-data-v10
	# 1. get-data-v10
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 0.5/01-harm-annotated/annotation-data-1.json -o 0.5/01-harm-annotated/all-annotations.tsv -j2c
	# 3. harmonize data
	../../py3env/bin/python3 0.5/spanning_trees.py -r 1.0/relations.tsv -w 0.5/01-harm-annotated/all-annotations.tsv -o 1.0/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.0/harmonizewfl.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeWFL 1.0/harmonized.pickle \
		Save UDer-1.0-la-WFL.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.0-la-WFL.tsv > UDer-1.0-la-WFL-v2.tsv
	mv UDer-1.0-la-WFL-v2.tsv UDer-1.0-la-WFL.tsv

UDer-1.1-la-WFL.tsv: get-data-v11
	# 1. get-data-v11
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.1/02-harm-annotated/annotation-data-1.json -o 1.1/02-harm-annotated/all-annotations.tsv -j2c
	# 3. harmonize data
	../../py3env/bin/python3 1.1/spanning_trees.py -r 1.1/relations.tsv -w 1.1/02-harm-annotated/all-annotations.tsv -o 1.1/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.1/harmonizewfl.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeWFL 1.1/harmonized.pickle \
		Save UDer-1.1-la-WFL.tsv
	../../py3env/bin/python3 1.1/edit-json-column.py UDer-1.1-la-WFL.tsv > UDer-1.1-la-WFL-v2.tsv
	mv UDer-1.1-la-WFL-v2.tsv UDer-1.1-la-WFL.tsv


01-harm-annotation: ../../py3env/ get-data-v05
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 0.5/relations.tsv -o 0.5/01-harm-annotated/annotation-data.json -j

02-harm-annotation: ../../py3env/ get-data-v11
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i <(grep -v 'Compounding' 1.1/relations.tsv) -o 1.1/02-harm-annotated/annotation-data.json -j


clean:
	rm -rf original-data/ 0.5/relations.tsv 0.5/01-harm-annotated/all-annotations.tsv 0.5/harmonized.pickle UDer-0.5-la-WFL.tsv
	rm -rf 1.0/relations.tsv 1.0/harmonized.pickle UDer-1.0-la-WFL.tsv
	rm -rf 1.1/relations.tsv 1.1/02-harm-annotated/all-annotations.tsv 1.1/harmonized.pickle UDer-1.1-la-WFL.tsv
