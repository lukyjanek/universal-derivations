.PHONY: clean get-data-v05 UDer-0.5-cs-DeriNet.tsv 01-harm-annotation
SHELL=/bin/bash

../../py3env/:
	cd ../../ && $(MAKE) py3env/

../../derinet2/:
	cd ../../ && $(MAKE) derinet2/

get-data-v05: ../../py3env/
	mkdir original-data/
	# 1. download data
	wget -O ../../@input-data/derinet-2-0.tsv.gz https://github.com/vidraj/derinet/raw/master/data/releases/cs/derinet-2-0.tsv.gz
	gunzip -c ../../@input-data/derinet-2-0.tsv.gz > original-data/derinet-2-0.tsv


UDer-0.5-cs-DeriNet.tsv: ../../derinet2/ ../../py3env/ get-data-v05
	# 1. get-data-v05
	# 2. harmonise
	../../py3env/bin/python3 0.5/harmonizepos.py original-data/derinet-2-0.tsv > UDer-0.5-cs-DeriNet.tsv

UDer-1.0-cs-DeriNet.tsv: UDer-0.5-cs-DeriNet.tsv
	cp UDer-0.5-cs-DeriNet.tsv UDer-1.0-cs-DeriNet.tsv

UDer-1.1-cs-DeriNet.tsv: UDer-1.0-cs-DeriNet.tsv
	cp UDer-1.0-cs-DeriNet.tsv UDer-1.1-cs-DeriNet.tsv


clean:
	rm -rf original-data/ UDer-0.5-cs-DeriNet.tsv
	rm -rf UDer-1.0-cs-DeriNet.tsv UDer-1.1-cs-DeriNet.tsv
