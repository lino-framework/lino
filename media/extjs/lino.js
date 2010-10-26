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



Lino.VBorderPanel = Ext.extend(Ext.Panel,{
    constructor : function(config) {
      config.layout = 'border';
      delete config.layoutConfig;
      Lino.VBorderPanel.superclass.constructor.call(this,config);
      for(var i=0; i < this.items.length;i++) {
        var item = this.items.get(i);
        if (this.isVertical(item) && item.collapsible) {
          item.on('collapse',this.onBodyResize,this);
          item.on('expand',this.onBodyResize,this);
        }
      }
    },
    isVertical : function(item) {
       return (item.region == 'north' || item.region == 'south' || item.region == 'center');
    },
    onBodyResize: function(w, h){
        //~ console.log('VBorderPanel.onBodyResize',this.title)
        var sumflex = 0;
        var availableHeight = this.getInnerHeight();
        for(var i=0; i < this.items.length;i++) {
          var item = this.items.get(i);
          //~ if (this.isVertical(item) && item.getResizeEl()) {
          if (this.isVertical(item)) {
              if (item.collapsed || item.flex == 0) {
                  //~ item.syncSize()
                  //~ item.doLayout()
                  //~ if (item.region == "north") console.log('region north',item.getHeight(),item.id, item);
                  //~ if (item.getHeight() == 0) console.log(20100921,'both flex and getHeight() are 0!');
                  availableHeight -= item.getHeight();
              } else {
                  sumflex += item.flex;
              }
          } 
          //~ else console.log('non-vertical item in VBoderPanel:',item)
        }
        var hunit = availableHeight / sumflex;
        for(var i=0; i < this.items.length;i++) {
          var item = this.items.get(i);
          if (this.isVertical(item)) {
              if (item.flex != 0 && ! item.collapsed) {
                  item.setHeight(hunit * item.flex);
                  //~ console.log(item.region,' : height set to',item.getHeight());
              }
          }
          //~ else console.log('non-vertical item in VBoderPanel:',item)
        }
        Lino.VBorderPanel.superclass.onBodyResize.call(this, w, h);
    }
});


/*
The following two overrides are from
http://www.sencha.com/forum/showthread.php?98165-vbox-layout-with-two-grids-grid-collapse-does-not-stretch-non-collapsed-grid&p=463266  

Ext.override(Ext.layout.BoxLayout, {
    getVisibleItems: function(ct) {
        var ct  = ct || this.container,
            t   = ct.getLayoutTarget(),
            cti = ct.items.items,
            len = cti.length,
            i, c, items = [];

        for (i = 0; i < len; i++) {
            if((c = cti[i]).rendered && this.isValidParent(c, t) && c.hidden !== true){ // no collapsed check
                items.push(c);
            }
        }

        return items;
    }
});

Ext.override(Ext.layout.VBoxLayout, {
    calculateChildBoxes: function(visibleItems, targetSize) {
        var visibleCount = visibleItems.length,

            padding      = this.padding,
            topOffset    = padding.top,
            leftOffset   = padding.left,
            paddingVert  = topOffset  + padding.bottom,
            paddingHoriz = leftOffset + padding.right,

            width        = targetSize.width - this.scrollOffset,
            height       = targetSize.height,
            availWidth   = Math.max(0, width - paddingHoriz),

            isStart      = this.pack == 'start',
            isCenter     = this.pack == 'center',
            isEnd        = this.pack == 'end',

            nonFlexHeight= 0,
            maxWidth     = 0,
            totalFlex    = 0,

            //used to cache the calculated size and position values for each child item
            boxes        = [],

            //used in the for loops below, just declared here for brevity
            child, childWidth, childHeight, childSize, childMargins, canLayout, i, calcs, flexedHeight, horizMargins, stretchWidth;

            //gather the total flex of all flexed items and the width taken up by fixed width items
            for (i = 0; i < visibleCount; i++) {
                child = visibleItems[i];
                childHeight = child.collapsed ? child.getHeight() : child.height;
                childWidth  = child.width;
                canLayout   = !child.hasLayout && Ext.isFunction(child.doLayout);


                // Static height (numeric) requires no calcs
                if (!Ext.isNumber(childHeight)) {

                    // flex and not 'auto' height
                    if (child.flex && !childHeight) {
                        totalFlex += child.flex;

                    // Not flexed or 'auto' height or undefined height
                    } else {
                        //Render and layout sub-containers without a flex or width defined, as otherwise we
                        //don't know how wide the sub-container should be and cannot calculate flexed widths
                        if (!childHeight && canLayout) {
                            child.doLayout();
                        }

                        childSize = child.getSize();
                        childWidth = childSize.width;
                        childHeight = childSize.height;
                    }
                }

                childMargins = child.margins;

                nonFlexHeight += (childHeight || 0) + childMargins.top + childMargins.bottom;

                // Max width for align - force layout of non-layed out subcontainers without a numeric width
                if (!Ext.isNumber(childWidth)) {
                    if (canLayout) {
                        child.doLayout();
                    }
                    childWidth = child.getWidth();
                }

                maxWidth = Math.max(maxWidth, childWidth + childMargins.left + childMargins.right);

                //cache the size of each child component
                boxes.push({
                    component: child,
                    height   : childHeight || undefined,
                    width    : childWidth || undefined
                });
            }

            //the height available to the flexed items
            var availableHeight = Math.max(0, (height - nonFlexHeight - paddingVert));

            if (isCenter) {
                topOffset += availableHeight / 2;
            } else if (isEnd) {
                topOffset += availableHeight;
            }

            //temporary variables used in the flex height calculations below
            var remainingHeight = availableHeight,
                remainingFlex   = totalFlex;

            //calculate the height of each flexed item, and the left + top positions of every item
            for (i = 0; i < visibleCount; i++) {
                child = visibleItems[i];
                calcs = boxes[i];

                childMargins = child.margins;
                horizMargins = childMargins.left + childMargins.right;

                topOffset   += childMargins.top;

                if (isStart && child.flex && !child.collapsed && !child.height) {
                    flexedHeight     = Math.ceil((child.flex / remainingFlex) * remainingHeight);
                    remainingHeight -= flexedHeight;
                    remainingFlex   -= child.flex;

                    calcs.height = flexedHeight;
                    calcs.dirtySize = true;
                }

                calcs.left = leftOffset + childMargins.left;
                calcs.top  = topOffset;

                switch (this.align) {
                    case 'stretch':
                        stretchWidth = availWidth - horizMargins;
                        calcs.width  = stretchWidth.constrain(child.minWidth || 0, child.maxWidth || 1000000);
                        calcs.dirtySize = true;
                        break;
                    case 'stretchmax':
                        stretchWidth = maxWidth - horizMargins;
                        calcs.width  = stretchWidth.constrain(child.minWidth || 0, child.maxWidth || 1000000);
                        calcs.dirtySize = true;
                        break;
                    case 'center':
                        var diff = availWidth - calcs.width - horizMargins;
                        if (diff > 0) {
                            calcs.left = leftOffset + horizMargins + (diff / 2);
                        }
                }

                topOffset += calcs.height + childMargins.bottom;
            }

        return {
            boxes: boxes,
            meta : {
                maxWidth: maxWidth
            }
        };
    }
});


Lino.collapse_handler = function(ct) {
  return function onExpandCollapse(c) {
  //      Horrible Ext 2.* collapse handling has to be defeated...
      console.log(20100912);
      if (c.queuedBodySize) {
          delete c.queuedBodySize.width;
          delete c.queuedBodySize.height;
      }
      ct.doLayout();
  }
};

*/


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
  if (msg == undefined) msg = '';
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
   Lino.notify(action.result.message);
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
           Ext.Msg.alert('Failure', action.result.message);
   }
};



/*
Lino.save_wc_handler = function(ww) {
  return function(event,toolEl,panel,tc) {
    var pos = panel.getPosition();
    var size = panel.getSize();
    wc = ww.get_window_config();
    Ext.applyIf(wc,{ 
      x:pos[0],y:pos[1],height:size.height,width:size.width,
      maximized:panel.maximized});
    Lino.do_action(ww,{url:'/window_configs/'+ww.config.permalink_name,params:wc,method:'POST'});
  }
};

*/

Lino.report_window_button = function(ww,handler) {
  return {
    qtip:'Show report in own window', 
    id:"up",
    handler: function(event,toolEl,panel, tc) {
      console.log('report_window_button',panel);
      var bp = ww.get_master_params();
      console.log('report_window_button',bp)
      //~ action(panel,{record_id:-99999,base_params:bp});
      
      //~ var bp = panel.ww.get_master_params();
      //~ handler(panel,{base_params:bp});
      panel.ww = ww; // for HtmlBox. see blog/2010/1022
      handler(panel,{base_params:bp});
    }
  }
}


Lino.show_download = function (caller,fmt) {
    //~ console.log(caller.get_selected());
    var url = caller.ww.config.url_data; // ls_url;
    var l = caller.get_selected();
    if (l.length == 0) Lino.notify('No selection.');
    console.log('show_download',caller,l)
    for (var i = 0; i < l.length; i++) 
        window.open(url + '/' + String(l[i].id) + '?fmt='+fmt)
    //~ caller.get_selected().forEach(function(pk) {
      //~ console.log(pk);
      //~ window.open(url+pk+'.pdf');
    //~ })
}

//~ Lino.save_gc_handler = function(panel) {
  //~ return function() {
    //~ console.log('TODO: save_gc_handler',panel,panel.ls_data_url);
    //~ wc = ww.get_window_config();
    //~ console.log('save_wc_handler',ww,{url:ww.config.url_action,params:wc,method:'POST'});
    //~ Lino.do_action(ww,{url:ww.config.url_action,params:wc,method:'POST'});
    //~ Lino.do_action(ww,{url:'/grid_configs/'+ww.config.permalink_name,params:wc,method:'PUT'});
  //~ }
//~ };



Lino.delete_selected = function(caller) {
  //~ console.log("Lino.delete_selected",caller);
  var recs1 = caller.get_selected();
  var recs = [];
  for ( var i=0; i < recs1.length; i++ ) { if (! recs1[i].phantom) recs.push(recs1[i]); }
  if (recs.length == 0) {
    Lino.notify("Please select at least one record.");
    return;
  };
  //~ console.log(recs);
  Ext.MessageBox.show({
    title: 'Confirmation',
    msg: "Delete " + String(recs.length) + " rows. Are you sure?",
    buttons: Ext.MessageBox.YESNOCANCEL,
    fn: function(btn) {
      if (btn == 'yes') {
        for ( var i=0; i < recs.length; i++ ) {
          Lino.do_action(caller,{method:'DELETE',url:'/api'+caller.ls_url+'/'+recs[i].id})
        }
        caller.after_delete();
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

Lino.refresh_handler = function (ww) {
  return function() { 
      console.log('refresh',ww);
      ww.main_item.doLayout(false,true);
      //~ ww.main_item.syncSize();
  }
};
Lino.tools_close_handler = function (ww) {
  return function() { 
      ww.close();
  }
};
Lino.permalink_handler = function (ww) {
  return function() { 
    //~ console.log(20100923,ww.get_permalink());
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
  //~ console.log(rowIndex,colIndex,record,metaData);
  if (record.phantom) return '';
  return value;
}

Lino.build_buttons = function(panel,actions) {
  if (actions) {
    var buttons = Array(actions.length);
    for (var i=0; i < actions.length; i++) { 
      //~ console.log("build_bbar",btn.text,":",actions[i]);
      //~ if (actions[i].handler)
          //~ actions[i].handler = actions[i].handler.createCallback(panel);
      buttons[i] = new Ext.Toolbar.Button(actions[i]);
      if (actions[i].panel_btn_handler)
          buttons[i].on('click',actions[i].panel_btn_handler.createCallback(panel,buttons[i]));
      //~ var btn = {
        //~ text: actions[i].label
      //~ };
      //~ btn.handler = actions[i].handler.createCallback(scope);
      //~ buttons[i] = new Ext.Button(btn);
    }
    return buttons
  }
}

Lino.do_when_visible = function(cmp,todo) {
  //~ if (cmp.el && cmp.el.dom) 
  if (cmp.isVisible()) { 
    // 'visible' means 'rendered and not hidden'
    //~ console.log('Lino.do_when_visible() now',cmp.title,todo);
    todo(); 
  } else { 
    //~ console.log('Lino.do_when_visible() must defer because not isVisible()',todo,cmp);
    //~ todo.defer(1000);
    if (cmp.rendered) {
      //~ console.log(cmp,'-> cmp is rendered but not visible: and now?');
      //~ console.log(cmp.title,'-> cmp is rendered but not visible: wait a second...');
      //~ var fn = function() {Lino.do_when_visible(cmp,todo)};
      //~ fn.defer(100);
      
      Lino.do_when_visible.defer(100,this,[cmp,todo]);
      
      //~ var ve = cmp.getVisibilityEl();
      //~ console.log(cmp,'-> cmp is rendered but not visible: forward to visibilityEl', ve);
      //~ ve.on('click',todo)
      
      //~ ve.on('show',function(){console.log('show',cmp)})
      //~ if (ve == cmp) {
        //~ console.log(cmp,'visibilityEl is same as cmp: and now?');
        //~ return
      //~ }
      //~ if (ve === undefined) {
        //~ console.log(cmp,'visibilityEl is undefined: and now?');
        //~ return
      //~ }
      //~ return Lino.do_when_visible(ve,todo)
      //~ cmp.on('show',function(){console.log('show',cmp)})
      //~ cmp.on('added',function(){console.log('added',cmp)})
      //~ cmp.on('afterrender',function(){console.log('afterrender',cmp)})
      //~ cmp.on('beforestatesave',function(){console.log('beforestatesave',cmp)})
      //~ cmp.on('enable',function(){console.log('enable',cmp)})
      //~ cmp.on('hide',function(){console.log('hide',cmp)})
      //~ cmp.on('render',function(){console.log('render',cmp)})
      //~ cmp.getVisibilityEl().on('show',todo,cmp,{single:true});
      //~ if (cmp.hidden) {
        //~ console.log('Lino.do_when_visible() later (on show)',cmp,todo);
        //~ cmp.on('show',todo,cmp,{single:true});
      //~ } else {
        //~ console.log('Lino.do_when_visible() later (on activate)',cmp,todo);
        //~ cmp.on('activate',todo,cmp,{single:true});
      //~ }
    } else {
      //~ console.log(cmp.title,'-> on render');
      cmp.on('afterrender',todo,cmp,{single:true});
    }
  }
  
};    

Lino.show_detail_handler = function(action) {
  return function(panel,btn) {
    var rec = panel.get_current_record();
    if (rec == undefined) {
      Lino.notify("There's no selected record.");
      return;
    }
    if (rec.phantom) {
      Lino.notify("Cannot show detail of phantom record.");
      return;
    }
    //~ action(panel,{record_id:master.id,base_params:panel.ww.config.base_params});
    //~ var bp = panel.ww.get_master_params();
    //~ var bp = panel.ww.get_base_params();
    //~ var bp = panel.getStore().baseParams;
    //~ var bp = panel.ww.config.base_params;
    //~ console.log('show_detail_handler()',panel.get_base_params());
    action(panel,{record_id:rec.id,base_params:panel.get_base_params()});
  }
};

Lino.show_insert_handler = function(action) {
  return function(panel,btn) {
    //~ if (panel.getStore !== undefined)
      //~ var bp = panel.getStore().baseParams;
    //~ else
    var bp = panel.get_base_params();
    //~ console.log('20101025 insert_handler',bp)
    action(panel,{record_id:-99999,base_params:bp});
    //~ action(panel,{record_id:-99999,base_params:panel.get_base_params()});
  }
};


Lino.submit_detail = function(panel,btn) {
  var rec = panel.get_current_record();
  if (rec) {
    //~ console.log('Save handler: this=',this);
    panel.form.submit({
      url:'/api'+panel.ls_url + '/' + rec.id,
      method: 'PUT',
      scope: panel,
      success: function(form, action) {
        Lino.notify(action.result.message);
        //~ this.caller.refresh();
      },
      failure: Lino.on_submit_failure,
      clientValidation: true
    })
  } else Lino.notify("Sorry, no current record.");
};


Lino.submit_insert = function(panel,btn) {
  panel.form.submit({
    url:'/api'+panel.ls_url,
    method: 'POST',
    params: panel.get_base_params(), // 20101025
    scope: panel,
    success: function(form, action) {
      Lino.notify(action.result.message);
      panel.ww.close();
      if (panel.ww.caller) panel.ww.caller.refresh();
      //~ this.caller.refresh();
    },
    failure: Lino.on_submit_failure,
    clientValidation: true
  })
};

if (Ext.ux.grid !== undefined) {
    Lino.GridFilters = Ext.extend(Ext.ux.grid.GridFilters,{
      encode:true,
      local:false
    });
} else {
    Lino.GridFilters = function() {}; // dummy
    Ext.override(Lino.GridFilters,{
      init : function() {}
    });
};

Lino.FormPanel = Ext.extend(Ext.form.FormPanel,{
  constructor : function(ww,config,params){
    this.ww = ww;
    if (params) Ext.apply(config,params);
    //~ console.log('FormPanel.constructor() 1',config)
    //~ Ext.applyIf(config,{base_params:{}});
    //~ console.log('FormPanel.constructor() 2',config)
    config.bbar = Lino.build_buttons(this,config.ls_bbar_actions);
    if (config.has_navigator) {
      config.tbar = this.tbar_items().concat([
        this.first = new Ext.Toolbar.Button({
          tooltip:"First",disabled:true,handler:this.moveFirst,scope:this,iconCls:'x-tbar-page-first'}),
        this.prev = new Ext.Toolbar.Button({
          tooltip:"Previous",disabled:true,handler:this.movePrev,scope:this,iconCls:'x-tbar-page-prev'}),
        this.next = new Ext.Toolbar.Button({
          tooltip:"Next",disabled:true,handler:this.moveNext,scope:this,iconCls:'x-tbar-page-next'}),
        this.last = new Ext.Toolbar.Button({
          tooltip:"Last",disabled:true,handler:this.moveLast,scope:this,iconCls:'x-tbar-page-last'}),
        '->',
        this.displayItem = new Ext.Toolbar.TextItem({})
      ]);
    }
    config.bbar = config.bbar.concat([
      '->',
      {text:'Layout Editor',handler:this.edit_detail_config,qtip:"Edit Detail Layout",scope:this}
    ])
    this.before_row_edit = config.before_row_edit.createDelegate(this);
    
    Lino.FormPanel.superclass.constructor.call(this, config);
    //~ 20101025 Ext.applyIf(this,{base_params:{}});
    //~ this.base_params = config.base_params;
    //~ console.log(20100930,this.base_params);
  },
  get_base_params : function() {
    return this.ww.config.base_params;
  },
  set_base_params : function(p) {
    this.ww.config.base_params = p;
  },
  after_delete : function() {
    this.ww.close();
    if (this.ww.caller) this.ww.caller.refresh();
  },
  moveFirst : function() {this.goto_record_id(this.current_record.navinfo.first)},
  movePrev : function() {this.goto_record_id(this.current_record.navinfo.prev)},
  moveNext : function() {this.goto_record_id(this.current_record.navinfo.next)},
  moveLast : function() {this.goto_record_id(this.current_record.navinfo.last)},
  
  goto_record_id : function(record_id) {
    console.log('Lino.FormPanel.goto_record_id()',record_id);
    Lino.notify(); 
    var this_ = this;
    Ext.Ajax.request({ 
      waitMsg: 'Loading record...',
      method: 'GET',
      //~ params: this.ww.config.base_params,
      params: this.ww.config.base_params,
      url:'/api'+this.ls_url + '/' + record_id,
      //~ params: {query: this.search_field.getValue()},
      success: function(response) {   
        // todo: convert to Lino.action_handler.... but result 
        if (response.responseText) {
          var rec = Ext.decode(response.responseText);
          //~ console.log('goto_record_id success',rec);
          if (rec.navinfo && rec.navinfo.recno == 0) {
              /* 
                recno 0 means "the requested pk exists but is not contained in the requested queryset".
                This can happen after search_change on a detail.
              */
              this_.goto_record_id(rec.navinfo.first);
          } else {
              this_.set_current_record(rec);
              //~ this_.window.setTitle(rec.title);
          }
        }
      },
      failure: Lino.ajax_error_handler
    });
  },
  set_current_record : function(record) {
    this.current_record = record;
    //~ console.log('Lino.FormPanel.set_current_record',record);
    //~ this.config.main_panel.form.load(record);    
    if (record) {
      this.enable();
      this.form.loadRecord(record) 
      this.ww.window.setTitle(record.title);
      if (record.data.disabled_fields) {
        //~ console.log('20100930 disabled_fields =',record.data.disabled_fields);
        //~ console.log('20100930 this.form =',this.form);
        //~ for (i in record.data.disabled_fields.length) {
        for (i = 0; i < record.data.disabled_fields.length; i++) {
            //~ var fld = this.form.findField(record.data.disabled_fields[i]);
            var flds = this.find('name',record.data.disabled_fields[i]);
            if (flds.length == 1) { 
              //~ console.log('20100930 fld',record.data.disabled_fields[i],'=',flds[0]);
              flds[0].disable(); 
            //~ } else {
                //~ console.log(20100617,record.data.disabled_fields[i], 'field not found');
            }
        }
      };
      if (this.has_navigator && record.navinfo) {
        this.first.setDisabled(!record.navinfo.first);
        this.prev.setDisabled(!record.navinfo.prev);
        this.next.setDisabled(!record.navinfo.next);
        this.last.setDisabled(!record.navinfo.last);
        this.displayItem.setText(record.navinfo.message);
      }
    } else {
      this.form.reset();
      this.disable();
      this.ww.window.setTitle('');
      if (this.has_navigator) {
        this.first.disable();
        this.prev.disable();
        this.next.disable();
        this.last.disable();
      }
    }
    //~ console.log('20100531 Lino.DetailMixin.on_load_master_record',this.main_form);
    this.before_row_edit(record);
  },
  search_change : function(field,oldValue,newValue) {
    //~ console.log('FormPanel.search_change()');
    this.ww.config.base_params['query'] = field.getValue(); // URL_PARAM_FILTER
    this.goto_record_id(this.current_record.id);
    //~ this.moveFirst();
  },
  get_selected : function() { return [ this.current_record ] },
  get_current_record : function() {  
    //~ console.log(20100714,this.current_record);
    return this.current_record },
  edit_detail_config : function () {
    var active_tab = {};
    var main = this.items.get(0);
    if (main.getActiveTab !== undefined) {
      var tabitem = main.getActiveTab();
      Ext.apply(active_tab,{tab : main.items.indexOf(tabitem)});
    }
    var editor = new Ext.form.TextArea();
    var close = function() { win.close(); }
    var _this = this;
    var save = function() { 
      console.log(arguments); 
      var params = {desc: editor.getValue()};
      Ext.apply(params,active_tab);
      var a = { 
        params:params, 
        method:'PUT',
        url:'/detail_config'+_this.ls_url,
        success: Lino.action_handler( function(result) {
          win.close();
          document.location = _this.ww.get_permalink();
        })
      };
      //~ console.log(a);
      Ext.Ajax.request(a);
    }
    var save_btn = new Ext.Button({text:'Save',handler:save,disabled:true});
    var win = new Ext.Window({title:'Detail Layout',
      items:editor, layout:'fit',
      width:500,height:500,
      bbar:[{text:'Cancel',handler:close},save_btn]});
    var a = { 
      params:active_tab, 
      method:'GET',
      url:'/detail_config'+_this.ls_url,
      success : function(response) {
        //~ console.log('Lino.do_action()',response,'action success');
        if (response.responseText) {
          var result = Ext.decode(response.responseText);
          if (result.success) {
            //~ console.log('Lino.do_action()',action.name,'result is',result);
            editor.setValue(result.desc);
            save_btn.enable();
          }
        }
      }
    };
    console.log(a);
    Ext.Ajax.request(a);
    win.show();
  },
  load_htmlbox_to : function(cmp,record) {
    //~ console.log('Lino.load_htmlbox_to()',cmp,record);
    Lino.do_when_visible(cmp,function() {
      cmp.items.get(0).getEl().update(record.data[cmp.name])
    });
  },
  load_picture_to : function(cmp,record) {
    //~ console.log('FormPanel.load_picture_to()',record);
    if (record)
      var src = '/api'+this.ww.main_item.ls_url + "/" + record.id + "?fmt=image"
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
    //~ f();
  }
});

Lino.foo = function () {
  console.log(arguments);
}

Lino.action_handler = function (on_success) {
  return function (response) {
    if (response.responseText) {
      var result = Ext.decode(response.responseText);
      //~ console.log('Lino.do_action()',action.name,'result is',result);
      if (result.success) on_success(result);
      if (result.alert_msg) Ext.MessageBox.alert('Alert',result.alert_msg);
      if (result.message) Lino.notify(result.message);
    }
  }
}



Lino.getRowClass = function(record, rowIndex, rowParams, store) {
  if (record.phantom) {
    //~ console.log(20101009);
    //~ rowParams.bodyStyle = "color:red;background-color:blue";
    return 'lino-phantom-row';
    }
  return '';
}
    
Lino.GridPanel = Ext.extend(Ext.grid.EditorGridPanel,{
  clicksToEdit:2,
  enableColLock: false,
  autoHeight: false,
  viewConfig: {
          //autoScroll:true,
          //autoFill:true,
          //forceFit=True,
          //enableRowBody=True,
          //~ showPreview:true,
          //~ scrollOffset:200,
          getRowClass: Lino.getRowClass,
          //~ enableRowBody: true,
          emptyText:"Nix gefunden!"
        },
  
  constructor : function(ww,config,params){
    this.ww = ww;
    if (params) Ext.apply(config,params);
    //~ Ext.applyIf(config,{base_params:{}});
    //~ this.ww = ww;
    var bp = { fmt:'json' };
    Ext.apply(bp,ww.config.base_params);
    
    //~ function on_proxy_load( proxy, transactionObject, callbackOptions ) {
      //~ console.log('on_proxy_load',transactionObject)
    //~ }
    var proxy = new Ext.data.HttpProxy({ 
      url: '/api'+config.ls_url, 
      method: "GET"
      //~ listeners: {load:on_proxy_load} 
    });
    //~ config.store = new Ext.data.JsonStore({ 
    config.store = new Ext.data.ArrayStore({ 
      listeners: { exception: Lino.on_store_exception }, 
      //~ proxy: new Ext.data.HttpProxy({ url: config.ls_data_url+'?fmt=json', method: "GET" }), remoteSort: true, 
      proxy: proxy, 
      idIndex: config.pk_index,
      remoteSort: true, 
      baseParams: bp, 
      fields: config.ls_store_fields, 
      totalProperty: "count", 
      root: "rows", 
      //~ id: "id" });
      idProperty: config.ls_id_property });
      
    //~ proxy.on('load 1 20101021',function() {
      //~ console.log('arrayData:',config.store.reader.arrayData);
    //~ });
      
    //~ console.log('config.pk_index',config.pk_index,config.store),
    delete config.ls_store_fields;
    
    this.before_row_edit = config.before_row_edit.createDelegate(this);
    delete config.before_row_edit;

    if (config.ls_quick_edit) {
      config.selModel = new Ext.grid.CellSelectionModel()
      this.get_selected = function() {
        //~ console.log(this.getSelectionModel().selection);
        if (this.getSelectionModel().selection)
            return [ this.getSelectionModel().selection.record ];
        return [this.store.getAt(0)];
      };
      this.get_current_record = function() { 
        if (this.getSelectionModel().selection) 
          return this.getSelectionModel().selection.record;
        return this.store.getAt(0);
      };
    } else { 
      config.selModel = new Ext.grid.RowSelectionModel() 
      this.get_selected = function() {
        var sels = this.getSelectionModel().getSelections();
        if (sels.length == 0) sels = [this.store.getAt(0)];
        return sels
        //~ var sels = this.getSelectionModel().getSelections();
        //~ return Ext.pluck(sels,'id');
      };
      this.get_current_record = function() { 
        var rec = this.getSelectionModel().getSelected();
        if (rec == undefined) rec = this.store.getAt(0);
        return rec

      };
    };
    delete config.ls_quick_edit
    
    config.tbar = new Ext.PagingToolbar({ 
      prependButtons: true, pageSize: 10, displayInfo: true, 
      store: config.store, 
      items: this.tbar_items()
    });
    config.bbar = Lino.build_buttons(this,config.ls_bbar_actions);
    delete config.ls_bbar_actions
    
    var menu = [];
    var set_gc = function(name) {
      return function() {
        //~ console.log('set_gc() 20100812');
        this.getColumnModel().setConfig(this.apply_grid_config(name,this.ls_grid_configs,this.ls_columns));
      }
    }
    for (k in config.ls_grid_configs) {
      menu.push({text:config.ls_grid_configs[k].label,handler:set_gc(k),scope:this})
    }
    if(menu.length > 1) {
      config.bbar = config.bbar.concat([
        {text:'View',menu: menu,tooltip:"Select another view of this report"}
      ]);
    }
    config.bbar = config.bbar.concat([
      '->',
      //~ {text:'GC',handler:this.manage_grid_configs,qtip:"Manage Grid Configurations",scope:this},
      {text:'Save GC',handler:this.save_grid_config,qtip:"Save Grid Configuration",scope:this}
    ]);
    
    config.plugins = [new Lino.GridFilters()];
    
    //~ config.colModel = new ext.grid.columnModel({defaultSortable:true,
      //~ columns:this.apply_grid_config(config.gc_name,config.ls_grid_configs,config.ls_columns)});
    config.columns = this.apply_grid_config(config.gc_name,config.ls_grid_configs,config.ls_columns);
    
    Lino.GridPanel.superclass.constructor.call(this, config);
    
    
    this.on('beforeedit',function(e) { this.before_row_edit(e.record)},this);
  },
  
  get_base_params : function() {
    //~ return this.ww.config.base_params;
    return this.getStore().baseParams;
  },
  set_base_params : function(p) {
    //~ console.log('GridPanel.set_base_params',p)
    for (k in p) this.getStore().setBaseParam(k,p[k]);
  },
  
  search_change : function(field,oldValue,newValue) {
    //~ console.log('search_change',field.getValue(),oldValue,newValue)
    this.store.setBaseParam('query',field.getValue()); // URL_PARAM_FILTER
    this.store.load({params: { start: 0, limit: this.getTopToolbar().pageSize }});
  },
  
  apply_grid_config : function(name,grid_configs,rpt_columns) {
    //~ var rpt_columns = this.ls_columns;
    var gc = grid_configs[name];    
    //~ console.log('apply_grid_config() 20100812',name,gc);
    this.gc_name = name;
    if (gc == undefined) {
      return rpt_columns;
      //~ config.columns = config.ls_columns;
      //~ return;
    } 
    //~ delete config.ls_filters
    
    //~ console.log(20100805,config.ls_columns);
    var columns = Array(gc.columns.length);
    for (var j = 0; j < rpt_columns.length;j++) {
      var col = rpt_columns[j];
      for (var i = 0; i < gc.columns.length; i++) {
        if (col.dataIndex == gc.columns[i]) {
          col.width = gc.widths[i];
          columns[i] = col;
          break;
        }
      }
    }
    
    //~ var columns = Array(rpt_columns.length);
    //~ for (var i = 0; i < rpt_columns.length; i++) {
      //~ columns[i] = rpt_columns[gc.columns[i]];
      //~ columns[i].width = gc.widths[i];
    //~ }
    
    if (gc.hidden_cols) {
      for (var i = 0; i < gc.hidden_cols.length; i++) {
        var hc = gc.hidden_cols[i];
        for (var j = 0; j < columns.length;j++) {
          var col = columns[j];
          if (col.dataIndex == hc) {
            col.hidden = true;
            break
          }
        }
      }
    }
    if (gc.filters) {
      //~ console.log(20100811,'config.ls_filters',config.ls_filters);
      //~ console.log(20100811,'config.ls_grid_config.filters',config.ls_grid_config.filters);
      for (var i = 0; i < gc.filters.length; i++) {
        var fv = gc.filters[i];
        for (var j = 0; j < columns.length;j++) {
          var col = columns[j];
          if (col.dataIndex == fv.field) {
            //~ console.log(20100811, f,' == ',fv);
            if (fv.type == 'string') {
              col.filter.value = fv.value;
              //~ if (fv.comparison !== undefined) f.comparison = fv.comparison;
            } else {
              //~ console.log(20100811, fv);
              col.filter.value = {};
              col.filter.value[fv.comparison] = fv.value;
            }
            break;
          }
        };
      }
    }
    
    return columns;
    //~ config.columns = cols;
    //~ delete config.ls_columns
  },
  
  get_current_grid_config : function () {
    var cm = this.getColumnModel();
    var widths = Array(cm.config.length);
    //~ var hiddens = Array(cm.config.length);
    var columns = Array(cm.config.length);
    //~ var columns = Array(cm.config.length);
    var hidden_cols = [];
    //~ var filters = this.filters.getFilterValues();
    var p = this.filters.buildQuery(this.filters.getFilterData())
    for (var i = 0; i < cm.config.length; i++) {
      var col = cm.config[i];
      columns[i] = col.dataIndex;
      //~ hiddens[i] = col.hidden;
      widths[i] = col.width;
      if (col.hidden) hidden_cols.push(col.dataIndex);
    }
    //~ p['hidden_cols'] = hidden_cols;
    p['widths'] = widths;
    p['columns'] = columns;
    p['name'] = this.gc_name;
    var gc = this.ls_grid_configs[this.gc_name];
    if (gc == undefined) 
      p['label'] = this.gc_name;
    else 
      p['label'] = gc.label
    //~ p['name'] = this.ls_grid_config ? this.ls_grid_config.name : '';
    if (hidden_cols.length > 0) p['hidden_cols'] = hidden_cols;
    //~ if (filters.length > 0) p['filters'] = filters;
    //~ console.log('20100810 save_grid_config',p);
    return p;
  },
  
  manage_grid_configs : function() {
    var data = [];
    for (k in this.ls_grid_configs) {
      var v = this.ls_grid_configs[k];
      var i = [k,String(v.columns),String(v.hidden_cols),String(v.filters)];
      data.push(i)
    }
    if (this.ls_grid_configs[this.gc_name] == undefined) {
      var v = this.get_current_grid_config();
      var i = [k,String(v.columns),String(v.hidden_cols),String(v.filters)];
      data.push(i);
    }
    //~ console.log(20100811, data);
    var main = new Ext.grid.GridPanel({
      store: new Ext.data.ArrayStore({
        idIndex:0,
        fields:['name','columns','hidden_cols','filters'],
        autoDestroy:true,
        data: data}),
      //~ autoHeight:true,
      selModel: new Ext.grid.RowSelectionModel(),
      listeners: { 
        rowdblclick: function(grid,rowIndex,e) {
          console.log('row doubleclicked',grid, rowIndex,e);
        },
        rowclick: function(grid,rowIndex,e) {
          console.log('row clicked',grid, rowIndex,e);
        }
      },
      columns: [ 
        {dataIndex:'name',header:'Name'}, 
        {dataIndex:'columns',header:'columns'}, 
        {dataIndex:'hidden_cols',header:'hidden columns'}, 
        {dataIndex:'filters',header:'filters'} 
      ]
    });
    var win = new Ext.Window({title:'GridConfigs Manager',layout:'fit',items:main,height:200});
    win.show();
  },
  
  edit_grid_config : function(name) {
    gc = this.ls_grid_configs[name];
    var win = new Ext.Window({
      title:'Edit Grid Config',layout:'vbox', 
      //~ layoutConfig:'stretch'
      items:[
        {xtype:'text', value: gc.name},
        {xtype:'text', value: gc.columns},
        {xtype:'text', value: gc.hidden_cols},
        {xtype:'text', value: gc.filters}
      ]
    });
    win.show();
  },
  
  save_grid_config : function () {
    //~ console.log('TODO: save_grid_config',this);
    //~ p.column_widths = Ext.pluck(this.colModel.columns,'width');
    var a = { params:this.get_current_grid_config(), method:'PUT',url:'/grid_config'+this.ls_url};
    Lino.do_action(this,a);
  },
  
  on_beforeedit : function(e) {
    //~ console.log('20100803 GridPanel.on_beforeedit()',e);
    if (e.record.data.disabled_fields) {
      //~ console.log('20100803 GridPanel.on_beforeedit()',e.record.data.disabled_fields);
      for (i in e.record.data.disabled_fields) {
        if(e.record.data.disabled_fields[i] == e.field) {
          //~ console.log(20100803,'cancel');
          e.cancel = true;
          Lino.notify(String.format('Field "{0}" is disabled for this record',e.field));
          //~ Lino.notify(e.field + ' : this field is disabled for record ' + e.record.title);
          return
        }
      }
    }
    
  },
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
    Ext.apply(p,this.get_base_params()); // needed for POST, ignored for PUT
    //~ Ext.apply(p,this.ww.config.base_params);
    //~ Ext.apply(p,this.store.baseParams);
    var self = this;
    var on_success = Lino.action_handler( function(result) {
      self.getStore().commitChanges(); // get rid of the red triangles
      self.getStore().reload();        // reload our datastore.
    });
    var req = {
        waitMsg: 'Saving your data...',
        success: on_success,
        params:p
    };
    if (e.record.phantom) {
      Ext.apply(req,{
        method: 'POST',
        url: '/api'+this.ls_url
      });
    } else {
      Ext.apply(req,{
        method: 'PUT',
        url: '/api'+this.ls_url+'/'+e.record.id
      });
    }
    Ext.Ajax.request(req);
    //~ if (e.record.phantom) {
      //~ Lino.do_action(this,{
        //~ method:'POST',url: '/api'+this.ls_url,
        //~ params:p,
        //~ after_success:on_success})
    //~ } else {
      //~ Lino.do_action(this,{
        //~ method:'PUT',
        //~ url: '/api'+this.ls_url+'/'+e.record.id, 
        //~ params:p, 
        //~ after_success:on_success});
    //~ }
  },

  initComponent : function(){
    //~ console.log('Lino.GridMixin.setup 1',this);
    //~ this.tbar = this.pager;
    Lino.GridPanel.superclass.initComponent.call(this);
    this.on('afteredit', this.on_afteredit);
    this.on('beforeedit', this.on_beforeedit);
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
  after_delete : function() {
    this.refresh();
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
  on_master_changed : function() {
    //~ cmp = this;
    //~ console.log('Lino.GridPanel.on_master_changed()',this.title);
    var todo = function() {
      //~ console.log('exec Lino.GridPanel.on_master_changed()',this.title);
      //~ var src = caller.config.url_data + "/" + record.id + ".jpg"
      //~ var p = this.ww.get_master_params();
      //~ for (k in p) this.getStore().setBaseParam(k,p[k]);
      this.set_base_params(this.ww.get_master_params());
      this.getStore().load(); 
    };
    Lino.do_when_visible(this,todo.createDelegate(this));
  }
  });
  

Lino.MainPanelMixin = {
  tbar_items : function() {
      return [ 
        this.search_field = new Ext.form.TextField({ 
          fieldLabel: "Search", 
          listeners: { scope:this, change:this.search_change }
          //~ value: this.get_base_params().query
          //~ scope:this, 
          //~ enableKeyEvents: true, 
          //~ listeners: { keypress: this.search_keypress }, 
          //~ id: "seachString" 
        }), 
        { scope:this, text: "csv", handler: function() { window.open('/api'+this.ls_url+'?fmt=csv') } } 
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









Lino.WindowWrapperBase = {

  setup : function() {
    console.log('Lino.WindowWrapper.setup',this);
    //~ this.window.window_wrapper = this;
    //~ this.main_item.ww = this;
    //~ 20101021 this.main_item.set_base_params(this.base_params);
    //~ Ext.apply(this.window,{renderTo: 'main_area'});
    
    Ext.apply(this.window_config,{items: this.main_item});
    
    if (this.config.active_tab) {
      //~ console.log('active_tab',config.active_tab,this.main_item.items.get(0));
      this.main_item.items.get(0).activeTab = this.config.active_tab;
      //~ this.main_item.items.get(0).activate(config.active_tab);
    }
  
    this.window = new Ext.Window(this.window_config);
    var main_area = Ext.getCmp('main_area')
    this.window.on('show', function(win) {
        main_area.on('resize', win.onWindowResize, win);
    });
    this.window.on('hide', function(win) {
        main_area.un('resize', win.onWindowResize, win);
    });
    
    //~ if (this.caller) {
      //~ var p = this.caller.ww.get_master_params();
      //~ console.log('get_master_params() from caller',p);
      //~ this.main_item.set_base_params(p);
    //~ }
    
    if (this.config.data_record) {
      console.log('Lino.WindowWrapper with data_record',this.config.data_record);
      //~ this.main_item.on_master_changed.defer(2000,this.main_item,[config.data_record]);
      //~ Lino.do_when_visible(this.main_item,function(){this.on_master_changed(config.data_record)});
      //~ this.main_item.on('afterrender',function(){this.main_item.on_master_changed(config.data_record)},this,{single:true});
      this.main_item.set_current_record(this.config.data_record);
      //~ return;
    } 
    if (this.config.record_id !== undefined) { // may be 0 
      console.log('Lino.WindowWrapper with record_id',this.config.record_id);
      this.main_item.goto_record_id(this.config.record_id);
    }
    
    //~ console.log('Lino.WindowWrapper.setup done',this);
  },
  show : function() {
      //~ console.time('WindowWrapper.show()');
      this.setup();
      this.window.show();
  },
  close : function() { 
      this.window.close();
  }
};


Lino.unused_IndexWrapper = function(config) {
  Ext.apply(config,{layout:'fit',maximized:true, constrain: true, renderTo: 'main_area'});
  this.main_item = config.main_item
  this.window_config = config;
  //~ this.window = new Ext.Panel(config);
  //~ this.window = new Ext.Window(config);
};

Ext.override(Lino.unused_IndexWrapper,Lino.WindowWrapperBase);

Lino.WindowWrapper = function(caller,config,params) {
  //~ console.log('Lino.WindowWrapper.constructor','config:',config,'params:',params);
  //~ console.time('WindowWrapper.constructor()');
  this.caller = caller;
  if (params) Ext.apply(config,params);
  //~ console.log('Lino.WindowWrapper.constructor 2','config:',config);
  Ext.applyIf(config,{base_params:{}});
  //~ console.log('Lino.WindowWrapper.constructor 3','config:',config);
  this.config = config;
  //~ this.config = config_fn(this); 
  this.slaves = {};
  //~ this.before_row_edit = config.before_row_edit.createDelegate(this);
  //~ if (this.config.actions) {
      //~ console.log('config.actions no longer used!!!');
  //~ }
  //~ console.log('Lino.WindowWrapper.constructor',config.title,'gonna call setup.');
  
  //~ this.main_item = config.main_panel;
  
  this.window_config = {
    layout: "fit", 
    maximized: true, renderTo: 'main_area', constrain: true,
    //~ autoHeight: true,
    title: this.config.title,
    //~ items: this.main_item, 
    //~ bbar: this.bbar_actions,
    //~ bbar: Lino.build_buttons(this,this.config.ls_bbar_actions),
    tools: [ 
      //~ { qtip: this.config.qtip, handler: Lino.save_wc_handler(this), id: "save" }, 
      //~ { qtip: 'Call doLayout() on main Container.', handler: Lino.refresh_handler(this), id: "refresh" },
      { qtip: 'permalink', handler: Lino.permalink_handler(this), id: "pin" },
      { qtip: 'close', handler: Lino.tools_close_handler(this), id: "close" } 
    ] 
  };
  
  //~ this.setup();
  
  //~ console.timeEnd('WindowWrapper.constructor()');
  //~ console.log('Lino.WindowWrapper.constructor',config.title,'returned from setup');
};

Ext.override(Lino.WindowWrapper,Lino.WindowWrapperBase);

//~ Lino.hidden_windows = [];

//~ Ext.apply(Lino.WindowWrapper.prototype,{
Ext.override(Lino.WindowWrapper,{
  closeAction : 'close',
  get_current_record : function() { 
    //~ if (this.main_item) return this.main_item.get_current_record()
    return this.main_item.get_current_record()
  },
  get_selected : function() { 
    return this.main_item.get_selected();
  },
  get_permalink : function() {
    var p = this.main_item.get_base_params() || {};
    console.log('get_permalink',p,this.get_permalink_params());
    Ext.apply(p,this.get_permalink_params());
    return this.get_permalink_url() + "?" + Ext.urlEncode(p);
  },
  get_master_params : function() {
    var p = {}
    p['mt'] = this.config.content_type; // ext_requests.URL_PARAM_MASTER_TYPE
    rec = this.get_current_record()
    if (rec) {
      if (rec.phantom) {
          p['mk'] = undefined; // ext_requests.URL_PARAM_MASTER_PK
      }else{
          p['mk'] = rec.id; // ext_requests.URL_PARAM_MASTER_PK
      }
    } else {
      p['mk'] = undefined;
    }
    //~ console.log('get_master_params returns',p);
    return p;
  },
  //~ get_base_params : function() { return {} },
  get_values : function() {
    var v = {};
    return v;
  },
  get_permalink_url : function() {
      return '/api'+this.main_item.ls_url;
  },
  get_permalink_params : function() {
      return {fmt:'grid'};
  },
  on_render : function() {},
  refresh : function() {},
  
  hide : function() { this.window.hide() },
  get_window_config : function() { return {} }
  
});



Lino.GridMixin = {
  refresh : function() { 
    this.main_item.refresh();
  }
};

Lino.GridMasterWrapper = Ext.extend(Lino.WindowWrapper,Lino.GridMixin);
Lino.GridMasterWrapper.override({
  setup : function() {
    //~ this.main_item.store.proxy.on('load',
    console.log('GridMasterWrapper.setup');
    this.main_item.store.on('load', function() {
        //~ console.log('GridMasterWrapper load',this.main_item.store.reader.arrayData);
        this.window.setTitle(this.main_item.store.reader.arrayData.title);
      }, this
    );
    Lino.WindowWrapper.prototype.setup.call(this);
  },
  add_row_listener : function(fn,scope) {
    // this.main_grid.add_row_listener(fn,scope);
    this.main_item.getSelectionModel().addListener('rowselect',fn,scope);
    //~ console.log(20100509,'Lino.GridMasterWrapper.add_row_listener',this.config.title);
  }
});



Lino.DetailWrapperBase = Ext.extend(Lino.WindowWrapper, {});
Lino.DetailWrapperBase.override({
  on_submit: function() {
    this.main_form.form.submit({
      //~ url:this.caller.config.url_data + '/' + this.config.record_id,
      url:'/api'+this.main_item.ls_url + '/' + this.config.record_id,
      //~ params: this.caller.get_master_params(this.caller.get_current_record()),
      method: 'PUT',
      scope: this,
      success: function(form, action) {
        Lino.notify(action.result.message);
        //~ this.close();
        this.caller.refresh();
      },
      failure: Lino.on_submit_failure,
      clientValidation: true
    })
  }
  //~ setup:function() {
    //~ this.main_item = this.config.main_panel;
    //~ Lino.WindowWrapper.prototype.setup.call(this);
    
  //~ }
})

Lino.DetailWrapper = Ext.extend(Lino.DetailWrapperBase, {
  //~ setup : function() {
    //~ Lino.DetailWrapperBase.prototype.setup.call(this);
  //~ },
  get_permalink_url : function() {
      return '/api'+this.main_item.ls_url+'/'+this.get_current_record().id;
  },
  get_permalink_params : function() {
    var p = {fmt:'detail'};
    var main = this.main_item.items.get(0);
    if (main.activeTab) {
      var tab = main.items.indexOf(main.activeTab);
      //~ console.log('main.activeTab',tab,main.activeTab);
      p.tab = tab
    }
    return p;
  },
  unused_get_permalink : function() {
    //~ return this.config.permalink_name +'(undefined,{record_id:'+this.current_record.id+'})';
    var url = '/api'+this.main_item.ls_url+'/'+this.get_current_record().id + '?fmt=detail';
    var main = this.main_item.items.get(0);
    if (main.activeTab) {
      var tab = main.items.indexOf(main.activeTab);
      //~ console.log('main.activeTab',tab,main.activeTab);
      url += '&tab=' + String(tab)
    }
    return url
  }
});

Lino.InsertWrapper = Ext.extend(Lino.DetailWrapperBase, {
  get_permalink_url : function() {
      return '/api'+this.main_item.ls_url;
  },
  get_permalink_params : function() {
      return {fmt:'insert'};
  },
  unused_get_permalink : function() {
    //~ return this.config.permalink_name +'(undefined,{record_id:'+this.current_record.id+'})';
    return '/api'+this.main_item.ls_url+'?fmt=insert';
  },
  
  on_submit: function() {
    this.main_form.form.submit({
      //~ url:this.caller.config.url_data,
      //~ url:this.caller.ls_data_url,
      url:'/api'+this.main_item.ls_url,
      params: this.get_master_params(),
      method: 'POST',
      scope: this,
      success: function(form, action) {
        Lino.notify(action.result.message);
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




function initializeFooBarDropZone(cmp) {
    console.log('initializeFooBarDropZone',cmp);
    cmp.dropTarget = new Ext.dd.DropTarget(cmp.bwrap, {
      //~ ddGroup     : 'gridDDGroup',
      notifyEnter : function(ddSource, e, data) {
        console.log('notifyEnter',ddSource,e,data);
        //Add some flare to invite drop.
        cmp.body.stopFx();
        cmp.body.highlight();
      },
      notifyDrop  : function(ddSource, e, data){
        console.log('notifyDrop',ddSource,e,data);
        // Reference the record (single selection) for readability
        //~ var selectedRecord = ddSource.dragData.selections[0];


        // Load the record into the form
        //~ formPanel.getForm().loadRecord(selectedRecord);


        // Delete record from the grid.  not really required.
        //~ ddSource.grid.store.remove(selectedRecord);

        return(true);
      }
    })
}
