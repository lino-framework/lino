# -*- coding: UTF-8 -*-
import os
import os.path
import sys



def init_demo():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.apps.pcsw.settings'
    from django.conf import settings
    from django.core.management import call_command
    assert settings.DATABASES['default']['NAME'] == ':memory:'
    call_command('initdb','std','few_languages','few_countries','few_cities','demo',interactive=False)
    settings.LINO.setup()
    settings.LINO.cbss_environment = 'test'
    settings.LINO.cbss_user_params = dict(
       UserID='123456', 
       Email='info@exemple.be', 
       OrgUnit='0123456', 
       MatrixID=17, 
       MatrixSubID=1)

def run_test():
    init_demo()
    
    from lino.modlib.cbss.models import IdentifyPersonRequest
    ipr = IdentifyPersonRequest.objects.get(pk=1)
    ipr.execute_request(None)
    print ipr.response_xml
    #~ ipr = IdentifyPersonRequest(last_name="SAFFRE",birth_date=IncompleteDate('1968-06-01'))


if __name__ == '__main__':
    run_test()
    
