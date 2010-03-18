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
Lino.save_window_config = function(caller,unused_url) {
  return function(event,toolEl,panel,tc) {
    var url = '/save_window_config'
    // var url = '/save_win/' + panel._permalink_name
    // console.log(panel.id,panel.getSize(),panel.getPosition());
    var pos = panel.getPosition();
    var size = panel.getSize();
    // var w = size['width'] * 100 / Lino.viewport.getWidth();
    // var h = size['height'] * 100 / Lino.viewport.getHeight();
    wc = caller.get_window_config();
    Ext.applyIf(wc,{ name: panel._permalink_name,
      x:pos[0],y:pos[1],height:size.height,width:size.width,
      max:panel.maximized});
    Lino.do_dialog(caller,url,wc);
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
      failure: Lino.ajax_error_handler
    })
  }
};

Lino.build_ajax_request = function(caller,url,params) {
  // console.log('Lino.do_dialog()',url,params);
  var step_dialog = function(result) {
    if (result.dialog_id) {
      if (caller) Ext.apply(params,caller.get_values());
      params['dialog_id'] = result.dialog_id;
      params['last_button'] = result.last_button;
      Ext.Ajax.request({ url:'/step_dialog', params:params, success: handle_response});
    }
  }
  var abort_dialog = function(result) {
    if (result.dialog_id) {
      params['dialog_id'] = result.dialog_id;
      params['last_button'] = result.last_button;
      Ext.Ajax.request({ url:'/abort_dialog', params:params, success: handle_response});
    }
  }
  var handle_response = function(response) {
    var result = Ext.decode(response.responseText);
    // console.log('Lino.do_dialog() got',result);
    if (result.alert_msg) Ext.MessageBox.alert('Alert',result.alert_msg);
    if (result.notify_msg) Lino.notify(result.notify_msg);
    if (result.show_window) {
      caller = new result.show_window(caller);
      caller.show();
    }
    if (result.redirect) window.open(result.redirect);
    if (result.refresh_caller && caller) caller.refresh();
    if (result.close_caller && caller) {
      caller.close();
      caller = caller.caller;
    }
    if (result.refresh_menu) Lino.load_main_menu();
    if (result.confirm_msg) {
      Ext.MessageBox.show({
        title: 'Confirmation',
        msg: result.confirm_msg,
        buttons: Ext.MessageBox.YESNOCANCEL,
        fn: function(btn) {
          if (btn == 'yes') step_dialog(result);
          else abort_dialog(result);
        }
      })
    } else if (result.show_modal_window) {
      var on_click = function(btn_name) {result.last_button = btn_name;step_dialog(result)};
      caller = new result.show_modal_window(caller,on_click)
      // ww.ok = function(btn_name) {result.last_button = btn_name;step_dialog(result)};
      // ww.cancel = function(btn_name) {result.last_button = btn_name;abort_dialog(result)};
      caller.show();
    } else {
      step_dialog(result);
    }
  }
  return { 
    waitMsg: 'Please wait...',
    url: url,
    params: params, 
    success: handle_response,
    failure: Lino.ajax_error_handler
  }
}

Lino.do_dialog = function(caller,url,params) {
  var rc = Lino.build_ajax_request(caller,url,params);
  Ext.Ajax.request(rc);
};

Lino.submit_form = function (caller,url,pkname) {
  params = {};
  var rec = caller.get_current_record();
  if (rec) params[pkname] = rec.id;
  var rc = Lino.build_ajax_request(caller,url,params);
  rc.clientValidation = true;
  rc.waitMsg = 'Saving Data...';
  caller.main_panel.form.submit(rc);
}    

Lino.unused_form_submit = function (url,pkname) {
  return function(btn,evt) {
    params = {};
    var rec = this.get_current_record();
    if (rec) params[pkname] = rec.id;
    var caller = this;
    this.main_panel.form.submit({
      clientValidation: true,
      url: url, 
      failure: function(form, action) {
        // console.log("form:",form);
        Ext.MessageBox.alert('Submit failed!', 
        action.result ? action.result.msg : '(undefined action result)');
      }, 
      params: p, 
      waitMsg: 'Saving Data...', 
      success: function (form, action) {
        Lino.notify(action.result ? action.result.msg : '(undefined action result)');
        // this.main_grid.getStore().reload();
        caller.refresh();
      }
    })
  } 
};




"""

        def js():
            yield "Lino.action_handler = function(caller,url) {"
            yield "  return function(event) {"
            yield "    Lino.do_dialog(caller,url,\
              {%s:caller.get_selected()});" % ext_requests.POST_PARAM_SELECTED
            yield "}};"
            
        s += py2js(js)

        if False: s += """
Lino.slave_handler = function (caller,url) { 
  return function(btn,evt) {
    Lino.do_dialog(caller,url,{});
  }
};
""" 
        s += """
        
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
      if(!win.hidden) {windows+=sep+win._permalink_name;sep=","}
    });
    document.location = "%s?show=" + windows;
};""" % uri

        s += """
Lino.form_action = function (caller,needs_validation,url) { 
  console.log('Lino.form_action()',caller,name,needs_validation);
  return function(btn,evt) {
    if (needs_validation && !caller.main_panel.form.isValid()) {
        Ext.MessageBox.alert('error',"One or more fields contain invalid data.");
        return;
    }
    // Lino.do_action(caller,url,name,caller.get_values());
    Lino.do_dialog(caller,url,caller.get_values());
  }
};

Lino.toggle_window = function(btn,state,ww) {
  console.log('Lino.toggle_window',ww);
  if(state) { ww.show() } else { ww.hide() }
};

Lino.ajax_error_handler = function(response,options) {
    console.log('AJAX failure:',response,options);
    // Ext.MessageBox.alert('Action failed','Lino server did not respond to Ajax request');
}
// Ext.Ajax.on('requestexception',Lino.ajax_error_handler)

Lino.submit_property = function (caller,e) {
  /*
  e.grid - This grid
  e.record - The record being edited
  e.field - The field name being edited
  e.value - The value being set
  e.originalValue - The original value for the field, before the edit.
  e.row - The grid row index
  e.column - The grid column index
  */
  // var p = e.record.data;
  var p = {};
  // p['grid_afteredit_colname'] = e.field;
  // p[e.field] = e.value;
  p['mt'] = caller.content_type // URL_PARAM_MASTER_TYPE
  p['mk'] = caller.get_current_record().id // URL_PARAM_MASTER_PK
  console.log('submit_property()',e.record.data);
  p['name'] = e.record.data.name
  p['value'] = e.record.data.value
  Ext.Ajax.request({
    method: 'POST',
    waitMsg: 'Please wait...',
    url: '/submit_property',
    params: p, 
    success: function(response) {
      var result=Ext.decode(response.responseText);
      // console.log(result);
      if (result.success) {
        // Lino.load_properties();        // reload our datastore.
      } else {
        Ext.MessageBox.alert('Action failed',result.msg);
      }
    },
    failure: Lino.ajax_error_handler
  })
};

Lino.load_properties = function(caller,pw,url,record) { 
  if(pw.hidden) return;
  if(record === undefined) return;
  // console.log('load_properties',caller,url,record);
  var params = {mt:caller.content_type, mk:record.id}; // URL_PARAM_MASTER_TYPE, URL_PARAM_MASTER_PK
  var on_success = function(response) {
    var result = Ext.decode(response.responseText);
    pw.window.setTitle(result.title);
    // var grid = caller.properties_window.items.get(0);
    var grid = pw.window.items.get(0).items.get(0);
    for (i in result.rows) {
      grid.setProperty(result.rows[i].name,result.rows[i].value)
    }
  };
  Ext.Ajax.request({
    waitMsg: 'Loading properties...',
    url: url,
    method: 'GET',
    params: params,
    scope: this,
    success: on_success,
    failure: Lino.ajax_error_handler
  });
}"""


        s += """
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
    var rowHeight = 22; // experimental value
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
    // console.log('calculatePageSize():',height,'/',rowHeight,'->',ps);
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
            yield "};"
            
        s += py2js(js)
        
        def js():
            yield "Lino.search_handler = function(caller) { return function(field, e) {"
            yield "  if(e.getKey() == e.RETURN) {"
            # yield "    console.log('keypress',field.getValue(),store)"
            yield "    caller.main_grid.getStore().setBaseParam('%s',field.getValue());" % ext_requests.URL_PARAM_FILTER
            yield "    caller.main_grid.getStore().load({params: { start: 0, limit: caller.pager.pageSize }});" 
            yield "  }"
            yield "}};"
        
        s += py2js(js)
        
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
    failure: Lino.ajax_error_handler
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
    // contextParams : array of names of variables to add to query
    // contextValues : array of values of variables to add to query
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
        if(this.contextParams && this.contextValues) {
          for(i = 0; i <= this.contextParams.length; i++)
            p[this.contextParams[i]] = this.contextValues[i];
        }
        return p;
    },
    setContextValues : function(values){
      if(this.contextParams) {
        console.log(this.name,'.setContextValues',this.contextParams,'=',values);
        if (this.contextValues === undefined) {
          this.contextValues = values;
          this.lastQuery = null;
          return
        }
        for(i = 0; i <= this.contextParams.length; i++) {
          if (this.contextValues[i] != values[i]) {
            this.contextValues[i] = values[i];
            this.lastQuery = null;
          }
        }
      }   
    }
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
  Ext.QuickTips.init();
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





