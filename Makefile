.PHONY: UDer-collection UDer-resource UDer-statistics
SHELL=/bin/bash

version:=1.1
all: UDer-collection

# install virtual environment (base)
py3env/:
	virtualenv -p python3 py3env
	source py3env/bin/activate; \
	pip3 install networkx==2.4; \
	pip3 install xlrd==1.2.0; \
	pip3 install textdistance==4.1.5; \
	pip3 install pandas==1.0.4; \
	pip3 install numpy==1.18.1; \
	pip3 install scikit-learn==0.24.2  # older: 0.22.1; \
	pip3 install scipy==1.4.1; \
	pip3 install matplotlib==3.2.1; \

# clone DeriNet API
derinet2/:
	git clone https://github.com/vidraj/derinet.git
	cp -r derinet/tools/data-api/derinet2 .
	rm -rf derinet


# Build individual UDer resource; arguments: version, language, resource
UDer-resource: py3env/ derinet2/
	# check existence of version
	if grep -q ^UDer-$(version)-$(language)-$(resource).tsv: $(language)/$(resource)/Makefile ; then \
		# prepare data ;\
		cd $(language)/$(resource)/ && $(MAKE) UDer-$(version)-$(language)-$(resource).tsv ;\
		# include to collection ;\
		cd ../../ && mkdir -p UDer-$(version)/$(language)-$(resource)/ ;\
		cp $(language)/$(resource)/$(version)/LICENSE UDer-$(version)/$(language)-$(resource)/ ;\
		cp $(language)/$(resource)/$(version)/README.md UDer-$(version)/$(language)-$(resource)/ ;\
		cp $(language)/$(resource)/UDer-$(version)-$(language)-$(resource).tsv UDer-$(version)/$(language)-$(resource)/ ;\
		if grep -q UDer-$(version)-$(language)-$(resource)-rules.txt <(ls $(language)/$(resource)/); then \
			mv $(language)/$(resource)/UDer-$(version)-$(language)-$(resource)-rules.txt UDer-$(version)/$(language)-$(resource)/ ;\
		fi ;\
		# clean pipeline ;\
		cd $(language)/$(resource)/ && $(MAKE) clean ;\
		# calculate statistics and add them to README.md ;\
		py3env/bin/python3 @data-statistics/uder_statistics.py UDer-$(version)/$(language)-$(resource)/UDer-$(version)-$(language)-$(resource).tsv >> UDer-$(version)/$(language)-$(resource)/README.md ;\
		echo -e "===============================================================================\n</pre>" >> UDer-$(version)/$(language)-$(resource)/README.md ;\
	fi


# Build UDer collection
UDer-collection:
	$(MAKE) UDer-resource version=$(version) language=cs resource=DeriNet
	$(MAKE) UDer-resource version=$(version) language=en resource=WordNet
	$(MAKE) UDer-resource version=$(version) language=et resource=EstWordNet
	$(MAKE) UDer-resource version=$(version) language=es resource=DeriNetES
	$(MAKE) UDer-resource version=$(version) language=fa resource=DeriNetFA
	$(MAKE) UDer-resource version=$(version) language=pl resource=PolishWFN
	$(MAKE) UDer-resource version=$(version) language=pt resource=NomLexPT
	$(MAKE) UDer-resource version=$(version) language=la resource=WFL
	$(MAKE) UDer-resource version=$(version) language=fr resource=Demonette
	$(MAKE) UDer-resource version=$(version) language=de resource=DErivBase
	$(MAKE) UDer-resource version=$(version) language=fi resource=FinnWordNet
	$(MAKE) UDer-resource version=$(version) language=cs resource=EtymWordNetCS
	$(MAKE) UDer-resource version=$(version) language=ca resource=EtymWordNetCA
	$(MAKE) UDer-resource version=$(version) language=gd resource=EtymWordNetGD
	$(MAKE) UDer-resource version=$(version) language=pl resource=EtymWordNetPL
	$(MAKE) UDer-resource version=$(version) language=pt resource=EtymWordNetPT
	$(MAKE) UDer-resource version=$(version) language=ru resource=EtymWordNetRU
	$(MAKE) UDer-resource version=$(version) language=sh resource=EtymWordNetSH
	$(MAKE) UDer-resource version=$(version) language=sv resource=EtymWordNetSV
	$(MAKE) UDer-resource version=$(version) language=tr resource=EtymWordNetTR
	$(MAKE) UDer-resource version=$(version) language=ru resource=DerivBaseRU
	$(MAKE) UDer-resource version=$(version) language=en resource=CatVar
	$(MAKE) UDer-resource version=$(version) language=en resource=ECelex
	$(MAKE) UDer-resource version=$(version) language=du resource=DCelex
	$(MAKE) UDer-resource version=$(version) language=de resource=GCelex
	$(MAKE) UDer-resource version=$(version) language=it resource=DerIvaTario
	$(MAKE) UDer-resource version=$(version) language=hr resource=DerivBaseHR
	# pre-prepared: (need to annotate and harmonize)
	# $(MAKE) UDer-resource version=$(version) language=sl resource=Sloleks
	# $(MAKE) UDer-resource version=$(version) language=it resource=EtymWordNetIT
	# $(MAKE) UDer-resource version=$(version) language=la resource=EtymWordNetLA
	# $(MAKE) UDer-resource version=$(version) language=en resource=EtymWordNetEN
	# $(MAKE) UDer-resource version=$(version) language=fr resource=EtymWordNetFR
	# $(MAKE) UDer-resource version=$(version) language=es resource=EtymWordNetES
	# $(MAKE) UDer-resource version=$(version) language=eo resource=EtymWordNetEO
	# $(MAKE) UDer-resource version=$(version) language=de resource=EtymWordNetDE
	# $(MAKE) UDer-resource version=$(version) language=fi resource=EtymWordNetFI
	# $(MAKE) UDer-resource version=$(version) language=nl resource=EtymWordNetNL
	# $(MAKE) UDer-resource version=$(version) language=hu resource=EtymWordNetHU
	# $(MAKE) UDer-resource version=$(version) language=da resource=EtymWordNetDA
	# $(MAKE) UDer-resource version=$(version) language=gl resource=EtymWordNetGL
	# $(MAKE) UDer-resource version=$(version) language=is resource=EtymWordNetIS
	# $(MAKE) UDer-resource version=$(version) language=ga resource=EtymWordNetGA
	find UDer-$(version)/ -type f -name '*.tsv' | while read file; do gzip $$file; done
	cp CHANGELOG.md UDer-$(version)/
	cp README.md UDer-$(version)/
