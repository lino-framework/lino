DJANGO_ADMIN = python l:\\snapshots\\django\\django\\bin\\django-admin.py
LINO_ROOT := /cygdrive/t/hgwork/lino
LINO_ROOT := `cygpath -m $(LINO_ROOT)`
APPS = dsbe igen
#~ MODULES = system
MODULES = thirds products properties contacts countries notes sales finan links uploads

#LANGUAGES = de fr nl et
#INPUT_FILES = lino\\actions.py lino\\ui\\extjs\\ext_ui.py lino\\modlib\\fields.py lino\\modlib\\system\\models.py

.PHONY: mm cm makedocs

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  mm  run django-admin makemessages on modlib"
	@echo "  cm  run django-admin compilemessages on modlib"


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
  
