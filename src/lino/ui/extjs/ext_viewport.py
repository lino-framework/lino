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

from django.conf import settings
from lino.ui.extjs import ext_requests
from lino.utils.jsgen import py2js, js_code, id2js


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
    Lino.do_dialog(caller,url,{
      x:pos[0],y:pos[1],h:size['height'],w:size['width'],
      max:panel.maximized});
    // Lino.do_action(caller,url,'save_window_config',{
    //  x:pos[0],y:pos[1],h:size['height'],w:size['width'],
    //  max:panel.maximized});
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

Lino.old_do_action = function(caller,url,name,params) {
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
  console.log('Lino.do_dialog()',url,params);
  var step_dialog = function(result) {
    if (result.dialog_id) {
      params['dialog_id'] = result.dialog_id;
      Ext.Ajax.request({ url:'/step_dialog', params:params, success: handle_response});
    }
  }
  var abort_dialog = function(result) {
    if (result.dialog_id) {
      params['dialog_id'] = result.dialog_id;
      Ext.Ajax.request({ url:'/abort_dialog', params:params, success: handle_response});
    }
  }
  var handle_response = function(response) {
    var abort = false;
    var result = Ext.decode(response.responseText);
    // console.log('Lino.do_dialog() got',result);
    if (result.alert_msg) Ext.MessageBox.alert('Alert',result.alert_msg);
    if (result.notify_msg) Lino.notify(result.notify_msg);
    if (result.exec_js) new result.exec_js(caller);
    if (result.must_reload && caller) caller.refresh();
    if (result.stop_caller && caller) caller.stop();
    if (result.refresh_menu) Lino.load_main_menu();
    if (result.confirm_msg) {
      Ext.Msg.show({
        title: 'Confirmation',
        msg: result.confirm_msg,
        buttons: Ext.Msg.YESNOCANCEL,
        fn: function(btn) {
          if (btn == 'yes') step_dialog(result);
          else if (btn == 'no') abort_dialog(result);
        }
      }) 
    } else {
      step_dialog(result);
    }
  }
  Ext.Ajax.request({
    waitMsg: 'Please wait...',
    url: url,
    params: params, 
    success: handle_response,
    failure: function(response){
      Ext.MessageBox.alert('Error','Lino.do_dialog() could not connect to the server.');
    }
  });
};

Lino.grid_action = function(caller,name,url) {
  return function(event) {
    // Lino.do_action(caller,url,name,{selected:caller.get_selected()});
    Lino.do_dialog(caller,url,{selected:caller.get_selected()});
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
    // Lino.do_action(caller,url,name,{});
    Lino.do_dialog(caller,url,{});
  }
};
Lino.notify = function(msg) {
  console.log(msg);
}
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
    // Lino.do_action(caller,url,name,caller.get_values());
    Lino.do_dialog(caller,url,caller.get_values());
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
    // if(windows[i]) Lino.do_action(undefined,'/permalink_do/'+windows[i],windows[i],{});
    if(windows[i]) Lino.do_dialog(undefined,'/permalink_do/'+windows[i],{});
  }
        """
        s += "\n}); // end of onReady()"
        s += "\n</script></head><body></body></html>"
        return s





