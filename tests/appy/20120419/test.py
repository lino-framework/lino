# -*- coding: UTF-8 -*-
import os
import os.path
import sys

#~ from appy.pod.renderer import Renderer
from lino.utils.appy_pod import Renderer
#~ from appy.pod.pod_parser import OdInsert



APPY_PARAMS = dict()

#~ APPY_PARAMS.update(ooPort=8100)
#~ APPY_PARAMS.update(pythonWithUnoPath=r'C:\PROGRA~1\LIBREO~1\program\python.exe')

def init_demo():
    #~ os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.apps.pcsw.settings'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.apps.pim.settings'
    #~ os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.tutorials.t3a.settings'
    from django.conf import settings
    from django.core.management import call_command
    assert settings.DATABASES['default']['NAME'] == ':memory:'
    #~ call_command('initdb','std','few_countries','be',interactive=False)
    call_command('initdb','std','few_countries','few_cities','demo',interactive=False)
    settings.LINO.setup()

def demo_table():
    from django.conf import settings
    from lino.ui.extjs3 import urls
    return settings.LINO.modules.countries.Cities.request(ui=urls.ui)

def run_test():
    tpl = os.path.join(os.path.abspath(os.path.dirname(__file__)),'test_template.odt')
    target = 'test_result.odt'
    if os.path.exists(target): 
        os.remove(target)
        
    init_demo()
    
    context = dict()
    context.update(demo_table=demo_table)
    
        
    #~ ti = TableInserter()
    #~ APPY_PARAMS.update(finalizeFunction=ti.finalize)
    #~ context.update(insert_table=ti.insert_table)
    renderer = Renderer(tpl,context,target,**APPY_PARAMS)
    #~ ti.renderer = renderer
    
    # add a reference to the renderer under the name `appy_renderer`
    #~ renderer.contentParser.env.context.update(appy_renderer=renderer)
    
    renderer.run()
    print "Generated file", target
    os.startfile(target)    


if __name__ == '__main__':
    run_test()
    