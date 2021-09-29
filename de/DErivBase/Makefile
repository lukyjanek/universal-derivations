SHELL=/bin/bash

get-data-v05:
	mkdir -p original-data/
	# 1. download data
	wget -O ../../@input-data/DErivBase-v2.0.zip https://www.ims.uni-stuttgart.de/documents/ressourcen/lexika/derivbase/derivbase-v2.0.zip
	unzip ../../@input-data/DErivBase-v2.0.zip -d original-data/
	# 2. preprocess data
	../../py3env/bin/python3 0.5/extract_relations.py original-data/derivbase/DErivBase-v2.0-rulePaths.txt | sort | uniq > 0.5/relations.tsv
	cat original-data/derivbase/DErivBase-v2.0-families.txt | grep -v ' ' > 0.5/singletons.tsv


UDer-0.5-de-DErivBase.tsv: get-data-v05
	# 1. get-data-v05
	# 2. process annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 0.5/relations.tsv -o 0.5/prep-to-predict.tsv -c
	cat 0.5/prep-to-predict.tsv | grep ^. | cut -f 2,3 > 0.5/to-predict.tsv
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 0.5/01-harm-annotated/annotation-data-1.json -o 0.5/01-harm-annotated/all-annotations.tsv -j2c
	# 3. machine learning
	../../py3env/bin/python3 -B 0.5/predict_scores.py -a 0.5/01-harm-annotated/all-annotations.tsv -l 3 -p 0.5/to-predict.tsv -m DT -w 0.5/predicted.tsv
	# 4. harmonise
	../../py3env/bin/python3 0.5/spanning_trees.py -s 0.5/singletons.tsv -r 0.5/relations.tsv -w 0.5/predicted.tsv -o 0.5/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 0.5/harmonizederivbase.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeDerivBase 0.5/harmonized.pickle \
		Save UDer-0.5-de-DErivBase.tsv

UDer-1.0-de-DErivBase.tsv: get-data-v05
	# 1. get-data-v05
	mv 0.5/singletons.tsv 1.0/singletons.tsv
	mv 0.5/relations.tsv 1.0/relations.tsv
	cp original-data/derivbase/DErivBase-v1.4.1-rules.txt UDer-1.0-de-DErivBase-rules.txt
	# 2. process annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.0/prep-to-predict.tsv -c
	cat 1.0/prep-to-predict.tsv | grep ^. | cut -f 2,3 > 1.0/to-predict.tsv
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/02-harm-annotated/annotation-data-1.json -o 1.0/02-harm-annotated/all-annotations.tsv -j2c
	# 3. machine learning
	# ../../py3env/bin/python3 -B 1.0/predict_scores.py -rel 1.0/relations.tsv -a 1.0/02-harm-annotated/all-annotations.tsv -fsmi mi.tsv -fsce ce.tsv -ev model-performances.txt -dev
	# ../../py3env/bin/python3 -B ../../@shared-scripts/baseline.py -a 1.0/02-harm-annotated/all-annotations.tsv -fs baseline-fmeasure.tsv -w 1.0/predicted-baseline.tsv -p 1.0/to-predict.tsv -n 'DErivBase'
	../../py3env/bin/python3 -B 1.0/predict_scores.py -rel 1.0/relations.tsv -a 1.0/02-harm-annotated/all-annotations.tsv -p 1.0/to-predict.tsv -m LOGR4 -w 1.0/predicted.tsv
	# 4. harmonise
	# for w in -1000000 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 1000000 ; do \
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.0/02-harm-annotated/all-annotations.tsv | sed 's/$$/\t /g' | cut -f 2,3,4) -w 1.0/predicted.tsv -v $$w -ev uas-validation-eval.tsv ;\
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.0/02-harm-annotated/all-annotations.tsv | sed 's/$$/\t /g' | cut -f 2,3,4) -w 1.0/predicted.tsv -v $$w -ev uas-holdout-eval.tsv ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.0/02-harm-annotated/all-annotations.tsv) -p uas-validation-eval.tsv -o UAS-validation.txt -v $$w ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.0/02-harm-annotated/all-annotations.tsv) -p uas-holdout-eval.tsv -o UAS-holdout.txt -v $$w ;\
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.0/02-harm-annotated/all-annotations.tsv | sed 's/$$/\t /g' | cut -f 2,3,4) -w 1.0/predicted-baseline.tsv -v $$w -ev uas-validation-baseline-eval.tsv ;\
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.0/02-harm-annotated/all-annotations.tsv | sed 's/$$/\t /g' | cut -f 2,3,4) -w 1.0/predicted-baseline.tsv -v $$w -ev uas-holdout-baseline-eval.tsv ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.0/02-harm-annotated/all-annotations.tsv) -p uas-validation-baseline-eval.tsv -o UAS-validation-baseline.txt -v $$w ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.0/02-harm-annotated/all-annotations.tsv) -p uas-holdout-baseline-eval.tsv -o UAS-holdout-baseline.txt -v $$w ;\
	# done
	../../py3env/bin/python3 1.0/spanning_trees.py -s 1.0/singletons.tsv -r 1.0/relations.tsv -w 1.0/predicted.tsv -v 0.1 -o 1.0/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 0.5/harmonizederivbase.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeDerivBase 1.0/harmonized.pickle \
		Save UDer-1.0-de-DErivBase.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.0-de-DErivBase.tsv > UDer-1.0-de-DErivBase-v2.tsv
	mv UDer-1.0-de-DErivBase-v2.tsv UDer-1.0-de-DErivBase.tsv

UDer-1.1-de-DErivBase.tsv: get-data-v05
	# 1. get-data-v05
	mv 0.5/singletons.tsv 1.1/singletons.tsv
	mv 0.5/relations.tsv 1.1/relations.tsv
	cp original-data/derivbase/DErivBase-v1.4.1-rules.txt UDer-1.1-de-DErivBase-rules.txt
	# 2. process annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.1/relations.tsv -o 1.1/prep-to-predict.tsv -c
	cat 1.1/prep-to-predict.tsv | grep ^. | cut -f 2,3 > 1.1/to-predict.tsv
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.1/03-harm-annotated/annotation-data-1.json -o 1.1/03-harm-annotated/all-annotations.tsv -j2c
	# 3. machine learning
	../../py3env/bin/python3 -B 1.0/predict_scores.py -rel 1.1/relations.tsv -a 1.1/03-harm-annotated/all-annotations.tsv -p 1.1/to-predict.tsv -m LOGR4 -w 1.1/predicted.tsv
	# 4. harmonise
	../../py3env/bin/python3 1.1/spanning_trees.py -s 1.1/singletons.tsv -r 1.1/relations.tsv -w 1.1/predicted.tsv -v 0.1 -o 1.1/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.1/harmonizederivbase.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeDerivBase 1.1/harmonized.pickle \
		Save UDer-1.1-de-DErivBase.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.1-de-DErivBase.tsv > UDer-1.1-de-DErivBase-v2.tsv
	mv UDer-1.1-de-DErivBase-v2.tsv UDer-1.1-de-DErivBase.tsv


01-harm-annotation: get-data-v05
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 0.5/relations.tsv -o 0.5/01-harm-annotated/annotation-data.json -j

02-harm-annotation:
	cp 0.5/01-harm-annotated/annotation-data-1.json 1.0/02-harm-annotated/annotation-data-1.json


clean:
	rm -rf original-data/ 0.5/relations.tsv 0.5/singletons.tsv 0.5/prep-to-predict.tsv 0.5/to-predict.tsv 0.5/predicted.tsv 0.5/01-harm-annotated/all-annotations.tsv 0.5/harmonized.pickle UDer-0.5-de-DErivBase.tsv
	rm -rf original-data/ 1.0/relations.tsv 1.0/singletons.tsv 1.0/prep-to-predict.tsv 1.0/to-predict.tsv 1.0/predicted.tsv 1.0/02-harm-annotated/all-annotations.tsv 1.0/harmonized.pickle UDer-1.0-de-DErivBase.tsv UDer-1.0-de-DErivBase-v2.tsv UDer-1.0-de-DErivBase-rules.txt
	rm -rf original-data/ 1.1/relations.tsv 1.1/singletons.tsv 1.1/prep-to-predict.tsv 1.1/to-predict.tsv 1.1/predicted.tsv 1.1/03-harm-annotated/all-annotations.tsv 1.1/harmonized.pickle UDer-1.1-de-DErivBase.tsv UDer-1.1-de-DErivBase-v2.tsv UDer-1.1-de-DErivBase-rules.txt
