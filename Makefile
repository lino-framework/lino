DJANGO_ADMIN = python l:\\snapshots\\django\\django\\bin\\django-admin.py
LINO_ROOT := /cygdrive/t/hgwork/lino/lino
#~ MODULES = system
MODULES = products dsbe properties contacts countries notes sales finan links uploads igen 

#LANGUAGES = de fr nl et
#INPUT_FILES = lino\\actions.py lino\\ui\\extjs\\ext_ui.py lino\\modlib\\fields.py lino\\modlib\\system\\models.py

.PHONY: mm cm

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  mm  run django-admin makemessages on modlib"
	@echo "  cm  run django-admin compilemessages on modlib"


mm:
	cd $(LINO_ROOT) && $(DJANGO_ADMIN) makemessages -i 'modlib*' -i 'test_apps*' -s -a
	for MOD in $(MODULES); \
  do \
    cd $(LINO_ROOT)/modlib/$$MOD && $(DJANGO_ADMIN) makemessages -s -a; \
  done
  
unused:  
	for LANG in $(LANGUAGES); \
  do \
    xgettext --from-code UTF-8 -d django -p lino\\modlib\\system\\locale\\$$LANG\\LC_MESSAGES $(INPUT_FILES); \
  done



cm:  
	cd $(LINO_ROOT) && $(DJANGO_ADMIN) compilemessages 
	@for MOD in $(MODULES); \
  do \
    cd $(LINO_ROOT)/modlib/$$MOD && $(DJANGO_ADMIN) compilemessages; \
  done
  
unused2:  
	cd $(LINO_ROOT)/lino/modlib/system && $(DJANGO_ADMIN) compilemessages
        

