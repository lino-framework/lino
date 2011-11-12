DJANGO_ADMIN = python l:\\snapshots\\django\\django\\bin\\django-admin.py
LINO_ROOT := /cygdrive/t/hgwork/lino
LINO_ROOT := `cygpath -m $(LINO_ROOT)`
APPS = dsbe igen
#~ MODULES = system
MODULES = isip mails cal jobs thirds products properties contacts countries notes sales finan links uploads users
TESTS_OPTIONS = --verbosity=2 --traceback

#LANGUAGES = de fr nl et
#INPUT_FILES = lino\\actions.py lino\\ui\\extjs\\ext_ui.py lino\\modlib\\fields.py lino\\modlib\\system\\models.py

.PHONY: mm cm makedocs tests

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  mm     run django-admin makemessages on modlib"
	@echo "  cm     run django-admin compilemessages on modlib"
	@echo "  tests  run Lino test suite"
  

mm:
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
	$(DJANGO_ADMIN) test --settings=lino.test_apps.1.settings  $(TESTS_OPTIONS)
	$(DJANGO_ADMIN) test --settings=lino.test_apps.20100212.settings $(TESTS_OPTIONS)
	#~ $(DJANGO_ADMIN) test --settings=lino.apps.std.settings
	$(DJANGO_ADMIN) test --settings=lino.apps.dsbe.settings $(TESTS_OPTIONS)
	$(DJANGO_ADMIN) test --settings=lino.apps.igen.settings $(TESTS_OPTIONS)


appdocs:
	$(DJANGO_ADMIN) makedocs --settings lino.apps.dsbe.settings docs/dsbe/appdocs
	$(DJANGO_ADMIN) makedocs --settings lino.apps.igen.settings docs/igen/appdocs

