SHELL=/bin/bash

../../@input-data/DeriNetRU-0.5.tsv.gz:
	@echo "$$(tput setaf 1)You need DeriNetRU-0.5.tsv.gz. Contact the authors."

get-data-v05: ../../@input-data/DeriNetRU-0.5.tsv.gz
	cp ../../@input-data/DeriNetRU-0.5.tsv.gz .


UDer-1.1-ru-DeriNetRU.tsv: get-data-v05
	# 1. get-data-v05
	# 2. harmonise
	zcat DeriNetRU-0.5.tsv.gz > UDer-1.1-ru-DeriNetRU.tsv


clean:
	rm -rf DeriNetRU-0.5.tsv.gz UDer-1.1-ru-DeriNetRU.tsv
