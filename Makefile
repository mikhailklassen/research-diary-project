# Custom Makefile for Compiling Research Diaries
# ----------------------------------------------
#
#  Author:   Mikhail Klassen
#  Email:    klassm@mcmaster.ca
#  Created:  21 November 2011
#  Modified: 3 January 2012

# Set the diary year you wish to compile and user info
YEAR := 2012
AUTHOR := FirstName LastName
INSTITUTION := InstitutionName

# Do not edit past this line
RM := rm -rf
SHELL := /bin/bash

TEXFILE := $(YEAR)-Research-Diary.tex
LOGFILE := $(YEAR)-Research-Diary.log
DVIFILE := $(YEAR)-Research-Diary.dvi
PSFILE := $(YEAR)-Research-Diary.ps
PDFFILE := $(YEAR)-Research-Diary.pdf
AUXFILE := $(YEAR)-Research-Diary.aux
OUTFILE := $(YEAR)-Research-Diary.out

.PHONY : clean

anthology:
	-@echo 'Creating anthology for research diary entries from the year $(YEAR)'
	-@$(SHELL) scripts/create_anthology.sh "$(YEAR)" "$(AUTHOR)" "$(INSTITUTION)"
	-latex -interaction=batchmode -halt-on-error $(TEXFILE) 
	-dvips -q -o "$(PSFILE)" "$(DVIFILE)" -R0
	-ps2pdf "$(PSFILE)" "$(PDFFILE)"
	-okular $(PDFFILE)


clean:
	-$(RM) $(TEXFILE)
	-$(RM) $(LOGFILE) $(DVIFILE) $(PSFILE) $(AUXFILE) $(OUTFILE)
	-$(RM) *.tmp
	-@echo 'Done cleaning'
