SHELL=/bin/bash

../../py3env/:
	cd ../../ && $(MAKE) py3env/

../../derinet2/:
	cd ../../ && $(MAKE) derinet2/

get-data-v11: ../../py3env/
	mkdir -p original-data/
	# 1. download data
	wget -O ../../@input-data/Sloleks2.0.LMF.zip 'https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1230/Sloleks2.0.LMF.zip?sequence=3&isAllowed=y'
	unzip -q ../../@input-data/Sloleks2.0.LMF.zip  -d original-data/
	# 2. preproces data
	../../py3env/bin/python3 1.1/extract_relations.py original-data/Sloleks2.0.LMF/sloleks_clarin_2.0.xml > 1.1/relations.tsv


UDer-1.1-sl-Sloleks.tsv: ../../derinet2/ ../../py3env/ get-data-v11
	# 1. get-data-v11
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.1/relations.tsv -o 1.1/prep-to-predict.tsv -c
	cat 1.1/prep-to-predict.tsv | grep ^. | cut -f 2,3 > 1.1/to-predict.tsv
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.1/01-harm-annotated/annotation-data-1.json -o 1.1/01-harm-annotated/all-annotations.tsv -j2c
	# 3. machine learning
	# ../../py3env/bin/python3 -B 1.1/predict_scores.py -a 1.1/01-harm-annotated/all-annotations.tsv -fsmi mi.tsv -fsce ce.tsv -ev model-performances.txt -dev
	# ../../py3env/bin/python3 -B ../../@shared-scripts/baseline.py -a 1.1/01-harm-annotated/all-annotations.tsv -fs baseline-fmeasure.tsv -w 1.1/predicted-baseline.tsv -p 1.1/to-predict.tsv -n 'Sloleks'
	../../py3env/bin/python3 -B 1.1/predict_scores.py -a 1.1/01-harm-annotated/all-annotations.tsv -p 1.1/to-predict.tsv -m PER -w 1.1/predicted.tsv
	# 4. harmonise
	# for w in -1000000 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 1000000 ; do \
	# 	../../py3env/bin/python3 1.1/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.1/01-harm-annotated/all-annotations.tsv | cut -f 2,3) -w 1.1/predicted.tsv -v $$w -ev uas-validation-eval.tsv ;\
	# 	../../py3env/bin/python3 1.1/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.1/01-harm-annotated/all-annotations.tsv | cut -f 2,3) -w 1.1/predicted.tsv -v $$w -ev uas-holdout-eval.tsv ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.1/01-harm-annotated/all-annotations.tsv) -p uas-validation-eval.tsv -o UAS-validation.txt -v $$w ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.1/01-harm-annotated/all-annotations.tsv) -p uas-holdout-eval.tsv -o UAS-holdout.txt -v $$w ;\
	# 	../../py3env/bin/python3 1.1/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.1/01-harm-annotated/all-annotations.tsv | cut -f 2,3) -w 1.1/predicted-baseline.tsv -v $$w -ev uas-validation-baseline-eval.tsv ;\
	# 	../../py3env/bin/python3 1.1/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.1/01-harm-annotated/all-annotations.tsv | cut -f 2,3) -w 1.1/predicted-baseline.tsv -v $$w -ev uas-holdout-baseline-eval.tsv ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.1/01-harm-annotated/all-annotations.tsv) -p uas-validation-baseline-eval.tsv -o UAS-validation-baseline.txt -v $$w ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.1/01-harm-annotated/all-annotations.tsv) -p uas-holdout-baseline-eval.tsv -o UAS-holdout-baseline.txt -v $$w ;\
	# done
	../../py3env/bin/python3 1.1/spanning_trees.py -r 1.1/relations.tsv -w 1.1/predicted.tsv -v 0.0 -o 1.1/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.1/harmonizesloleks.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeSloleks 1.1/harmonized.pickle \
		Save UDer-1.1-sl-Sloleks.tsv
	../../py3env/bin/python3 1.1/edit-json-column.py UDer-1.1-sl-Sloleks.tsv > UDer-1.1-sl-Sloleks-v2.tsv
	mv UDer-1.1-sl-Sloleks-v2.tsv UDer-1.1-sl-Sloleks.tsv


01-harm-annotation: ../../py3env/ get-data-v11
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.1/relations.tsv -o 1.1/01-harm-annotated/annotation-data.json -j


clean:
	rm -rf original-data/ 1.1/relations.tsv 1.1/prep-to-predict.tsv 1.1/to-predict.tsv 1.1/predicted.tsv 1.1/01-harm-annotated/all-annotations.tsv 1.1/harmonized.pickle UDer-1.1-sl-Sloleks-v2.tsv UDer-1.1-sl-Sloleks.tsv
