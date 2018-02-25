#!/usr/bin bash

mkdir raw_csv

for file in raw/* ; do
    echo "Converting Excel $file to CSV format."
    in2csv "$file" > "raw_csv/$(basename "${file/.xls}").csv"
done
