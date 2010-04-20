/*
 Copyright 2009-2010 Luc Saffre
 This file is part of the Lino project.
 Lino is free software; you can redistribute it and/or modify 
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.
 Lino is distributed in the hope that it will be useful, 
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
 GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with Lino; if not, see <http://www.gnu.org/licenses/>.
*/
Ext.namespace('Lino');
Lino.on_store_exception = function (store,type,action,options,reponse,arg) {
  // console.log("Ha! on_store_exception() was called!");
  console.log("on_store_exception:",store,type,action,options,reponse,arg);
};





Lino.save_wc_handler = function(ww) {
  return function(event,toolEl,panel,tc) {
    var url = ww.config.url_action+'.wc';
    // var url = '/save_window_config'
    // var url = '/save_win/' + panel._permalink_name
    // console.log(panel.id,panel.getSize(),panel.getPosition());
    var pos = panel.getPosition();
    var size = panel.getSize();
    // var w = size['width'] * 100 / Lino.viewport.getWidth();
    // var h = size['height'] * 100 / Lino.viewport.getHeight();
    wc = ww.get_window_config();
    Ext.applyIf(wc,{ 
      // name: ww._permalink_name,
      x:pos[0],y:pos[1],height:size.height,width:size.width,
      maximized:panel.maximized});
    //~ Lino.do_dialog(caller,url,wc);
    Lino.do_action(ww,url,wc,'POST');
    //~ Ext.Ajax.request({ 
      //~ waitMsg: 'Saving window config...',
      //~ method: 'PUT',
      //~ url: url,
      //~ params: params, 
      //~ success: on_success,
      //~ failure: Lino.ajax_error_handler
    //~ });
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

Lino.unused_build_ajax_request = function(caller,url,params) {
  // console.log('Lino.do_dialog()',url,params);
  var step_dialog = function(result) {
    if (result.dialog_id) { // server wants me to continue this dialog
      // if (caller) Ext.apply(params,caller.get_values());
      params['dialog_id'] = result.dialog_id;
      params['last_button'] = result.last_button;
      if (caller && caller.main_panel) {
        if (!caller.main_panel.form.isValid()) {
          Lino.notify("One or more fields contain invalid data.");
          return;
        }
        // var rec = caller.get_current_record();
        // if (rec) params['pk'] = rec.id;
        console.log("using form.submit()");
        caller.main_panel.form.submit({ url:'/step_dialog', params:params, 
          success: function(form, action) { 
            console.log('build_ajax_request',action.result); 
            handle_response(action.result)
          }});
      } else {
        console.log("using Ajax.request()");
        Ext.Ajax.request({ url:'/step_dialog', params:params, success: handle_response});
      }

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
    if (result.exec_js) { result.exec_js(caller) };
    if (result.show_window) {
      var ww = result.show_window(caller);
      ww.show();
      // caller = new result.show_window(caller);
      // caller.show();
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

Lino.do_action = function(caller,url,params,method) {
  var on_success = function(response) {
    var result = Ext.decode(response.responseText);
    // console.log('Lino.do_dialog() got',result);
    if (result.alert_msg) Ext.MessageBox.alert('Alert',result.alert_msg);
    if (result.notify_msg) Lino.notify(result.notify_msg);
    if (result.exec_js) { result.exec_js(caller) };
    if (result.show_window) {
      var ww = result.show_window(caller);
      ww.show();
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
    }
  };
  Ext.Ajax.request({ 
    waitMsg: 'Please wait...',
    url: url,
    params: params, 
    method: method,
    success: on_success,
    failure: Lino.ajax_error_handler
  });
};

Lino.unused_do_dialog = function(caller,url,params) {
  var rc = Lino.build_ajax_request(caller,url,params);
  Ext.Ajax.request(rc);
};
Lino.submit_form = function (caller,url,pkname,must_validate) {
  // still used for submit button in DetailSlaveWrapper
  if (must_validate && !caller.config.main_panel.form.isValid()) {
      Lino.notify("One or more fields contain invalid data.");
      return;
  }
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

Lino.notify = function(msg) {
  console.log(msg);
  Ext.getCmp('konsole').update(msg);
}
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
};

Lino.goto_permalink = function () {
    var windows = "";
    var sep = '';
    Ext.WindowMgr.each(function(win) {
      if(!win.hidden && !win.window_wrapper.caller) { 
        windows += sep + win.window_wrapper.config.permalink_name; 
        sep = ","
      }
    });
    //~ document.location = "/permalink/?show=" + windows;
    if (windows) document.location = "?permalink=" + windows;
};

Lino.run_permalink = function() {
  var links = Lino.gup('permalink').split(',');
  for ( i=0; i < links.length; i++ ) {
    //~ console.log(links[i]);
    // if(windows[i]) eval(windows[i]+".show()");
    // if(windows[i]) Lino.do_action(undefined,'/permalink_do/'+windows[i],windows[i],{});
    if(links[i]) {
      Lino.do_action(undefined,'/api/'+links[i]+'.act',{},'GET');
      //~ var a = links[i].split('.');
      //~ if (a.length == 2) {
          //~ Lino.do_dialog(undefined,'/action/'+a[0]+'/'+a[1],{});
      //~ }
    }
  }
}


Lino.unused_form_action = function (caller,needs_validation,url) { 
  // console.log('Lino.form_action()',caller,name,needs_validation);
  return function(btn,evt) {
    if (needs_validation && !caller.main_panel.form.isValid()) {
        Ext.MessageBox.alert('error',"One or more fields contain invalid data.");
        return;
    }
    // Lino.do_action(caller,url,name,caller.get_values());
    Lino.do_dialog(caller,url,caller.get_values());
  }
};

/* 
Lino.toggle_window = function(btn,state,ww) {
  console.log('Lino.toggle_window',ww);
  if(state) { ww.show() } else { ww.hide() }
}; 
*/

Lino.open_window_handler = function(caller,action) {
  return function(event) {
    if (!caller.setup_child(action)) return;
    // caller[name].show();
}};


Lino.toggle_window_handler = function(caller,action) {
  return function(btn,state) {
    // console.log(20100406,'toggle_window_handler',name);
    if (!caller.setup_child(action,btn)) return;
    if(state) { 
      caller[action.name].show() 
    } else { 
      caller[action.name].hide() 
    }
  }
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
  var p = caller.get_master_params(caller.get_current_record());
  // p['grid_afteredit_colname'] = e.field;
  // p[e.field] = e.value;
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
  console.log('load_properties',caller,url,record);
  if(pw.window.hidden) return;
  var params = caller.get_master_params(record);
  //~ if(record === undefined) return;
  //~ var params = {mt:caller.config.content_type, mk:record.id}; // URL_PARAM_MASTER_TYPE, URL_PARAM_MASTER_PK
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
}


Lino.main_menu = new Ext.Toolbar({});

// Path to the blank image should point to a valid location on your server
Ext.BLANK_IMAGE_URL = '/extjs/resources/images/default/s.gif';

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
  //~ add_row_listener : function(fn,scope) {
    //~ this.getSelectionModel().addListener('rowselect',fn,scope);
  //~ }
  });
  

Lino.cell_context_menu = function(grid,row,col,e) {
  // console.log('contextmenu',grid,row,col,e);
  e.stopEvent();
  grid.getView().focusRow(row);
  if(!this.cmenu.el){this.cmenu.render(); }
  var xy = e.getXY();
  xy[1] -= this.cmenu.el.getHeight();
  this.cmenu.showAt(xy);
}


Lino.on_load_menu = function(response) {
  // console.log('success',response.responseText);
  // console.log('on_load_menu before',Lino.main_menu);
  var p = Ext.decode(response.responseText);
  // console.log('on_load_menu p',p);
  // Lino.viewport.hide();
  // Lino.viewport.remove(Lino.main_menu);
  Lino.main_menu.removeAll();
  Lino.main_menu.add(p);
  // Lino.main_menu = new Ext.Toolbar(p);
  // console.log('on_load_menu after',Lino.main_menu);
  // Lino.viewport.add(Lino.main_menu);
  Lino.viewport.doLayout();
  // console.log('on_load_menu viewport',Lino.viewport);
  // Lino.viewport.show();
  i = Lino.main_menu.get(0);
  if (i) i.focus();
};      

Lino.load_main_menu = function() {
  Ext.Ajax.request({
    waitMsg: 'Loading main menu...',
    url: '/menu',
    success: Lino.on_load_menu,
    failure: Lino.ajax_error_handler
  });
};



/** 
  config: 
  name
  title
  width,height,x,y,maximized
  url
  name
  content_type
  bbar
  columns
  fields
  actions : array of {name,label,url}
  content_type
**/

Lino.WindowWrapper = function(caller,config) {
  this.caller = caller;
  this.config = config; 
  if (config.actions) {
      this.bbar = Array(config.actions.length);
      for(var i=0;i<config.actions.length;i++) { 
        var btn = {
          text: config.actions[i].label,
        }
        if (config.actions[i].type == 'toggle_window') {
          btn.toggleHandler = Lino.toggle_window_handler(this,config.actions[i]);
          btn.enableToggle = true;
        } else if (config.actions[i].type == 'open_window') {
          btn.handler = Lino.open_window_handler(this,config.actions[i]);
        }
        this.bbar[i] = new Ext.Button(btn);
      }
  }
  //~ console.log('Lino.WindowWrapper.constructor',config.title,this);
  this.setup();
};
Ext.apply(Lino.WindowWrapper.prototype,{
  closeAction : 'close',
  show : function() {
    console.log('Lino.WindowWrapper.show',this);
    this.window.show();
    this.window.syncSize();
    this.window.focus();
  },
  get_master_params : function(record) {
    var p = {}
    p['mt'] = this.config.content_type; // ext_requests.URL_PARAM_MASTER_TYPE
    if (record) {
      p['mk'] = record.id; // ext_requests.URL_PARAM_MASTER_PK
    } else {
      p['mk'] = undefined;
    }
    return p;
  },
  get_values : function() {
    var v = {};
    return v;
  },
  setup : function() { 
    this.window = new Ext.Window({ layout: "fit", title: this.config.title, items: this.main_item, 
      height: this.config.wc.height, width: this.config.wc.width, maximizable: true, maximized: this.config.wc.maximized, 
      y: this.config.wc.y, x: this.config.wc.x, 
      closeAction:this.closeAction,
      tools: [ { qtip: this.config.qtip, handler: Lino.save_wc_handler(this), id: "save" } ] 
      });
    this.window.window_wrapper = this;
    //~ if (this.caller) this.window._permalink_name = this.config.permalink_name;
    this.window.on('render',this.on_render,this)
  },
  on_render : function() {},
  refresh : function() {},
  hide : function() { this.window.hide() },
  close : function() { this.window.close() },  
  setup_child : function(action,btn) {
    if (this[action.name]) return (this[action.name] != 'loading');
    this[action.name] = 'loading';
    console.log(20100414,'Lino.setup_child() ',this,action.name,'=',this[action.name]);
    var p = this.get_master_params(this.get_current_record())
    Ext.Ajax.request({
      method: 'GET',
      waitMsg: 'Please wait...',
      url: action.url, // caller.config.url + '/' + name + '.act',
      params: p, 
      scope: this,
      success: function(response) {
        var result = Ext.decode(response.responseText);
        if (result.show_window) {
          //~ console.log(20100414,'setup_child.show_window',name,caller); // [name]);
          this[action.name+'_button'] = btn;
          this[action.name] = result.show_window(this);
          this[action.name].show();
        } 
        if (result.alert_msg) Ext.MessageBox.alert('Alert',result.alert_msg);
        if (result.notify_msg) Lino.notify(result.notify_msg);
      },
      failure: Lino.ajax_error_handler
    })
    return false;
  },
});

Lino.GridWindowWrapper = Ext.extend(Lino.WindowWrapper,{
  setup : function() {
    this.store = new Ext.data.JsonStore({ 
      listeners: { exception: Lino.on_store_exception }, 
      proxy: new Ext.data.HttpProxy({ url: this.config.url_data+'.json', method: "GET" }), remoteSort: true, 
      fields: this.config.fields, 
      totalProperty: "count", 
      root: "rows", 
      id: "id" });
    this.pager = new Ext.PagingToolbar({ prependButtons: true, items: [ 
      { scope:this, xtype: "textfield", listeners: { keypress: Lino.search_handler(this) }, 
        fieldLabel: "Search", enableKeyEvents: true, id: "seachString" }, 
      { scope:this, text: "Download", handler: function() {window.open(this.config.url_data+'.csv');} } 
    ], pageSize: 10, store: this.store, displayInfo: true });
    
    this.main_grid = new Lino.GridPanel({ clicksToEdit: 2, xtype: "container", tbar: this.pager, 
      selModel: new Ext.grid.RowSelectionModel({singleSelect:false}), 
      emptyText: "Nix gefunden...", 
      bbar: this.bbar, 
      viewConfig: { showPreview: true, scrollOffset: 200, emptyText: "Nix gefunden!" }, 
      enableColLock: false, store: this.store, colModel: this.config.colModel });
      
    this.main_item = this.main_grid;
      
    this.main_grid.on('afteredit', Lino.grid_afteredit(this,this.config.url_data+'.submit'));
    // this.main_grid.on('cellcontextmenu', Lino.cell_context_menu, this);
    this.main_grid.on('resize', function(cmp,aw,ah,rw,rh) {
        this.pager.pageSize = cmp.calculatePageSize(this,aw,ah,rw,rh) || 10;
        this.refresh();
      }, this, {delay:500});
    Lino.WindowWrapper.prototype.setup.call(this);
  },
  get_window_config : function() {
    var wc = { window_config_type: 'grid' }
    wc['column_widths'] = Ext.pluck(this.main_grid.colModel.columns,'width');
    return wc;
  },
  get_current_record : function() { 
    return this.main_grid.getSelectionModel().getSelected()
  },
});

Lino.GridMasterWrapper = Ext.extend(Lino.GridWindowWrapper, {
  add_row_listener : function(fn,scope) {
    // this.main_grid.add_row_listener(fn,scope);
    this.main_grid.getSelectionModel().addListener('rowselect',fn,scope);
  },
  refresh : function() { 
    this.store.load({params:{limit:this.pager.pageSize,start:this.pager.cursor}});
  },
  get_selected : function() {
    var sel_pks = '';
    var sels = this.main_grid.getSelectionModel().getSelections();
    for(var i=0;i<sels.length;i++) { sel_pks += sels[i].id + ','; };
    return sel_pks;
  },
});


Lino.SlaveWrapper = Ext.extend(Lino.WindowWrapper, {
  closeAction : 'hide',
  setup : function() {
    console.log('Lino.SlaveWrapper.setup',this.config.name,this);
    //~ Lino.WindowWrapper.prototype.setup.call(this);
    this.caller.window.on('close',function() { this.close() },this);
    this.caller.window.on('hide',function(){ this.window.hide()},this);
    this.window.on('hide',function(){ 
      //~ console.log(20100414,this.config.name);
      this.caller[this.config.name+'_button'].toggle(false)
    },this);
    this.window.on('show',function(){
      this.load_record(this.caller.get_current_record())
    },this);
  },
  on_render : function() {
    //~ console.log('Lino.SlaveWrapper.on_render',this.config.title,this);
    this.caller.add_row_listener( function(sm,ri,rec){this.load_record(rec)}, this );
    // var sels = this.caller.main_grid.getSelectionModel().getSelections();
    // if (sels.length > 0) this.load_record(sels[0]);
    //~ console.log('Lino.SlaveWrapper.on_render b');
    this.load_record(this.caller.get_current_record());
    //~ console.log('Lino.SlaveWrapper.on_render c');
  },
  add_row_listener : function(fn,scope) {
    this.caller.add_row_listener(fn,scope);
  },  
  
});

Lino.GridSlaveWrapper = Ext.extend(Lino.SlaveWrapper, {
  setup : function() {
    Lino.GridWindowWrapper.prototype.setup.call(this);
    Lino.SlaveWrapper.prototype.setup.call(this);
  },
  get_window_config  : Lino.GridWindowWrapper.prototype.get_window_config,
  get_current_record  : Lino.GridWindowWrapper.prototype.get_current_record,
  load_record : function(record) {
    this.current_record = record;
    this.store.load({params:this.get_master_params(record)}); 
  },
});


Lino.DetailSlaveWrapper = Ext.extend(Lino.SlaveWrapper, {
  setup:function() {
    //~ console.log('Lino.DetailSlaveWrapper setup',20100409,this);
    this.main_item = this.config.main_panel;
    Lino.WindowWrapper.prototype.setup.call(this);
    Lino.SlaveWrapper.prototype.setup.call(this);
  },
  get_selected : function() { return this.current_record.id },
  get_current_record : function() {  return this.current_record },
  load_record : function(record) {
    this.current_record = record;
    this.config.main_panel.form.load(record);
  },
});

Lino.PropertiesWrapper = Ext.extend(Lino.SlaveWrapper, {
  setup : function() {
    // console.log('Lino.GridMasterWrapper configure',20100401,this);
    this.main_item = this.config.main_panel;
    Lino.WindowWrapper.prototype.setup.call(this);
    Lino.SlaveWrapper.prototype.setup.call(this);
  },
  load_record : function(rec) {
    Lino.load_properties(this.caller,this,this.config.url_data+'.json',rec);
  },
  get_window_config : function() {
    var wc = { window_config_type: 'props' }
    var cm = this.window.items.get(0).get(0).colModel;
    var col_widths = new Array(cm.getColumnCount());
    var col_hidden = new Array(cm.getColumnCount());
    for(i=0;i<cm.getColumnCount();i++) {
      col_widths[i] = cm.getColumnWidth(i);
      col_hidden[i] = cm.isHidden(i);
    }
    wc['column_widths'] = col_widths;
    wc['column_hidden'] = col_hidden;
    return wc;
  },
});


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
        console.log('setContextValues',this.name,this.contextParams,'=',values);
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
