#!/bin/bash

Year="$1"
Author="$2"
Institution="$3"
Name="$Year-Research-Diary"
FileName=$Name".tex"
tmpName=$Name".tmp"

if [ -z "$Year" ]; then echo "ERROR: Year not specified."; exit; fi
if [ -z "$Author" ]; then echo "ERROR: Author not specified."; exit; fi
if [ -z "$Institution" ]; then echo "ERROR: Institution not specified."; exit; fi

echo "Research Diary"
echo "User: $Author ($Institution)"
echo "Year: $Year"

path=`pwd`
if [ "`basename $path`" == 'scripts' ]; then
    cd ..
fi

if [ -d $Year ]; then
    echo "Directory for year $Year found. Continuing..."
else
    echo "ERROR: No directory for $Year exists"
    exit;
fi

touch $FileName
echo "%" >> $FileName
echo "% Research Diary for $Author ($Institution), $Year" >> $FileName
echo "%" >> $FileName
echo "\documentclass[letterpaper,11pt]{article}" >> $FileName
echo "\newcommand{\userName}{$Author}" >> $FileName
echo "\newcommand{\institution}{$Institution}" >> $FileName
echo "\usepackage{researchdiary}" >> $FileName
echo " " >> $FileName
echo "\title{Research Diary - $Year}" >> $FileName
echo "\author{$Author}" >> $FileName
echo " " >> $FileName

echo "\chead{\textsc{Research Diary}}" >> $FileName
echo "\lhead{\textsc{\userName}}" >> $FileName
echo "\rfoot{\textsc{\thepage}}" >> $FileName
echo "\cfoot{\textit{Last modified: \today}}" >> $FileName
echo "\lfoot{\textsc{\institution}}" >> $FileName
echo "\graphicspath{{$Year/}{~/research/diary/$Year/}{~/research/diary/$Year/images/}}" >> $FileName

echo " " >> $FileName
echo " " >> $FileName
echo "\begin{document}" >> $FileName
echo "\begin{center} \begin{LARGE}" >> $FileName
echo "\textbf{Research Diary} \\\\[3mm]" >> $FileName
echo "\textbf{$Year} \\\\[2cm]" >> $FileName
echo "\end{LARGE} \begin{large}" >> $FileName
echo "$Author \end{large} \\\\" >> $FileName
echo "$Institution \\\\[7in]" >> $FileName
echo "\textsc{Compiled \today}" >> $FileName
echo "\end{center}" >> $FileName
echo "\thispagestyle{empty}" >> $FileName
echo "\newpage" >> $FileName

for i in $( ls $Year/$Year-*.tex ); do
    echo -e "\n%%% --- $i --- %%%\n" >> $tmpName
    echo "\rhead{`grep workingDate $i | cut -d { -f 4 | cut -d } -f 1`}" >> $tmpName
    sed -n '/\\begin{document}/,/\\end{document}/p' $i >> $tmpName
    echo -e "\n" >> $tmpName
    echo "\newpage" >> $tmpName
done

sed -i 's/\\begin{document}//g' $tmpName
sed -i 's/\\end{document}//g' $tmpName
sed -i 's/\\includegraphics\(.*\){\([A-Za-z0-9]*\)\/\([A-Za-z0-9_-]*\)/\\includegraphics\1{\3/g' $tmpName
sed -i 's/\\newcommand/\\renewcommand/g' $tmpName

cat $tmpName >> $FileName

echo "\end{document}" >> $FileName

if [ "$Year" == '2011' ]; then
    sed -i '/\\begin{extract}/,/\\end{extract}/d' 2011-Research-Diary.tex
    sed -i 's/\\begin{extract\*}//g' 2011-Research-Diary.tex
    sed -i 's/\\end{extract\*}//g' 2011-Research-Diary.tex
fi

if [ "$Year" == '2010' ]; then
    sed -i 's/mcmaster_logo.png/mcmaster_logo.eps/g' 2010-Research-Diary.tex
fi

if [ "`basename $path`" == 'scripts' ]; then
    cd scripts
fi
