DJANGO_ADMIN = python l:\\snapshots\\django\\django\\bin\\django-admin.py
LINO_ROOT := /cygdrive/t/hgwork/lino
LINO_ROOT := `cygpath -m $(LINO_ROOT)`
APPS = cosi 
MODULES = vat accounts ledger households outbox \
  cal products properties contacts countries notes \
  sales finan uploads users postings about
TESTS_OPTIONS = --verbosity=2 --traceback
MMOPTS := -s -a --settings lino.apps.sphinxdocs.settings
CMOPTS := --settings lino.apps.sphinxdocs.settings

.PHONY: mm cm makedocs tests sdist

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  mm     run django-admin makemessages on modlib"
	@echo "  cm     run django-admin compilemessages on modlib"
	@echo "  tests  run Lino test suite"
  

mm:
	pwd
	cd $(LINO_ROOT)/lino && $(DJANGO_ADMIN) makemessages -i 'sandbox*' -i 'modlib*' -i 'apps*' -i 'test_apps*' $(MMOPTS)
	for MOD in $(MODULES); do \
	  cd $(LINO_ROOT)/lino/modlib/$$MOD && pwd && $(DJANGO_ADMIN) makemessages $(MMOPTS); \
	done
	for i in $(APPS); do \
    cd $(LINO_ROOT)/lino/apps/$$i && pwd && $(DJANGO_ADMIN) makemessages $(MMOPTS); \
	done
  

cm:  
	cd $(LINO_ROOT)/lino && $(DJANGO_ADMIN) compilemessages $(CMOPTS)
	@for MOD in $(MODULES); \
	do \
	  cd $(LINO_ROOT)/lino/modlib/$$MOD && $(DJANGO_ADMIN) compilemessages $(CMOPTS); \
	done
	for i in $(APPS); do \
	  cd $(LINO_ROOT)/lino/apps/$$i && $(DJANGO_ADMIN) compilemessages $(CMOPTS); \
	done
  
tests:  
	python lino/utils/__init__.py
	#~ python lino/utils/sphinx.py
	python lino/utils/rstgen.py
	python lino/utils/appy_pod.py
	python lino/utils/ssin.py
	python lino/utils/memo.py
	python lino/modlib/contacts/utils.py
	python lino/utils/html2xhtml.py
	python lino/utils/demonames.py
	python lino/utils/odsreader.py
	export DJANGO_SETTINGS_MODULE=lino.apps.std.settings ; python lino/core/choicelists.py
	export DJANGO_SETTINGS_MODULE=lino.apps.std.settings ; python lino/utils/jsgen.py
	export DJANGO_SETTINGS_MODULE=lino.apps.std.settings ; python lino/utils/ranges.py
	export DJANGO_SETTINGS_MODULE=lino.apps.std.settings ; python lino/modlib/ledger/utils.py
	export DJANGO_SETTINGS_MODULE=lino.apps.std.settings ; python lino/modlib/accounts/utils.py
	$(DJANGO_ADMIN) test --settings=lino.test_apps.1.settings  $(TESTS_OPTIONS)
	$(DJANGO_ADMIN) test --settings=lino.test_apps.20100212.settings $(TESTS_OPTIONS)
	$(DJANGO_ADMIN) test --settings=lino.test_apps.20100519.settings $(TESTS_OPTIONS)
	$(DJANGO_ADMIN) test --settings=lino.test_apps.quantityfield.settings $(TESTS_OPTIONS)
	$(DJANGO_ADMIN) test --settings=lino.test_apps.human.settings $(TESTS_OPTIONS)
	#~ $(DJANGO_ADMIN) test --settings=lino.apps.std.settings
	#~ $(DJANGO_ADMIN) test --settings=lino.apps.pcsw.settings $(TESTS_OPTIONS)
	#~ $(DJANGO_ADMIN) test --settings=lino.apps.igen.settings $(TESTS_OPTIONS)
	$(DJANGO_ADMIN) test --settings=lino.apps.presto.settings $(TESTS_OPTIONS)

tt:  
	export DJANGO_SETTINGS_MODULE=lino.apps.std.settings ; python lino/modlib/accounts/utils.py
	export DJANGO_SETTINGS_MODULE=lino.apps.std.settings ; python lino/core/choicelists.py

unused_appdocs:
	$(DJANGO_ADMIN) makedocs --settings lino.apps.pcsw.settings docs/pcsw/appdocs
	$(DJANGO_ADMIN) makedocs --settings lino.apps.igen.settings docs/igen/appdocs

sdist:
	python setup.py register sdist --formats=gztar,zip upload 
	#~ python setup.py register sdist --formats=gztar,zip --dist-dir=docs/dist upload 
	#~ python setup.py sdist --formats=gztar,zip --dist-dir=docs/dist
  
