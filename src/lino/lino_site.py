## Copyright 2009 Luc Saffre
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
  the account/ views are initially copied from django.contrib.auth.views with the 
  following changes:
    - implemented as methods of LinoSite
    - context has the Lino Standard Context variables (title, main_menu
    - Moved email sending code from PasswordResetForm.save() to Linosite.password_reset()
  
"""


import os
import sys
import imp

from django.conf import settings

#from timtools.tools.my_import import my_import as import_module
#from django.contrib.admin.sites import AdminSite
from django import template 
from django.views.decorators.cache import never_cache 
from django.db import models
#from django.shortcuts import render_to_response 
#from django.contrib.auth.models import User


from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.template import RequestContext, Context, loader
from django.utils.http import urlquote, base36_to_int
from django.utils.translation import ugettext as _

from django.conf.urls.defaults import patterns, url, include
#auth = models.get_app('auth')
from django.contrib.auth import models as auth

from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import int_to_base36

from django.utils.safestring import mark_safe


from django.db.models import loading
#~ def db_apps():
    #~ return [a.__name__.split('.')[-2] for a in loading.get_apps()]

import lino
from lino import reports
from lino import layouts
from lino import actions
from lino.utils import perms
from lino.utils import menus
#from . import layouts

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"), max_length=75)

    def clean_email(self):
        """
        Validates that a user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]
        self.users_cache = auth.User.objects.filter(email__iexact=email)
        if len(self.users_cache) == 0:
            raise forms.ValidationError(
              _("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        return email



class LinoSite:
    help_url = "http://code.google.com/p/lino"
    index_html = "This is the main page."
    title = "Unnamed LinoSite"
    domain = "www.example.com"
    
  
    def __init__(self):
        
        #self.django_settings = settings
        
        self._menu = menus.Menu("","Main Menu")
        self._setting_up = False
        self._setup_done = False
        self.root_path = '/lino/'
        self._response = None

        for name,url,version in self.thanks_to():
            lino.log.info("%s %s <%s>",name,version,url)
        self.app_labels = [a.__name__.split('.')[-2] for a in loading.get_apps()]
        lino.log.info("%d applications: %s.", len(self.app_labels),", ".join(self.app_labels))
        
        
        
    def versions(self):
        def HREF(name,url,version):
            return mark_safe('<a href="%s">%s</a> %s' % (url,name,version))
        for name,url,version in self.thanks_to():
            yield HREF(name,url,version)
            
          
    def thanks_to(self):
        import lino
        version = lino.__version__
        from django.utils.version import get_svn_revision
        svn_rev = get_svn_revision(os.path.dirname(__file__))
        if svn_rev != u'SVN-unknown':
            version += " " + svn_rev
        yield ("Lino",
               "http://lino.saffre-rumma.ee",
               version)
        
        import django
        yield ("Django",
               "http://www.djangoproject.com",
               django.get_version())
        
        import reportlab
        yield ("ReportLab Toolkit",
               "http://www.reportlab.org/rl_toolkit.html",
               reportlab.Version)
                   
        import yaml
        version = getattr(yaml,'__version__','')
        yield ("PyYaml","http://pyyaml.org/",version)
        
        import dateutil
        version = getattr(dateutil,'__version__','')
        yield ("python-dateutil","http://labix.org/python-dateutil",version)
        
        import sys
        version = "%d.%d.%d" % sys.version_info[:3]
        yield ("Python","http://www.python.org/",version)
        
        try:
            # l:\snapshot\xhtml2pdf
            import ho.pisa as pisa
            version = getattr(pisa,'__version__','')
            yield ("xhtml2pdf","http://www.xhtml2pdf.com//",version)
        except ImportError:
            pisa = None
        

    def setup(self):
        if self._setup_done:
            return
        if self._setting_up:
            raise Exception("LinoSite.setup() called recursively.")
        self._setting_up = True
        
        #~ for app_name in self.django_settings.INSTALLED_APPS:
            #~ if loading.module_exists(app_name + ".reports"):
                #~ import_module('.reports', app_name)
        
        lino.log.info("Setting up Lino reports...")
        #from lino import reports
        reports.setup()
        layouts.setup()
        actions.setup()
        
        from lino.ui import extjs
        self.ui = extjs.ui
        
        if hasattr(settings,'LINO_SETTINGS'):
            lino.log.info("Reading %s...", settings.LINO_SETTINGS)
            execfile(settings.LINO_SETTINGS,dict(lino=self))
        else:
            lino.log.warning("settings.LINO_SETTINGS entry is missing")
            
        self.ui.setup_site(self)
          
        lino.log.info("LinoSite %r is ready.", self.title)
          
        self._setup_done = True
        self._setting_up = False
        
        
        
    def add_menu(self,*args,**kw):
        return self._menu.add_menu(*args,**kw)
       
    #~ def sort_menu_items(self,*args,**kw):
        #~ return self._menu.sort_items(*args,**kw)


    def context(self,request,**kw):
        d = dict(
          main_menu = menus.MenuRenderer(self._menu,request),
          root_path = self.root_path,
          lino = self,
          settings = settings,
          debug = True,
          #skin = self.skin,
          request = request
        )
        d.update(kw)
        return d
        
        
    def old_index(self, request):
        context = self.context(request,title=self._menu.label)
        return render_to_response(self.index_template, context,
            context_instance=template.RequestContext(request)
        )
    
    def login(self,request, template_name='registration/login.html', 
              redirect_field_name=REDIRECT_FIELD_NAME):
        "Displays the login form and handles the login action."
        redirect_to = request.REQUEST.get(redirect_field_name, '')
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                # Light security check -- make sure redirect_to isn't garbage.
                if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                    redirect_to = settings.LOGIN_REDIRECT_URL
                from django.contrib.auth import login
                login(request, form.get_user())
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                return HttpResponseRedirect(redirect_to)
            print "not valid"
        else:
            form = AuthenticationForm(request)
        request.session.set_test_cookie()
        if Site._meta.installed:
            current_site = Site.objects.get_current()
        else:
            current_site = RequestSite(request)
        context = self.context(request,
            title = _('Login'),
            form = form,
            redirect_field_name = redirect_to,
            site = current_site,
            site_name = current_site.name,
        )
        return render_to_response(template_name, context, 
            context_instance=RequestContext(request))
    login = never_cache(login)


    
    def logout(self,request, next_page=None, 
              template_name='registration/logged_out.html', 
              redirect_field_name=REDIRECT_FIELD_NAME):
        "Logs out the user and displays 'You are logged out' message."
        from django.contrib.auth import logout
        logout(request)
        if next_page is None:
            redirect_to = request.REQUEST.get(redirect_field_name, '')
            if redirect_to:
                return HttpResponseRedirect(redirect_to)
            else:
                context = self.context(request,
                    title=_('Logged out')
                )
                return render_to_response(template_name, context, 
                  context_instance=RequestContext(request))
        else:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page or request.path)
            
            
    def password_reset(self,request, is_admin_site=False, 
                      template_name='registration/password_reset_form.html',
                      email_template_name='registration/password_reset_email.html',
                      token_generator=default_token_generator,
                      post_reset_redirect=None):
        if post_reset_redirect is None:
            post_reset_redirect = reverse(self.password_reset_done)
        if request.method == "POST":
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                domain_override = None
                use_https = request.is_secure()
                if is_admin_site:
                    domain_override = request.META['HTTP_HOST']
                else:
                    if not Site._meta.installed:
                        domain_override = RequestSite(request).domain
                # this was previously in form.save(**opts)
                for user in form.users_cache:
                    if not domain_override:
                        current_site = Site.objects.get_current()
                        site_name = current_site.name
                        domain = current_site.domain
                    else:
                        site_name = domain = domain_override
                    t = loader.get_template(email_template_name)
                    token = token_generator.make_token(user)
                    uid = int_to_base36(user.id)
                    c = {
                        'email': user.email,
                        'domain': domain,
                        'site_name': site_name,
                        'uid': uid,
                        'user': user,
                        'token': token,
                        'protocol': use_https and 'https' or 'http',
                        'confirm_path': reverse(
                          self.password_reset_confirm,
                          kwargs=dict(uidb36=uid,token=token)),
                    }
                    #sender = settings.ADMINS[0][1]
                    send_mail(
                      _("Password reset on %s") % site_name,
                      t.render(Context(c)), None, [user.email])
                
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = PasswordResetForm()
        context = self.context(request,
            form=form,
            title=_("Password reset"),
        )
        return render_to_response(template_name, context, 
          context_instance=RequestContext(request))

    def password_reset_done(self,request, template_name='registration/password_reset_done.html'):
        context = self.context(request,
            title="password_reset_done()"
        )
        return render_to_response(template_name,context,context_instance=RequestContext(request))

    def password_reset_confirm(self,request, uidb36=None, token=None, 
                               template_name='registration/password_reset_confirm.html',
                               token_generator=default_token_generator, 
                               set_password_form=SetPasswordForm,
                               post_reset_redirect=None):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        assert uidb36 is not None and token is not None # checked by URLconf
        if post_reset_redirect is None:
            post_reset_redirect = reverse(self.password_reset_complete)
        try:
            uid_int = base36_to_int(uidb36)
        except ValueError:
            raise Http404

        user = get_object_or_404(auth.User, id=uid_int)
        context_instance = RequestContext(request)

        if token_generator.check_token(user, token):
            context_instance['validlink'] = True
            if request.method == 'POST':
                form = set_password_form(user, request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(post_reset_redirect)
            else:
                form = set_password_form(None)
        else:
            context_instance['validlink'] = False
            form = None
        context = self.context(request,
            title=_('Password reset'),
            form = form,
        )
        return render_to_response(template_name,context,context_instance=context_instance)

    def password_reset_complete(self,request, 
                    template_name='registration/password_reset_complete.html'):
        context = self.context(request,
            title=_('Password reset complete')
        )
        return render_to_response(template_name, context,
          context_instance=RequestContext(request,{'login_url': settings.LOGIN_URL}))

    def password_change(self,request, 
                        template_name='registration/password_change_form.html',
                        post_change_redirect=None):
        if post_change_redirect is None:
            post_change_redirect = reverse(self.password_change_done)
        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_change_redirect)
        else:
            form = PasswordChangeForm(request.user)
        context = self.context(request,
            title="password_change()",
            form=form,
        )
        return render_to_response(template_name, context, 
          context_instance=RequestContext(request))
    password_change = login_required(password_change)

    def password_change_done(self,request, 
                             template_name='registration/password_change_done.html'):
        context = self.context(request,
            title=_('Password change successful'),
        )
        return render_to_response(template_name, context,context_instance=RequestContext(request))
            
    def get_urls(self):
        self.setup()
        #~ for k,v in self.model_reports.items():
            #~ print k,v
        
        urlpatterns = patterns('',
            (r'^accounts/login/$', self.login),
            (r'^accounts/logout/$', self.logout),
            (r'^accounts/password_change/$', self.password_change),
            (r'^accounts/password_change/done/$', self.password_change_done),
            (r'^accounts/password_reset/$', self.password_reset),
            (r'^accounts/password_reset/done/$', self.password_reset_done),
            (r'^accounts/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
              self.password_reset_confirm),
            (r'^accounts/reset/done/$', self.password_reset_complete),
        )
        #~ urlpatterns = AdminSite.get_urls(self)
        #~ from lino.utils import urls
        #~ urlpatterns += urls.get_urls()
        
        urlpatterns += self.ui.get_urls()
        
        #urlpatterns += urls.url_patterns
        #urlpatterns += self._menu.get_urls() # self._menu.name)
        return urlpatterns
        #return self._menu.get_urls()
        
    def add_program_menu(self):
        return
        m = self.add_menu("app","~Application",)
        #~ m.add_item(url="/accounts/login/",label="Login",can_view=perms.is_anonymous)
        #~ m.add_item(url="/accounts/logout/",label="Logout",can_view=perms.is_authenticated)
        #m.add_item(system.Login(),can_view=perms.is_anonymous)
        #m.add_item(system.Logout(),can_view=perms.is_authenticated)
        
    def get_menu(self,request):
        self.setup()
        return menus.menu_request(self._menu,request)
        
      
    def fill(self):
      
        from django.core.management import call_command
        from timtools.console import syscon
        #from lino import reports
        
        sites = reports.get_app('sites')
        
        options = dict(interactive=False)
        if not syscon.confirm("Gonna reset database %s. Are you sure?" 
            % settings.DATABASE_NAME):
            return
        lino.log.warning("lino_site.fill() %s", (" ".join(self.app_labels)))
        lino.log.info("reset")
        if False: # settings.DATABASE_ENGINE == 'sqlite3':
            if settings.DATABASE_NAME != ':memory:':
                if os.path.exists(settings.DATABASE_NAME):
                    os.remove(settings.DATABASE_NAME)
        else:
            call_command('reset',*self.app_labels,**options)
        #call_command('reset','songs','auth',interactive=False)
        lino.log.info("syncdb")
        call_command('syncdb',**options)
        #call_command('flush',interactive=False)
        lino.log.info("loaddata demo")
        call_command('loaddata','demo')
        auth.User.objects.create_superuser('root','luc.saffre@gmx.net','1234')
        auth.User.objects.create_user('user','luc.saffre@gmx.net','1234')
        sites.Site(id=2,domain=self.domain,name=self.title).save()
        #self.setup()
        
            

  
  
#~ class Skin:
    #~ body = dict(
      #~ background = "#eee",
      #~ text = "#333",
      #~ link = "#5b80b2",
    #~ )
    #~ params = dict(
      #~ background = "#5b80b2",
      #~ text = "yellow",
      #~ link = "#5b80b2",
    #~ )
    #~ grid = dict(
      #~ background = "#bbbbbb",
      #~ text = "yellow",
      #~ border = "1pt solid white",
      #~ link = "#5b80b2",
    #~ )
    

    #~ background_color = "#eee"
    #~ text_color = "#333"
    #~ link_color = "#5b80b2"
    #~ header_text_color = "#666"
    

lino_site = LinoSite()
#lino_site.setup()

#'get_urls','fill','context'

fill = lino_site.fill
context = lino_site.context
get_urls = lino_site.get_urls
get_menu = lino_site.get_menu