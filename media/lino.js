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

function PseudoConsole() {
    this.log = function() {};
};
if (typeof(console) == 'undefined') console = new PseudoConsole();

Lino.notify = function(msg) {
  console.log(msg);
  //~ Ext.getCmp('konsole').update(msg);
  Ext.getCmp('konsole').update(msg.replace(/\n/g,'<br/>'));
};

//~ Lino.debug = function() {
  //~ if(typeof(console)!="undefined") console.log(arguments);
//~ };

Lino.show_about = function() {
  new Ext.Window({
    width: 400, height: 400,
    title: "About",
    html: '<a href="http://www.extjs.com" target="_blank">ExtJS</a> version ' + Ext.version
  }).show();
};

Lino.on_store_exception = function (store,type,action,options,reponse,arg) {
  console.log("on_store_exception:",store,type,action,options,reponse,arg);
};

Lino.on_submit_success = function(form, action) {
   Lino.notify(action.result.msg);
   this.close();
};

Lino.on_submit_failure = function(form, action) {
    switch (action.failureType) {
        case Ext.form.Action.CLIENT_INVALID:
            Ext.Msg.alert('Failure', 'Form fields may not be submitted with invalid values');
            break;
        case Ext.form.Action.CONNECT_FAILURE:
            Ext.Msg.alert('Failure', 'Ajax communication failed');
            break;
        case Ext.form.Action.SERVER_INVALID:
           Ext.Msg.alert('Failure', action.result.msg);
   }
};




Lino.save_wc_handler = function(ww) {
  return function(event,toolEl,panel,tc) {
    //~ var url = ww.config.url_action;
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
    Lino.do_action(ww,{url:ww.config.url_action,params:wc,method:'POST'});
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


Lino.grid_afteredit_handler = function (caller) {
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
    Ext.apply(p,caller.store.baseParams);
    function after_success(result) {
      caller.main_grid.getStore().commitChanges(); // get rid of the red triangles
      caller.main_grid.getStore().reload();        // reload our datastore.
    };
    //~ console.log(e.record.id);
    if (e.record.id == -99999) {
      Lino.do_action(caller,{
        method:'POST',url: caller.config.url_data,
        params:p,after_success:after_success})
    } else 
      Lino.do_action(caller,{
        method:'PUT',url: caller.config.url_data+'/'+e.record.id, 
        params:p, after_success:after_success});
    //~ Ext.Ajax.request({
      //~ waitMsg: 'Please wait...',
      //~ method: 'PUT',
      //~ url: caller.config.url_data + '/' + e.record.id,
      //~ params: p, 
      //~ success: on_success,
      //~ failure: Lino.ajax_error_handler
    //~ })
  }
};


Lino.delete_selected = function(caller) {
  var pk_list = caller.get_selected();
  Ext.MessageBox.show({
    title: 'Confirmation',
    msg: "Delete " + String(pk_list.length) + " rows. Are you sure?",
    buttons: Ext.MessageBox.YESNOCANCEL,
    fn: function(btn) {
      if (btn == 'yes') {
        //~ for (i in pk_list) {
        for ( var i=0; i < pk_list.length; i++ ) {
          Lino.do_action(caller,{method:'DELETE',url:caller.config.url_data+'/'+pk_list[i]})
        }
        //~ pk_list.forEach(function(pk) {
          //~ Lino.do_action(caller,{method:'DELETE',url:caller.config.url_data+'/'+pk})
        //~ });
        caller.refresh();
      }
      else Lino.notify("Dann eben nicht.");
    }
  });
};

Lino.do_action = function(caller,action) {
  action.success = function(response) {
    //~ console.log('Lino.do_action()',action,'action success');
    if (response.responseText) {
      var result = Ext.decode(response.responseText);
      //~ console.log('Lino.do_action()',action.name,'result is',result);
      if (result.success && action.after_success) action.after_success(result);
      if (result.alert_msg) Ext.MessageBox.alert('Alert',result.alert_msg);
      if (result.message) Lino.notify(result.message);
      if (result.notify_msg) Lino.notify(result.notify_msg);
      if (result.js_code) { 
        //~ console.log('Lino.do_action()',action,'gonna call js_code in',result);
        var jsr = result.js_code(caller);
        //~ console.log('Lino.do_action()',action,'returned from js_code in',result);
        if (action.after_js_code) {
          //~ console.log('Lino.do_action()',action,'gonna call after_js_code');
          action.after_js_code(jsr);
          //~ console.log('Lino.do_action()',action,'returned from after_js_code');
        //~ } else {
          //~ console.log('Lino.do_action()',action,' : after_js_code is false');
        }
      };
      //~ if (result.show_window) {
        //~ var ww = result.show_window(caller);
        //~ ww.show();
      //~ };
      //~ if (result.redirect) window.open(result.redirect);
      //~ if (result.refresh_caller && caller) caller.refresh();
      //~ if (result.close_caller && caller) {
        //~ caller.close();
      //~ }
      //~ if (result.refresh_menu) Lino.load_main_menu();
      //~ if (result.confirm_msg) {
        //~ Ext.MessageBox.show({
          //~ title: 'Confirmation',
          //~ msg: result.confirm_msg,
          //~ buttons: Ext.MessageBox.YESNOCANCEL,
          //~ fn: function(btn) {
            //~ if (btn == 'yes') step_dialog(result);
            //~ else abort_dialog(result);
          //~ }
        //~ })
      //~ }
    }
  };
  Ext.applyIf(action,{
    waitMsg: 'Please wait...',
    failure: Lino.ajax_error_handler
  });
  Ext.Ajax.request(action);
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
};    

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
  //~ Lino.debug("run_permalink");
  var links = Lino.gup('permalink').split(',');
  for ( i=0; i < links.length; i++ ) {
  //~ for ( i in links ) {
    //~ console.log(links[i]);
    // if(windows[i]) eval(windows[i]+".show()");
    // if(windows[i]) Lino.do_action(undefined,'/permalink_do/'+windows[i],windows[i],{});
    if(links[i]) {
      Lino.do_action(undefined,{url:'/ui/'+links[i],method:'GET'});
      //~ var a = links[i].split('.');
      //~ if (a.length == 2) {
          //~ Lino.do_dialog(undefined,'/action/'+a[0]+'/'+a[1],{});
      //~ }
    }
  }
}



Lino.ajax_error_handler = function(response,options) {
    Lino.notify('AJAX failure:'+String(response)+','+String(options));
    // Ext.MessageBox.alert('Action failed','Lino server did not respond to Ajax request');
}
// Ext.Ajax.on('requestexception',Lino.ajax_error_handler)

//~ Lino.submit_property = function (caller,e) {
Lino.unused_submit_property_handler = function(caller) { 
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
    // var p = e.record.data;
    var p = caller.get_master_params(caller.get_current_record());
    // p['grid_afteredit_colname'] = e.field;
    // p[e.field] = e.value;
    //~ console.log('submit_property()',e.record.data);
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
  }
};
Lino.submit_property_handler = function(caller) { 
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
    // var p = e.record.data;
    //~ var p = caller.get_master_params(caller.get_current_record());
    // p['grid_afteredit_colname'] = e.field;
    // p[e.field] = e.value;
    //~ console.log('submit_property()',e.record.data);
    var rec = caller.get_current_record();
    var p = {}
    //~ p['property_'+e.record.data.name] = e.record.data.value
    p[e.record.data.name] = e.record.data.value
    Ext.Ajax.request({
      method: 'PUT',
      waitMsg: 'Please wait...',
      url: caller.config.url_data + '/' + rec.id,
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
  }
};
Lino.unused2_submit_property_handler = function(caller) { 
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
    // var p = e.record.data;
    var p = caller.get_master_params(caller.get_current_record());
    // p['grid_afteredit_colname'] = e.field;
    // p[e.field] = e.value;
    //~ console.log('submit_property()',e.record.data);
    p['name'] = e.record.data.name
    p['value'] = e.record.data.value
    Ext.Ajax.request({
      method: 'POST',
      waitMsg: 'Please wait...',
      url: '/api/properties/PropValuesByOwner',
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
  }
};

Lino.load_properties = function(caller,pw,url,record) { 
  //~ console.log('load_properties',caller,url,record);
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
Ext.BLANK_IMAGE_URL = '/media/extjs/resources/images/default/s.gif'; // settings.MEDIA_URL


// used as Ext.grid.Column.renderer for id columns in order to hide the special id value -99999
Lino.id_renderer = function(value, metaData, record, rowIndex, colIndex, store) {
  if (value == -99999) return '';
  return value;
}



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
    //~ console.log('GridPanel.postEdit()',value, originalValue, r, field);
    return value;
  }
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
  var r = Ext.decode(response.responseText);
  // console.log('on_load_menu p',p);
  // Lino.viewport.hide();
  // Lino.viewport.remove(Lino.main_menu);
  if (! r.success) { 
    console.log("on_load_menu() got unexpected resonse ",r);
    return; 
  }
  if (r.message) Lino.notify(r.message);
  Lino.main_menu.removeAll();
  Lino.main_menu.add(r.load_menu);
  Lino.main_menu.add({text:"Help",menu:[{
    text:"About", handler: Lino.show_about
  }]});
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
    method: 'GET',
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



Lino.button_handler = function(caller,action) {
  //~ var action = caller.config.bbar_actions[i];
  Ext.applyIf(action, {
    params : {},
    method:'GET'
  });
  return function(event) {
    action.params.selected = caller.get_selected(); // POST_PARAM_SELECTED
    //~ Ext.apply(action.params,caller.get_base_params());
    Lino.do_action(caller,action);
  }
};

Lino.toggle_button_handler = function(master,action) {
  //~ var action = master.config.bbar_actions[i];
  Ext.applyIf(action, {params : {}, method:'GET'});
  return function(btn,state) {
    if (master.slaves[action.name] == 'loading') {
      Lino.notify('loading...');
      return;
    }
    if(state) { 
      if (master.slaves[action.name]) {
        //~ console.log('Lino.toggle_button_handler() ',master,action.name,' exists : show again.');
        master.slaves[action.name].show();
      } else {
        master.slaves[action.name] = 'loading';
        //~ console.log('Lino.toggle_button_handler() ',master,action.name,'=',master.slaves[action.name]);
        Ext.apply(action.params,master.get_master_params(master.get_current_record()));
        //~ action.params.selected = caller.get_selected(); // POST_PARAM_SELECTED
        action.after_js_code = function(slave) { 
          master.slaves[action.name] = slave;
          //~ console.log('Lino.toggle_button_handler.after_js_code() ',caller,action.name,'=',caller.slaves[action.name]);
          // when master closes, close slave:
          master.window.on('close',function() { slave.close() });
          // when master hides, hide slave:          
          master.window.on('hide',function(){ slave.hide()});
          // when slave's close button is clicked, toggle button off:
          slave.window.on('hide',function(){ btn.toggle(false,false)});
          // when slave is shown, update it's data:
          slave.window.on('show',function(){ slave.on_master_change(master.get_current_record())});
          //~ js_result.on_master_change(caller.get_current_record());
          master.add_row_listener( function(sm,ri,rec){slave.on_master_change(rec)}, slave );
          // js_result.on_master_change(caller.get_current_record());
          
          // show slave:
          slave.show();
        };
        Lino.do_action(master,action);
      }
    } else {
      master.slaves[action.name].hide();
    }
  }
};


Lino.WindowWrapper = function(caller,config) {
  //~ console.log('Lino.WindowWrapper.constructor',config.title,' : caller is ',caller);
  this.caller = caller;
  this.config = config; 
  this.slaves = {};
  if (config.actions) {
      this.bbar_actions = Array(config.actions.length);
      for(var i=0;i<config.actions.length;i++) { 
        var btn = {
          text: config.actions[i].label
        };
        if (config.actions[i].opens_a_slave) {
          btn.toggleHandler = Lino.toggle_button_handler(this,config.actions[i]);
          btn.enableToggle = true;
        } else  {
          btn.handler = Lino.button_handler(this,config.actions[i]);
        }
        this.bbar_actions[i] = new Ext.Button(btn);
      }
      //~ Lino.debug(this.bbar_actions);
  }
  //~ console.log('Lino.WindowWrapper.constructor',config.title,'gonna call setup.');
  this.setup();
  //~ console.log('Lino.WindowWrapper.constructor',config.title,'returned from setup');
};
//~ Ext.apply(Lino.WindowWrapper.prototype,{
Ext.override(Lino.WindowWrapper,{
  closeAction : 'close',
  show : function() {
    //~ console.log('Lino.WindowWrapper.show',this);
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
  //~ get_base_params : function() { return {} },
  get_values : function() {
    var v = {};
    return v;
  },
  setup : function() { 
    //~ console.log('Lino.WindowWrapper.setup',this);
    this.window = new Ext.Window({ layout: "fit", title: this.config.title, items: this.main_item, 
      height: this.config.wc.height, width: this.config.wc.width, maximizable: true, maximized: this.config.wc.maximized, 
      y: this.config.wc.y, x: this.config.wc.x, 
      closeAction:this.closeAction,
      bbar: this.bbar_actions,
      tools: [ { qtip: this.config.qtip, handler: Lino.save_wc_handler(this), id: "save" } ] 
      });
    this.window.window_wrapper = this;
    //~ console.log('Lino.WindowWrapper.setup done',this);
    //~ if (this.caller) this.window._permalink_name = this.config.permalink_name;
    //~ this.window.on('beforeshow',this.on_render,this)
    //~ this.window.on('beforerender',this.on_render,this)
  },
  on_render : function() {},
  refresh : function() {},
  hide : function() { this.window.hide() },
  close : function() { this.window.close() },  
  get_window_config : function() { return {} }
});

Lino.template_handler = function(tpl,cmp) {
  return function(record) {
      console.log(20100509,'Lino.template_handler',cmp);
      if (cmp.el) tpl.overwrite(cmp.el,record.data);
      //~ cmp.el = 'foo <img src="/media/images/empty.jpg"/> bar'
  }
};
Lino.TemplateBoxPlugin = function(caller,s) {
  this.tpl = new Ext.XTemplate(s);
  this.caller = caller;
};
Ext.override(Lino.TemplateBoxPlugin,{
  init : function (cmp) {
    this.caller.add_row_listener(Lino.template_handler(this.tpl,cmp));
    //~ function(record) {
      //~ this.tpl.overwrite(cmp.body,{'national_id':'123'});
    //~ });
  }
});

Lino.load_picture = function(caller,cmp,record) {
  if (record && cmp.el) {
    var src = caller.config.url_data + "/" + record.id + ".jpg"
    //~ console.log('Lino.load_picture()',src);
    cmp.el.dom.src = src; 
  } else console.log('Lino.load_picture() no record or cmp not rendered',caller,cmp,record);
}
//~ Lino.PictureBox_handler = function(caller,cmp) {
  //~ return function(sm,ri,record) {
      //~ console.log(20100509,'Lino.imgbox_handler',caller,record,cmp);
      //~ if (record && cmp.el) {
        //~ cmp.el.dom.src = caller.config.url_data + "/" + record.id + ".jpg"; 
      //~ }
      
  //~ }
//~ };
Lino.PictureBoxPlugin = function(caller) {
  this.caller = caller;
};
Ext.override(Lino.PictureBoxPlugin,{
  init : function (cmp) {
    //~ console.log('Lino.PictureBoxPlugin.init()',this);
    cmp.on('render',function(){ Lino.load_picture(this.caller,cmp,this.caller.get_current_record())},this);
    this.caller.add_row_listener(function(sm,ri,rec) { Lino.load_picture(this.caller,cmp,rec) }, this );
    //~ this.caller.add_row_listener(Lino.PictureBox_handler(this.caller,cmp));
    //~ function(record) {
      //~ this.tpl.overwrite(cmp.body,{'national_id':'123'});
    //~ });
  }
});



Lino.GridMixin = {
  setup : function() {
    //~ console.log('Lino.GridMixin.setup',this);
    this.store = new Ext.data.JsonStore({ 
      listeners: { exception: Lino.on_store_exception }, 
      proxy: new Ext.data.HttpProxy({ url: this.config.url_data+'.json', method: "GET" }), remoteSort: true, 
      fields: this.config.fields, 
      totalProperty: "count", 
      root: "rows", 
      id: "id" });
    //~ console.log('Lino.GridMixin.setup 1',this);
    this.pager = new Ext.PagingToolbar({ 
      prependButtons: true, pageSize: 10, displayInfo: true, 
      store: this.store, 
      items: [ 
        { xtype: "textfield", 
          fieldLabel: "Search", 
          listeners: { scope:this, change:this.search_change }
          //~ scope:this, 
          //~ enableKeyEvents: true, 
          //~ listeners: { keypress: this.search_keypress }, 
          //~ id: "seachString" 
        }, 
        { scope:this, text: "csv", handler: function() { window.open(this.config.url_data+'.csv') } } 
      ]});
    //~ console.log('Lino.GridMixin.setup 2',this);
    
    this.main_grid = new Lino.GridPanel({ clicksToEdit: 2, xtype: "container", tbar: this.pager, 
      selModel: new Ext.grid.RowSelectionModel({singleSelect:false}), 
      emptyText: "Nix gefunden...", 
      //~ bbar: this.bbar_actions, 
      viewConfig: { showPreview: true, scrollOffset: 200, emptyText: "Nix gefunden!" }, 
      enableColLock: false, store: this.store, colModel: this.config.colModel });
      
    this.main_item = this.main_grid;
      
    this.main_grid.on('afteredit', Lino.grid_afteredit_handler(this));
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
    if (this.main_grid) return this.main_grid.getSelectionModel().getSelected();
  },
  unused_search_keypress : function(field, e) {
    if(e.getKey() == e.RETURN) {
      console.log('keypress',field.getValue(),store)
      this.main_grid.getStore().setBaseParam('query',field.getValue()); // URL_PARAM_FILTER
      this.main_grid.getStore().load({params: { start: 0, limit: this.pager.pageSize }});
    }
  },
  search_change : function(field,oldValue,newValue) {
    //~ console.log('search_change',field.getValue(),oldValue,newValue)
    this.main_grid.getStore().setBaseParam('query',field.getValue()); // URL_PARAM_FILTER
    this.main_grid.getStore().load({params: { start: 0, limit: this.pager.pageSize }});
  },
  refresh : function() { 
    this.store.load({params:{limit:this.pager.pageSize,start:this.pager.cursor}});
  },
  get_selected : function() {
    //~ var sel_pks = '';
    var sels = this.main_grid.getSelectionModel().getSelections();
    return Ext.pluck(sels,'id');
    //~ for(var i=0;i<sels.length;i++) { sel_pks += sels[i].id + ','; };
    //~ return sel_pks;
  }
  
};

Lino.GridMasterWrapper = Ext.extend(Lino.WindowWrapper,Lino.GridMixin);
Lino.GridMasterWrapper.override({
  add_row_listener : function(fn,scope) {
    // this.main_grid.add_row_listener(fn,scope);
    this.main_grid.getSelectionModel().addListener('rowselect',fn,scope);
    //~ console.log(20100509,'Lino.GridMasterWrapper.add_row_listener',this.config.title);
  }
});


Lino.SlaveMixin = {
  closeAction : 'hide',
  add_row_listener : function(fn,scope) {
    this.caller.add_row_listener(fn,scope);
  }
  //~ get_base_params : function() { return this.caller.get_master_params(this.caller.get_current_record()) }
};

Lino.DetailMixin = {
  get_selected : function() { return [ this.current_record.id ] },
  get_current_record : function() {  return this.current_record },
  on_master_change : function(record) {
    this.current_record = record;
    //~ console.log('Lino.DetailMixin.on_master_change',record);
    //~ this.config.main_panel.form.load(record);    
    if (record) {
      this.main_form.enable();
      this.main_form.form.loadRecord(record) 
    } else {
      this.main_form.form.reset();
      this.main_form.disable();
    }
  }
};



Lino.GridSlaveWrapper = Ext.extend(Lino.WindowWrapper,{});
Lino.GridSlaveWrapper.override(Lino.SlaveMixin);
Lino.GridSlaveWrapper.override(Lino.GridMixin);
Lino.GridSlaveWrapper.override({
  on_master_change : function(record) {
    //~ this.current_record = record;
    console.log('GridSlaveWrapper.on_master_change()',record)
    var p = this.caller.get_master_params(record);
    for (k in p) this.store.setBaseParam(k,p[k]);
    this.store.load(); // {params:this.get_master_params(record)}); 
  }
});

Lino.DetailSlaveWrapper = Ext.extend(Lino.WindowWrapper,{});
Lino.DetailSlaveWrapper.override(Lino.SlaveMixin);
Lino.DetailSlaveWrapper.override(Lino.DetailMixin);
Lino.DetailSlaveWrapper.override({
  setup:function() {
    //~ console.log('Lino.DetailSlaveWrapper setup',20100409,this);
    this.main_item = this.config.main_panel;
    this.bbar_actions = [
      {
        text: "Save", 
        scope: this,
        handler: function() {
          var rec = this.get_current_record();
          if (rec) {
            //~ console.log('Save handler: this=',this);
            this.main_form.form.submit({
              url:this.caller.config.url_data + '/' + rec.id,
              method: 'PUT',
              scope: this,
              success: function(form, action) {
                Lino.notify(action.result.msg);
                this.caller.refresh();
              },
              failure: Lino.on_submit_failure,
              clientValidation: true
            })
          } else Lino.notify("Sorry, no current record.");
        }
      },
      { text: "Cancel", scope: this, handler: function() { this.close()} }
    ];
    Lino.WindowWrapper.prototype.setup.call(this);
    this.main_form = this.window.getComponent(0);
    //~ Lino.SlaveMixin.prototype.setup.call(this);
  }
});
//~ Ext.override(Lino.DetailSlaveWrapper,Lino.DetailMixin);

Lino.InsertWrapper = Ext.extend(Lino.WindowWrapper, {});
Lino.InsertWrapper.override(Lino.DetailMixin);
Lino.InsertWrapper.override({
  setup:function() {
    //~ console.log('Lino.DetailSlaveWrapper setup',20100409,this);
    this.main_item = this.config.main_panel;
    this.bbar_actions = [
      {
        text: "Submit", 
        scope: this,
        handler: function() {
          this.main_form.form.submit({
            url:this.caller.config.url_data,
            params: this.caller.caller.get_master_params(this.caller.caller.get_current_record()),
            method: 'POST',
            scope: this,
            success: function(form, action) {
              Lino.notify(action.result.msg);
              this.close();
              this.caller.refresh();
            },
            failure: Lino.on_submit_failure,
            clientValidation: true
          })
        }
      },
      { text: "Cancel", scope: this, handler: function() { this.close()} }
    ];
    //~ this.main_item.bbar = this.config.bbar_actions;
    //~ this.main_item = Ext.Panel({
        //~ items: this.config.main_panel,
        //~ bbar: this.config.bbar_actions,
        //~ autoScroll: true,});
    Lino.WindowWrapper.prototype.setup.call(this);
    this.main_form = this.window.getComponent(0);
    //~ var data = {};
    //~ if (this.config.fk_name) {
      //~ var master = this.caller.caller.get_current_record();
      //~ if (master) {
          //~ data[this.config.fk_name+'Hidden'] = master.id;
      //~ }
    //~ }
    //~ var rec = new this.caller.store.recordType(data);
    //~ var rec = new this.caller.store.recordType(this.config.formdata);
    var rec = this.caller.store.getById(-99999);
    console.log(rec);
    this.on_master_change(rec);
  }
})

Lino.PropertiesWrapper = Ext.extend(Lino.WindowWrapper, {});
Lino.PropertiesWrapper.override(Lino.SlaveMixin);
Lino.PropertiesWrapper.override({
  setup : function() {
    // console.log('Lino.GridMasterWrapper configure',20100401,this);
    this.main_item = this.config.main_panel;
    //~ Ext.applyIf(this.main_item,{listeners: {}});
    //~ Ext.apply(this.main_item.listeners,{afteredit: Lino.submit_property_handler(this)});
    //~ this.main_item.listeners = {afteredit: Lino.submit_property_handler(this)};
    Lino.WindowWrapper.prototype.setup.call(this);
    //~ Lino.SlaveMixin.prototype.setup.call(this);
  },
  get_current_record : function() {  return this.caller.get_current_record() },
  on_master_change : function(rec) {
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
  }
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
