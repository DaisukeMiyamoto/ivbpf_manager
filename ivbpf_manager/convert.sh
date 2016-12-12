#!/bin/bash -x
#CONVERTER="libreoffice --headless --convert-to xls:MS Excel 97"
EXCEL2XOONIPS="/usr/local/xoonips/bin/excel2xoonips"

for i in 1 2 5 10 112 9 12 8 3 7 13; do
    libreoffice --headless --convert-to xls:"MS Excel 97" newdb${i}.xlsx
    $EXCEL2XOONIPS newdb${i}.xls newdb${i}.zip
    rm -f newdb${i}.xls
done
