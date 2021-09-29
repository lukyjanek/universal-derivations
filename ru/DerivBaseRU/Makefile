SHELL=/bin/bash

../../py3env/:
	cd ../../ && $(MAKE) py3env

../../derinet2/:
	cd ../../ && $(MAKE) derinet2


get-data-v10: ../../py3env/
	mkdir -p original-data/
	# 1. download data
	wget -O ../../@input-data/derivbaseRU-connections.zip https://github.com/s231644/DerivBaseRu/raw/master/data/wiktionary/v001.00-connections.zip
	wget -O ../../@input-data/derivbaseRU-noun.txt https://github.com/s231644/DerivBaseRu/raw/master/data/wiktionary/noun.txt
	wget -O ../../@input-data/derivbaseRU-verb.txt https://raw.githubusercontent.com/s231644/DerivBaseRu/master/data/wiktionary/verb.txt
	wget -O ../../@input-data/derivbaseRU-adj.txt https://github.com/s231644/DerivBaseRu/raw/master/data/wiktionary/adj.txt
	wget -O ../../@input-data/derivbaseRU-adv.txt https://raw.githubusercontent.com/s231644/DerivBaseRu/master/data/wiktionary/adv.txt
	# 2. preproces data
	cat ../../@input-data/derivbaseRU-noun.txt | sed -e 's/$$/_N/g' > original-data/noun-tagged.txt
	cat ../../@input-data/derivbaseRU-adj.txt | sed -e 's/$$/_A/g' > original-data/adj-tagged.txt
	cat ../../@input-data/derivbaseRU-verb.txt | sed -e 's/$$/_V/g' > original-data/verb-tagged.txt
	cat ../../@input-data/derivbaseRU-adv.txt | sed -e 's/$$/_D/g' > original-data/adv-tagged.txt
	unzip -d original-data/ ../../@input-data/derivbaseRU-connections.zip
	for file in $$(ls original-data/connections_*.csv) ; do \
		sed '1d' $$file > $$(echo $$file | sed 's/_/-/g' | sed 's/\.csv/-data\.csv/g') ;\
	done
	../../py3env/bin/python3 1.0/extract_relations.py "$$(ls original-data/*-tagged.txt)" "$$(ls original-data/connections-*-data.csv)" 1.0/relations.tsv 1.0/singletons.tsv


UDer-1.0-ru-DerivBaseRU.tsv: ../../derinet2/ ../../py3env/ get-data-v10
	# 1. get-data-v10
	../../py3env/bin/python3 1.0/extract_rules.py 1.0/relations.tsv UDer-1.0-ru-DerivBaseRU-rules.txt
	# 2. process annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/01-harm-annotated/first-annotation-data.json -o 1.0/01-harm-annotated/all-annotations.tsv -j2c
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/02-harm-annotated/second-annotation-data.json -o 1.0/02-harm-annotated/all-annotations.tsv -j2c
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.0/prep-to-predict.tsv -c
	cat 1.0/prep-to-predict.tsv | grep ^. | cut -f 2,3 > 1.0/to-predict.tsv
	# 3. machine learning
	# ../../py3env/bin/python3 -B 1.0/predict_scores.py -rel 1.0/relations.tsv -a <(cat 1.0/01-harm-annotated/all-annotations.tsv 1.0/02-harm-annotated/all-annotations.tsv) -fsmi mi.tsv -fsce ce.tsv -ev model-performances.txt -dev
	# ../../py3env/bin/python3 -B ../../@shared-scripts/baseline.py -a <(cat 1.0/01-harm-annotated/all-annotations.tsv 1.0/02-harm-annotated/all-annotations.tsv) -fs baseline-fmeasure.tsv -w 1.0/predicted-baseline.tsv -p 1.0/to-predict.tsv -n 'DerivBase.Ru'
	../../py3env/bin/python3 -B 1.0/predict_scores.py -rel 1.0/relations.tsv -a <(cat 1.0/01-harm-annotated/all-annotations.tsv 1.0/02-harm-annotated/all-annotations.tsv) -p 1.0/to-predict.tsv -m LOGR2 -w 1.0/predicted.tsv
	# 4. harmonise
	# for w in -1000000 0.0 0.1 0.2 0.3 0.4 0.5 1.0 0.7 0.8 0.9 1.0 1000000 ; do \
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a <(cat 1.0/01-harm-annotated/all-annotations.tsv 1.0/02-harm-annotated/all-annotations.tsv) | sed 's/$$/\t /g' | cut -f 2,3,4) -w 1.0/predicted.tsv -v $$w -ev uas-validation-eval.tsv ;\
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a <(cat 1.0/01-harm-annotated/all-annotations.tsv 1.0/02-harm-annotated/all-annotations.tsv) | sed 's/$$/\t /g' | cut -f 2,3,4) -w 1.0/predicted.tsv -v $$w -ev uas-holdout-eval.tsv ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a <(cat 1.0/01-harm-annotated/all-annotations.tsv 1.0/02-harm-annotated/all-annotations.tsv)) -p uas-validation-eval.tsv -o UAS-validation.txt -v $$w ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a <(cat 1.0/01-harm-annotated/all-annotations.tsv 1.0/02-harm-annotated/all-annotations.tsv)) -p uas-holdout-eval.tsv -o UAS-holdout.txt -v $$w ;\
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a <(cat 1.0/01-harm-annotated/all-annotations.tsv 1.0/02-harm-annotated/all-annotations.tsv) | sed 's/$$/\t /g' | cut -f 2,3,4) -w 1.0/predicted-baseline.tsv -v $$w -ev uas-validation-baseline-eval.tsv ;\
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a <(cat 1.0/01-harm-annotated/all-annotations.tsv 1.0/02-harm-annotated/all-annotations.tsv) | sed 's/$$/\t /g' | cut -f 2,3,4) -w 1.0/predicted-baseline.tsv -v $$w -ev uas-holdout-baseline-eval.tsv ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.0/02-harm-annotated/all-annotations.tsv) -p uas-validation-baseline-eval.tsv -o UAS-validation-baseline.txt -v $$w ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.0/02-harm-annotated/all-annotations.tsv) -p uas-holdout-baseline-eval.tsv -o UAS-holdout-baseline.txt -v $$w ;\
	# done
	../../py3env/bin/python3 1.0/spanning_trees.py -s 1.0/singletons.tsv -r 1.0/relations.tsv -w 1.0/predicted.tsv -v 0.0 -o 1.0/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.0/harmonizederivbaseru.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeDerivBaseRu 1.0/harmonized.pickle \
		Save UDer-1.0-ru-DerivBaseRU.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.0-ru-DerivBaseRU.tsv > UDer-1.0-ru-DerivBaseRU-v2.tsv
	mv UDer-1.0-ru-DerivBaseRU-v2.tsv UDer-1.0-ru-DerivBaseRU.tsv

UDer-1.1-ru-DerivBaseRU.tsv: ../../derinet2/ ../../py3env/ get-data-v10
	# 1. get-data-v10
	../../py3env/bin/python3 1.0/extract_rules.py 1.0/relations.tsv UDer-1.1-ru-DerivBaseRU-rules.txt
	# 2. process annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/01-harm-annotated/first-annotation-data.json -o 1.0/01-harm-annotated/all-annotations.tsv -j2c
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/02-harm-annotated/second-annotation-data.json -o 1.0/02-harm-annotated/all-annotations.tsv -j2c
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.1/prep-to-predict.tsv -c
	cat 1.1/prep-to-predict.tsv | grep ^. | cut -f 2,3 > 1.1/to-predict.tsv
	# 3. machine learning
	../../py3env/bin/python3 -B 1.0/predict_scores.py -rel 1.0/relations.tsv -a <(cat 1.0/01-harm-annotated/all-annotations.tsv 1.0/02-harm-annotated/all-annotations.tsv) -p 1.1/to-predict.tsv -m LOGR2 -w 1.1/predicted.tsv
	# 4. harmonise
	../../py3env/bin/python3 1.1/spanning_trees.py -s 1.0/singletons.tsv -r 1.0/relations.tsv -w 1.1/predicted.tsv -v 0.0 -o 1.1/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.1/harmonizederivbaseru.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeDerivBaseRu 1.1/harmonized.pickle \
		Save UDer-1.1-ru-DerivBaseRU.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.1-ru-DerivBaseRU.tsv > UDer-1.1-ru-DerivBaseRU-v2.tsv
	mv UDer-1.1-ru-DerivBaseRU-v2.tsv UDer-1.1-ru-DerivBaseRU.tsv


01-harm-annotation: ../../py3env/ get-data-v10
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.0/01-harm-annotated/annotation-data.json -j

02-harm-annotation: ../../py3env/ get-data-v10
	mkdir -p russian-corpora/
	wget -P russian-corpora/ https://raw.githubusercontent.com/UniversalDependencies/UD_Russian-PUD/master/ru_pud-ud-test.conllu
	wget -P russian-corpora/ https://raw.githubusercontent.com/UniversalDependencies/UD_Russian-GSD/master/ru_gsd-ud-dev.conllu
	wget -P russian-corpora/ https://raw.githubusercontent.com/UniversalDependencies/UD_Russian-GSD/master/ru_gsd-ud-test.conllu
	wget -P russian-corpora/ https://raw.githubusercontent.com/UniversalDependencies/UD_Russian-GSD/master/ru_gsd-ud-train.conllu
	wget -P russian-corpora/ https://raw.githubusercontent.com/UniversalDependencies/UD_Russian-Taiga/master/ru_taiga-ud-dev.conllu
	wget -P russian-corpora/ https://raw.githubusercontent.com/UniversalDependencies/UD_Russian-Taiga/master/ru_taiga-ud-test.conllu
	wget -P russian-corpora/ https://raw.githubusercontent.com/UniversalDependencies/UD_Russian-Taiga/master/ru_taiga-ud-train.conllu
	wget -P russian-corpora/ https://raw.githubusercontent.com/UniversalDependencies/UD_Russian-SynTagRus/master/ru_syntagrus-ud-dev.conllu
	wget -P russian-corpora/ https://raw.githubusercontent.com/UniversalDependencies/UD_Russian-SynTagRus/master/ru_syntagrus-ud-test.conllu
	wget -P russian-corpora/ https://raw.githubusercontent.com/UniversalDependencies/UD_Russian-SynTagRus/master/ru_syntagrus-ud-train.conllu
	for file in $$(ls russian-corpora/*.conllu) ; do \
		cat $$file | grep ^[0-9] | cut -f 3 >> russian-corpora/lexemes.txt ;\
	done
	cat russian-corpora/lexemes.txt | sort | uniq -c > russian-corpora/lexemes-freq.txt
	../../py3env/bin/python3 1.0/second_annotation.py 1.0/relations.tsv russian-corpora/lexemes-freq.txt 1.0/01-harm-annotated/annotation-data-1.json 1.0/02-harm-annotated/annotation-data.json


clean:
	rm -rf original-data/ russian-corpora/ 1.0/relations.tsv 1.0/singletons.tsv 1.0/prep-to-predict.tsv 1.0/to-predict* 1.0/predicted.tsv 1.0/01-harm-annotated/all-annotations.tsv 1.0/02-harm-annotated/all-annotations.tsv 1.0/harmonized.pickle UDer-1.0-ru-DerivBaseRU-v2.tsv UDer-1.0-ru-DerivBaseRU.tsv UDer-1.0-ru-DerivBaseRU-rules.txt
	rm -rf 1.1/prep-to-predict.tsv 1.1/to-predict* 1.1/predicted.tsv 1.1/harmonized.pickle UDer-1.1-ru-DerivBaseRU.tsv UDer-1.1-ru-DerivBaseRU-v2.tsv UDer-1.1-ru-DerivBaseRU-rules.txt
