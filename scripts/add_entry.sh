#!/bin/sh

year=`date +%G`
month=`date +%m`
day=`date +%d`

echo "Today is $year / $month / $day"

if [ ! -d "$year" ]; then
    mkdir $year
    mkdir $year/images
    cd $year
    ln -s ../images/mcmaster_logo.eps .
    ln -s ../images/mcmaster_logo.png .
    ln -s ../scripts/researchdiary.sty .
    ln -s ../scripts/clean.sh clean
    ln -s ../scripts/compile_today.sh compile_today
    cd ..
fi

if [ -d "$year" ]; then
    echo "Adding new entry to directory $year."
fi

cd $year
filename=$year-$month-$day.tex

if [ -f "$filename" ]; then
    echo "A file called '$filename' already exists in diretory $year. Aborting addition of new entry."
    exit
fi

cp ../scripts/entry.tex $filename

sed -i "s/@year/$year/g" $filename
sed -i "s/@MONTH/`date +%B`/g" $filename
sed -i "s/@dday/$day/g" $filename
sed -i "s/@day/`date +%e`/g" $filename

echo "Finished adding $filename to $year."
