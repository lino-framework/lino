
SITENAME               = lino
#~ DJANGO_SETTINGS_MODULE = dsbe.demo.settings
#~ DJANGO_SETTINGS_MODULE = lino.demos.std.settings
TEMPDIR                = C:\\temp\\sphinxbuild\\$(SITENAME)
BUILDDIR               = $(TEMPDIR)\\html
CACHEDIR               = $(TEMPDIR)\\doctrees
OPENHTML               = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
AUTODOC                = python l:\\snapshots\\sphinx-autopackage-script\\generate_modules.py
#~ LINO_SRC     = t:\\hgwork\\lino\\lino
# LINO_SRC     = `python -c "import lino,os; print os.path.dirname(lino.__file__)"`


# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python l:\\snapshots\\sphinx\\sphinx-build.py
PAPER         =

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS)


.PHONY: help clean html show web pickle htmlhelp latex changes linkcheck autodoc

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  pickle    to make pickle files"
	@echo "  json      to make JSON files"
	@echo "  htmlhelp  to make HTML files and a HTML help project"
	@echo "  latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  changes   to make an overview over all changed/added/deprecated items"
	@echo "  linkcheck to check all external links for integrity"

clean:
	-rm -rf $(CACHEDIR)
	-rm -rf $(BUILDDIR)

html:
	mkdir -p $(CACHEDIR) 
	mkdir -p $(BUILDDIR)
	$(SPHINXBUILD) -b html -d $(CACHEDIR) $(ALLSPHINXOPTS) . $(BUILDDIR)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)."

unused:        
	set DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE); $(SPHINXBUILD) -b html -d $(CACHEDIR) $(ALLSPHINXOPTS) . $(BUILDDIR)

autodoc:
	#~ $(AUTODOC) t:\\hgwork\\lino -d autodoc/lino -s rst -n Lino
	$(AUTODOC) t:\\hgwork\\dsbe -d autodoc/dsbe -s rst -n Lino-DSBE
	#~ $(AUTODOC) lino -d autodoc/lino -s rst -n Lino
	#~ $(AUTODOC) dsbe -d autodoc/dsbe -s rst -n Lino-DSBE
  
show:
	$(OPENHTML) $(BUILDDIR)\index.html
  
upload:
	cd $(BUILDDIR) && rsync -r --progress --delete --times ./ luc@saffre-rumma.ee:/var/cache/sphinxbuild/$(SITENAME)



pickle:
	mkdir -p .build/pickle .build/doctrees
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) .build/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

web: pickle

json:
	mkdir -p .build/json .build/doctrees
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) .build/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	mkdir -p .build/htmlhelp .build/doctrees
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) .build/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in .build/htmlhelp."

latex:
	mkdir -p .build/latex .build/doctrees
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) .build/latex
	@echo
	@echo "Build finished; the LaTeX files are in .build/latex."
	@echo "Run \`make all-pdf' or \`make all-ps' in that directory to" \
	      "run these through (pdf)latex."

changes:
	mkdir -p .build/changes .build/doctrees
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) .build/changes
	@echo
	@echo "The overview file is in .build/changes."

linkcheck:
	mkdir -p .build/linkcheck .build/doctrees
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) .build/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in .build/linkcheck/output.txt."
