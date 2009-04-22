# initally copied from django.contrib.admin
# see also comments and docstring of original module


#~ LOADING = False

#~ def autodiscover():
    #~ global LOADING
    #~ if LOADING:
        #~ return
    #~ LOADING = True

    #~ import imp
    #~ from lino.tools.my_import import my_import
    #~ from django.conf import settings
    

    #~ for app in settings.INSTALLED_APPS:
        #~ mod = my_import(app)
        #~ try:
            #~ app_path = mod.__path__
        #~ except AttributeError:
            #~ continue

        #~ try:
            #~ imp.find_module('lino_setup', app_path)
        #~ except ImportError:
            #~ continue
        #~ mod = my_import("%s.lino_setup" % app)
    #~ LOADING = False

