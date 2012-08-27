Lanyon
----------------------
Use yaml and markdown with a spritz of LaTeX to keep a research diary on your 
UNIX/Linux system, with useful tools and scripts to simplify the process, and 
produce nice-looking output.  This tool can be thought of as
research-diary-project The Next Generation.  It draws big inspiration from
[hyde](http://hyde.github.com), and thus has been given the name of Dr. Jekyll's
eminently skeptical colleague, Dr. Hastie Lanyon.

Requirements
======================
* [pyyaml](http://pyyaml.org/wiki/PyYAML)
* [python-markdown](http://freewisdom.org/projects/python-markdown/)
* [jinja2](http://jinja.pocoo.org/docs/)
* [envoy](https://github.com/kennethreitz/envoy)
* [pandoc](http://johnmacfarlane.net/pandoc/)
* A latex compiler of your choice

The first three packages are all python modules, and if you have pip installed
on your system, you can install them using

    # pip install PyYAML
    # pip install Markdown
    # pip install Jinja2

Envoy is in PyPI, but the version is old.  You __must__ install the github
version for this package to work.  This might be fixed in the future.  I'll keep
an eye on it.

Pandoc is a really cool tool written by the fantastically talented John
MacFarlane.  You ought to have that sucker installed anyway, and can likely get
it through your distro's package manager (or from the website if you are on OS
X or Windows).

Installation
======================
I haven't yet put together an install script, so for the time being, everything
you need is right here in the main directory.  I'd recommend putting a simlink
for lanyon into your `/usr/bin` with the following command inside the lanyon
directory:

    ln -s `pwd`/src/lanyon.py /usr/bin/lanyon
	

Basic Usage
======================
After getting lanyon, you will notice there are 3 directories, and 2 files in
the root directory.  The `README.md` file is the document you are currently
reading.  The params.yaml file contains the configuration options for your
journal.  The options are described below

* _author_ The author name for the journals (That's you!)
* _institution_ Your university or company
* _frequency_ Whether you want a new journal file entry daily, weekly, or
  monthly
* _latex\_compiler_ How you want LaTeX files to be built into pdfs.  This option
  is a list of commands which will be run sequentially, with `FILENAME` used for
  the basename.
* _pdf\_viewer_ What program shall be used to view pdf files.

The three directories you should currently see in the lanyon root are entries,
images, and sr.  The `entries` directory will contain the raw text entries for
your journal. Any images you include will be placed in `images`, and the source
for `lanyon.py` and the various templates for Jinja2 are in `src`.

Once you have configured lanyon to your liking, you can make your first skeleton
entry using the following command `lanyon add`.  This will put a new file in the
entries directory, with a name corresponding to today's date.

You can start editing it right away, but I'd recommend you first look at
example.md in the entries directory.  It shows you the basic layout of what an
entry should look like.  The body of the entry is plain markdown, but any latex
inside it will be passed on through and compiled as latex.  Keep in mind that
yaml requires the body lines to be indented by a single space.

To compile your new entry into a pdf, just run `lanyon build`, and the most
recent entry in the `entries` directory will be compiled to latex (a tex file
will be placed in the `latex` directory, and a pdf (in the `pdf` directory).
And that's about it for the basic usage.

Advanced Usage
======================
You can also use lanyon to compile a big book of entries for an entire year's
work using the `lanyon book YEAR` command.
