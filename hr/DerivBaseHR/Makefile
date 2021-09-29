SHELL=/bin/bash

get-data-v10:
	mkdir -p original-data/
	# 1. download data
	wget -O ../../@input-data/DerivBase.hr.v1.tar.gz http://takelab.fer.hr/data/derivbasehr/DerivBase.hr.v1.tar.gz
	tar -xzf ../../@input-data/DerivBase.hr.v1.tar.gz -C original-data/
	# 2. preproces data
	../../py3env/bin/python3 1.0/extract_relations.py original-data/DerivBase.hr.v1/DerivBase.hr.K.v1.0 > 1.0/relations.tsv
	cat original-data/DerivBase.hr.v1/DerivBase.hr.K.v1.0 | grep -v ' ' > 1.0/singletons.tsv


UDer-1.0-hr-DerivBaseHR.tsv: get-data-v10
	# 1. get-data-v10
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.0/prep-to-predict.tsv -c
	cat 1.0/prep-to-predict.tsv | grep ^. | cut -f 2,3 > 1.0/to-predict.tsv
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/01-harm-annotated/annotation-data-1.json -o 1.0/01-harm-annotated/all-annotations.tsv -j2c
	# 3. machine learning
	# ../../py3env/bin/python3 -B 1.0/predict_scores.py -a 1.0/01-harm-annotated/all-annotations.tsv -fsmi mi.tsv -fsce ce.tsv -ev model-performances.txt -dev
	# ../../py3env/bin/python3 -B ../../@shared-scripts/baseline.py -a 1.0/01-harm-annotated/all-annotations.tsv -fs baseline-fmeasure.tsv -w 1.0/predicted-baseline.tsv -p 1.0/to-predict.tsv -n 'DerivBase.Hr'
	split -l 500000 1.0/to-predict.tsv -d 1.0/to-predict-part
	for part in $$(ls -1 1.0/to-predict-part*) ; do \
		../../py3env/bin/python3 -B 1.0/predict_scores.py -a 1.0/01-harm-annotated/all-annotations.tsv -p $$part -m DT -w 1.0/predicted.tsv ;\
	done
	rm -rf 1.0/to-predict-part*
	# 4. harmonise
	# for w in -1000000 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 1000000 ; do \
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.0/01-harm-annotated/all-annotations.tsv | cut -f 2,3) -w 1.0/predicted.tsv -v $$w -ev uas-validation-eval.tsv ;\
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.0/01-harm-annotated/all-annotations.tsv | cut -f 2,3) -w 1.0/predicted.tsv -v $$w -ev uas-holdout-eval.tsv ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.0/01-harm-annotated/all-annotations.tsv) -p uas-validation-eval.tsv -o UAS-validation.txt -v $$w ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.0/01-harm-annotated/all-annotations.tsv) -p uas-holdout-eval.tsv -o UAS-holdout.txt -v $$w ;\
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.0/01-harm-annotated/all-annotations.tsv | cut -f 2,3) -w 1.0/predicted-baseline.tsv -v $$w -ev uas-validation-baseline-eval.tsv ;\
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.0/01-harm-annotated/all-annotations.tsv | cut -f 2,3) -w 1.0/predicted-baseline.tsv -v $$w -ev uas-holdout-baseline-eval.tsv ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.0/01-harm-annotated/all-annotations.tsv) -p uas-validation-baseline-eval.tsv -o UAS-validation-baseline.txt -v $$w ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.0/01-harm-annotated/all-annotations.tsv) -p uas-holdout-baseline-eval.tsv -o UAS-holdout-baseline.txt -v $$w ;\
	# done
	../../py3env/bin/python3 1.0/spanning_trees.py -s 1.0/singletons.tsv -r 1.0/relations.tsv -w 1.0/predicted.tsv -v 0.2 -o 1.0/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.0/harmonizederivbasehr.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeDerivBaseHR 1.0/harmonized.pickle \
		Save UDer-1.0-hr-DerivBaseHR.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.0-hr-DerivBaseHR.tsv > UDer-1.0-hr-DerivBaseHR-v2.tsv
	mv UDer-1.0-hr-DerivBaseHR-v2.tsv UDer-1.0-hr-DerivBaseHR.tsv

UDer-1.1-hr-DerivBaseHR.tsv: get-data-v10
	# 1. get-data-v10
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.1/prep-to-predict.tsv -c
	cat 1.1/prep-to-predict.tsv | grep ^. | cut -f 2,3 > 1.1/to-predict.tsv
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/01-harm-annotated/annotation-data-1.json -o 1.0/01-harm-annotated/all-annotations.tsv -j2c
	# 3. machine learning
	split -l 500000 1.1/to-predict.tsv -d 1.1/to-predict-part
	for part in $$(ls -1 1.1/to-predict-part*) ; do \
		../../py3env/bin/python3 -B 1.0/predict_scores.py -a 1.0/01-harm-annotated/all-annotations.tsv -p $$part -m DT -w 1.1/predicted.tsv ;\
	done
	rm -rf 1.1/to-predict-part*
	# 4. harmonise
	../../py3env/bin/python3 1.1/spanning_trees.py -s 1.0/singletons.tsv -r 1.0/relations.tsv -w 1.1/predicted.tsv -v 0.2 -o 1.1/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.1/harmonizederivbasehr.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeDerivBaseHR 1.1/harmonized.pickle \
		Save UDer-1.1-hr-DerivBaseHR.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.1-hr-DerivBaseHR.tsv > UDer-1.1-hr-DerivBaseHR-v2.tsv
	mv UDer-1.1-hr-DerivBaseHR-v2.tsv UDer-1.1-hr-DerivBaseHR.tsv


01-harm-annotation: get-data-v10
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.0/01-harm-annotated/annotation-data.json -j


clean:
	rm -rf original-data/ 1.0/relations.tsv 1.0/singletons.tsv 1.0/prep-to-predict.tsv 1.0/to-predict.tsv 1.0/predicted.tsv 1.0/01-harm-annotated/all-annotations.tsv 1.0/harmonized.pickle UDer-1.0-hr-DerivBaseHR-v2.tsv UDer-1.0-hr-DerivBaseHR.tsv
	rm -rf original-data/ 1.1/prep-to-predict.tsv 1.1/to-predict.tsv 1.1/predicted.tsv 1.1/harmonized.pickle UDer-1.1-hr-DerivBaseHR-v2.tsv UDer-1.1-hr-DerivBaseHR.tsv
