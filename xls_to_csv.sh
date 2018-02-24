#!/usr/bin bash

for file in data/raw/* ; do
    echo "Converting Excel $file to CSV format."
    in2csv "$file" > "data/raw_csv/$(basename "${file/.xls}").csv"
done
