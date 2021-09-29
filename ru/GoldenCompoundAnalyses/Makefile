SHELL=/bin/bash

../../py3env/:
	cd ../../ && $(MAKE) py3env

../../derinet2/:
	cd ../../ && $(MAKE) derinet2

../../@input-data/ru-gold-compound-analysis-val.csv:
	wget -O ../../@input-data/ru-gold-compound-analysis-test.csv https://raw.githubusercontent.com/s231644/rucompoundsplitter/main/data/gold_analyses/test.csv
	wget -O ../../@input-data/ru-gold-compound-analysis-train.csv https://raw.githubusercontent.com/s231644/rucompoundsplitter/main/data/gold_analyses/train.csv
	wget -O ../../@input-data/ru-gold-compound-analysis-val.csv https://raw.githubusercontent.com/s231644/rucompoundsplitter/main/data/gold_analyses/val.csv

get-data-v11: ../../py3env/ ../../@input-data/ru-gold-compound-analysis-val.csv
	../../py3env/bin/python3 1.1/extract_original_data.py \
		--input_train='../../@input-data/ru-gold-compound-analysis-train.csv' \
		--input_test='../../@input-data/ru-gold-compound-analysis-test.csv' \
		--input_val='../../@input-data/ru-gold-compound-analysis-val.csv' \
		--output_relations='1.1/relations.tsv'


UDer-1.1-ru-GoldenCompoundAnalyses.tsv: ../../derinet2/ ../../py3env/ get-data-v11
	# 1. get-data-v11
	# 2. harmonise
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.1/harmonizegoldencompoundanalyses.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeGoldenCompoundAnalyses 1.1/relations.tsv \
		Save UDer-1.1-ru-GoldenCompoundAnalyses.tsv


clean:
	rm -rf UDer-1.1-ru-GoldenCompoundAnalyses.tsv 1.1/relations.tsv UDer-1.1-ru-GoldenCompoundAnalyses-rules.txt
