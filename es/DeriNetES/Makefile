.PHONY: clean get-data-v05 UDer-0.5-es-DeriNetES.tsv
SHELL=/bin/bash

../../py3env/:
	cd ../../ && $(MAKE) py3env/

../../derinet2/:
	cd ../../ && $(MAKE) derinet2/

get-data-v05: ../../py3env/
	# 1. download data
	wget -O ../../@input-data/derinet-es-2019-05-10.tsv https://ufal.mff.cuni.cz/~vidra/derinet/derinet-es-2019-05-10.tsv

get-data-v11: ../../py3env/
	# 1. download data
	wget -O ../../@input-data/derinet-es-2020-06-10.tsv https://ufal.mff.cuni.cz/~vidra/derinet/derinet-es-2020-06-10.tsv


UDer-0.5-es-DeriNetES.tsv: ../../derinet2/ ../../py3env/ get-data-v05
	# 1. get-data-v05
	# 2. harmonise
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		Load -f DERINET_V1 ../../@input-data/derinet-es-2019-05-10.tsv \
		Save UDer-0.5-es-DeriNetES.tsv

UDer-1.0-es-DeriNetES.tsv: UDer-0.5-es-DeriNetES.tsv
	cp UDer-0.5-es-DeriNetES.tsv UDer-1.0-es-DeriNetES.tsv

UDer-1.1-es-DeriNetES.tsv: ../../derinet2/ ../../py3env/ get-data-v11
	# 1. get-data-v11
	# 2. harmonise
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		Load -f DERINET_V2 ../../@input-data/derinet-es-2020-06-10.tsv \
		Save UDer-1.1-es-DeriNetES.tsv


clean:
	rm -rf UDer-0.5-es-DeriNetES.tsv
	rm -rf UDer-1.0-es-DeriNetES.tsv
	rm -rf UDer-1.1-es-DeriNetES.tsv
