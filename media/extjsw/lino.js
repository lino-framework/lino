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


/*
Based on feature request developed in http://extjs.net/forum/showthread.php?t=75751
*/
Ext.override(Ext.form.ComboBox, {
    contextParams : {}, 
    // contextParams : array of names of variables to add to query
    // contextValues : array of values of variables to add to query
    // queryContext : null, 
    // contextParam : null, 
    setValue : function(v,record){
        //~ if(this.name == 'country') console.log('20100531 country ComboBox.setValue()',v,record);
        var text = v;
        if(this.valueField){
          if(v === null) { 
              // console.log(this.name,'.setValue',v,'no lookup needed, value is null');
              v = null;
          } else if (record != undefined) {
            text = record.data[this.name];
            //~ console.log(this.name,'.setValue',v,'got text ',this.name,' from record ',record);
          } else {
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
        if(this.contextParams) Ext.apply(p,this.contextParams);
        //~ if(this.contextParams && this.contextValues) {
          //~ for(i = 0; i <= this.contextParams.length; i++)
            //~ p[this.contextParams[i]] = this.contextValues[i];
        //~ }
        return p;
    },
    setContextValue : function(name,value) {
      //~ console.log('setContextValue',this,this.name,':',name,'=',value);
      //~ if (this.contextValues === undefined) {
          //~ this.contextValues = Array(); // this.contextParams.length);
      //~ }
      if (this.contextParams[name] != value) {
        //~ console.log('setContextValue 1',this.contextParams);
        this.contextParams[name] = value;
        this.lastQuery = null;
        //~ console.log('setContextValue 2',this.contextParams);
      }
    }
});



function PseudoConsole() {
    this.log = function() {};
};
if (typeof(console) == 'undefined') console = new PseudoConsole();

Lino.notify = function(msg) {
  console.log(msg);
  //~ Ext.getCmp('konsole').update(msg);
  Ext.getCmp('konsole').update(msg.replace(/\n/g,'<br/>'));
};

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
    //~ console.log('save_wc_handler',panel.id,panel.getSize(),panel.getPosition());
    var pos = panel.getPosition();
    var size = panel.getSize();
    wc = ww.get_window_config();
    Ext.applyIf(wc,{ 
      x:pos[0],y:pos[1],height:size.height,width:size.width,
      maximized:panel.maximized});
    //~ console.log('save_wc_handler',ww,{url:ww.config.url_action,params:wc,method:'POST'});
    //~ Lino.do_action(ww,{url:ww.config.url_action,params:wc,method:'POST'});
    Lino.do_action(ww,{url:'/window_configs/'+ww.config.permalink_name,params:wc,method:'POST'});
  }
};



Lino.delete_selected = function(caller) {
  //~ console.log("Lino.delete_selected",caller);
  var pk_list = caller.get_selected();
  Ext.MessageBox.show({
    title: 'Confirmation',
    msg: "Delete " + String(pk_list.length) + " rows. Are you sure?",
    buttons: Ext.MessageBox.YESNOCANCEL,
    fn: function(btn) {
      if (btn == 'yes') {
        for ( var i=0; i < pk_list.length; i++ ) {
          Lino.do_action(caller,{method:'DELETE',url:caller.ls_data_url+'/'+pk_list[i]})
        }
        caller.refresh();
      }
      else Lino.notify("Dann eben nicht.");
    }
  });
};

Lino.do_action = function(caller,action) {
  action.success = function(response) {
    //~ console.log('Lino.do_action()',response,'action success');
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

Lino.tools_close_handler = function (ww) {
  return function() { 
      ww.close();
  }
};
Lino.permalink_handler = function (ww) {
  return function() { 
    document.location = ww.get_permalink();
    //~ document.location = "?permalink=" + ww.get_permalink();
    //~ document.location = "?permalink=" + ww.config.permalink_name +'()';
  }
};
//~ Lino.run_permalink = function() {
  //~ var plink = Lino.gup('permalink');
  //~ if(plink) { eval('Lino.'+plink); }
//~ }




Lino.ajax_error_handler = function(response,options) {
    console.log('AJAX failure:',response,options);
    // Ext.MessageBox.alert('Action failed','Lino server did not respond to Ajax request');
}
// Ext.Ajax.on('requestexception',Lino.ajax_error_handler)

Lino.main_menu = new Ext.Toolbar({});

// Path to the blank image should point to a valid location on your server
Ext.BLANK_IMAGE_URL = '/media/extjs/resources/images/default/s.gif'; // settings.MEDIA_URL


// used as Ext.grid.Column.renderer for id columns in order to hide the special id value -99999
Lino.id_renderer = function(value, metaData, record, rowIndex, colIndex, store) {
  //~ if (value == -99999) return '';
  if (record.phantom) return '';
  return value;
}

Lino.build_buttons = function(scope,actions) {
  if (actions) {
    var buttons = Array(actions.length);
    for(var i=0;i<actions.length;i++) { 
      //~ console.log("build_bbar",btn.text,":",actions[i]);
      if (actions[i].handler)
          actions[i].handler = actions[i].handler.createCallback(scope);
      buttons[i] = new Ext.Toolbar.Button(actions[i]);
      //~ var btn = {
        //~ text: actions[i].label
      //~ };
      //~ btn.handler = actions[i].handler.createCallback(scope);
      //~ buttons[i] = new Ext.Button(btn);
    }
    return buttons
  }
}

Lino.submit_detail = function(caller) {
  var rec = caller.get_current_record();
  if (rec) {
    //~ console.log('Save handler: this=',this);
    caller.form.submit({
      url:caller.ls_data_url + '/' + rec.id,
      method: 'PUT',
      scope: caller,
      success: function(form, action) {
        Lino.notify(action.result.msg);
        //~ this.caller.refresh();
      },
      failure: Lino.on_submit_failure,
      clientValidation: true
    })
  } else Lino.notify("Sorry, no current record.");
};

Lino.do_when_visible = function(cmp,todo) {
  //~ if (cmp.el && cmp.el.dom) 
  if (cmp.isVisible()) { 
    // 'visible' means 'rendered and not hidden'
    todo(); 
  } else { 
    //~ console.log('Lino.load_slavegrid() deferred',record);
    if (cmp.rendered) {
      cmp.on('show',todo,cmp,{single:true});
    } else {
      cmp.on('render',todo,cmp,{single:true});
    }
  }
  
};    


Lino.submit_insert = function(caller) {
  caller.form.submit({
    url:caller.ls_data_url,
    method: 'POST',
    scope: caller,
    success: function(form, action) {
      Lino.notify(action.result.msg);
      //~ this.caller.refresh();
    },
    failure: Lino.on_submit_failure,
    clientValidation: true
  })
};

Lino.FormPanel = Ext.extend(Ext.form.FormPanel,{
  constructor : function(config,params){
    if (params) 
      Ext.apply(config,params);
    config.bbar = Lino.build_buttons(this,config.ls_bbar_actions);
    //~ config.tbar = Lino.build_buttons(this,config.ls_tbar_actions);
    config.tbar = this.tbar_items().concat([
      this.first = new Ext.Toolbar.Button({tooltip:"First",disabled:true,handler:this.moveFirst,scope:this,iconCls:'x-tbar-page-first'}),
      this.prev = new Ext.Toolbar.Button({tooltip:"Previous",disabled:true,handler:this.movePrev,scope:this,iconCls:'x-tbar-page-prev'}),
      this.next = new Ext.Toolbar.Button({tooltip:"Next",disabled:true,handler:this.moveNext,scope:this,iconCls:'x-tbar-page-next'}),
      this.last = new Ext.Toolbar.Button({tooltip:"Last",disabled:true,handler:this.moveLast,scope:this,iconCls:'x-tbar-page-last'}),
      '->',
      this.displayItem = new Ext.Toolbar.TextItem({})
    ]);
    
    this.before_row_edit = config.before_row_edit.createDelegate(this);
    
    //~ config.bbar.push({
        //~ text: "Save", 
        //~ scope: this,
        //~ handler: Lino.submit_detail
      //~ });
    //~ console.log('20100629',this.ls_data_url);
    //~ config.bbar.push({
        //~ text: "Cancel", 
        //~ handler: function() { history.back()}
    //~ });
    Lino.FormPanel.superclass.constructor.call(this, config);
    //~ if (config.data_record) {
      //~ this.load_master_record(config.data_record);
      //~ return;
    //~ } 
  },
  moveFirst : function() {this.goto_record_id(this.current_record.navinfo.first)},
  movePrev : function() {this.goto_record_id(this.current_record.navinfo.prev)},
  moveNext : function() {this.goto_record_id(this.current_record.navinfo.next)},
  moveLast : function() {this.goto_record_id(this.current_record.navinfo.last)},
  goto_record_id : function(record_id) {
    //~ console.log('Lino.DetailWrapperBase.goto_record_id() calls Ajax');
    var this_ = this;
    Ext.Ajax.request({ 
      waitMsg: 'Loading record...',
      method: 'GET',
      url:this.ls_data_url + '/' + record_id,
      params: {query: this.search_field.getValue()},
      success: function(response) {
        if (response.responseText) {
            var rec = Ext.decode(response.responseText);
            //~ console.log('Lino.WindowWrapper.config.record_id success',rec);
            this_.load_master_record(rec);
            //~ this_.window.setTitle(rec.title);
        }
      },
      failure: Lino.ajax_error_handler
    });
  },
  load_master_record : function(record) {
    this.current_record = record;
    //~ console.log('20100531 Lino.DetailMixin.load_master_record',record);
    //~ this.config.main_panel.form.load(record);    
    if (record) {
      this.enable();
      this.form.loadRecord(record) 
      this.ww.window.setTitle(record.title);
      if (record.disabled_fields) {
        //~ console.log(20100617,record.disabled_fields);
        for (i in record.disabled_fields) {
            var fld = this.form.findField(record.disabled_fields[i]);
            if (fld) { 
              fld.disable(); 
            } else {
                console.log(20100617,record.disabled_fields[i], 'field not found');
            }
        }
      };
      if (record.navinfo) {
        this.first.setDisabled(!record.navinfo.first);
        this.prev.setDisabled(!record.navinfo.prev);
        this.next.setDisabled(!record.navinfo.next);
        this.last.setDisabled(!record.navinfo.last);
        this.displayItem.setText(record.navinfo.msg);
      }
    } else {
      this.form.reset();
      this.disable();
      this.ww.window.setTitle('');
      this.first.disable();
      this.prev.disable();
      this.next.disable();
      this.last.disable();
    }
    //~ console.log('20100531 Lino.DetailMixin.on_load_master_record',this.main_form);
    this.before_row_edit(record);
  },
  search_change : function(field,oldValue,newValue) {
    //~ console.log('search_change not yet implemented');
    this.moveFirst();
  },
  get_selected : function() { return [ this.current_record.id ] },
  get_current_record : function() {  
    //~ console.log(20100714,this.current_record);
    return this.current_record },
  load_picture_to : function(cmp,record) {
    //~ console.log('Lino.load_picture()',record);
    if (record)
      var src = this.ww.main_item.ls_data_url + "/" + record.id + "?fmt=image"
    else
      var src = 'empty.jpg';
    var f = function() {
      //~ console.log('Lino.load_picture()',src);
      cmp.el.dom.src = src;
      //~ this.el.dom.onclick = 'Lino.img_onclick(src)';
      //~ this.el.dom.onclick = 'window.open(src)';
      //~ cmp.el.on('click',function() {window.open(src)});
      
    };
    Lino.do_when_visible(cmp,f);
  }
});



    
Lino.GridPanel = Ext.extend(Ext.grid.EditorGridPanel,{
  clicksToEdit:2,
  enableColLock: false,
  viewConfig: {
          //autoScroll:true,
          //autoFill:true,
          //forceFit=True,
          //enableRowBody=True,
          showPreview:true,
          scrollOffset:200,
          emptyText:"Nix gefunden!"
        },
  
  constructor : function(config,params){
    if (params) Ext.apply(config,params);
    //~ this.ww = ww;
    config.store = new Ext.data.JsonStore({ 
      listeners: { exception: Lino.on_store_exception }, 
      //~ proxy: new Ext.data.HttpProxy({ url: config.ls_data_url+'?fmt=json', method: "GET" }), remoteSort: true, 
      proxy: new Ext.data.HttpProxy({ url: config.ls_data_url, method: "GET" }), remoteSort: true, 
      baseParams: {fmt:'json'}, 
      fields: config.ls_store_fields, 
      totalProperty: "count", 
      root: "rows", 
      //~ id: "id" });
      idProperty: config.ls_id_property });
      
    this.before_row_edit = config.before_row_edit.createDelegate(this);

    if (config.ls_quick_edit) {
      config.selModel = new Ext.grid.CellSelectionModel()
    } else { 
      config.selModel = new Ext.grid.RowSelectionModel() 
    };
    config.tbar = new Ext.PagingToolbar({ 
      prependButtons: true, pageSize: 10, displayInfo: true, 
      store: config.store, 
      items: this.tbar_items()
    });
    config.bbar = Lino.build_buttons(this,config.ls_bbar_actions);
    Lino.GridPanel.superclass.constructor.call(this, config);
    this.on('beforeedit',function(e) { this.before_row_edit(e.record)},this);
  },
  
  search_change : function(field,oldValue,newValue) {
    //~ console.log('search_change',field.getValue(),oldValue,newValue)
    this.store.setBaseParam('query',field.getValue()); // URL_PARAM_FILTER
    this.store.load({params: { start: 0, limit: this.getTopToolbar().pageSize }});
  },
  
  //~ on_beforeedit : function(e) {
    //~ console.log('20100723 GridPanel.on_beforeedit()',e);
  //~ },
  on_afteredit : function(e) {
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
    //~ p['grid_afteredit_colname'] = e.field;
    //~ p[e.field] = e.value;
    //~ console.log('20100723 GridPanel.on_afteredit()',e);
    // add value used by ForeignKeyStoreField CHOICES_HIDDEN_SUFFIX
    p[e.field+'Hidden'] = e.value;
    // p[pk] = e.record.data[pk];
    // console.log("grid_afteredit:",e.field,'=',e.value);
    Ext.apply(p,this.store.baseParams);
    var self = this;
    function after_success(result) {
      self.getStore().commitChanges(); // get rid of the red triangles
      self.getStore().reload();        // reload our datastore.
    };
    //~ console.log(e.record.id);
    if (e.record.phantom) {
      //~ p.id = undefined;
      Lino.do_action(this,{
        method:'POST',url: this.ls_data_url,
        params:p,
        after_success:after_success})
    } else {
      Lino.do_action(this,{
        method:'PUT',
        //~ url: caller.config.url_data+'/'+e.record.id, 
        url: this.ls_data_url+'/'+e.record.id, 
        params:p, 
        after_success:after_success});
    }
  },

  initComponent : function(){
    //~ console.log('Lino.GridMixin.setup 1',this);
    //~ this.tbar = this.pager;
    Lino.GridPanel.superclass.initComponent.call(this);
    this.on('afteredit', this.on_afteredit);
    // this.main_grid.on('cellcontextmenu', Lino.cell_context_menu, this);
    this.on('resize', function(cmp,aw,ah,rw,rh) {
        cmp.getTopToolbar().pageSize = cmp.calculatePageSize(this,aw,ah,rw,rh) || 10;
        cmp.refresh();
      }, this, {delay:500});
  },

  unused_search_keypress : function(field, e) {
    if(e.getKey() == e.RETURN) {
      //~ console.log('keypress',field.getValue(),store)
      this.main_grid.getStore().setBaseParam('query',field.getValue()); // URL_PARAM_FILTER
      this.main_grid.getStore().load({params: { start: 0, limit: this.getTopToolbar().pageSize }});
    }
  },
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
  refresh : function() { 
    this.store.load({params:{limit:this.getTopToolbar().pageSize,start:this.getTopToolbar().cursor}});
  },
  get_selected : function() {
    if (this.ls_quick_edit) {
        //~ console.log(this.getSelectionModel().selection);
        return [ this.getSelectionModel().selection.record.id ];
    } else {
        var sels = this.getSelectionModel().getSelections();
        return Ext.pluck(sels,'id');
    }
  },
  get_current_record : function() { 
    if (this.ls_quick_edit) {
        if (this.getSelectionModel().selection) return this.getSelectionModel().selection.record;
    } else {
        return this.getSelectionModel().getSelected();
    }
  },
  add_row_listener : function(fn,scope) {
    this.getSelectionModel().addListener('rowselect',fn,scope);
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
  },
  load_master_record : function(master_record) {
    if (master_record) {
      var todo = function() {
        //~ var src = caller.config.url_data + "/" + record.id + ".jpg"
        //~ console.log('Lino.load_slavegrid()',record);
        var p = this.ww.get_master_params(master_record);
        for (k in p) this.getStore().setBaseParam(k,p[k]);
        this.getStore().load(); 
      };
      Lino.do_when_visible(this,todo);
    } 
    //~ else console.log('load_slavegrid() : no record',record);
  }
  });
  

Lino.MainPanelMixin = {
  tbar_items : function() {
      return [ 
        this.search_field = new Ext.form.TextField({ 
          fieldLabel: "Search", 
          listeners: { scope:this, change:this.search_change }
          //~ scope:this, 
          //~ enableKeyEvents: true, 
          //~ listeners: { keypress: this.search_keypress }, 
          //~ id: "seachString" 
        }), 
        { scope:this, text: "csv", handler: function() { window.open(this.ls_data_url+'?fmt=csv') } } 
      ];
  }
};

Ext.override(Lino.GridPanel,Lino.MainPanelMixin);
Ext.override(Lino.FormPanel,Lino.MainPanelMixin);

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
  //~ console.log('on_load_menu before',response);
  var r = Ext.decode(response.responseText);
  // console.log('on_load_menu p',p);
  // Lino.viewport.hide();
  // Lino.viewport.remove(Lino.main_menu);
  if (! r.success) { 
    Lino.notify("on_load_menu() got unexpected resonse ",r);
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

Lino.template_handler = function(tpl,cmp) {
  return function(record) {
      //~ console.log(20100509,'Lino.template_handler',cmp);
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

Lino.PictureBoxPlugin = {
  init : function (cmp) {
      Lino.do_when_visible(cmp,function() { cmp.el.on('click',function() { Lino.img_onclick(cmp) }) });
      //~ cmp.el.on('click',Lino.img_click_handler(cmp.el.dom.src));
  }
}


Lino.img_onclick = function(cmp) {
  //~ console.log('img_onclick',cmp,arguments);
  window.open(cmp.el.dom.src);
};

Lino.SlavePlugin = function(caller) {
  this.caller = caller;
};
Lino.chooser_handler = function(combo,name) {
  return function(cmp,newValue,oldValue) {
    //~ console.log('Lino.chooser_handler()',cmp,oldValue,newValue);
    combo.setContextValue(name,newValue);
  }
};



Lino.ComboBox = Ext.extend(Ext.form.ComboBox,{
  triggerAction: 'all',
  submitValue: true,
  displayField: 'text', // ext_requests.CHOICES_TEXT_FIELD
  valueField: 'value' // ext_requests.CHOICES_VALUE_FIELD
});

Lino.ChoicesFieldElement = Ext.extend(Lino.ComboBox,{
  mode: 'local',
  forceSelection: false
});


Lino.SimpleRemoteComboStore = Ext.extend(Ext.data.JsonStore,{
  constructor: function(config){
      Lino.SimpleRemoteComboStore.superclass.constructor.call(this, Ext.apply(config, {
          totalProperty: 'count',
          root: 'rows',
          id: 'value', // ext_requests.CHOICES_VALUE_FIELD
          fields: ['value' ], // ext_requests.CHOICES_VALUE_FIELD, // ext_requests.CHOICES_TEXT_FIELD
          listeners: { exception: Lino.on_store_exception }
      }));
  }
});

Lino.ComplexRemoteComboStore = Ext.extend(Ext.data.JsonStore,{
  constructor: function(config){
      Lino.ComplexRemoteComboStore.superclass.constructor.call(this, Ext.apply(config, {
          totalProperty: 'count',
          root: 'rows',
          id: 'value', // ext_requests.CHOICES_VALUE_FIELD
          fields: ['value','text'], // ext_requests.CHOICES_VALUE_FIELD, // ext_requests.CHOICES_TEXT_FIELD
          listeners: { exception: Lino.on_store_exception }
      }));
  }
});

Lino.RemoteComboFieldElement = Ext.extend(Lino.ComboBox,{
  mode: 'remote',
  //~ typeAhead: true,
  //~ forceSelection:false,
  minChars: 2, // default 4 is to much
  queryDelay: 300, // default 500 is maybe slow
  queryParam: 'query', // ext_requests.URL_PARAM_FILTER)
  typeAhead: true,
  selectOnFocus: true, // select any existing text in the field immediately on focus.
  resizable: true
});

Lino.SimpleRemoteComboFieldElement = Ext.extend(Lino.RemoteComboFieldElement,{
  displayField: 'value', 
  valueField: null
});

Lino.old_WindowWrapperBase = {
  show : function() {
      //~ console.time('WindowWrapper.show()');
    //~ console.log('Lino.WindowWrapper.show',this);
      var main = Ext.getCmp('main_area');
      //~ main.suspendEvents();
      //~ main.hide();
      //~ console.log(main);
      var old = main.items.first();
      Lino.hidden_windows.push(old);
      //~ console.log(main.items);
      //~ Ext.apply(this.window,{autoSize: true});
      Ext.apply(this.window,{autoSize: true,id:'current_window'});
      //~ main.el.dom.innerHtml = '<div>coucou</div>'
      main.items.replace(this.window);
      //~ console.log(main.items);
      main.doLayout();
      //~ main.show();
      //~ main.resumeEvents();
      //~ console.timeEnd('WindowWrapper.show()');
  },
  close : function() { 
      //~ var main = Ext.getCmp('main_area');
      //~ main.items[0].destroy();
      var main = Ext.getCmp('main_area');
      var current = main.items.first();
      var w = Lino.hidden_windows.pop();
      if (w) { 
        main.items.replace(w);
      } else {
        main.removeAll();
      }
      current.destroy();
  }
};

Lino.WindowWrapperBase = {
  show : function() {
      //~ console.time('WindowWrapper.show()');
      //~ Ext.apply(this.window,{renderTo: 'main_area'});
      this.window.show();
  },
  close : function() { 
      this.window.close();
  }
};


Lino.IndexWrapper = function(config) {
  Ext.apply(config,{layout:'fit',maximized:true, constrain: true, renderTo: 'main_area'});
  //~ this.window = new Ext.Panel(config);
  this.window = new Ext.Window(config);
};

Ext.override(Lino.IndexWrapper,Lino.WindowWrapperBase);

Lino.WindowWrapper = function(caller,config,params) {
  console.log('Lino.WindowWrapper.constructor',config);
  //~ console.time('WindowWrapper.constructor()');
  this.caller = caller;
  this.config = config; 
  //~ this.config = config_fn(this); 
  if (params) 
    Ext.apply(this.config,params);
  this.slaves = {};
  //~ this.before_row_edit = config.before_row_edit.createDelegate(this);
  if (this.config.actions) {
      console.log('config.actions no longer used!!!');
  }
  //~ console.log('Lino.WindowWrapper.constructor',config.title,'gonna call setup.');
  this.setup();
  this.main_item.ww = this;
  if (config.data_record) {
    //~ console.log('Lino.WindowWrapper with data_record');
    this.main_item.load_master_record(config.data_record);
    return;
  } 
  if (config.record_id) {
    this.main_item.goto_record_id(config.record_id);
  }
  //~ console.timeEnd('WindowWrapper.constructor()');
  //~ console.log('Lino.WindowWrapper.constructor',config.title,'returned from setup');
};

Ext.override(Lino.WindowWrapper,Lino.WindowWrapperBase);

//~ Lino.hidden_windows = [];

//~ Ext.apply(Lino.WindowWrapper.prototype,{
Ext.override(Lino.WindowWrapper,{
  closeAction : 'close',
  setup : function() { 
    //~ console.log('Lino.WindowWrapper.setup',this);
    this.window = new Ext.Window({ 
      layout: "fit", 
      maximized: true,
      renderTo: 'main_area', constrain: true,
      //~ autoHeight: true,
      title: this.config.title,
      items: this.main_item, 
      //~ bbar: this.bbar_actions,
      //~ bbar: Lino.build_buttons(this,this.config.ls_bbar_actions),
      tools: [ 
        { qtip: this.config.qtip, handler: Lino.save_wc_handler(this), id: "save" }, 
        { qtip: 'permalink', handler: Lino.permalink_handler(this), id: "pin" },
        { qtip: 'close', handler: Lino.tools_close_handler(this), id: "close" } 
      ] 
    });
    this.window.window_wrapper = this;
    //~ console.log('Lino.WindowWrapper.setup done',this);
  },
  get_current_record : function() { 
    //~ if (this.main_item) return this.main_item.get_current_record()
    return this.main_item.get_current_record()
  },
  get_selected : function() { 
    return this.main_item.get_selected();
  },
  get_master_params : function(record) {
    var p = {}
    p['mt'] = this.config.content_type; // ext_requests.URL_PARAM_MASTER_TYPE
    if (record) {
      if (record.phantom) {
          p['mk'] = undefined; // ext_requests.URL_PARAM_MASTER_PK
      }else{
          p['mk'] = record.id; // ext_requests.URL_PARAM_MASTER_PK
      }
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
  get_permalink : function() {
      return this.main_item.ls_data_url + '?fmt=grid';
      //~ return this.config.permalink_name+'()'  ;
  },
  on_render : function() {},
  refresh : function() {},
  hide : function() { this.window.hide() },
  get_window_config : function() { return {} }
  
});



Lino.GridMixin = {
  setup : function() {
    //~ console.log('Lino.GridMixin.setup',this);
    //~ console.log('Lino.GridMixin.setup 2',this);
    //~ this.main_grid = new Lino.GridPanel({ clicksToEdit: 2, xtype: "container", tbar: this.pager, 
      //~ selModel: new Ext.grid.RowSelectionModel({singleSelect:false}), 
      //~ emptyText: "Nix gefunden...", 
      //~ // bbar: this.bbar_actions, 
      //~ viewConfig: { showPreview: true, scrollOffset: 200, emptyText: "Nix gefunden!" }, 
      //~ enableColLock: false, store: this.store, colModel: this.config.colModel });
      
    //~ this.main_item = this.main_grid;
    this.main_item = this.config.main_panel;
    //~ this.main_item.on('beforeedit',this.main_item.on_beforeedit,this);
      
    Lino.WindowWrapper.prototype.setup.call(this);
  },
  refresh : function() { 
    this.main_item.refresh();
  },
  //~ get_selected : function() {
    //~ var sels = this.main_item.getSelectionModel().getSelections();
    //~ return Ext.pluck(sels,'id');
  //~ },
  get_window_config : function() {
    var wc = { window_config_type: 'grid' };
    wc['column_widths'] = Ext.pluck(this.main_item.colModel.columns,'width');
    return wc;
  }
};

Lino.GridMasterWrapper = Ext.extend(Lino.WindowWrapper,Lino.GridMixin);
Lino.GridMasterWrapper.override({
  add_row_listener : function(fn,scope) {
    // this.main_grid.add_row_listener(fn,scope);
    this.main_item.getSelectionModel().addListener('rowselect',fn,scope);
    //~ console.log(20100509,'Lino.GridMasterWrapper.add_row_listener',this.config.title);
  }
});


//~ Lino.SlaveMixin = {
  //~ closeAction : 'hide',
  //~ add_row_listener : function(fn,scope) {
    //~ this.caller.add_row_listener(fn,scope);
  //~ }
//~ };


//~ Lino.GridSlaveWrapper = Ext.extend(Lino.WindowWrapper,{});
//~ Lino.GridSlaveWrapper.override(Lino.SlaveMixin);
//~ Lino.GridSlaveWrapper.override(Lino.GridMixin);
//~ Lino.GridSlaveWrapper.override({
  //~ unused_load_master_record : function(record) {
    //~ Lino.load_slavegrid(this.caller,this.main_grid,record);
  //~ }
//~ });

//~ Lino.DetailSlaveWrapper = Ext.extend(Lino.WindowWrapper,{});
//~ Lino.DetailSlaveWrapper.override(Lino.SlaveMixin);
//~ Lino.DetailSlaveWrapper.override({
  //~ setup:function() {
    //~ this.main_item = this.config.main_panel;
    //~ Lino.WindowWrapper.prototype.setup.call(this);
    //~ this.main_form = this.main_item;
  //~ }
//~ });

Lino.DetailWrapperBase = Ext.extend(Lino.WindowWrapper, {});
Lino.DetailWrapperBase.override({
  on_submit: function() {
    this.main_form.form.submit({
      //~ url:this.caller.config.url_data + '/' + this.config.record_id,
      url:this.main_item.ls_data_url + '/' + this.config.record_id,
      //~ params: this.caller.get_master_params(this.caller.get_current_record()),
      method: 'PUT',
      scope: this,
      success: function(form, action) {
        Lino.notify(action.result.msg);
        //~ this.close();
        this.caller.refresh();
      },
      failure: Lino.on_submit_failure,
      clientValidation: true
    })
  },
  setup:function() {
    //~ console.log('Lino.DetailSlaveWrapper setup',20100409,this);
    this.main_item = this.config.main_panel;
    //~ this.bbar_actions = [
      //~ {
        //~ text: "Submit", 
        //~ scope: this,
        //~ handler: this.on_submit
      //~ },
      //~ { text: "Cancel", scope: this, handler: function() { this.close()} }
    //~ ];
    //~ var row_actions = Lino.build_buttons(this,this.config.ls_bbar_actions);
    //~ if (row_actions) this.bbar_actions = this.bbar_actions.concat(row_actions);
    //~ this.bbar_actions = Lino.build_buttons(this,this.config.ls_bbar_actions);
    
    Lino.WindowWrapper.prototype.setup.call(this);
    //~ this.main_form = this.window.getComponent(0);
    
  }
})

Lino.DetailWrapper = Ext.extend(Lino.DetailWrapperBase, {
  setup:function() {
    Lino.DetailWrapperBase.prototype.setup.call(this);
  },
  get_permalink : function() {
    //~ return this.config.permalink_name +'(undefined,{record_id:'+this.current_record.id+'})';
    return this.main_item.ls_data_url+'/'+this.main_item.current_record.id + '?fmt=detail';
  }
});

Lino.InsertWrapper = Ext.extend(Lino.DetailWrapperBase, {
  get_permalink : function() {
    //~ return this.config.permalink_name +'(undefined,{record_id:'+this.current_record.id+'})';
    return this.main_item.ls_data_url+'?fmt=insert';
  },
  on_submit: function() {
    this.main_form.form.submit({
      //~ url:this.caller.config.url_data,
      //~ url:this.caller.ls_data_url,
      url:this.main_item.ls_data_url,
      //~ params: this.caller.get_master_params(this.caller.get_current_record()),
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

Ext.override(Ext.form.BasicForm,{
    loadRecord : function(record){
        var field, id;
        for(id in record.data){
            if(!Ext.isFunction(record.data[id]) && (field = this.findField(id))){
                field.setValue(record.data[id],record);
                if(this.trackResetOnLoad){
                    field.originalValue = field.getValue();
                }
            }
        }
        return this;
    }
});
