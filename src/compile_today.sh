#!/bin/sh

year=`date +%G`
month=`date +%m`
day=`date +%d`

TEXFILE=$year-$month-$day.tex
PSFILE=$year-$month-$day.ps
DVIFILE=$year-$month-$day.dvi
PDFFILE=$year-$month-$day.pdf

echo "Compiling $TEXFILE."

latex -interaction=batchmode -halt-on-error $TEXFILE 
dvips -q -o "$PSFILE" "$DVIFILE" -R0
ps2pdf "$PSFILE" "$PDFFILE"

rm -f *.out *.dvi *.ps *.tex.backup *~ *.aux *.log

okular $PDFFILE >& /dev/null &
