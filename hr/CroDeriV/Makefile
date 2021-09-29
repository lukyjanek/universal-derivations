SHELL=/bin/bash

../../@input-data/croderiv_uder.zip:
	@echo "$$(tput setaf 1)You need croderiv_uder.zip. Contact the authors."

get-data-v11: ../../@input-data/croderiv_uder.zip
	unzip ../../@input-data/croderiv_uder.zip


UDer-1.1-hr-CroDeriV.tsv: get-data-v11
	# 1. get-data-v11
	# 2. harmonise
	cp croderiv_uder.uder UDer-1.1-hr-CroDeriV.tsv


clean:
	rm -rf croderiv_uder.uder UDer-1.1-hr-CroDeriV.tsv
