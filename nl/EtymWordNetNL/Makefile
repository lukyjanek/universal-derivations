.PHONY: clean get-data-vxx UDer-x.x-nl-EtymWordNetNL.tsv 01-harm-annotation
SHELL=/bin/bash

../../py3env/:
	cd ../../ && $(MAKE) py3env/

../../derinet2/:
	cd ../../ && $(MAKE) derinet2/

../../@input-data/etymwn-20130208.zip:
	wget -O ../../@input-data/etymwn-20130208.zip https://cs.rutgers.edu/~gd343/downloads/etymwn-20130208.zip

get-data-vxx: ../../py3env/ ../../@input-data/etymwn-20130208.zip
	mkdir -p original-data/
	# 1. download data
	unzip ../../@input-data/etymwn-20130208.zip -d original-data/
	# 2. preproces data
	cat original-data/etymwn.tsv | grep -e 'nld:.*nld:' | grep -e 'rel:is_derived_from' | sed -e 's/nld: //g' -e 's/\trel:is_derived_from//g' | awk -F "\t" '{ print $$2 "\t" $$1}' > x.x/relations.tsv
	cat original-data/etymwn.tsv | grep -e 'nld:.*nld:' | grep -e 'rel:has_derived_form' | sed -e 's/nld: //g' -e 's/\trel:has_derived_form//g' | awk -F "\t" '{ print $$1 "\t" $$2}' >> x.x/relations.tsv
	cat x.x/relations.tsv | grep -ve '[[:punct:]]' -ve ' ' -ve '[0-9]' | sort | uniq > x.x/relations-copy.tsv
	mv x.x/relations-copy.tsv x.x/relations.tsv


UDer-x.x-nl-EtymWordNetNL.tsv: ../../derinet2/ ../../py3env/ get-data-vxx
	# 1. get-data-vxx
	# 2. proces annotations
	../../py3env/bin/python3 ../../annot_data.py -i x.x/relations.tsv -o x.x/prep-to-predict.tsv -c
	cat x.x/prep-to-predict.tsv | grep ^. | cut -f 2,3 > x.x/to-predict.tsv
	../../py3env/bin/python3 ../../annot_data.py -i x.x/01-harm-annotated/annotation-data.json.1 -o x.x/01-harm-annotated/all-annotations.tsv -j2c
	# 3. machine learning

	# # 3. harmonise
	# ../../py3env/bin/python3 harmonize.py -r input-data/relations.tsv -w input-data/01-harm-annotated/all-annotations.tsv -o input-data/harmonized.pickle
	# mkdir -p ../../derinet2/derinet/modules/uder
	# cp modules/harmonizewfl.py ../../derinet2/derinet/modules/uder/
	# ../../py3env/bin/python3 ../../derinet2/process_scenario.py \
	# 	uder.HarmonizeWFL input-data/harmonized.pickle \
	# 	Save UDer-0.4-la-WFL.tsv


01-harm-annotation: ../../py3env/ get-data-vxx
	../../py3env/bin/python3 ../../annot_data.py -i x.x/relations.tsv -o x.x/01-harm-annotated/annotation-data.json -j


clean:
	rm -rf original-data/ x.x/relations.tsv x.x/01-harm-annotated/all-annotations.tsv x.x/harmonized.pickle UDer-x.x-nl-EtymWordNetNL.tsv