SHELL=/bin/bash

../../py3env/:
	cd ../../ && $(MAKE) py3env/

../../derinet2/:
	cd ../../ && $(MAKE) derinet2/

../../@input-data/derivatario.csv:  # FIX: incorrect URL
	wget -O ../../@input-data/derivatario.csv http://derivatario.sns.it/derivatario.csv

../../@input-data/Lemmi_rango_txt.zip:  # FIX: incorrect URL
	wget -O ../../@input-data/Lemmi_rango_txt.zip http://linguistica.sns.it/CoLFIS/files/Lemmi_rango_txt.zip


get-data-v10: ../../py3env/ ../../@input-data/derivatario.csv ../../@input-data/Lemmi_rango_txt.zip
	mkdir -p original-data/
	# 1. download data
	unzip -q ../../@input-data/Lemmi_rango_txt.zip -d original-data/
	# 2. preproces data
	cat original-data/Lemmi_rango.txt | sed -e '1d' | sed -e "s/[\'\:\(\)\-\–\/\<\>\.\?\!\+\&]/a/g" -e 's/[\"-]/a/g' -e 's/\,\s[a-zA-Z0-9]*/a/g' -e 's/[a-zA-Z0-9]\s[a-zA-Z0-9]/a/g' -e 's/[a-zA-Z0-9]\s[a-zA-Z0-9]/a/g' -e 's/[a-zA-Z0-9]\s[a-zA-Z0-9]/a/g' | tr -s ' ' | cut -d ' ' -f 1,17  | sed -e 's/VaaC@/VA-IN-TC@/g' | sed -e 's/aaC@/V-IN-TC@/g' | sed -e 's/3407 MINUTO/3407 E@/g' | sed -e 's/88190 W/88190 E/g' > original-data/derivatario-pos-list.txt
	cat ../../@input-data/derivatario.csv | while read -r a; do echo -ne $$a'\t' >> original-data/derivatario-with-pos.txt; echo $$a | cut -d ';' -f 1 | tr '\n' ' ' | sed -e 's/^/\^/g' | grep -f - original-data/derivatario-pos-list.txt | cut -d ' ' -f 2 >> original-data/derivatario-with-pos.txt; done
	../../py3env/bin/python3 1.0/extract_relations.py original-data/derivatario-with-pos.txt 1.0/relations.tsv 1.0/singletons.tsv


UDer-1.0-it-DerIvaTario.tsv: ../../derinet2/ ../../py3env/ get-data-v10
	# 1. get-data-v10
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.0/prep-to-predict.tsv -c
	cat 1.0/prep-to-predict.tsv | grep ^. | cut -f 2,3 > 1.0/to-predict.tsv
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/01-harm-annotated/annotation-data-1.json -o 1.0/01-harm-annotated/all-annotations.tsv -j2c
	# 3. machine learning
	# ../../py3env/bin/python3 -B 1.0/predict_scores.py -a 1.0/01-harm-annotated/all-annotations.tsv -fsmi mi.tsv -fsce ce.tsv -ev model-performances.txt -dev
	# ../../py3env/bin/python3 -B ../../@shared-scripts/baseline.py -a 1.0/01-harm-annotated/all-annotations.tsv -fs baseline-fmeasure.tsv -w 1.0/predicted-baseline.tsv -p 1.0/to-predict.tsv -n 'DerIvaTario'
	../../py3env/bin/python3 -B 1.0/predict_scores.py -a 1.0/01-harm-annotated/all-annotations.tsv -p 1.0/to-predict.tsv -m DT2 -w 1.0/predicted.tsv
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
	../../py3env/bin/python3 1.0/spanning_trees.py -s 1.0/singletons.tsv -r 1.0/relations.tsv -w 1.0/predicted.tsv -v 0.6 -o 1.0/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.0/harmonizederivatario.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeDerIvaTario 1.0/harmonized.pickle \
		Save UDer-1.0-it-DerIvaTario.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.0-it-DerIvaTario.tsv > UDer-1.0-it-DerIvaTario-v2.tsv
	mv UDer-1.0-it-DerIvaTario-v2.tsv UDer-1.0-it-DerIvaTario.tsv

UDer-1.1-it-DerIvaTario.tsv: ../../derinet2/ ../../py3env/ get-data-v10
	# 1. get-data-v10
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.1/prep-to-predict.tsv -c
	cat 1.1/prep-to-predict.tsv | grep ^. | cut -f 2,3 > 1.1/to-predict.tsv
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/01-harm-annotated/annotation-data-1.json -o 1.0/01-harm-annotated/all-annotations.tsv -j2c
	# 3. machine learning
	../../py3env/bin/python3 -B 1.1/predict_scores.py -a 1.0/01-harm-annotated/all-annotations.tsv -p 1.1/to-predict.tsv -m DT2 -w 1.1/predicted.tsv
	# 4. harmonise
	../../py3env/bin/python3 1.1/spanning_trees.py -s 1.0/singletons.tsv -r 1.0/relations.tsv -w 1.1/predicted.tsv -v 0.6 -o 1.1/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.1/harmonizederivatario.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeDerIvaTario 1.1/harmonized.pickle \
		Save UDer-1.1-it-DerIvaTario.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.1-it-DerIvaTario.tsv > UDer-1.1-it-DerIvaTario-v2.tsv
	mv UDer-1.1-it-DerIvaTario-v2.tsv UDer-1.1-it-DerIvaTario.tsv

01-harm-annotation: ../../py3env/ get-data-v10
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.0/01-harm-annotated/annotation-data.json -j


clean:
	rm -rf original-data/ 1.0/relations.tsv 1.0/predicted.tsv 1.0/to-predict.tsv 1.0/prep-to-predict.tsv 1.0/singletons.tsv 1.0/01-harm-annotated/all-annotations.tsv 1.0/harmonized.pickle 1.0/UDer-1.0-it-DerIvaTario-v2.tsv UDer-1.0-it-DerIvaTario.tsv
	rm -rf original-data/ 1.1/predicted.tsv 1.1/to-predict.tsv 1.1/prep-to-predict.tsv 1.1/harmonized.pickle UDer-1.1-it-DerIvaTario-v2.tsv UDer-1.1-it-DerIvaTario.tsv
