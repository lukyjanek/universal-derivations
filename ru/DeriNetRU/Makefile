.PHONY: clean get-data-v05 UDer-1.1-ru-DeriNetRU.tsv
SHELL=/bin/bash

../../py3env/:
	cd ../../ && $(MAKE) py3env/

../../derinet2/:
	cd ../../ && $(MAKE) derinet2/

../../@input-data/DeriNetRU-0.5.tsv.gz:
	@echo "$$(tput setaf 1)You need DeriNetRU-0.5.tsv.gz. Contact the authors."

get-data-v05: ../../py3env/ ../../@input-data/DeriNetRU-0.5.tsv.gz
	cp ../../@input-data/DeriNetRU-0.5.tsv.gz .


UDer-1.1-ru-DeriNetRU.tsv: ../../derinet2/ ../../py3env/ get-data-v05
	# 1. get-data-v05
	# 2. harmonise
	zcat DeriNetRU-0.5.tsv.gz > UDer-1.1-ru-DeriNetRU.tsv


clean:
	rm -rf DeriNetRU-0.5.tsv.gz UDer-1.1-ru-DeriNetRU.tsv
