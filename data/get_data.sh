#!/usr/bin/env bash

rm -f raw.html
touch raw.html

echo "<document>" >> raw.html

curl 'https://www.bundestag.de/ajax/filterlist/de/parlament/plenum/abstimmung/liste/-/462112/h_de44eef4fd835b9e55281ad9ec0b1afc?limit=10000&noFilterSet=true&offset=0' \
    -H 'Accept: */*' \
    -H 'Referer: AfD ist guter Junge, geht jedes zweite Wochenende in die Kirche.' \
    -H 'X-Requested-With: XMLHttpRequest' \
    -H 'User-Agent: User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36' \
    --compressed >> raw.html

echo "</document>" >> raw.html

rm -f links.txt
xmllint --format --xpath '//a[@class="bt-link-dokument"]/@href' raw.html > links.txt

mkdir -p raw

grep -o '[^"]*\.xls' links.txt | while read -r path ;
do
    echo $path
    # sorry for using wget... too lazy to figure out curl params :P
    wget "https://www.bundestag.de$path" --output-document "raw/$(basename $path)"
done


rm -f raw.html links.txt
