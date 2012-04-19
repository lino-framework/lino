DJANGO_ADMIN = python l:\\snapshots\\django\\django\\bin\\django-admin.py
LINO_ROOT := /cygdrive/t/hgwork/lino
LINO_ROOT := `cygpath -m $(LINO_ROOT)`
APPS = pcsw igen
MODULES = debts families cv isip mails cal jobs thirds products properties contacts countries notes sales finan links uploads users newcomers
TESTS_OPTIONS = --verbosity=2 --traceback

#LANGUAGES = de fr nl et
#INPUT_FILES = lino\\actions.py lino\\ui\\extjs\\ext_ui.py lino\\modlib\\fields.py lino\\modlib\\system\\models.py

.PHONY: mm cm makedocs tests sdist

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  mm     run django-admin makemessages on modlib"
	@echo "  cm     run django-admin compilemessages on modlib"
	@echo "  tests  run Lino test suite"
  

mm:
	#~ $(DJANGO_ADMIN) dtl2py --settings lino.apps.pcsw.settings
	#~ $(DJANGO_ADMIN) dtl2py --settings lino.apps.igen.settings
	pwd
	cd $(LINO_ROOT)/lino && $(DJANGO_ADMIN) makemessages -i 'modlib*' -i 'apps*' -i 'test_apps*' -s -a
	for MOD in $(MODULES); do \
	  cd $(LINO_ROOT)/lino/modlib/$$MOD && pwd && $(DJANGO_ADMIN) makemessages -s -a; \
	done
	for i in $(APPS); do \
    cd $(LINO_ROOT)/lino/apps/$$i && pwd && $(DJANGO_ADMIN) makemessages -s -a; \
	done
  

cm:  
	cd $(LINO_ROOT)/lino && $(DJANGO_ADMIN) compilemessages 
	@for MOD in $(MODULES); \
	do \
	  cd $(LINO_ROOT)/lino/modlib/$$MOD && $(DJANGO_ADMIN) compilemessages; \
	done
	for i in $(APPS); do \
	  cd $(LINO_ROOT)/lino/apps/$$i && $(DJANGO_ADMIN) compilemessages; \
	done
  
tests:  
	export DJANGO_SETTINGS_MODULE=lino.apps.std.settings ; python lino/utils/choicelists.py
	python lino/utils/jsgen.py
	python lino/utils/__init__.py
	python lino/utils/ranges.py
	#~ python lino\utils\xmlgen\__init__.py
	python lino/utils/xmlgen/cbss/__init__.py
	python lino/utils/xmlgen/intervat/__init__.py
	python lino/utils/xmlgen/odf/__init__.py
	python lino\utils\rstgen.py
	python lino\modlib\contacts\utils.py
	$(DJANGO_ADMIN) test --settings=lino.test_apps.1.settings  $(TESTS_OPTIONS)
	$(DJANGO_ADMIN) test --settings=lino.test_apps.20100212.settings $(TESTS_OPTIONS)
	#~ $(DJANGO_ADMIN) test --settings=lino.apps.std.settings
	$(DJANGO_ADMIN) test --settings=lino.apps.pcsw.settings $(TESTS_OPTIONS)
	#~ $(DJANGO_ADMIN) test --settings=lino.apps.igen.settings $(TESTS_OPTIONS)


unused_appdocs:
	$(DJANGO_ADMIN) makedocs --settings lino.apps.pcsw.settings docs/pcsw/appdocs
	$(DJANGO_ADMIN) makedocs --settings lino.apps.igen.settings docs/igen/appdocs

sdist:
	python setup.py register sdist --formats=gztar,zip --dist-dir=docs/dist upload 
	#~ python setup.py sdist --formats=gztar,zip --dist-dir=docs/dist
  
html:
	cd docs ; export DJANGO_SETTINGS_MODULE=lino.apps.std.settings ; make html

upload:
	cd docs ; make upload
	