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


/**
 Thanks to Animal <http://www.sencha.com/forum/showthread.php?12288-OPEN-635-Ext.Button-config-option-href-foo>

 and to grEvenX <http://www.sencha.com/forum/showthread.php?97659-Ext.LinkButton-code-from-Animal-needs-update-for-ExtJS-3.2>

 * @class Ext.LinkButton
 * @extends Ext.Button
 * A Button which encapsulates an &lt;a> element to enable navigation, or downloading of files.
 * @constructor
 * Creates a new LinkButton
 */ 
Ext.LinkButton = Ext.extend(Ext.Button, {
  template: new Ext.Template(
        '<table id="{4}" cellspacing="0" class="x-btn {3}"><tbody class="{1}">',
            '<tr><td class="x-btn-tl"><i> </i></td><td class="x-btn-tc"></td><td class="x-btn-tr"><i> </i></td></tr>',
            '<tr>',
                '<td class="x-btn-ml"><i> </i></td>',
                '<td class="x-btn-mc">',
                    '<em class="{2}" unselectable="on">',
                        '<a href="{5}" style="display:block" target="{6}" class="x-btn-text">{0}</a>',
                    '</em>',
                '</td>',
                '<td class="x-btn-mr"><i> </i></td>',
            '</tr>',
            '<tr><td class="x-btn-bl"><i> </i></td><td class="x-btn-bc"></td><td class="x-btn-br"><i> </i></td></tr>',
        '</tbody></table>'
    ).compile(),

    buttonSelector : 'a:first',

    /** 
     * @cfg String href
     * The URL to create a link for.
     */
    /** 
     * @cfg String target
     * The target for the &lt;a> element.
     */
    /** 
     * @cfg Object
     * A set of parameters which are always passed to the URL specified in the href
     */
    baseParams: {},

//  private
    params: {},

    getTemplateArgs: function() {
        return Ext.Button.prototype.getTemplateArgs.apply(this).concat([this.getHref(), this.target]);
    },

    onClick : function(e){
        if(e.button != 0){
            return;
        }
        if(!this.disabled){
            if (this.fireEvent("click", this, e) == false) {
                e.stopEvent();
            } else {
                if(this.handler){
                    this.handler.call(this.scope || this, this, e);
                }
            }
        }
    },

    // private
    getHref: function() {
        var result = this.href;
        var p = Ext.urlEncode(Ext.apply(Ext.apply({}, this.baseParams), this.params));
        if (p.length) {
            result += ((this.href.indexOf('?') == -1) ? '?' : '&') + p;
        }
        return result;
    },

    /**
     * Sets the href of the link dynamically according to the params passed, and any {@link #baseParams} configured.
     * @param {Object} Parameters to use in the href URL.
     */
    setParams: function(p) {
        this.params = p;
        this.el.child(this.buttonSelector, true).href = this.getHref();
    }
});
Ext.reg('linkbutton', Ext.LinkButton);


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
              console.log(this.name,'.setValue',v,'no lookup needed because value is null');
              v = null;
          } else if (record != undefined) {
            text = record.data[this.name];
            console.log(this.name,'.setValue',v,'got text "',text,'" from given record ',record);
          } else {
            // if(this.mode == 'remote' && !Ext.isDefined(this.store.totalLength)){
            if(this.mode == 'remote' && ( this.lastQuery === null || (!Ext.isDefined(this.store.totalLength)))){
                console.log(this.name,'.setValue',v,'must wait for load');
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
                    console.log(this.name,'.setValue',v,' : loads store with params ',params);
                    this.store.load({params: params});
                }else{
                    console.log(this.name,'.setValue',v,' : but store is loading',this.store.lastOptions);
                }
                return;
            //~ }else{
              //~ if (this.mode == 'remote') 
                //~ console.log(this.name,'.setValue',v,' : store already loaded, lastQuery is "',this.lastQuery,'"');
              //~ else
                //~ console.log(this.name,'.setValue',v,' : local mode (no need to load)');
            }
            var r = this.findRecord(this.valueField, v);
            if(r){
                text = r.data[this.displayField];
                //~ console.log(this.name,'.setValue',v,', findRecord() returned ',r, ', text is ',text);
            }else if(this.valueNotFoundText !== undefined){
                text = this.valueNotFoundText;
            }
          }
        }
        this.lastSelectionText = text;
        if(this.hiddenField){
            this.hiddenField.value = v;
            //~ console.log('.setValue hiddenField',this.hiddenField.name,' = ',v);
        }
        Ext.form.ComboBox.superclass.setValue.call(this, text);
        this.value = v; // warum war das hier? 20100707
        //~ console.log('.setValue 20100707 done',this);
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
    //~ setContextValues : function(values){
      //~ if(this.contextParams) {
        //~ console.log('setContextValues',this.name,this.contextParams,'=',values);
        //~ if (this.contextValues === undefined) {
          //~ this.contextValues = values;
          //~ this.lastQuery = null;
          //~ return
        //~ }
        //~ for(i = 0; i <= this.contextParams.length; i++) {
          //~ if (this.contextValues[i] != values[i]) {
            //~ this.contextValues[i] = values[i];
            //~ this.lastQuery = null;
          //~ }
        //~ }
      //~ }   
    //~ },
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



function PseudoConsole() {
    this.log = function() {};
};
if (typeof(console) == 'undefined') console = new PseudoConsole();

Lino.notify = function(msg) {
  console.log(msg);
  //~ Ext.getCmp('konsole').update(msg);
  Ext.get('konsole').update(msg.replace(/\n/g,'<br/>'));
  //~ Ext.getCmp('konsole').update(msg.replace(/\n/g,'<br/>'));
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
    //~ p['grid_afteredit_colname'] = e.field;
    //~ p[e.field] = e.value;
    //~ console.log('grid_afteredit 20100707',p);
    // add value used by ForeignKeyStoreField CHOICES_HIDDEN_SUFFIX
    //~ p[e.field+'Hidden'] = e.value;
    // p[pk] = e.record.data[pk];
    // console.log("grid_afteredit:",e.field,'=',e.value);
    Ext.apply(p,caller.store.baseParams);
    function after_success(result) {
      caller.getStore().commitChanges(); // get rid of the red triangles
      caller.getStore().reload();        // reload our datastore.
    };
    //~ console.log(e.record.id);
    if (e.record.phantom) {
      //~ p.id = undefined;
      Lino.do_action(caller,{
        method:'POST',url: caller.ls_data_url,
        params:p,after_success:after_success})
    } else 
      Lino.do_action(caller,{
        method:'PUT',
        //~ url: caller.config.url_data+'/'+e.record.id, 
        url: caller.ls_data_url+'/'+e.record.id, 
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


Lino.comboRenderer = function(displayField){
    return function(value,metadata,record,ri,ci,store){
        if (record) return record.get(displayField)
        //~ var record = combo.findRecord(combo.valueField, value);
        //~ return record ? record.get(combo.displayField) : combo.valueNotFoundText;
        return ''; 
    }
}


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

/*******************
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

*************************/

Lino.ajax_error_handler = function(response,options) {
    console.log('AJAX failure:',response,options);
    // Ext.MessageBox.alert('Action failed','Lino server did not respond to Ajax request');
}
// Ext.Ajax.on('requestexception',Lino.ajax_error_handler)

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
        //~ console.log('submit_property_handler',response);
        var result=Ext.decode(response.responseText);
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
    //~ console.log('Lino.load_properties',response);
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
  //~ if (value == -99999) return '';
  if (record.phantom) return '';
  return value;
}

Lino.bbar_action_handler = function (caller,a) {
  //~ console.log(20100629,caller,a);
  if (a.client_side) return function(btn,evt) { 
    return a.handler(caller);
  };
  if (a.needs_selection) return function(btn,evt) { 
    var l = caller.get_selected();
    if (l.length == 0)  {
      Lino.notify('No selection.');
      return;
    } 
    if (l.length == 1) {
      window.location = caller.ls_data_url+'/'+l[0]+'?fmt='+a.name; 
    } else {
      for (var i = 0; i < l.length; i++) {
        window.open(caller.ls_data_url+'/'+l[i]+'?fmt='+a.name);
        //~ window.location = caller.ls_data_url+'/'+l[i]+'?fmt='+a.name; 
      }
    }
  }; else return function(btn,evt) { 
    window.location = caller.ls_data_url+'?fmt='+a.name; 
  };
};



Lino.build_bbar = function(caller,actions) {
  if (actions) {
    var bbar = Array(actions.length);
    for(var i=0;i<actions.length;i++) { 
      var btn = {
        text: actions[i].label
      };
      btn.scope = caller;
      btn.handler = Lino.bbar_action_handler(caller,actions[i]) ;
      //~ btn.handler = actions[i].handler.createCallback(caller);
      //~ btn.href = actions[i].url;
      //~ bbar[i] = new Ext.LinkButton(btn);
      bbar[i] = new Ext.Button(btn);
    }
    //~ console.log(20100624,bbar);
    return bbar
  }
};

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
    config.bbar = Lino.build_bbar(this,config.ls_bbar_actions);
    //~ config.bbar.push({
        //~ text: "Save", 
        //~ scope: this,
        //~ handler: Lino.submit_detail
      //~ });
    //~ console.log('20100629',this.ls_data_url);
    config.bbar.push({
        text: "Cancel", 
        handler: function() { history.back()}
    });
    Lino.FormPanel.superclass.constructor.call(this, config);
    if (config.data_record) {
      this.load_master_record(config.data_record);
      return;
    } 
  },
  load_master_record : function(record) {
    this.current_record = record;
    //~ console.log('20100531 Lino.DetailMixin.load_master_record',record);
    //~ this.config.main_panel.form.load(record);    
    if (record) {
      this.enable();
      this.form.loadRecord(record) 
      this.setTitle(record.title);
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
      }
    } else {
      this.form.reset();
      this.disable();
      this.setTitle('');
    }
    //~ console.log('20100531 Lino.DetailMixin.on_load_master_record',this.main_form);
    console.log('TODO: before_row_edit',this);
    //~ this.before_row_edit(record);
  },
  get_selected : function() { return [ this.current_record.id ] },
  get_current_record : function() {  return this.current_record }
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
    config.store = new Ext.data.JsonStore({ 
      listeners: { exception: Lino.on_store_exception }, 
      proxy: new Ext.data.HttpProxy({ url: config.ls_data_url+'?fmt=json', method: "GET" }), remoteSort: true, 
      fields: config.ls_store_fields, 
      totalProperty: "count", 
      root: "rows", 
      //~ id: "id" });
      idProperty: config.ls_id_property });
    if (config.ls_quick_edit) {
      config.selModel = new Ext.grid.CellSelectionModel()
    } else { 
      config.selModel = new Ext.grid.RowSelectionModel() 
    };
    config.tbar = new Ext.PagingToolbar({ 
      prependButtons: true, pageSize: 10, displayInfo: true, 
      store: config.store, 
      items: [ 
        { xtype: "textfield", 
          fieldLabel: "Search", 
          listeners: { scope:this, change:this.search_change }
          //~ scope:this, 
          //~ enableKeyEvents: true, 
          //~ listeners: { keypress: this.search_keypress }, 
          //~ id: "seachString" 
        }, 
        { scope:this, text: "csv", handler: function() { window.open(this.ls_data_url+'?fmt=csv') } } 
      ]});
      
    config.bbar = Lino.build_bbar(this,config.ls_bbar_actions);
    Lino.GridPanel.superclass.constructor.call(this, config);
    if (config.setup_events) config.setup_events();
    this.on('beforeedit',function(e) { 
      console.log(20100708,this); this.before_row_edit(e.record)
    },this);
  },

  initComponent : function(){
    //~ console.log('Lino.GridMixin.setup 1',this);
    //~ this.tbar = this.pager;
    Lino.GridPanel.superclass.initComponent.call(this);
    this.on('afteredit', Lino.grid_afteredit_handler(this));
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
  search_change : function(field,oldValue,newValue) {
    //~ console.log('search_change',field.getValue(),oldValue,newValue)
    this.store.setBaseParam('query',field.getValue()); // URL_PARAM_FILTER
    this.store.load({params: { start: 0, limit: this.getTopToolbar().pageSize }});
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
        if (this.getSelectionModel().selection) 
          return [ this.getSelectionModel().selection.record.id ];
        return []
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
  get_master_params : function(record) {
    var p = {}
    p['mt'] = this.ls_content_type; // ext_requests.URL_PARAM_MASTER_TYPE
    if (record) {
      p['mk'] = record.id; // ext_requests.URL_PARAM_MASTER_PK
    } else {
      p['mk'] = undefined;
    }
    return p;
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


Lino.button_handler = function(caller,action) {
  return function(event) { action.handler(caller) }
};

Lino.toggle_button_handler = function(master,action) {
  //~ var action = master.config.bbar_actions[i];
  return function(btn,state) {
    //~ console.log('toggle_button_handler');
    if(state) { 
      if (master.slaves[action.name]) {
        master.slaves[action.name].show();
      } else {
        var slave = new action.handler(master);
        master.slaves[action.name] = slave;
        //~ console.log('Lino.toggle_button_handler.after_js_code() ',caller,action.name,'=',caller.slaves[action.name]);
        // when master closes, close slave:
        master.window.on('close',function() { slave.close() });
        // when master hides, hide slave:          
        master.window.on('hide',function(){ slave.hide()});
        // when slave's close button is clicked, toggle button off:
        slave.window.on('hide',function(){ btn.toggle(false,false)});
        // when slave is shown, update it's data:
        slave.window.on('show',function(){ slave.load_master_record(master.get_current_record())});
        //~ js_result.load_master_record(caller.get_current_record());
        master.add_row_listener( function(sm,ri,rec){slave.load_master_record(rec)}, slave );
        // js_result.load_master_record(caller.get_current_record());
        
        // show slave:
        slave.show();
      }
    } else {
      master.slaves[action.name].hide();
    }
  }
};

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

Lino.SlavePlugin = function(caller) {
  //~ console.log(20100624,caller);
  this.caller = caller;
};
Lino.load_picture = function(caller,cmp,record) {
  if (record && cmp.el && cmp.el.dom) {
    var src = caller.ls_data_url + "/" + record.id + "?fmt=picture"
    //~ console.log('Lino.load_picture()',src);
    cmp.el.dom.src = src; 
  } else console.log('Lino.load_picture() no record or cmp not rendered',caller,cmp,record);
}
Lino.PictureBoxPlugin = Ext.extend(Lino.SlavePlugin,{
  init : function (cmp) {
    //~ console.log('Lino.PictureBoxPlugin.init()',this);
    if (this.caller) {
      cmp.on('render',function(){ Lino.load_picture(this.caller,cmp,this.caller.get_current_record())},this);
      this.caller.add_row_listener(function(sm,ri,rec) { Lino.load_picture(this.caller,cmp,rec) }, this );
    }
  }
});
Lino.chooser_handler = function(combo,name) {
  return function(cmp,newValue,oldValue) {
    //~ console.log('Lino.chooser_handler()',cmp,oldValue,newValue);
    combo.setContextValue(name,newValue);
  }
};
//~ Lino.chooser_handler = function(ww,context_values) {
  //~ return function(cmp,ownerCt,index) {
    //~ console.log('Lino.chooser_handler()',cmp,ww,context_values);
    //~ ww.add_row_listener(function(sm,ri,rec) { 
      //~ var values = Array(context_values.length);
      //~ for (var i = 0; i < context_values.length; i++)
          //~ values[i] = rec.data[context_values[i]];
      //~ cmp.setContextValues(values);        
    //~ }, ww );
  //~ }
//~ };
Lino.unused_ChooserPlugin = function(caller,context_values) {
  this.caller = caller;
  this.context_values = context_values;
};
Ext.override(Lino.unused_ChooserPlugin,{
  init : function (cmp) {
    //~ console.log('Lino.ChooserPlugin.init()',this);
    // cmp.on('render',function(){ Lino.load_picture(this.caller,cmp,this.caller.get_current_record())},this);
    if (this.caller) this.caller.add_row_listener(function(sm,ri,rec) { 
      var values = Array(this.context_values.length);
      for (var i = 0; i < this.context_values.length; i++)
          values[i] = rec.data[this.context_values[i]];
      cmp.setContextValues(values);        
    }, this );
  }
});


Lino.load_slavegrid = function(caller,cmp,record) {
  if (record && cmp.el) {
    //~ var src = caller.config.url_data + "/" + record.id + ".jpg"
    //~ console.log('Lino.load_slavegrid()',record);
    var p = caller.get_master_params(record);
    for (k in p) cmp.getStore().setBaseParam(k,p[k]);
    cmp.getStore().load(); 
  } else console.log('Lino.load_picture() no record or cmp not rendered',caller,cmp,record);
}
Lino.SlaveGridPlugin = Ext.extend(Lino.SlavePlugin,{
  init : function (cmp) {
    if (this.caller) {
      cmp.on('render',function(){ Lino.load_slavegrid(this.caller,cmp,this.caller.get_current_record())},this);
      this.caller.add_row_listener(function(sm,ri,rec) { Lino.load_slavegrid(this.caller,cmp,rec) }, this );
    }
  }
});


Lino.ComboBox = Ext.extend(Ext.form.ComboBox,{
  triggerAction: 'all',
  submitValue: true,
});

Lino.ChoicesFieldElement = Ext.extend(Lino.ComboBox,{
  mode: 'local',
  forceSelection: false
});


Lino.RemoteComboStore = Ext.extend(Ext.data.JsonStore,{
  constructor: function(config){
      Lino.RemoteComboStore.superclass.constructor.call(this, Ext.apply(config, {
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
  displayField: 'text', // ext_requests.CHOICES_TEXT_FIELD
  valueField: 'value', // ext_requests.CHOICES_VALUE_FIELD
  //~ typeAhead: true,
  //~ forceSelection:false,
  minChars: 2, // default 4 is to much
  queryDelay: 300, // default 500 is maybe slow
  queryParam: 'query', // ext_requests.URL_PARAM_FILTER)
  typeAhead: true,
  selectOnFocus: true, // select any existing text in the field immediately on focus.
  resizable: true
});





/* If you change this, then change also USE_WINDOWS in ext_ui.py */
/************* not used in extjsu *****************
Lino.USE_WINDOWS = true;

Lino.WindowWrapper = function(config_fn) {
  //~ console.log('Lino.WindowWrapper.constructor',config.title,' : caller is ',caller);
  //~ this.caller = caller;
  this.config = config_fn(this); 
  this.slaves = {};
  if (this.config.actions) {
      this.bbar_actions = Array(this.config.actions.length);
      for(var i=0;i<this.config.actions.length;i++) { 
        var btn = {
          text: this.config.actions[i].label
        };
        if (this.config.actions[i].opens_a_slave) {
          btn.toggleHandler = Lino.toggle_button_handler(this,this.config.actions[i]);
          btn.enableToggle = true;
        } else  {
          btn.handler = Lino.button_handler(this,this.config.actions[i]);
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
  setup : function() { 
    //~ console.log('Lino.WindowWrapper.setup',this);
    if (Lino.USE_WINDOWS) {
      this.window = new Ext.Window({ layout: "fit", title: this.config.title, items: this.main_item, 
        height: this.config.wc.height, width: this.config.wc.width, maximizable: true, maximized: this.config.wc.maximized, 
        y: this.config.wc.y, x: this.config.wc.x, 
        closeAction:this.closeAction,
        bbar: this.bbar_actions,
        tools: [ { qtip: this.config.qtip, handler: Lino.save_wc_handler(this), id: "save" } ] 
        });
    } else {
      this.window = new Ext.Panel({ layout: "fit", 
      //~ autoHeight: true,
        title: this.config.title, items: this.main_item, 
        bbar: this.bbar_actions,
        tools: [ { qtip: this.config.qtip, handler: Lino.save_wc_handler(this), id: "save" } ] 
      });
    }
    this.window.window_wrapper = this;
    //~ console.log('Lino.WindowWrapper.setup done',this);
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
  show : function() {
    //~ console.log('Lino.WindowWrapper.show',this);
    if (Lino.USE_WINDOWS) {
      this.window.show();
      this.window.syncSize();
      this.window.focus();
    } else {
      var cmp = Ext.getCmp('main_area');
      //~ cmp.update(this.window);
      cmp.update('');
      this.window.render('main_area');
      //~ Ext.DomHelper.overwrite(cmp,this.window);
    }
  },
  on_render : function() {},
  refresh : function() {},
  hide : function() { this.window.hide() },
  close : function() { this.window.close() },  
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
    this.main_item.on('beforeedit',function(e) { this.config.before_row_edit(e.record)},this);
      
    Lino.WindowWrapper.prototype.setup.call(this);
  },
  get_current_record : function() { 
    if (this.main_item) return this.main_item.getSelectionModel().getSelected();
  },
  refresh : function() { 
    this.main_item.refresh();
  },
  get_selected : function() {
    var sels = this.main_item.getSelectionModel().getSelections();
    return Ext.pluck(sels,'id');
  },
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


Lino.SlaveMixin = {
  closeAction : 'hide',
  add_row_listener : function(fn,scope) {
    this.caller.add_row_listener(fn,scope);
  }
  //~ get_base_params : function() { return this.caller.get_master_params(this.caller.get_current_record()) }
};



Lino.GridSlaveWrapper = Ext.extend(Lino.WindowWrapper,{});
Lino.GridSlaveWrapper.override(Lino.SlaveMixin);
Lino.GridSlaveWrapper.override(Lino.GridMixin);
Lino.GridSlaveWrapper.override({
  load_master_record : function(record) {
    Lino.load_slavegrid(this.caller,this.main_grid,record);
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
              url:this.caller.ls_data_url + '/' + rec.id,
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
******************/

/***
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
            params: this.caller.get_master_params(this.caller.get_current_record()),
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
    Lino.WindowWrapper.prototype.setup.call(this);
    this.main_form = this.window.getComponent(0);
    var rec = this.caller.store.getById(-99999);
    //~ console.log(rec);
    this.load_master_record(rec);
  },
  goto_record: function(id) {
  }
});
***/
/************
Lino.DetailWrapper = Ext.extend(Lino.WindowWrapper, {});
Lino.DetailWrapper.override(Lino.DetailMixin);
Lino.DetailWrapper.override({
  on_submit: function() {
    this.main_form.form.submit({
      //~ url:this.caller.config.url_data + '/' + this.config.record_id,
      url:this.caller.ls_data_url + '/' + this.config.record_id,
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
    this.bbar_actions = [
      {
        text: "Submit", 
        scope: this,
        handler: this.on_submit
      },
      { text: "Cancel", scope: this, handler: function() { this.close()} }
    ];
    var row_actions = Lino.build_bbar(this,this.config.ls_bbar_actions);
    if (row_actions) this.bbar_actions = this.bbar_actions.concat(row_actions);
    
    Lino.WindowWrapper.prototype.setup.call(this);
    this.main_form = this.window.getComponent(0);
    if (this.config.data_record) {
      this_.load_master_record(data_record);
      return;
    } 
    if (! this.config.record_id) {
      this.config.record_id = this.caller.get_current_record().id;
    }
    //~ console.log('Lino.DetailWrapper.setup() calls Ajax');
    var this_ = this;
    Ext.Ajax.request({ 
      waitMsg: 'Loading record...',
      method: 'GET',
      url:this.config.url_data + '/' + this.config.record_id,
      success: function(response) {
        if (response.responseText) {
            var rec = Ext.decode(response.responseText);
            //~ console.log('20100531 Lino.DetailWrapper.setup() success',rec);
            this_.load_master_record(rec);
            //~ this_.window.setTitle(rec.title);
        }
      },
      failure: Lino.ajax_error_handler
    });
  }
})

Lino.InsertWrapper = Ext.extend(Lino.DetailWrapper, {
  on_submit: function() {
    this.main_form.form.submit({
      //~ url:this.caller.config.url_data,
      url:this.caller.ls_data_url,
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

****************/

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
