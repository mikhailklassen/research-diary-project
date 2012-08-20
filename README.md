research-diary-project
======================

Use TeX/LaTeX to keep a research diary on your UNIX/Linux system, with useful tools and scripts to simplify the process.

Hipster Version
---------------

You know what this project needs?  More buzzword tools.  Luckily,
cool-kid-Keller is here to save the day.  I'm revamping the project to use
Jinja2, YaML, and Mardown to produce a cleaner journal source file, and the ability to
export your log entries to a wider array of outputs.  I'm drawing heavy
inspiration from tools like Jekyll and Hyde, and so I'm calling this version
Lanyon, after the late friend of the good Dr. Jekyll.

Note
====

The research diary employs the McMaster Logo. There is an eps and a png file. If you plan to compile
your research entries including eps images, you'll need to compile using latex instead of pdflatex.

In this case, there is nothing you need to do. The researchdiary.sty file is already prepared to handle
eps files. Other, you will need to modify the researchdiary.sty file, under the 'univlogo' definition,
to use mcmaster_logo.png instead of mcmaster_logo.eps. The researchdiary.sty file is located in the scripts/
directory. 

If you plan to include images that are in pdf, jpg, or png format, and hence will be compiling using
pdflatex, you must modify researchdiary.sty. If you stick to eps files, then everything may be left as is.

Adding entries
==============

To add a new entry, execute add_entry in the main diary directory. If this is the first time adding an
entry, a directory will be created for the current year, as well as an images subdirectory. The style
file for the research diary (researchdiary.sty) as well as the university logo will be soft-linked into
the directory for the current year. A script that compiles the entry for the current day will also be
soft-linked into the same directory.

After running add_entry, enter the directory for the current year and modify today's entry with the 
text editor of your choice, e.g. vim, emacs, or kile.

I also use a subfolder called images/, and within images/ I have subfolders for each day
as necessary. e.g.

    images/2011-10-19/

This avoids potential filename conflicts if I decide to create a figure for one day and simply name it
'graph.eps'

There is no script to automatically create these image subdirectories to avoid littering the main image
directory with many empty subdirectories.

Creating anthologies
====================

At the end of the year, to create a master file with all the entries of that year, you must modify the
Makefile, specifying the year you wish to compile, and setting your name and institution. After this,
save your modified Makefile and from the research diary main directory type

	$ make anthology

This will create a PDF will all the entries from the year specified. To clean up you main directory after
compilation, type

	$ make clean

And that's it!

Happy researching!

