SHELL=/bin/bash

get-data-v05:
	mkdir original-data/
	# 1. download data
	wget -O ../../@input-data/derinet-2-0.tsv.gz https://github.com/vidraj/derinet/raw/master/data/releases/cs/derinet-2-0.tsv.gz
	gunzip -c ../../@input-data/derinet-2-0.tsv.gz > original-data/derinet-2-0.tsv

get-data-v11:
	mkdir original-data/
	# 1. download data
	wget -O ../../@input-data/derinet-2-1.tsv.gz https://github.com/vidraj/derinet/raw/master/data/releases/cs/derinet-2-1.tsv.gz
	gunzip -c ../../@input-data/derinet-2-1.tsv.gz > original-data/derinet-2-1.tsv


UDer-0.5-cs-DeriNet.tsv: get-data-v05
	# 1. get-data-v05
	# 2. harmonise
	../../py3env/bin/python3 0.5/harmonizepos.py original-data/derinet-2-0.tsv > UDer-0.5-cs-DeriNet.tsv

UDer-1.0-cs-DeriNet.tsv: UDer-0.5-cs-DeriNet.tsv
	cp UDer-0.5-cs-DeriNet.tsv UDer-1.0-cs-DeriNet.tsv

UDer-1.1-cs-DeriNet.tsv: get-data-v11
	# 1. get-data-v11
	cp original-data/derinet-2-1.tsv UDer-1.1-cs-DeriNet.tsv


clean:
	rm -rf original-data/ UDer-0.5-cs-DeriNet.tsv
	rm -rf UDer-1.0-cs-DeriNet.tsv UDer-1.1-cs-DeriNet.tsv
