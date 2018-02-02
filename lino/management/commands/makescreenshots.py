# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Writes screenshots to <project_dir>/media/cache/screenshots
"""
# from future import standard_library
# standard_library.install_aliases()
from builtins import str

import logging
logger = logging.getLogger(__name__)

import subprocess
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
from django.utils.encoding import force_text
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.core.servers.basehttp import get_internal_wsgi_application
from django.core.servers.basehttp import WSGIRequestHandler

from django.conf import settings
#~ from django.test import LiveServerTestCase
from django.test.testcases import StoppableWSGIServer

from lino.core.utils import obj2str, full_model_name, sorted_models_list
from lino.utils import screenshots
from atelier.utils import SubProcessParent


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
    // console.log('Retry',msg,'('+String(limit),"attempts left)");
    window.setTimeout(function() { waitfor(msg,until,limit-1,todo)},1000);
};

var output = '%(target)s';
var address = '%(url)s';


// phantom.addCookie({ username: '%(username)s', password: '%(password)s'});

var data = 'username=%(username)s&password=%(password)s';
var page = require('webpage').create();
page.open('http://127.0.0.1:8000/auth','post',data,function (status) {
    // console.log('opened auth!');
    if (status !== 'success') {
        console.log('Unable to authenticate!');
        phantom.exit();
    }});

var page = require('webpage').create();
// page.settings = { userName: '%(username)s', password: '%(password)s'};
// page.customHeaders = { %(remote_user_header)s: '%(username)s'};
// page.customHeaders = { 'HTTP_%(remote_user_header)s': '%(username)s'};

page.viewportSize = { width: 1400, height: 800};
// page.viewportSize = { width: 1024, height: 768};
// page.viewportSize = { width: 1366, height: 744};
// page.viewportSize = { width: 800, height: 600};
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
        // return !Ext.Ajax.isLoading();
        // return (document.readyState == 'complete');
        if (typeof Lino != "undefined") {
            if (Lino.current_window) {
                if (!Lino.current_window.main_item.is_loading())
                    return true;
                // console.log("Lino.current_window still loading in ",document.documentElement.innerHTML);
                // console.log("Lino.current_window", Lino.current_window.main_item,"still loading." );
                // return true;
            }
        }
        // console.log("No Lino in ",document.documentElement.innerHTML);
        // console.log("No Lino in response");
        return false;
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


class Command(BaseCommand):
    help = __doc__

    option_list = BaseCommand.option_list + (
        make_option('--force', action='store_true',
                    dest='force', default=False,
                    help='Overwrite existing files.'),
    )

    def handle(self, *args, **options):

        if len(args):
            raise CommandError("Unexpected arguments %r" % args)

        # Igor Katson writes an interesting answer in
        # `Django Broken pipe in Debug mode
        # <http://stackoverflow.com/questions/7912672/django-broken-pipe-in-debug-mode>`__::
        # Monkeypatch python not to print "Broken Pipe" errors to stdout.
        import socketserver
        from wsgiref import handlers
        socketserver.BaseServer.handle_error = lambda *args, **kwargs: None
        handlers.BaseHandler.log_exception = lambda *args, **kwargs: None

        main(force=options['force'])
        #~ main()

    #~ ADDR = "http://127.0.0.1"
    ADDR = "127.0.0.1"
    PORT = 8000

    HTTPD = None

    def start_server(self):
        try:
            handler = get_internal_wsgi_application()
            self.HTTPD = StoppableWSGIServer(('', PORT), WSGIRequestHandler)
            self.HTTPD.set_app(handler)
            self.HTTPD.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)

    def stop_server(self):
        #~ server.terminate()
        self.HTTPD.shutdown()
        self.HTTPD.server_close()
        logger.info("terminated server.")

    def main(self, force=False, **kw):
        settings.SITE.startup()

        outputbase = os.path.join(settings.MEDIA_ROOT, 'cache', 'screenshots')

        urlbase = "http://" + ADDR + ":" + str(PORT)
        #~ urlbase="http://127.0.0.1:8000"
        pp = SubProcessParent()
        server = Process(target=self.start_server)
        server.start()
        #~ server.join()
        logger.info("started the server")

        count = 0
        assert not settings.SITE.remote_user_header
        try:
            for lng in settings.SITE.languages:
                if lng.django_code == 'de':  # temporary
                    for ss in screenshots.get_screenshots(lng.django_code):
                    #~ print "20130515 got screenshot", ss
                        target = ss.get_filename(outputbase)
                        if not force and os.path.exists(target):
                            logger.info("%s exists", target)
                            continue
                        for fn in (target, target + '.log'):
                            if os.path.exists(fn):
                                os.remove(fn)
                        url = ss.get_url(urlbase)
                        if url is None:
                            logger.info("No url for %s", target)
                            continue
                        logger.info("Build %s...", target)
                        ctx = dict(
                            url=url,
                            target=target,
                            username=ss.ar.get_user().username)
                        ctx.update(password='1234')
                        ctx.update(
                            remote_user_header=settings.SITE.remote_user_header)
                        f = file('tmp.js', 'wt')
                        f.write(JS_SRC % ctx)
                        f.close()
                        args = [PHANTOMJS]
                        args += ['--cookies-file=phantomjs_cookies.txt']
                        args += ['--disk-cache=true']
                        args += ['tmp.js']

                        try:
                            output = pp.check_output(args, **kw)
                        except subprocess.CalledProcessError as e:
                            output = e.output
                            file(target + '.log', 'wt').write(output)
                        count += 1

                        #~ p = pp.open_subprocess(args,**kw)
                        #~ p.wait()
                        #~ rc = p.returncode
                        #~ if rc != 0:
                            #~ raise Exception("`%s` returned %s" % (" ".join(args),rc))
                        if not os.path.exists(target):
                            raise Exception("File %s has not been created." %
                                            target)
            logger.info("Built %d screenshots.", count)
        except Exception as e:
            import traceback
            traceback.print_exc()
            #~ print e
            self.stop_server()
            raise
        finally:
            self.stop_server()
