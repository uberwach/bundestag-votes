all: data
data: get-data convert-csv build-dataset

get-data:
	cd data && mkdir -p raw && bash get_data.sh


convert-csv: get-data
	cd data && mkdir -p raw_csv && bash xls_to_csv.sh


build-dataset: convert-csv
	mkdir -p data/preprocessed
	python src/preprocessing.py


clean:
	rm -rf data/raw data/raw_csv data/preprocessed
