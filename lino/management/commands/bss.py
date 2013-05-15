# -*- coding: UTF-8 -*-
## Copyright 2012-2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
Writes a diagnostic status report about the data on this Site. 
Used to get a quick overview on the differences in two databases. 
"""

import logging
logger = logging.getLogger(__name__)

import os
import errno
#~ import codecs
import sys
from optparse import make_option 
from os.path import join


from multiprocessing import Process

from django.db import models
from django.utils.translation import ugettext as _
from django.utils import translation
from django.utils.encoding import force_unicode
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.core.servers.basehttp import WSGIServerException, get_internal_wsgi_application
from django.core.servers.basehttp import WSGIRequestHandler

from django.conf import settings
#~ from django.test import LiveServerTestCase
from django.test.testcases import StoppableWSGIServer

from lino.core.dbutils import obj2str, full_model_name, sorted_models_list, app_labels
from lino.utils import screenshots
from atelier.utils import SubProcessParent


from lino.utils.screenshots import register_screenshot
register_screenshot('index','');
register_screenshot('cal.CalendarPanel','/api/cal/CalendarPanel',username='alicia');
#~ register_screenshot('/api/cal/CalendarPanel?su=8&ul='+LANGUAGE,'cal.CalendarPanel-su.png');
#~ //~ register_screenshot('/api/cal/PanelEvents/266?an=detail&ul='+LANGUAGE,'cal.Event.detail.png');
#~ register_screenshot('/api/cal/PanelEvents/105?an=detail&ul='+LANGUAGE,'cal.Event.detail.png');
#~ 
#~ register_screenshot('/api/pcsw/Clients?ul='+LANGUAGE,'pcsw.Clients.grid.png');
#~ register_screenshot('/api/pcsw/Clients/122?ul='+LANGUAGE,'pcsw.Client.detail.png');
#~ register_screenshot('/api/pcsw/Clients/122?tab=1&ul='+LANGUAGE,'pcsw.Client.detail.1.png');
#~ register_screenshot('/api/pcsw/Clients/122?tab=2&ul='+LANGUAGE,'pcsw.Client.detail.2.png');
#~ 
#~ register_screenshot('/api/debts/Budgets/2?ul='+LANGUAGE,'debts.Budget.detail.png');
#~ register_screenshot('/api/debts/Budgets/2?tab=1&ul='+LANGUAGE,'debts.Budget.detail.1.png');
#~ register_screenshot('/api/debts/Budgets/2?tab=2&ul='+LANGUAGE,'debts.Budget.detail.2.png');
#~ register_screenshot('/api/debts/Budgets/2?tab=3&ul='+LANGUAGE,'debts.Budget.detail.3.png');
#~ register_screenshot('/api/debts/Budgets/2?tab=4&ul='+LANGUAGE,'debts.Budget.detail.4.png');
#~ register_screenshot('/api/jobs/JobsOverview?ul='+LANGUAGE,'jobs.JobsOverview.png');
#~ 
#~ 




PHANTOMJS = '/home/luc/snapshots/phantomjs-1.9.0-linux-i686/bin/phantomjs'

JS_SRC = """

function waitfor(msg,until,limit,todo) {
    if (until()) {
      console.log("Done",msg);
      todo(true);
      return;
    };
    if (limit <= 0) {
      console.log("Giving up",msg);
      todo(false);
      //~ task_done(msg,false);
      return;
    };
    console.log('Retry',msg,'('+String(limit),"attempts left)");
    window.setTimeout(function() { waitfor(msg,until,limit-1,todo)},1000);
};

var output = '%(target)s';
var address = '%(url)s';


// phantom.addCookie({ username: '%(username)s', password: '%(password)s'});

var data = 'username=%(username)s&password=%(password)s';
var page = require('webpage').create();
page.open('http://127.0.0.1:8000/auth','post',data,function (status) {
    console.log('opened auth!');
    if (status !== 'success') {
        console.log('Unable to authenticate!');
        phantom.exit();
    }});

var page = require('webpage').create();
// page.settings = { userName: '%(username)s', password: '%(password)s'};
// page.customHeaders = { %(remote_user_header)s: '%(username)s'};
// page.customHeaders = { 'HTTP_%(remote_user_header)s': '%(username)s'};

page.viewportSize = { width: 1024, height: 768};
page.onConsoleMessage = function (msg) { console.log(msg); };
page.onError = function (msg, trace) {
    console.log(msg);
    trace.forEach(function(item) {
        console.log('  ', item.file, ':', item.line);
    })
}

var is_loaded = function() { 
  return page.evaluate(function() { 
      // console.log('evaluate()');
        //~ return !Ext.Ajax.isLoading();
        if (typeof Lino != "undefined") {
            if (Lino.current_window) {
                if (Lino.current_window.main_item.is_loading()) 
                    return false;
                // console.log("Lino.current_window still loading in ",document.documentElement.innerHTML);
                console.log("Lino.current_window", Lino.current_window.main_item,"still loading." );
                return true;
            }
        }
        // console.log("No Lino in ",document.documentElement.innerHTML);
        console.log("No Lino in response");
    }
  );
};

var todo = function(ok) { 
    console.log("Rendering to",output,ok);
    page.render(output);
    if (ok) 
        phantom.exit();
    else
        phantom.exit(2);
};

var on_opened = function(status) { 
    if (status !== 'success') {
        console.log('Unable to load ',address,'status is:',status);
        phantom.exit(1);
    } else {
        waitfor(output,is_loaded,6,todo);
    }
};

console.log("Loading",address,'to',output);

page.open(address,on_opened);


"""


#~ ADDR = "http://127.0.0.1"
ADDR = "127.0.0.1"
PORT = 8000
HTTPD = StoppableWSGIServer(('', PORT), WSGIRequestHandler)

def start_server():
    try:
        handler = get_internal_wsgi_application()
        HTTPD.set_app(handler)
        HTTPD.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)

    
def start_server2(): # 
    pp = SubProcessParent()
    args = ['django-admin.py']
    args += ['runserver']
    args += ['--settings', settings.SETTINGS_MODULE]
    p = pp.open_subprocess(args)
    p.wait()
    


def build_screenshots(outputbase,force=False,**kw):
    urlbase = "http://" + ADDR + ":" + str(PORT)
    #~ urlbase="http://127.0.0.1:8000"
    pp = SubProcessParent()
    server = Process(target=start_server)
    server.start()
    #~ server.join()
    logger.info("started the server")
    
    count = 0
    assert not settings.SITE.remote_user_header
    try:
        for lng in settings.SITE.languages:
            for ss in screenshots.SCREENSHOTS.values():
                target = ss.get_filename(outputbase,lng.django_code)
                if not force and os.path.exists(target):
                    logger.info("%s exists",target)
                    continue
                logger.info("Build %s...",target)
                ctx = dict(url=ss.get_url(urlbase,lng.django_code),target=target,username=ss.username)
                ctx.update(password='1234')
                ctx.update(remote_user_header=settings.SITE.remote_user_header)
                f = file('tmp.js','wt')
                f.write(JS_SRC % ctx)
                f.close()
                args = [PHANTOMJS]
                args += ['--cookies-file=phantomjs_cookies.txt']
                args += ['tmp.js']
                
                p = pp.open_subprocess(args,**kw)
                p.wait()
                rc = p.returncode
                print rc
                count += 1
                if rc != 0:
                    raise Exception("`%s` returned %s" % (" ".join(args),rc))
                if not os.path.exists(target):
                    raise Exception("File %s has not been created" % target)
    finally:
        logger.info("Built %d screenshots.",count)
        #~ server.terminate()
        HTTPD.shutdown()
        HTTPD.server_close()
        logger.info("terminated server.")

    




class Command(BaseCommand):
    help = __doc__
    args = "output_dir"
    
    
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Required argument: output_dir")
            
        output_dir = args[0]
            
        #~ print settings.SITE.__class__
        settings.SITE.startup()
        #~ translation.activate(settings.LANGUAGE_CODE)
        
        build_screenshots(output_dir,force=True)
        
