SHELL=/bin/bash

../../@input-data/celex2.zip:
	@echo "$$(tput setaf 1)You need celex2.zip. It is not free. More info here:\n\thttps://catalog.ldc.upenn.edu/LDC96L14"


get-data-v10: ../../@input-data/celex2.zip
	mkdir -p original-data/
	# 1. download data
	unzip -q ../../@input-data/celex2.zip -d original-data/
	# 2. preproces data
	../../py3env/bin/python3 1.0/extract_relations.py original-data/celex2/german/gml/gml.cd 1.0/relations.tsv 1.0/singletons.tsv 1.0/compounds.tsv


morphology/:
	git clone https://github.com/petrasteiner/morphology.git

morphology/GMOLoutputneworthography: get-data-v10 morphology/
	cp original-data/celex2/german/gml/gml.cd morphology/GML.CD
	cp original-data/celex2/german/gol/gol.cd morphology/GOL.CD
	cp original-data/celex2/german/gsl/gsl.cd morphology/GSL.CD
	cd morphology/ && perl OrthCELEX.pl


UDer-1.0-de-GCelex.tsv: get-data-v10
	# 1. get-data-v10
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.0/prep-to-predict.tsv -c
	cat 1.0/prep-to-predict.tsv | grep ^. | cut -f 2,3 > 1.0/to-predict.tsv
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/01-harm-annotated/annotation-data-1.json -o 1.0/01-harm-annotated/all-annotations.tsv -j2c
	# 3. machine learning
	# ../../py3env/bin/python3 -B 1.0/predict_scores.py -a 1.0/01-harm-annotated/all-annotations.tsv -fsmi mi.tsv -fsce ce.tsv -ev model-performances.txt -dev
	# ../../py3env/bin/python3 -B ../../@shared-scripts/baseline.py -a <(cat 1.0/01-harm-annotated/all-annotations.tsv | sed 's/\t[0-9]*/\t/g' | sed 's/\t_/\t/g') -fs baseline-fmeasure.tsv -w 1.0/predicted-baseline.tsv -p <(cat 1.0/to-predict.tsv | sed 's/^[0-9]*_//g' | sed 's/\t[0-9]*/\t/g' | sed 's/\t_/\t/g') -n 'GCelex'
	../../py3env/bin/python3 -B 1.0/predict_scores.py -a 1.0/01-harm-annotated/all-annotations.tsv -p 1.0/to-predict.tsv -m DT3 -w 1.0/predicted.tsv
	# 4. harmonise
	# for w in -1000000 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 1000000 ; do \
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.0/01-harm-annotated/all-annotations.tsv | sed 's/$$/\t /g' | cut -f 2,3,4) -w 1.0/predicted.tsv -v $$w -ev uas-validation-eval.tsv ;\
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.0/01-harm-annotated/all-annotations.tsv | sed 's/$$/\t /g' | cut -f 2,3,4) -w 1.0/predicted.tsv -v $$w -ev uas-holdout-eval.tsv ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.0/01-harm-annotated/all-annotations.tsv) -p uas-validation-eval.tsv -o UAS-validation.txt -v $$w ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.0/01-harm-annotated/all-annotations.tsv) -p uas-holdout-eval.tsv -o UAS-holdout.txt -v $$w ;\
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.0/01-harm-annotated/all-annotations.tsv | sed 's/$$/\t /g' | cut -f 2,3,4) -w 1.0/predicted-baseline.tsv -v $$w -ev uas-validation-baseline-eval.tsv ;\
	# 	../../py3env/bin/python3 1.0/spanning_trees.py -r <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.0/01-harm-annotated/all-annotations.tsv | sed 's/$$/\t /g' | cut -f 2,3,4) -w 1.0/predicted-baseline.tsv -v $$w -ev uas-holdout-baseline-eval.tsv ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -V -a 1.0/01-harm-annotated/all-annotations.tsv) -p uas-validation-baseline-eval.tsv -o UAS-validation-baseline.txt -v $$w ;\
	# 	../../py3env/bin/python3 ../../@shared-scripts/uas_score.py -a <(../../py3env/bin/python3 ../../@shared-scripts/split_data.py -H -a 1.0/01-harm-annotated/all-annotations.tsv) -p uas-holdout-baseline-eval.tsv -o UAS-holdout-baseline.txt -v $$w ;\
	# done
	../../py3env/bin/python3 1.0/spanning_trees.py -s 1.0/singletons.tsv -c 1.0/compounds.tsv -r 1.0/relations.tsv -w 1.0/predicted.tsv -v 0.5 -o 1.0/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.0/harmonizegcelex.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeGCelex 1.0/harmonized.pickle \
		Save UDer-1.0-de-GCelex.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.0-de-GCelex.tsv > UDer-1.0-de-GCelex-v2.tsv
	mv UDer-1.0-de-GCelex-v2.tsv UDer-1.0-de-GCelex.tsv

UDer-1.1-de-GCelex.tsv: get-data-v10 morphology/GMOLoutputneworthography
	# 1. get-data-v10
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.1/prep-to-predict.tsv -c
	cat 1.1/prep-to-predict.tsv | grep ^. | cut -f 2,3 > 1.1/to-predict.tsv
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/01-harm-annotated/annotation-data-1.json -o 1.0/01-harm-annotated/all-annotations.tsv -j2c
	# 3. machine learning
	../../py3env/bin/python3 -B 1.0/predict_scores.py -a 1.0/01-harm-annotated/all-annotations.tsv -p 1.1/to-predict.tsv -m DT3 -w 1.1/predicted.tsv
	# 4. harmonise
	../../py3env/bin/python3 1.1/spanning_trees.py -s 1.0/singletons.tsv -c 1.0/compounds.tsv -r 1.0/relations.tsv -w 1.1/predicted.tsv -v 0.5 -o 1.1/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.1/harmonizegcelex.py ../../derinet2/derinet/modules/uder/
	cp 1.1/modernisegcelexorthography.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeGCelex 1.1/harmonized.pickle \
		uder.ModerniseGCelexOrthography morphology/GMOLoutputneworthography \
		Save UDer-1.1-de-GCelex-nomorphs.tsv
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		Load UDer-1.1-de-GCelex-nomorphs.tsv \
		de.InferCELEXMorphs \
		Save UDer-1.1-de-GCelex.tsv


01-harm-annotation: get-data-v10
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.0/01-harm-annotated/annotation-data.json -j


clean:
	rm -rf original-data/ 1.0/relations.tsv 1.0/singletons.tsv 1.0/compounds.tsv 1.0/prep-to-predict.tsv 1.0/to-predict.tsv 1.0/predicted.tsv 1.0/01-harm-annotated/all-annotations.tsv 1.0/harmonized.pickle UDer-1.0-de-GCelex.tsv
	rm -rf morphology/ 1.1/prep-to-predict.tsv 1.1/to-predict.tsv 1.1/predicted.tsv 1.1/harmonized.pickle UDer-1.1-de-GCelex.tsv morphology/gml.cd morphology/gsl.cd morphology/gol.cd morphology/GML* morphology/GMO* morphology/Doubleconsonants morphology/GOL* morphology/Checkfile
