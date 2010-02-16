## Copyright 2009-2010 Luc Saffre
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

import os
import cgi
#import traceback
import cPickle as pickle
from urllib import urlencode

from django.db import models
from django.conf import settings
from django.http import HttpResponse
from django.core import exceptions

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import lino
from lino import actions, layouts
from lino.ui import base
from lino.utils import actors
from lino.utils import menus
from lino.utils.jsgen import py2js, js_code, id2js
from lino.ui.extjs import ext_elems, ext_requests, ext_store
from lino.modlib.properties.models import Property

from django.conf.urls.defaults import patterns, url, include



def build_url(*args,**kw):
    url = "/".join(args)  
    if len(kw):
        url += "?" + urlencode(kw)
    return url
        


class SaveWindowConfig(actions.Command):
    def run(self,context,name):
        h = int(context.request.POST.get('h'))
        w = int(context.request.POST.get('w'))
        maximized = context.request.POST.get('max')
        if maximized == 'true':
            maximized = True
        else:
            maximized = False
        x = int(context.request.POST.get('x'))
        y = int(context.request.POST.get('y'))
        context.confirm("Save %r window config (%r,%r,%r,%r,%r)\nAre you sure?" % (name,x,y,h,w,maximized))
        #context.confirm("%r,%r,%r,%r : Are you sure?!" % (name,h,w,maximized))
        ui.window_configs[name] = (x,y,w,h,maximized)
        #ui.window_configs[name] = (w,h,maximized)
        ui.save_window_configs()


def permalink_do_view(request,name=None):
    name = name.replace('_','.')
    actor = actors.get_actor(name)
    context = ext_requests.ActionContext(request,ui,actor,None)
    context.run()
    return json_response(context.response)

def save_win_view(request,name=None):
    #print 'save_win_view()',name
    actor = SaveWindowConfig()
    context = ext_requests.ActionContext(request,ui,actor,None,name)
    context.run()
    return json_response(context.response)





"""
def menu2js(ui,v,**kw):    
    if isinstance(v,menus.Menu):
        if v.parent is None:
            return menu2js(ui,v.items,**kw)
            #kw.update(region='north',height=27,items=v.items)
            #return py2js(kw)
        kw.update(text=v.label,menu=dict(items=v.items))
        return menu2js(ui,kw)
        
    if isinstance(v,menus.MenuItem):
        url = ui.get_action_url(v.actor)
        handler = "function(btn,evt){Lino.do_action(undefined,%r,%r,{})}" % (url,id2js(v.actor.actor_id))
        return py2js(dict(text=v.label,handler=js_code(handler)))
        #~ if v.args:
            #~ handler = "function(btn,evt) {%s.show(btn,evt,%s);}" % (
                #~ id2js(v.actor.actor_id),
                #~ ",".join([py2js(a) for a in v.args]))
        #~ else:
            #~ handler = "function(btn,evt) {%s.show(btn,evt);}" % id2js(v.actor.actor_id)
        #~ return py2js(dict(text=v.label,handler=js_code(handler)))
        
    return py2js(v,**kw)        
"""  

def menu_view(request):
    from lino import lino_site
    s = py2js(lino_site.get_menu(request))
    return HttpResponse(s, mimetype='text/html')


def act_view(request,app_label=None,actor=None,action=None,**kw):
    actor = actors.get_actor2(app_label,actor)
    #action = actor.get_action(action)
    context = ext_requests.ActionContext(request,ui,actor,action)
    context.run()
    return json_response(context.response)

def props_view(request,app_label=None,model_name=None,**kw):
    model = resolve_model(app_label+'.'+model_name)
    raise NotImplementedError
    

def choices_view(request,app_label=None,rptname=None,fldname=None,**kw):
    rpt = actors.get_actor2(app_label,rptname)
    kw['choices_for_field'] = fldname
    return json_report_view_(request,rpt,**kw)
    
    
def grid_afteredit_view(request,**kw):
    kw['colname'] = request.POST['grid_afteredit_colname']
    kw['submit'] = True
    return json_report_view(request,**kw)

def form_submit_view(request,**kw):
    kw['submit'] = True
    return json_report_view(request,**kw)

def list_report_view(request,**kw):
    #kw['simple_list'] = True
    return json_report_view(request,**kw)
    
def csv_report_view(request,**kw):
    kw['csv'] = True
    return json_report_view(request,**kw)
    
    
def json_report_view(request,app_label=None,rptname=None,**kw):
    rpt = actors.get_actor2(app_label,rptname)
    return json_report_view_(request,rpt,**kw)

def json_report_view_(request,rpt,grid_action=None,colname=None,submit=None,choices_for_field=None,csv=False):
    if not rpt.can_view.passes(request):
        return json_response_kw(success=False,
            msg="User %s cannot view %s." % (request.user,rpt))
    if grid_action:
        #~ a = rpt.get_action(grid_action)
        #~ if a is None:
            #~ return json_response_kw(
                #~ success=False,
                #~ msg="Report %s has no action %r" % (rpt,grid_action))
        context = ext_requests.GridActionContext(request,ui,rpt,grid_action)
        context.run()
        #d = a.get_response(rptreq)
        return json_response(context.response)
            
    rh = rpt.get_handle(ui)
    if choices_for_field:
        rptreq = ext_requests.ChoicesReportRequest(request,rh,choices_for_field)
    elif csv:
        rptreq = ext_requests.CSVReportRequest(request,rh,choices_for_field)
        return rptreq.render_to_csv()
    else:
        rptreq = ext_requests.ViewReportRequest(request,rh)
        if submit:
            pk = request.POST.get(rh.store.pk.name) #,None)
            #~ if pk == reports.UNDEFINED:
                #~ pk = None
            try:
                data = rh.store.get_from_form(request.POST)
                if pk in ('', None):
                    #return json_response(success=False,msg="No primary key was specified")
                    instance = rptreq.create_instance(**data)
                    instance.save(force_insert=True)
                else:
                    instance = rpt.model.objects.get(pk=pk)
                    for k,v in data.items():
                        setattr(instance,k,v)
                    instance.save(force_update=True)
                return json_response_kw(success=True,
                      msg="%s has been saved" % instance)
            except Exception,e:
                lino.log.exception(e)
                #traceback.format_exc(e)
                return json_response_kw(success=False,msg="Exception occured: "+cgi.escape(str(e)))
        # otherwise it's a simple list:
    d = rptreq.render_to_json()
    return json_response(d)
    
def json_response_kw(**kw):
    return json_response(kw)
    
def json_response(x):
    #s = simplejson.dumps(kw,default=unicode)
    #return HttpResponse(s, mimetype='text/html')
    s = py2js(x)
    #lino.log.debug("json_response() -> %r", s)
    return HttpResponse(s, mimetype='text/html')




class Viewport:
  
    def __init__(self,title,*components):
        self.title = title
        #self.main_menu = main_menu
        
        #self.variables = []
        self.components = components
        #self.visibles = []
        #~ for c in components:
            #~ for v in c.ext_variables():
                #~ self.variables.append(v)
            #~ self.components.append(c)
            
        #~ self.variables.sort(lambda a,b:cmp(a.declaration_order,b.declaration_order))
        
        
    def render_to_html(self,request):
        s = """<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title id="title">%s</title>""" % self.title
        s += """
<!-- ** CSS ** -->
<!-- base library -->
<link rel="stylesheet" type="text/css" href="%sresources/css/ext-all.css" />""" % settings.EXTJS_URL
        s += """
<!-- overrides to base library -->
<!-- ** Javascript ** -->
<!-- ExtJS library: base/adapter -->
<script type="text/javascript" src="%sadapter/ext/ext-base.js"></script>""" % settings.EXTJS_URL
        widget_library = 'ext-all-debug'
        #widget_library = 'ext-all'
        s += """
<!-- ExtJS library: all widgets -->
<script type="text/javascript" src="%s%s.js"></script>""" % (settings.EXTJS_URL,widget_library)
        if True:
            s += """
<style type="text/css">
/* http://stackoverflow.com/questions/2106104/word-wrap-grid-cells-in-ext-js  */
.x-grid3-cell-inner, .x-grid3-hd-inner {
  white-space: normal; /* changed from nowrap */
}
</style>"""
        if True:
            s += """
<script type="text/javascript" src="%s/Exporter-all.js"></script>""" % settings.EXTJS_URL

        if False:
            s += """
<!-- overrides to library -->
<link rel="stylesheet" type="text/css" href="/media/lino.css">
<script type="text/javascript" src="/media/lino.js"></script>"""
        s += """
<!-- page specific -->
<script type="text/javascript">
Ext.namespace('Lino');
Lino.on_store_exception = function (store,type,action,options,reponse,arg) {
  // console.log("Ha! on_store_exception() was called!");
  console.log("on_store_exception:",store,type,action,options,reponse,arg);
};
Lino.save_window_config = function(caller,url) {
  return function(event,toolEl,panel,tc) {
    // console.log(panel.id,panel.getSize(),panel.getPosition());
    var pos = panel.getPosition();
    var size = panel.getSize();
    var w = size['width'] * 100 / Lino.viewport.getWidth();
    var h = size['height'] * 100 / Lino.viewport.getHeight();
    // Lino.do_action(url,'save_window_config',{h:Math.round(h),w:Math.round(w),max:panel.maximized});
    Lino.do_action(caller,url,'save_window_config',{
      x:pos[0],y:pos[1],h:size['height'],w:size['width'],
      max:panel.maximized});
  }
};

Lino.form_submit = function (job,url,store,pkname) {
  // console.log("Lino.form_submit:",job);
  return function(btn,evt) {
    p = {};
    // p[pkname] = store.getAt(0).data.id;
    // p[pkname] = job.current_pk;
    p[pkname] = job.get_current_record().id;
    // console.log('Lino.form_submit',p);
    job.main_panel.form.submit({
      clientValidation: false,
      url: url, 
      failure: function(form, action) {
        // console.log("form:",form);
        Ext.MessageBox.alert('Submit failed!', 
        action.result ? action.result.msg : '(undefined action result)');
      }, 
      params: p, 
      waitMsg: 'Saving Data...', 
      success: function (form, action) {
        Ext.MessageBox.alert('Saved OK',
          action.result ? action.result.msg : '(undefined action result)');
        store.reload();
      }
    })
  } 
};


Lino.grid_afteredit = function (caller,url) {
  return function(e) {
    /*
    e.grid - This grid
    e.record - The record being edited
    e.field - The field name being edited
    e.value - The value being set
    e.originalValue - The original value for the field, before the edit.
    e.row - The grid row index
    e.column - The grid column index
    */
    var p = e.record.data;
    // var p = {};
    p['grid_afteredit_colname'] = e.field;
    p[e.field] = e.value;
    // console.log(e);
    // add value used by ForeignKeyStoreField CHOICES_HIDDEN_SUFFIX
    p[e.field+'Hidden'] = e.value;
    // p[pk] = e.record.data[pk];
    // console.log("grid_afteredit:",e.field,'=',e.value);
    Ext.Ajax.request({
      waitMsg: 'Please wait...',
      url: url,
      params: p, 
      success: function(response) {
        // console.log('success',response.responseText);
        var result=Ext.decode(response.responseText);
        // console.log(result);
        if (result.success) {
          caller.main_grid.getStore().commitChanges(); // get rid of the red triangles
          caller.main_grid.getStore().reload();        // reload our datastore.
        } else {
          Ext.MessageBox.alert('Action failed',result.msg);
        }
      },
      failure: function(response) {
        // console.log(response);
        Ext.MessageBox.alert('Action failed','Lino server did not respond to Ajax request '+url);
      }
    })
  }
};

// Lino.jobs = Array();
// Lino.active_job = undefined;

Lino.do_action = function(caller,url,name,params) {
  var doit = function(confirmed) {
    params['confirmed'] = confirmed;
    console.log('Lino.do_action()',name,params);
    Ext.Ajax.request({
      waitMsg: 'Running action "' + name + '". Please wait...',
      url: url,
      params: params, 
      success: function(response){
        // console.log('raw response:',response.responseText);
        var result = Ext.decode(response.responseText);
        // console.log('got response:',result);
        if(result.success) {
          if (result.msg) Ext.MessageBox.alert('Success',result.msg);
          if (result.html) { new Ext.Window({html:result.html}).show(); };
          if (result.window) { new Ext.Window(result.window).show(); };
          if (result.call) {
            var job = new result.call(caller);
            // Lino.active_job = Lino.jobs.length;
            // Lino.jobs[Lino.jobs.length] = job;
            // job.run();
            // console.log(Lino.jobs);
          };
          if (result.redirect) { window.open(result.redirect); };
          if (result.must_reload && caller) caller.refresh();
          // Lino.last_result = result;
        } else {
          if (result.msg) Ext.MessageBox.alert('Action failed',result.msg);
          if(result.confirm) Ext.Msg.show({
            title: 'Confirmation',
            msg: result.confirm,
            buttons: Ext.Msg.YESNOCANCEL,
            fn: function(btn) {
              if (btn == 'yes') {
                  // console.log(btn);
                  doit(confirmed+1);
              }
            }
          })
        }
        if (result.stop_caller && caller) caller.stop();
        if (result.refresh_menu) Lino.load_main_menu();
      },
      failure: function(response){
        // console.log(response);
        Ext.MessageBox.alert('Error','Lino.do_action() could not connect to the server.');
      }
    });
  };
  doit(0);
};

Lino.do_dialog = function(caller,url,params) {
  var doit = function(dialog_step) {
    params['dialog_step'] = dialog_step;
    console.log('Lino.do_dialog()',url,params);
    Ext.Ajax.request({
      waitMsg: 'Please wait...',
      url: url,
      params: params, 
      success: function(response){
        var result = Ext.decode(response.responseText);
        if(result.success) {
          params['dialog_step'] = dialog_step;
          if (result.msg) Ext.MessageBox.alert('Success',result.msg);
          if (result.call) params['call_result'] = result.call(caller);
          if (result.must_reload && caller) caller.refresh();
          // Lino.last_result = result;
        } else {
          if (result.msg) Ext.MessageBox.alert('Action failed',result.msg);
          if(result.confirm) Ext.Msg.show({
            title: 'Confirmation',
            msg: result.confirm,
            buttons: Ext.Msg.YESNOCANCEL,
            fn: function(btn) {
              if (btn == 'yes') {
                  // console.log(btn);
                  doit(confirmed+1);
              }
            }
          })
        }
        if (result.stop_caller && caller) caller.stop();
        if (result.refresh_menu) Lino.load_main_menu();
      },
      failure: function(response){
        // console.log(response);
        Ext.MessageBox.alert('Error','Lino.do_action() could not connect to the server.');
      }
    });
  };
  doit(0);
};

Lino.grid_action = function(caller,name,url) {
  return function(event) {
    Lino.do_action(caller,url,name,{selected:caller.get_selected()});
  };
};
Lino.show_slave = function (caller,url,name,mt) { 
  return function(btn,evt) {
    // console.log('show_slave()',caller,url,name,mt)
    // p = caller.main_grid.getStore().baseParams;
    // console.log('show_detail',name,url,p)
    // Lino.do_action(caller,url,name,p);
    //var record = caller.get_current_record();
    //Lino.do_action(caller,url,name,{mt:mt,mk:record.id});
    Lino.do_action(caller,url,name,{});
  }
};
""" 

        s += """
Lino.gup = function( name )
{
  // Thanks to http://www.netlobo.com/url_query_string_javascript.html
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( window.location.href );
  if( results == null )
    return "";
  else
    return results[1];
};"""
        #uri = request.build_absolute_uri()
        uri = request.path
        s += """
Lino.goto_permalink = function () {
    var windows = "";
    var sep = '';
    Ext.WindowMgr.each(function(win){
      if(!win.hidden) {windows+=sep+win._permalink;sep=","}
    });
    document.location = "%s?show=" + windows;
};""" % uri

        s += """
Lino.form_action = function (caller,name,needs_validation,url) { 
  return function(btn,evt) {
    // console.log('Lino.form_action()',caller,name,needs_validation);
    if (needs_validation && !caller.main_panel.form.isValid()) {
        Ext.MessageBox.alert('error',"One or more fields contain invalid data.");
        return;
    }
    Lino.do_action(caller,url,name,caller.get_values());
  }
};


Lino.toggle_props = function (caller) {
  return function(btn,state) {
    // console.log('toggle_props()',btn,state);
    if(state) { caller.props.show() } 
    else { caller.props.hide() }
  }
};


Lino.main_menu = new Ext.Toolbar({});

// Path to the blank image should point to a valid location on your server
Ext.BLANK_IMAGE_URL = '%sresources/images/default/s.gif';""" % settings.EXTJS_URL

        s += """
Lino.GridPanel = Ext.extend(Ext.grid.EditorGridPanel,{
  afterRender : function() {
    Lino.GridPanel.superclass.afterRender.call(this);
    // this.getView().mainBody.focus();
    // console.log(20100114,this.getView().getRows());
    // if (this.getView().getRows().length > 0) {
    //  this.getView().focusRow(1);
    // }
    var tbar = this.getTopToolbar();
    // tbar.on('change',function() {this.getView().focusRow(1);},this);
    // tbar.on('change',function() {this.getSelectionModel().selectFirstRow();this.getView().mainBody.focus();},this);
    // tbar.on('change',function() {this.getView().mainBody.focus();},this);
    // tbar.on('change',function() {this.getView().focusRow(1);},this);
    this.nav = new Ext.KeyNav(this.getEl(),{
      pageUp: function() {tbar.movePrevious(); },
      pageDown: function() {tbar.moveNext(); },
      home: function() {tbar.moveFirst(); },
      end: function() {tbar.moveLast(); },
      scope: this
    });
  },
  // pageSize depends on grid height (Trying to remove scrollbar)
  // Thanks to Christophe Badoit on http://www.extjs.net/forum/showthread.php?t=82647
  calculatePageSize : function(caller,aw,ah,rw,rh) {
    if (!this.rendered) { return false; }
    var rowHeight = 41;
    var row = this.view.getRow(0);
    if (row) rowHeight = Ext.get(row).getHeight();
    // console.log('rowHeight',rowHeight,this,caller);
    // var height = this.getView().scroller.getHeight();
    // console.log('scroller.getHeight() is',this.getView().scroller.getHeight());
    // console.log('scroller',this.getView().scroller.getHeight());
    // console.log('mainBody',this.getView().mainBody.getHeight());
    // console.log('getInnerHeight() is',this.getInnerHeight());
    // console.log('getFrameHeight() is',this.getFrameHeight());
    // var height = this.getView().scroller.getHeight();
    var height = this.getInnerHeight();
    // var height = this.getView().mainBody.getHeight();
    // var height = this.getHeight() - this.getFrameHeight();
    var ps = Math.floor(height / rowHeight);
    // console.log(height,'/',rowHeight,'->',ps);
    ps -= 3; // experimental value
    return (ps > 1 ? ps : false);
  },
  postEditValue : function(value, originalValue, r, field){
    value = Lino.GridPanel.superclass.postEditValue.call(this,value,originalValue,r,field);
    console.log('GridPanel.postEdit()',value, originalValue, r, field);
    return value;
  },
  add_row_listener : function(fn,scope) {
    this.getSelectionModel().addListener('rowselect',fn,scope);
  }
  });

Lino.cell_context_menu = function(job) {
  return function(grid,row,col,e) {
    // console.log('contextmenu',grid,row,col,e);
    e.stopEvent();
    grid.getView().focusRow(row);
    if(!job.cmenu.el){job.cmenu.render(); }
    var xy = e.getXY();
    xy[1] -= job.cmenu.el.getHeight();
    job.cmenu.showAt(xy);
  }
}

        """
        
        def js():
            yield "Lino.load_master = function(store,caller,record) {"
            #~ yield "  console.log('load_master() mt=',caller.content_type,',mk=',record.id);"
            yield "  store.setBaseParam(%r,caller.content_type);" % ext_requests.URL_PARAM_MASTER_TYPE
            yield "  store.setBaseParam(%r,record.id);" % ext_requests.URL_PARAM_MASTER_PK
            yield "  store.load();" 
            yield "}"
            
        s += py2js(js())
        
        s += """
Lino.on_load_menu = function(response) {
  // console.log('success',response.responseText);
  // console.log('on_load_menu before',Lino.main_menu);
  var p = Ext.decode(response.responseText);
  // console.log('on_load_menu p',p);
  // Lino.viewport.hide();
  // Lino.viewport.remove(Lino.main_menu);
  Lino.main_menu.removeAll();
  Lino.main_menu.add(p);
  // Lino.main_menu = new Ext.Toolbar(p);"""
        #d.update(autoScroll=True)
        #~ d.update(items=js_code(
            #~ "[Lino.main_menu,"+",".join([
                  #~ c.as_ext() for c in self.components]) +"]"))
                    
        s += """
  // console.log('on_load_menu after',Lino.main_menu);"""
        s += """
  // Lino.viewport.add(Lino.main_menu);""" 
        #~ items = "[Lino.main_menu,"+",".join([
                  #~ c.as_ext() for c in self.components]) +"]"
        #~ s += """
  #~ Lino.viewport.add(%s);""" % py2js(self.components)
        s += """
  Lino.viewport.doLayout();
  // console.log('on_load_menu viewport',Lino.viewport);
  // Lino.viewport.show();
  i = Lino.main_menu.get(0);
  if (i) i.focus();"""
        s += """
};"""
        s += """
        
Lino.load_main_menu = function() {
  Ext.Ajax.request({
    waitMsg: 'Loading main menu...',
    url: '/menu',
    success: Lino.on_load_menu,
    failure: function(response) {
      // console.log(response);
      Ext.MessageBox.alert('error','could not connect to the LinoSite.');
    }
  });
};


(function(){
    var ns = Ext.ns('Ext.ux.plugins');

    /**
     * @class Ext.ux.plugins.DefaultButton
     * @extends Object
     *
     * Plugin for Button that will click() the button if the user presses ENTER while
     * a component in the button's form has focus.
     *
     * @author Stephen Friedrich
     * @date 09-DEC-2009
     * @version 0.1
     *
     */
    ns.DefaultButton =  Ext.extend(Object, {
        init: function(button) {
            button.on('afterRender', setupKeyListener, button);
        }
    });

    function setupKeyListener() {
        var formPanel = this.findParentByType('form');
        new Ext.KeyMap(formPanel.el, {
            key: Ext.EventObject.ENTER,
            shift: false,
            alt: false,
            fn: function(keyCode, e){
                if(e.target.type === 'textarea' && !e.ctrlKey) {
                    return true;
                }

                this.el.select('button').item(0).dom.click();
                return false;
            },
            scope: this
        });
    }

    Ext.ComponentMgr.registerPlugin('defaultButton', ns.DefaultButton);

})(); 


/*
Feature request developed in http://extjs.net/forum/showthread.php?t=75751
*/
Ext.override(Ext.form.ComboBox, {
    // queryContext : null, 
    // contextParam : null, 
    setValue : function(v){
        // if(this.name == 'country') console.log('country ComboBox.setValue()',v);
        var text = v;
        if(this.valueField){
          if(v === null) { 
              // console.log(this.name,'.setValue',v,'no lookup needed, value is null');
              v = null;
          }else{
            // if(this.mode == 'remote' && !Ext.isDefined(this.store.totalLength)){
            if(this.mode == 'remote' && ( this.lastQuery === null || (!Ext.isDefined(this.store.totalLength)))){
                // console.log(this.name,'.setValue',v,'must wait for load');
                this.store.on('load', this.setValue.createDelegate(this, arguments), null, {single: true});
                if(this.store.lastOptions === null || this.lastQuery === null){
                    var params;
                    if(this.valueParam){
                        params = {};
                        params[this.valueParam] = v;
                    }else{
                        var q = this.allQuery;
                        this.lastQuery = q;
                        this.store.setBaseParam(this.queryParam, q);
                        params = this.getParams(q);
                    }
                    // console.log(this.name,'.setValue',v,' : call load() with params ',params);
                    this.store.load({params: params});
                }else{
                    // console.log(this.name,'.setValue',v,' : but store is loading',this.store.lastOptions);
                }
                return;
            }else{
                // console.log(this.name,'.setValue',v,' : store is loaded, lastQuery is "',this.lastQuery,'"');
            }
            var r = this.findRecord(this.valueField, v);
            if(r){
                text = r.data[this.displayField];
            }else if(this.valueNotFoundText !== undefined){
                text = this.valueNotFoundText;
            }
          }
        }
        this.lastSelectionText = text;
        if(this.hiddenField){
            this.hiddenField.value = v;
        }
        Ext.form.ComboBox.superclass.setValue.call(this, text);
        this.value = v;
    },
    getParams : function(q){
        // p = Ext.form.ComboBox.superclass.getParams.call(this, q);
        // causes "Ext.form.ComboBox.superclass.getParams is undefined"
        var p = {};
        //p[this.queryParam] = q;
        if(this.pageSize){
            p.start = 0;
            p.limit = this.pageSize;
        }
        // now my code:
        if(this.queryContext) 
            p[this.contextParam] = this.queryContext;
        return p;
    },
    setQueryContext : function(qc){
        if(this.contextParam) {
            // console.log(this.name,'.setQueryContext',this.contextParam,'=',qc);
            if(this.queryContext != qc) {
                this.queryContext = qc;
                // delete this.lastQuery;
                this.lastQuery = null;
    }   }   }
});


/*
Ext.override(Ext.form.ComboBox, {
    setValue : function(v){
        // if(this.name == 'country') 
        // if(! v) { v = { text:'', value:undefined }};
        if(! v) { v = [undefined, '']};
        var text = v;
        this.lastSelectionText = v[1];
        if(this.hiddenField){
            this.hiddenField.value = v[0];
        }
        Ext.form.ComboBox.superclass.setValue.call(this, v[1]);
        this.value = v;
    },
    getValue : function(){
        v = Ext.form.ComboBox.superclass.getValue.call(this);
    },
    onSelect : function(record, index){
        if(this.fireEvent('beforeselect', this, record, index) !== false){
            this.setValue([record.data[this.valueField], record.data[this.displayField]]);
            this.collapse();
            this.fireEvent('select', this, record, index);
        }
    },
    beforeBlur : function(){
        var val = this.getRawValue(),
            rec = this.findRecord(this.displayField, val);
        if(!rec && this.forceSelection){
            if(val.length > 0 && val != this.emptyText){
                this.el.dom.value = Ext.isEmpty(this.lastSelectionText) ? '' : this.lastSelectionText;
                this.applyEmptyText();
            }else{
                this.clearValue();
            }
        }else{
            if(rec){
                val = [rec.get(this.valueField),rec.get(this.displayField)];
            }else{
                val = [undefined, '']
            }
            this.setValue(val);
        }
    },
    clearValue : function(){
        if(this.hiddenField){
            this.hiddenField.value = '';
        }
        this.setRawValue('');
        this.lastSelectionText = '';
        this.applyEmptyText();
        this.value = [undefined, ''];
    },

});
*/

"""   

        s += """
Ext.onReady(function(){ """

        for c in self.components:
            for ln in c.js_declare():
                s += "\n" + ln
            
        d = dict(layout='border')
        d.update(items=js_code(py2js([js_code('Lino.main_menu')]+list(self.components))))
        s += """
  Lino.main_menu = new Ext.Toolbar({region:'north',height:27});
  Lino.viewport = new Ext.Viewport(%s);""" % py2js(d)
        s += """
  Lino.viewport.render('body');""" 
    
        s += """
  Lino.load_main_menu();"""
        
        s += """
  var windows = Lino.gup('show').split(',');
  for(i=0;i<windows.length;i++) {
    // console.log(windows[i]);
    // if(windows[i]) eval(windows[i]+".show()");
    if(windows[i]) Lino.do_action(undefined,'/permalink_do/'+windows[i],windows[i],{});
  }
        """
        s += "\n}); // end of onReady()"
        s += "\n</script></head><body></body></html>"
        return s






class ExtUI(base.UI):
    _response = None
    
    
    window_configs_file = os.path.join(settings.PROJECT_DIR,'window_configs.pck')
    Panel = ext_elems.Panel
                
    def __init__(self):
        self.window_configs = {}
        if os.path.exists(self.window_configs_file):
            lino.log.info("Loading %s...",self.window_configs_file)
            wc = pickle.load(open(self.window_configs_file,"rU"))
            #lino.log.debug("  -> %r",wc)
            if type(wc) is dict:
                self.window_configs = wc
        else:
            lino.log.warning("window_configs_file %s not found",self.window_configs_file)
            
    def create_layout_element(self,lh,panelclass,name,**kw):
        
        if name == "_":
            return ext_elems.Spacer(lh,name,**kw)
            
        de = lh.link.get_data_elem(name)
        
        if isinstance(de,models.Field):
            return self.create_field_element(lh,de,**kw)
        if isinstance(de,generic.GenericForeignKey):
            return ext_elems.VirtualFieldElement(lh,name,de,**kw)
            
        from lino import reports
        
        if isinstance(de,reports.Report):
            e = ext_elems.GridElement(lh,name,de.get_handle(self),**kw)
            lh.slave_grids.append(e)
            return e
        if isinstance(de,actions.Action):
            e = ext_elems.ButtonElement(lh,name,de,**kw)
            lh._buttons.append(e)
            return e
            
        from lino import forms
        
        if isinstance(de,forms.Input):
            e = ext_elems.InputElement(lh,de,**kw)
            if not lh.start_focus:
                lh.start_focus = e
            return e
        if callable(de):
            return self.create_meth_element(lh,name,de,**kw)
            
        if not name in ('__str__','__unicode__','name','label'):
            value = getattr(lh.layout,name,None)
            if value is not None:
                if isinstance(value,basestring):
                    return lh.desc2elem(panelclass,name,value,**kw)
                if isinstance(value,layouts.StaticText):
                    return ext_elems.StaticTextElement(lh,name,value)
                #~ if isinstance(value,layouts.PropertyGrid):
                    #~ return ext_elems.PropertyGridElement(lh,name,value)
                raise KeyError("Cannot handle value %r in %s.%s." % (value,lh.layout.name,name))
        msg = "Unknown element %r referred in layout %s" % (name,lh.layout)
        #print "[Warning]", msg
        raise KeyError(msg)
        
    #~ def create_button_element(self,name,action,**kw):
        #~ e = self.ui.ButtonElement(self,name,action,**kw)
        #~ self._buttons.append(e)
        #~ return e
          
    def create_meth_element(self,lh,name,meth,**kw):
        rt = getattr(meth,'return_type',None)
        if rt is None:
            rt = models.TextField()
        e = ext_elems.MethodElement(lh,name,meth,rt,**kw)
        assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        lh._store_fields.append(e.field)
        return e
          
    #~ def create_virt_element(self,name,field,**kw):
        #~ e = self.ui.VirtualFieldElement(self,name,field,**kw)
        #~ return e
        
    #~ def field2elem(self,lh,field,**kw):
        #~ # used also by lino.ui.extjs.ext_elem.MethodElement
        #~ return lh.main_class.field2elem(lh,field,**kw)
        #~ # return self.ui.field2elem(self,field,**kw)
        
    def create_field_element(self,lh,field,**kw):
        e = lh.main_class.field2elem(lh,field,**kw)
        assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        lh._store_fields.append(e.field)
        return e
        #return FieldElement(self,field,**kw)
        


    def main_panel_class(self,layout):
        if isinstance(layout,layouts.RowLayout) : 
            return ext_elems.GridMainPanel
        if isinstance(layout,layouts.PageLayout) : 
            return ext_elems.DetailMainPanel
        if isinstance(layout,layouts.FormLayout) : 
            return ext_elems.FormMainPanel
        raise Exception("No element class for layout %r" % layout)
            

    
    def index(self, request):
        if self._response is None:
            from lino.lino_site import lino_site
            lino.log.debug("building extjs._response...")
            comp = ext_elems.VisibleComponent("index",
                xtype="panel",
                html=lino_site.index_html.encode('ascii','xmlcharrefreplace'),
                autoScroll=True,
                #width=50000,
                #height=50000,
                region="center")
            viewport = Viewport(lino_site.title,comp)
            s = viewport.render_to_html(request)
            self._response = HttpResponse(s)
        return self._response

    def save_window_configs(self):
        f = open(self.window_configs_file,'wb')
        pickle.dump(self.window_configs,f)
        f.close()
        self._response = None

  
    def get_urls(self):
        return patterns('',
            (r'^$', self.index),
            (r'^menu$', menu_view),
            (r'^list/(?P<app_label>\w+)/(?P<rptname>\w+)$', list_report_view),
            (r'^csv/(?P<app_label>\w+)/(?P<rptname>\w+)$', csv_report_view),
            (r'^grid_action/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<grid_action>\w+)$', json_report_view),
            (r'^submit/(?P<app_label>\w+)/(?P<rptname>\w+)$', form_submit_view),
            (r'^grid_afteredit/(?P<app_label>\w+)/(?P<rptname>\w+)$', grid_afteredit_view),
            (r'^form/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<action>\w+)$', act_view),
            (r'^form/(?P<app_label>\w+)/(?P<actor>\w+)$', act_view),
            (r'^action/(?P<app_label>\w+)/(?P<actor>\w+)$', act_view),
            (r'^dialog/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<action>\w+)$', self.dialog_view),
            (r'^dialog/(?P<app_label>\w+)/(?P<actor>\w+)$', self.dialog_view),
            (r'^choices/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<fldname>\w+)$', choices_view),
            (r'^save_win/(?P<name>\w+)$', save_win_view),
            (r'^permalink_do/(?P<name>\w+)$', permalink_do_view),
            (r'^props/(?P<app_label>\w+)/(?P<model_name>\w+)$', props_view),
        )
        
    def dialog_view(self,request,app_label=None,actor=None,action=None,**kw):
        dialog_id = request.POST.get('dialog_id',None)
        if dialog_id is None:
            actor = actors.get_actor2(app_label,actor)
            dlg = ext_requests.Dialog(request,self,actor,action)
            dlg.start()
            return json_response(dlg.get_response())
        else:
            context.run()
        return json_response(context.response)

        

    def get_action_url(self,a,**kw):
        url = "/action/" + a.app_label + "/" + a.name 
        if len(kw):
            url += "?" + urlencode(kw)
        return url
        
    def get_form_url(self,fh,**kw):
        url = "/form/" + fh.form.app_label + "/" + fh.form.name 
        if len(kw):
            url += "?" + urlencode(kw)
        return url
        
    def get_button_url(self,btn,**kw):
        a = btn.lh.link.actor
        return build_url("/form",a.app_label,a.name,btn.name,**kw)
        
    def get_choices_url(self,fke,**kw):
        return build_url("/choices",fke.lh.link.report.app_label,fke.lh.link.report.name,fke.field.name,**kw)
        
    def get_props_url(self,model,**kw):
        return build_url('/props',model._meta.app_label)
        
    def get_report_url(self,rh,master_instance=None,
            submit=False,grid_afteredit=False,grid_action=None,run=False,csv=False,**kw):
        #~ lino.log.debug("get_report_url(%s)", [rh.name,master_instance,
            #~ simple_list,submit,grid_afteredit,action,kw])
        if grid_afteredit:
            url = "/grid_afteredit/"
        elif submit:
            url = "/submit/"
        elif grid_action:
            url = "/grid_action/"
        elif run:
            url = "/action/"
        elif csv:
            url = "/csv/"
        else:
            url = "/list/"
        url += rh.report.app_label + "/" + rh.report.name
        if grid_action:
            url += "/" + grid_action
        if master_instance is not None:
            kw[ext_requests.URL_PARAM_MASTER_PK] = master_instance.pk
            mt = ContentType.objects.get_for_model(master_instance.__class__).pk
            kw[ext_requests.URL_PARAM_MASTER_TYPE] = mt
        if len(kw):
            url += "?" + urlencode(kw)
        return url
        
        
        
    def window_options(self,lh,**kw):
        name = id2js(lh.name)
        kw.update(title=lh.get_title(self))
        # kw.update(closeAction='hide')
        kw.update(maximizable=True)
        #kw.update(id=name)
        url = '/save_win/' + name
        js = 'Lino.save_window_config(this,%r)' % url
        kw.update(tools=[dict(id='save',handler=js_code(js))])
        kw.update(layout='fit')
        kw.update(items=lh._main)
        if lh.start_focus is not None:
            kw.update(defaultButton=lh.start_focus.name)
        wc = self.window_configs.get(name,None)
        #kw.update(defaultButton=self.lh.link.inputs[0].name)
        if wc is None:
            if lh.height is None:
                kw.update(height=300)
            else:
                kw.update(height=lh.height*EXT_CHAR_HEIGHT + 7*EXT_CHAR_HEIGHT)
            if lh.width is None:
                kw.update(width=400)
            else:
                kw.update(width=lh.width*EXT_CHAR_WIDTH + 10*EXT_CHAR_WIDTH)
        else:
            assert len(wc) == 5
            kw.update(x=wc[0])
            kw.update(y=wc[1])
            kw.update(width=wc[2])
            kw.update(height=wc[3])
            #kw.update(width=js_code('Lino.viewport.getWidth()*%d/100' % wc[0]))
            #kw.update(height=js_code('Lino.viewport.getHeight()*%d/100' % wc[1]))
            kw.update(maximized=wc[4])
        return kw
            
        
    def view_report(self,context,**kw):
        """
        called from Report.view()
        """
        rpt = context.actor
        rh = self.get_report_handle(rpt)
        #rr = ViewReportRequest(context.request,rh)
        layout = context.request.GET.get('layout')
        if layout is None:
            lh = rh.layouts[rpt.default_layout]
        else:
            lh = rh.layouts[int(layout)]
        #lh = rr.layout 
        # kw['defaultButton'] = js_code('this.main_grid')
        kw = self.window_options(lh,**kw)
        context.response.update(call=lh._main.js_job_constructor(**kw))
        
        
    def view_form(self,context,**kw):
        "called from Form.run()"
        frm = context.actor
        fh = self.get_form_handle(frm)
        #fh.setup()
        lh = fh.lh
        kw = self.window_options(lh,**kw)
        #rr = None
        context.response.update(call=lh._main.js_job_constructor(**kw))
        
    #~ def show_properties(self,context,row,**kw):
        #~ "called from lino.actions.ShowProperties.run()"
        #~ propseditor = ext_elems.ShowPropertiesWindow(row)
        #~ context.response.update(call=propseditor.js_job_constructor(**kw))

        
        
    def setup_report(self,rh):
        rh.store = ext_store.Store(rh)
        props = Property.properties_for_model(rh.report.model)
        if props.count() == 0:
            rh.props = None
        else:
            rh.props = ext_elems.PropertiesWindow(self,rh.report.model,props)

    def setup_form(self,fh):
        fh.props = None

ui = ExtUI()