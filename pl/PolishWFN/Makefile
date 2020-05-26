.PHONY: clean get-data-v05 UDer-0.5-pl-PolishWFN.tsv
SHELL=/bin/bash

../../py3env/:
	cd ../../ && $(MAKE) py3env/

../../derinet2/:
	cd ../../ && $(MAKE) derinet2/

get-data-v05: ../../py3env/
	mkdir original-data/
	# 1. donwload data
	wget -O ../../@input-data/polish-wfn-0.5.zip https://ufal.mff.cuni.cz/~vidra/derinet/polish-wfn-0.5.zip
	unzip ../../@input-data/polish-wfn-0.5.zip -d original-data/


UDer-0.5-pl-PolishWFN.tsv: ../../derinet2/ ../../py3env/ get-data-v05
	# 1. get-data-v05
	# 2. harmonise
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		Load -f DERINET_V1 original-data/polish-wfn-0.5/polish-wfn.tsv \
		Save UDer-0.5-pl-PolishWFN.tsv

UDer-1.0-pl-PolishWFN.tsv: UDer-0.5-pl-PolishWFN.tsv
	cp UDer-0.5-pl-PolishWFN.tsv UDer-1.0-pl-PolishWFN.tsv


clean:
	rm -rf original-data/ UDer-0.5-pl-PolishWFN.tsv
	rm -rf UDer-1.0-pl-PolishWFN.tsv
