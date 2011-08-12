// lino.js --- generated Thu Aug 11 22:03:03 2011 by Lino version 1.2.1.
Ext.BLANK_IMAGE_URL = '/media/extjs/resources/images/default/s.gif';
LANGUAGE_CHOICES = [ [ "en", "English" ], [ "de", "German" ], [ "fr", "French" ], [ "nl", "Dutch" ], [ "et", "Estonian" ] ];
STRENGTH_CHOICES = [ [ "0", "certainly not" ], [ "1", "rather not" ], [ "2", "normally" ], [ "3", "quite much" ], [ "4", "very much" ] ];
KNOWLEDGE_CHOICES = [ [ "0", "not at all" ], [ "1", "a bit" ], [ "2", "moderate" ], [ "3", "quite well" ], [ "4", "very well" ] ];
MEDIA_URL = '/media';
ROOT_URL = '';
/*
 Copyright 2009-2011 Luc Saffre
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
// test: Lino Tutorial (Lino version 1.2.1 using Python 2.7.1, Django 1.4 pre-alpha SVN-16376, python-dateutil 1.4.1, Cheetah 2.4.4, docutils 0.7, PyYaml 3.08, xhtml2pdf 3.0.32, ReportLab Toolkit 2.4, appy.pod 0.6.7 (2011/06/28 09:13))

/* MonthPickerPlugin: thanks to keypoint @ sencha forum
   http://www.sencha.com/forum/showthread.php?74002-3.x-Ext.ux.MonthMenu&p=356860#post356860
*/
Ext.namespace('Ext.ux'); 

Ext.ux.MonthPickerPlugin = function() { 
    var picker; 
    var oldDateDefaults; 

    this.init = function(pk) { 
        picker = pk; 
        picker.onTriggerClick = picker.onTriggerClick.createSequence(onClick); 
        picker.getValue = picker.getValue.createInterceptor(setDefaultMonthDay).createSequence(restoreDefaultMonthDay); 
        picker.beforeBlur = picker.beforeBlur.createInterceptor(setDefaultMonthDay).createSequence(restoreDefaultMonthDay); 
    }; 

    function setDefaultMonthDay() { 
        oldDateDefaults = Date.defaults.d; 
        Date.defaults.d = 1; 
        return true; 
    } 

    function restoreDefaultMonthDay(ret) { 
        Date.defaults.d = oldDateDefaults; 
        return ret; 
    } 

    function onClick(e, el, opt) { 
        var p = picker.menu.picker; 
        p.activeDate = p.activeDate.getFirstDateOfMonth(); 
        if (p.value) { 
            p.value = p.value.getFirstDateOfMonth(); 
        } 

        p.showMonthPicker(); 
         
        if (!p.disabled) { 
            p.monthPicker.stopFx(); 
            p.monthPicker.show(); 

            p.mun(p.monthPicker, 'click', p.onMonthClick, p); 
            p.mun(p.monthPicker, 'dblclick', p.onMonthDblClick, p); 
            p.onMonthClick = p.onMonthClick.createSequence(pickerClick); 
            p.onMonthDblClick = p.onMonthDblClick.createSequence(pickerDblclick); 
            p.mon(p.monthPicker, 'click', p.onMonthClick, p); 
            p.mon(p.monthPicker, 'dblclick', p.onMonthDblClick, p); 
        } 
    } 

    function pickerClick(e, t) { 
        var el = new Ext.Element(t); 
        if (el.is('button.x-date-mp-cancel')) { 
            picker.menu.hide(); 
        } else if(el.is('button.x-date-mp-ok')) { 
            var p = picker.menu.picker; 
            p.setValue(p.activeDate); 
            p.fireEvent('select', p, p.value); 
        } 
    } 

    function pickerDblclick(e, t) { 
        var el = new Ext.Element(t); 
        if (el.parent() 
            && (el.parent().is('td.x-date-mp-month') 
            || el.parent().is('td.x-date-mp-year'))) { 

            var p = picker.menu.picker; 
            p.setValue(p.activeDate); 
            p.fireEvent('select', p, p.value); 
        } 
    } 
}; 

Ext.preg('monthPickerPlugin', Ext.ux.MonthPickerPlugin);  

//~ /* 
  //~ http://www.diloc.de/blog/2008/03/05/how-to-submit-ext-forms-the-right-way/
//~ */
//~ /**
 //~ * This submit action is basically the same as the normal submit action,
 //~ * only that it uses the fields getSubmitValue() to compose the values to submit,
 //~ * instead of looping over the input-tags in the form-tag of the form.
 //~ *
 //~ * To use it, just use the OOSubmit-plugin on either a FormPanel or a BasicForm,
 //~ * or explicitly call form.doAction('oosubmit');
 //~ *
 //~ * @param {Object} form
 //~ * @param {Object} options
 //~ */
//~ Ext.ux.OOSubmitAction = function(form, options){
    //~ Ext.ux.OOSubmitAction.superclass.constructor.call(this, form, options);
//~ };

//~ Ext.extend(Ext.ux.OOSubmitAction, Ext.form.Action.Submit, {
    //~ /**
    //~ * @cfg {boolean} clientValidation Determines whether a Form's fields are validated
    //~ * in a final call to {@link Ext.form.BasicForm#isValid isValid} prior to submission.
    //~ * Pass <tt>false</tt> in the Form's submit options to prevent this. If not defined, pre-submission field validation
    //~ * is performed.
    //~ */
    //~ type : 'oosubmit',

    //~ // private
    //~ /**
     //~ * This is nearly a copy of the original submit action run method
     //~ */
    //~ run : function(){
        //~ var o = this.options;
        //~ var method = this.getMethod();
        //~ var isPost = method == 'POST';

        //~ var params = this.options.params || {};
        //~ if (isPost) Ext.applyIf(params, this.form.baseParams);

        //~ //now add the form parameters
        //~ this.form.items.each(function(field)
        //~ {
            //~ if (!field.disabled)
            //~ {
                //~ //check if the form item provides a specialized getSubmitValue() and use that if available
                //~ if (typeof field.getSubmitValue == "function")
                    //~ params[field.getName()] = field.getSubmitValue();
                //~ else
                    //~ params[field.getName()] = field.getValue();
            //~ }
        //~ });

        //~ //convert params to get style if we are not post
        //~ if (!isPost) params=Ext.urlEncode(params);

        //~ if(o.clientValidation === false || this.form.isValid()){
            //~ Ext.Ajax.request(Ext.apply(this.createCallback(o), {
                //~ url:this.getUrl(!isPost),
                //~ method: method,
                //~ params:params, //add our values
                //~ isUpload: this.form.fileUpload
            //~ }));

        //~ }else if (o.clientValidation !== false){ // client validation failed
            //~ this.failureType = Ext.form.Action.CLIENT_INVALID;
            //~ this.form.afterAction(this, false);
        //~ }
    //~ },

//~ });
//~ //add our action to the registry of known actions
//~ Ext.form.Action.ACTION_TYPES['oosubmit'] = Ext.ux.OOSubmitAction;




/**
JC Watsons solution (adapted to ExtJS 3.3.1 by LS) is elegant and simple:
`A "fix" for unchecked checkbox submission  behaviour
<http://www.sencha.com/forum/showthread.php?28449>`_

*/
Ext.lib.Ajax.serializeForm = function(form) {
    var fElements = form.elements || (document.forms[form] || Ext.getDom(form)).elements, 
        hasSubmit = false, 
        encoder = encodeURIComponent, 
        name, 
        data = '', 
        type, 
        hasValue;

    Ext.each(fElements, function(element){
        name = element.name;
        type = element.type;

        if (!element.disabled && name) {
            if (/select-(one|multiple)/i.test(type)) {
                Ext.each(element.options, function(opt){
                    if (opt.selected) {
                        hasValue = opt.hasAttribute ? opt.hasAttribute('value') : opt.getAttributeNode('value').specified;
                        data += String.format("{0}={1}&", encoder(name), encoder(hasValue ? opt.value : opt.text));
                    }
                });
            } else if (!(/file|undefined|reset|button/i.test(type))) {
                //~ if (!(/radio|checkbox/i.test(type) && !element.checked) && !(type == 'submit' && hasSubmit)) {
                if (!(type == 'submit' && hasSubmit)) {
                    data += encoder(name) + '=' + encoder(element.value) + '&';
                    hasSubmit = /submit/i.test(type);
                }
            }
        }
    });
    return data.substr(0, data.length - 1);
};




Ext.namespace('Lino');

Lino.status_bar = new Ext.ux.StatusBar({defaultText:'Lino version 1.2.1.'});


Lino.edit_tinymce_text = function(panel,options) {
  // `panel` is the HtmlBoxPanel
  
  var rec = panel.ww.get_current_record();
  var value = rec ? rec.data[panel.editor.name] : '';
  var saving = false;
  var todo_after_save = false;
  var discard_changes = false;
  
  
  function save() {
    //~ if (todo_after_save) {alert('tried to save again'); return; }
    if (saving) {alert('tried to save again'); return; }
    var url = panel.ww.main_item.get_record_url(rec.id);
    var params = Ext.apply({},panel.get_base_params());
    params[panel.editor.name] = editor.getValue();
    var a = { 
      params: params, 
      method: 'PUT',
      url: url,
      failure: function() {
          //~ if (editor.ed.getContainer()) 
          editor.ed.setProgressState(0);
          todo_after_save = false;
          saving = false;
          console.log('tinymce.save() failed. sorry.',arguments);
        },
      success: function() {
        saving = false;
        //~ if (editor.ed.getContainer()) 
        editor.ed.setProgressState(0);
        rec.data[panel.editor.name] = editor.getValue();
        if(todo_after_save) {
            var fn = todo_after_save;
            todo_after_save = false;
            fn();
        }
        //~ panel.ww.set_current_record(rec);
        panel.refresh();
      }
    };
    //~ if (editor.ed.getContainer()) 
    editor.ed.setProgressState(1); // Show progress
    saving = true;
    //~ console.log(a);
    Ext.Ajax.request(a);
  };
  function save_callback() {
      save();
      //~ save(function(){editor.ed.setDirty(false);})
      /* return true have the save button disabled.  
      That's not perfect because the PUT is asynchronous 
      and the response is not yet known.
      */
      return true;
  }
  //~ var actions = [
    //~ {text:"Save",handler:save}
  //~ ]; 
  //~ console.log(20110610,panel.editor.disabled);
  var settings = {};
  Ext.apply(settings,{
        readonly: panel.editor.disabled,
        //~ language: "de",
        plugins : "save,emotions,spellchecker,advhr,insertdatetime,preview,table,searchreplace,template", 
        // Theme options - button# indicated the row# only
        theme_advanced_buttons1 : "save,cancel,|,bold,italic,underline,|,justifyleft,justifycenter,justifyright,fontselect,fontsizeselect,formatselect,|,search,replace",
        theme_advanced_buttons2 : "cut,copy,paste,template,|,bullist,numlist,|,outdent,indent,|,undo,redo,|,link,unlink,anchor,image,|,code,preview,|,forecolor,backcolor",
        theme_advanced_buttons3 : "insertdate,inserttime,|,spellchecker,advhr,,removeformat,|,sub,sup,|,charmap,emotions,|,tablecontrols",      
        theme_advanced_resizing : false,
        save_onsavecallback : save_callback,
        save_enablewhendirty : true
        //~ save_oncancelcallback: on_cancel
  });
  Ext.apply(settings,options);
  var editor = new Ext.ux.TinyMCE({
      value : value,
      tinymceSettings: settings
    });
  var win = new Ext.Window({
    title: rec.title, 
    //~ bbar: actions,
    layout: 'fit',
    items: editor,
    width: 600, 
    height:500,
    minWidth: 100,
		minHeight: 100,
    modal: true,
    resizable: true,
    maximizable: true,
    //~ maximized: true,
    closeAction: "close"
    //~ hideMode: "offsets",
    //~ constrainHeader: true,
    //~ bodyStyle: 'padding: 10px'
  });

  win.on('beforeclose',function() {
    if (todo_after_save) return false;
    if (discard_changes) return true;
    if (editor.isDirty()) {
        //~ var ok = false;
        //~ var allowClose = true;
        var config = {title:"Confirmation"};
        config.buttons = Ext.MessageBox.YESNOCANCEL;
        config.msg = "Save changes to text ?";
        config.modal = true;
        config.fn = function(buttonId,text,opt) {
          //~ console.log('do_when_clean',buttonId)
          if (buttonId == "yes") {
              /* we cancel this close, but save()'s onSuccess will call again.*/
              //~ allowClose = false;
              todo_after_save = function(){win.close();}
              editor.ed.execCommand('mceSave');
              //~ editor.ed.save(function(){win.close();});
          } else if (buttonId == "no") { 
              discard_changes = true;
              win.close()
          //~ } else if (buttonId == "cancel") { 
            //~ ok = true;
              //~ allowClose = false;
          //~ } else { 
            //~ console.log('unknwon buttonId:',buttonId);
          }
        }
        Ext.MessageBox.show(config);
        return false;
        //~ return allowClose;
    }
  });
  win.show();
}





/* 
  Originally copied from Ext JS Library 3.3.1
  Modifications by Luc Saffre : 
  - rendering of phantom records
  - fire afteredit event
  - react on dblclcik, not on single click

 */
Lino.CheckColumn = Ext.extend(Ext.grid.Column, {

    processEvent : function(name, e, grid, rowIndex, colIndex){
        //~ console.log('20110713 Lino.CheckColumn.processEvent',name)
        if (name == 'click') {
        //~ if (name == 'mousedown') {
        //~ if (name == 'dblclick') {
            return this.toggleValue(grid, rowIndex, colIndex);
        } else {
            return Ext.grid.ActionColumn.superclass.processEvent.apply(this, arguments);
        }
    },
    
    toggleValue : function (grid,rowIndex,colIndex) {
        var record = grid.store.getAt(rowIndex);
        var dataIndex = grid.colModel.getDataIndex(colIndex);
        var startValue = record.data[dataIndex];
        var value = !startValue;
        //~ record.set(this.dataIndex, value);
        var e = {
            grid: grid,
            record: record,
            field: dataIndex,
            originalValue: startValue,
            value: value,
            row: rowIndex,
            column: colIndex,
            cancel:false
        };
        if(grid.fireEvent("validateedit", e) !== false && !e.cancel){
            record.set(dataIndex, value);
            delete e.cancel;
            grid.fireEvent("afteredit", e);
        }
        return false; // Cancel event propagation
    },

    renderer : function(v, p, record){
        if (record.phantom) return '';
        p.css += ' x-grid3-check-col-td'; 
        return String.format('<div class="x-grid3-check-col{0}">&#160;</div>', v ? '-on' : '');
    }

    // Deprecate use as a plugin. Remove in 4.0
    // init: Ext.emptyFn
});

// register ptype. Deprecate. Remove in 4.0
// Ext.preg('checkcolumn', Lino.CheckColumn);

// backwards compat. Remove in 4.0
// Ext.grid.CheckColumn = Lino.CheckColumn;

// register Column xtype
Ext.grid.Column.types.checkcolumn = Lino.CheckColumn;


/* 20110725 : 
Lino.on_tab_activate is necessary 
in contacts.Person.2.dtl 
(but don't ask me why...)
*/
Lino.on_tab_activate = function(item) {
  //~ console.log('activate',item); 
  if (item.rendered) item.doLayout();
}

Lino.TimeField = Ext.extend(Ext.form.TimeField,{
  format: 'H:i',
  increment: 15
  });
Lino.DateField = Ext.extend(Ext.form.DateField,{
  format: 'd.m.Y',
  altFormats: 'd/m/Y|Y-m-d'
  });
Lino.DateTimeField = Ext.extend(Ext.ux.form.DateTime,{
  dateFormat: 'd.m.Y',
  timeFormat: 'H:i',
  //~ hiddenFormat: 'd.m.Y H:i'
  });
Lino.URLField = Ext.extend(Ext.form.TriggerField,{
  triggerClass : 'x-form-search-trigger',
  vtype: 'url',
  onTriggerClick : function() {
    //~ console.log('Lino.URLField.onTriggerClick',this.value)
    //~ document.location = this.value;
    window.open(this.getValue(),'_blank');
  }
});

//~ Lino.make_dropzone = function(cmp) {
    //~ cmp.on('render', function(ct, position){
      //~ ct.el.on({
        //~ dragenter:function(event){
          //~ event.browserEvent.dataTransfer.dropEffect = 'move';
          //~ return true;
        //~ }
        //~ ,dragover:function(event){
          //~ event.browserEvent.dataTransfer.dropEffect = 'move';
          //~ event.stopEvent();
          //~ return true;
        //~ }
        //~ ,drop:{
          //~ scope:this
          //~ ,fn:function(event){
            //~ event.stopEvent();
            //~ console.log(20110516);
            //~ var files = event.browserEvent.dataTransfer.files;
            //~ if(files === undefined){
              //~ return true;
            //~ }
            //~ var len = files.length;
            //~ while(--len >= 0){
              //~ console.log(files[len]);
              //~ // this.processDragAndDropFileUpload(files[len]);
            //~ }
          //~ }
        //~ }
      //~ });
    //~ });
//~ };

//~ Lino.FileUploadField = Ext.ux.form.FileUploadField;

Lino.FileUploadField = Ext.extend(Ext.ux.form.FileUploadField,{
    onRender : function(ct, position){
      Lino.FileUploadField.superclass.onRender.call(this, ct, position);
      this.el.on({
        dragenter:function(event){
          event.browserEvent.dataTransfer.dropEffect = 'move';
          return true;
        }
        ,dragover:function(event){
          event.browserEvent.dataTransfer.dropEffect = 'move';
          event.stopEvent();
          return true;
        }
        ,drop:{
          scope:this
          ,fn:function(event){
            event.stopEvent();
            console.log(20110516);
            var files = event.browserEvent.dataTransfer.files;
            if(files === undefined){
              return true;
            }
            var len = files.length;
            while(--len >= 0){
              console.log(files[len]);
              //~ this.processDragAndDropFileUpload(files[len]);
            }
          }
        }
      });
    }
});

Lino.FileField = Ext.extend(Ext.form.TriggerField,{
  triggerClass : 'x-form-search-trigger',
  editable: false,
  onTriggerClick : function() {
    //~ console.log('Lino.URLField.onTriggerClick',this.value)
    //~ document.location = this.value;
    if (this.getValue()) window.open(MEDIA_URL + '/'+this.getValue(),'_blank');
  }
});

Lino.file_field_handler = function(ww,config) {
  if (ww instanceof Lino.DetailWrapper) {
      //~ return new Lino.URLField(config);
      return new Lino.FileField(config);
  }else{
      ww.fileUpload = true;
      var f = new Lino.FileUploadField(config);
      //~ Lino.make_dropzone(f);
      return f;
      //~ return new Ext.ux.form.FileUploadField(config);
      //~ return new Lino.FileField(config);
  }
}

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
              if (item.collapsed || item.flex == 0 || item.flex === undefined) {
                  //~ item.syncSize()
                  //~ item.doLayout()
                  //~ if (item.region == "north") console.log('region north',item.getHeight(),item.id, item);
                  //~ if (item.getHeight() == 0) console.log(20100921,'both flex and getHeight() are 0!');
                  availableHeight -= item.getHeight();
              } else {
                  sumflex += item.flex;
                  //~ console.log(item.flex);
              }
          } 
          //~ else console.log('non-vertical item in VBoderPanel:',item)
        }
        var hunit = availableHeight / sumflex;
        //~ console.log('sumflex=',sumflex,'hunit=',hunit, 'availableHeight=',availableHeight);
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
  modifications to the standard behaviour of a CellSelectionModel:
  
*/
Ext.override(Ext.grid.CellSelectionModel, {

    handleKeyDown : function(e){
        /* removed because F2 wouldn't pass
        if(!e.isNavKeyPress()){
            return;
        }
        */
        //~ console.log('handleKeyDown',e)
        var k = e.getKey(),
            g = this.grid,
            s = this.selection,
            sm = this,
            walk = function(row, col, step){
                return g.walkCells(
                    row,
                    col,
                    step,
                    g.isEditor && g.editing ? sm.acceptsNav : sm.isSelectable, 
                    sm
                );
            },
            cell, newCell, r, c, ae;

        switch(k){
            case e.ESC:
            case e.PAGE_UP:
            case e.PAGE_DOWN:
                
                break;
            default:
                
                // e.stopEvent(); // removed because Browser keys like Alt-Home, Ctrl-R wouldn't work
                break;
        }

        if(!s){
            cell = walk(0, 0, 1); 
            if(cell){
                this.select(cell[0], cell[1]);
            }
            return;
        }

        cell = s.cell;  
        r = cell[0];    
        c = cell[1];    
        
        switch(k){
            case e.TAB:
                if(e.shiftKey){
                    newCell = walk(r, c - 1, -1);
                }else{
                    newCell = walk(r, c + 1, 1);
                }
                break;
            case e.HOME:
                if (! (g.isEditor && g.editing)) {
                  if (!e.hasModifier()){
                      newCell = [r, 0];
                      //~ console.log('home',newCell);
                      break;
                  }else if(e.ctrlKey){
                      var t = g.getTopToolbar();
                      var activePage = Math.ceil((t.cursor + t.pageSize) / t.pageSize);
                      if (activePage > 1) {
                          e.stopEvent();
                          t.moveFirst();
                          return;
                      }
                      newCell = [0, c];
                      break;
                  }
                }
            case e.END:
                if (! (g.isEditor && g.editing)) {
                  c = g.colModel.getColumnCount()-1;
                  if (!e.hasModifier()) {
                      newCell = [r, c];
                      //~ console.log('end',newCell);
                      break;
                  }else if(e.ctrlKey){
                      var t = g.getTopToolbar();
                      var d = t.getPageData();
                      if (d.activePage < d.pages) {
                          e.stopEvent();
                          var self = this;
                          t.on('change',function(tb,pageData) {
                              var r = g.store.getCount()-2;
                              self.select(r, c);
                              //~ console.log('change',r,c);
                          },this,{single:true});
                          t.moveLast();
                          return;
                      } else {
                          newCell = [g.store.getCount()-1, c];
                          //~ console.log('ctrl-end',newCell);
                          break;
                      }
                  }
                }
            case e.DOWN:
                newCell = walk(r + 1, c, 1);
                break;
            case e.UP:
                newCell = walk(r - 1, c, -1);
                break;
            case e.RIGHT:
                newCell = walk(r, c + 1, 1);
                break;
            case e.LEFT:
                newCell = walk(r, c - 1, -1);
                break;
            case e.F2:
                if (!e.hasModifier()) {
                    if (g.isEditor && !g.editing) {
                        g.startEditing(r, c);
                        e.stopEvent();
                        return;
                    }
                    break;
                }
            case e.INSERT:
                if (!e.hasModifier()) {
                    if (g.ls_insert_handler && !g.editing) {
                        e.stopEvent();
                        Lino.show_insert(g);
                        return;
                    }
                    break;
                }
            case e.DELETE:
                if (!e.hasModifier()) {
                    if (!g.editing) {
                        e.stopEvent();
                        Lino.delete_selected(g);
                        return;
                    }
                    break;
                }
            case e.ENTER:
                e.stopEvent();
                g.onCellDblClick(r,c);
                break;
        }

        if(newCell){
        
            e.stopEvent();
            
            r = newCell[0];
            c = newCell[1];

            this.select(r, c); 

            if(g.isEditor && g.editing){ 
                ae = g.activeEditor;
                if(ae && ae.field.triggerBlur){
                    
                    ae.field.triggerBlur();
                }
                g.startEditing(r, c);
            }
        }
    }


});

 

function PseudoConsole() {
    this.log = function() {};
};
if (typeof(console) == 'undefined') console = new PseudoConsole();

Lino.notify = function(msg) {
  if (msg == undefined) msg = ''; else console.log(msg);
  //~ Ext.getCmp('konsole').update(msg);
  Lino.status_bar.setStatus({
    text: msg,
    iconCls: 'ok-icon',
    clear: true // auto-clear after a set interval
  });
  //~ Ext.getCmp('konsole').setTitle(msg.replace(/\n/g,'<br/>'));
  //~ Ext.getCmp('konsole').update(msg.replace(/\n/g,'<br/>'));
};
Lino.alert = function(msg) {
  //~ if (msg == undefined) msg = ''; else console.log(msg);
  Ext.MessageBox.alert('Notify',msg);
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
    Lino.notify();
    switch (action.failureType) {
        case Ext.form.Action.CLIENT_INVALID:
            Ext.Msg.alert('Client-side failure', 'Form fields may not be submitted with invalid values');
            break;
        case Ext.form.Action.CONNECT_FAILURE:
            Ext.Msg.alert('Connection failure', 'Ajax communication failed');
            break;
        case Ext.form.Action.SERVER_INVALID:
            Ext.Msg.alert('Server-side failure', action.result.message);
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
      //~ console.log('report_window_button',panel);
      var bp = ww.get_master_params();
      panel.ww = ww; // for HtmlBox. see blog/2010/1022
      handler(panel,{base_params:bp});
    }
  }
}




Lino.delete_selected = function(caller) {
  //~ console.log("Lino.delete_selected",caller);
  var recs1 = caller.get_selected();
  var recs = [];
  for ( var i=0; i < recs1.length; i++ ) { if (! recs1[i].phantom) recs.push(recs1[i]); }
  if (recs.length == 0) {
    Lino.notify("Please select at least one record.");
    return;
  };
  if (recs.length == 1) {
      if (recs[0].disable_delete) {
        Lino.alert(recs[0].disable_delete);
        return;
      }
  };
  //~ console.log(recs);
  Ext.MessageBox.show({
    title: 'Confirmation',
    msg: "Delete " + String(recs.length) + " rows. Are you sure?",
    buttons: Ext.MessageBox.YESNOCANCEL,
    fn: function(btn) {
      if (btn == 'yes') {
        for ( var i=0; i < recs.length; i++ ) {
          Lino.do_action(caller,{
              method:'DELETE',
              url:ROOT_URL+'/api'+caller.ls_url+'/'+recs[i].id
          })
        }
        caller.after_delete();
      }
      else Lino.notify("Dann eben nicht.");
    }
  });
};

Lino.action_handler = function (panel,on_success,gridmode) {
  return function (response) {
    if (response.responseText) {
      var result = Ext.decode(response.responseText);
      //~ console.log('Lino.do_action()',action.name,'result is',result);
      if (on_success && result.success) on_success(result);
      if (result.message) {
          if (result.alert && ! gridmode) {
              //~ Ext.MessageBox.alert('Alert',result.alert_msg);
              Ext.MessageBox.alert('Alert',result.message);
          } else {
              Lino.notify(result.message);
          }
      }
      if (result.refresh_all) {
          panel.ww.main_item.refresh();
      } else {
          if (result.refresh) panel.refresh();
      }
      if (result.open_url) {
          if (!result.message)
              Lino.notify('Open new window <a href="'+result.open_url+'" target="_blank">'+result.open_url+'</a>');
          window.open(result.open_url,'foo',"");
          //~ document.location = result.open_url;
      }
    }
  }
};

Lino.do_action = function(caller,action) {
  action.success = function(response) {
    console.log('Lino.do_action()',response,'action success');
    if (response.responseText) {
      var result = Ext.decode(response.responseText);
      //~ console.log('Lino.do_action()',action.name,'result is',result);
      if (result.success && action.after_success) action.after_success(result);
      if (result.message) {
          if (result.alert) {
              //~ Ext.MessageBox.alert('Alert',result.alert_msg);
              Ext.MessageBox.alert('Alert',result.message);
          } else {
              Lino.notify(result.message);
          }
      }
      
      //~ if (result.alert_msg) Ext.MessageBox.alert('Alert',result.alert_msg);
      //~ if (result.message) Lino.notify(result.message);
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

//~ Lino.gup = function( name )
//~ {
  //~ // Thanks to http://www.netlobo.com/url_query_string_javascript.html
  //~ name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  //~ var regexS = "[\\?&]"+name+"=([^&#]*)";
  //~ var regex = new RegExp( regexS );
  //~ var results = regex.exec( window.location.href );
  //~ if( results == null )
    //~ return "";
  //~ else
    //~ return results[1];
//~ };

//~ Lino.refresh_handler = function (ww) {
  //~ return function() { 
      //~ console.log('refresh',ww);
      //~ ww.main_item.doLayout(false,true);
      //~ ww.main_item.syncSize();
  //~ }
//~ };

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
    //~ console.log('AJAX failure:',response,options);
    Ext.MessageBox.alert('Action failed',
      'Lino server did not respond to Ajax request');
}
// Ext.Ajax.on('requestexception',Lino.ajax_error_handler)

Lino.main_menu = new Ext.Toolbar({});

// Path to the blank image should point to a valid location on your server
//~ Ext.BLANK_IMAGE_URL = MEDIA_URL + '/extjs/resources/images/default/s.gif'; 


// used as Ext.grid.Column.renderer for id columns in order to hide the special id value -99999
Lino.id_renderer = function(value, metaData, record, rowIndex, colIndex, store) {
  //~ if (record.phantom) return '';
  return value;
}

Lino.raw_renderer = function(value, metaData, record, rowIndex, colIndex, store) {
  return value;
}

Lino.text_renderer = function(value, metaData, record, rowIndex, colIndex, store) {
  //~ return "not implemented"; 
  return value;
}

//~ Lino.cell_button_renderer = function(value, metaData, record, rowIndex, colIndex, store) {
  //~ return '<input type="button" onclick="alert(value)" value=" ? ">' ;
//~ }


//~ Lino.default_renderer = function(value, metaData, record, rowIndex, colIndex, store) {
  //~ if (record.phantom) return '';
  //~ return value;
//~ }

Lino.fk_renderer = function(fkname,handlername) {
  //~ console.log('Lino.fk_renderer handler=',handler);
  return function(value, metaData, record, rowIndex, colIndex, store) {
    //~ console.log('Lino.fk_renderer',fkname,rowIndex,colIndex,record,metaData,store);
    if (record.phantom) return '';
    //~ if (value) 
        //~ return '<a href="' + url + '/' + String(record.data[fkname])\
          //~ + '?fmt=detail" target="_blank" onclick="Lino.on_fk_click">' + value + '</a>';
    if (value) {
        //~ var s = '<a href="#" onclick="' ;
        var s = '<a href="javascript:' ;
        s += handlername + '(undefined,{record_id:\'' + String(record.data[fkname]) + '\'})">';
        s += value + '</a>';
        //~ console.log('Lino.fk_renderer',value,'-->',s);
        return s
    }
    return '';
  }
};

//~ Lino.gfk_renderer = function() {
  //~ return function(value, metaData, record, rowIndex, colIndex, store) {
    //~ if (record.phantom) return '';
    //~ console.log('Lino.gfk_renderer',value,colIndex,record,metaData,store);
    //~ return value;
  //~ }
//~ };


Lino.build_buttons = function(panel,actions) {
  if (actions) {
    var buttons = Array(actions.length);
    var cmenu = Array(actions.length);
    for (var i=0; i < actions.length; i++) { 
      buttons[i] = new Ext.Toolbar.Button(actions[i]);
      cmenu[i] = actions[i]
      if (actions[i].panel_btn_handler) {
          var h = actions[i].panel_btn_handler.createCallback(panel,buttons[i]);
          if (actions[i].must_save) {
              //~ buttons[i].on('click',function() { panel.do_when_clean(h) });
              buttons[i].on('click',panel.do_when_clean.createDelegate(panel,[h]));
          } else {
              buttons[i].on('click',h);
          }
          cmenu[i].handler = actions[i].panel_btn_handler.createCallback(panel,cmenu[i]);
      }
    }
    return {bbar:buttons, cmenu:new Ext.menu.Menu(cmenu)};
  }
}

Lino.do_when_visible = function(cmp,todo) {
  //~ if (cmp.el && cmp.el.dom) 
  if (cmp.isVisible()) { 
    // 'visible' means 'rendered and not hidden'
    //~ console.log(cmp.title,'-> cmp is visible now');
    todo(); 
  } else { 
    //~ console.log('Lino.do_when_visible() must defer because not isVisible()',todo,cmp);
    //~ todo.defer(1000);
    if (cmp.rendered) {
      //~ console.log(cmp,'-> cmp is rendered but not visible: and now?');
      //~ console.log(cmp.title,'-> cmp is rendered but not visible: try again in a moment...');
      //~ var fn = function() {Lino.do_when_visible(cmp,todo)};
      //~ fn.defer(100);
      
      Lino.do_when_visible.defer(50,this,[cmp,todo]);
      //~ Lino.do_when_visible.defer(100,this,[cmp,todo]);
      
    } else {
      //~ console.log(cmp.title,'-> after render');
      cmp.on('afterrender',todo,cmp,{single:true});
    }
  }
  
};    

/*
*/
Lino.do_on_current_record = function(panel,fn,phantom_fn) {
  var rec = panel.get_current_record();
  if (rec == undefined) {
    Lino.notify("There's no selected record.");
    return;
  }
  if (rec.phantom) {
    if (phantom_fn) {
      phantom_fn(panel);
    } else {
      Lino.notify("Action not available on phantom record.");
    }
    return;
  }
  return fn(rec);
};

Lino.row_action_handler = function(action_name) {
  return function(panel,btn) {
    Lino.do_on_current_record(panel,function(rec) {
      //~ console.log(panel);
      var url = panel.get_record_url(rec.id);
      var p = Ext.apply({},panel.get_base_params());
      //~ var p = Ext.apply({},panel.get_master_params());
      p.an = action_name;
      //~ url += "?" + Ext.urlEncode(p);
      //~ window.open(url);
      Ext.Ajax.request({
        method: 'GET',
        url: url,
        params: p,
        success: Lino.action_handler(panel,function(result){})
      });
    });
  }
};

Lino.show_detail = function(panel,btn) {
  Lino.do_on_current_record(panel,
    function(rec) {
      panel.loadMask.show();
      //~ panel.my_load_mask.show();
      //~ alert('foo');
      //~ panel.ww.window.showMask('Bitte nochmal warten');
      //~ panel.ww.window.getEl().mask('Bitte nochmal warten','x-mask-loading');
      //~ panel.el.mask('Bitte nochmal warten','x-mask-loading');
      //~ panel.disable();
      panel.ls_detail_handler(panel,{
        record_id:rec.id,base_params:panel.get_base_params()
      });
      //~ panel.my_load_mask.hide();
      panel.loadMask.hide();
      //~ panel.ww.window.hideMask();
      //~ panel.el.unmask();
    },
    Lino.show_insert
  );
};

Lino.show_fk_detail = function(combo,e,handler) {
    //~ console.log(combo,e,handler);
    pk = combo.getValue();
    if (pk) {
        handler(undefined,{record_id: pk})
      } else {
        Lino.notify("Cannot show detail for empty foreign key.");
      }
};

Lino.show_insert = function(panel,btn) {
  var bp = panel.get_base_params();
  //~ console.log('20101025 insert_handler',bp)
  panel.ls_insert_handler(panel,{record_id:-99999,base_params:bp});
};

Lino.show_insert_duplicate = function(panel,btn) {
  Lino.do_on_current_record(panel,
    function(rec) {
      var newRec = {};
      Ext.apply(newRec,rec);
      newRec.id = -99999;
      panel.ls_insert_handler(panel,{data_record:rec,base_params:panel.get_base_params()});
    });
};

//~ Lino.update_row_handler = function(action_name) {
  //~ return function(panel,btn) {
    //~ Lino.notify("Sorry, " + action_name + " is not implemented.");
  //~ }
//~ };



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


//~ Lino.ButtonField = Ext.extend(Ext.form.TextField,{
//~ Lino.ButtonField = Ext.extend(Ext.form.Field,{
    //~ editable : false,
    //~ constructor : function(ww,config,params){
      //~ this.ww = ww;
      //~ if (params) Ext.apply(config,params);
      //~ Lino.ButtonField.superclass.constructor.call(this, config);
    //~ },
    //~ setButtons : function(buttons){
      //~ console.log('setButtons',buttons);
    //~ },
    //~ onRender : function(ct, position){
        //~ if(!this.el){
            //~ this.panel = new Ext.Container({items:[
              //~ {xtype:'button',text:'upload'},
              //~ {xtype:'button',text:'show'},
              //~ {xtype:'button',text:'edit'}
            //~ ]});
            //~ this.panel.ownerCt = this;
            //~ this.el = this.panel.getEl();

        //~ }
        //~ Lino.ButtonField.superclass.onRender.call(this, ct, position);
    //~ },

  
//~ });

Lino.FieldBoxMixin = {
  before_init : function(ww,config,params) {
    this.ww = ww;
    if (params) Ext.apply(config,params);
    var actions = Lino.build_buttons(this,config.ls_bbar_actions);
    if (actions) config.bbar = actions.bbar;
  },
  //~ constructor : function(ww,config,params){
    //~ this.ww = ww;
    //~ if (params) Ext.apply(config,params);
    //~ var actions = Lino.build_buttons(this,config.ls_bbar_actions);
    //~ if (actions) config.bbar = actions.bbar;
    //~ Lino.FieldBoxMixin.superclass.constructor.call(this, config);
  //~ },
  do_when_clean : function(todo) { todo() },
  //~ format_data : function(html) { return '<div class="htmlText">' + html + '</div>' },
  format_data : function(html) { return html },
  get_base_params : function() {
    // needed for insert action
    return this.base_params;
  },
  set_base_params : function(p) {
    this.base_params = p;
  },
  set_base_param : function(k,v) {
    this.base_params[k] = v;
  }
};

Lino.HtmlBoxPanel = Ext.extend(Ext.Panel,{
  disabled_in_insert_window : true,
  constructor : function(ww,config,params) {
    this.before_init(ww,config,params);
    Lino.HtmlBoxPanel.superclass.constructor.call(this, config);
  },
  //~ constructor : function(ww,config,params){
    //~ this.ww = ww;
    //~ if (params) Ext.apply(config,params);
    //~ var actions = Lino.build_buttons(this,config.ls_bbar_actions);
    //~ if (actions) config.bbar = actions.bbar;
    //~ Lino.FieldBoxMixin.constructor.call(this, ww,config,params);
  //~ },
  //~ constructor : function(ww,config,params){
    //~ this.ww = ww;
    //~ if (params) Ext.apply(config,params);
    //~ var actions = Lino.build_buttons(this,config.ls_bbar_actions);
    //~ if (actions) config.bbar = actions.bbar;
    //~ Lino.FieldBoxMixin.superclass.constructor.call(this, config);
  //~ },
  //~ disable : function() { var tb = this.getBottomToolbar(); if(tb) tb.disable()},
  //~ enable : function() { var tb = this.getBottomToolbar(); if(tb) tb.enable()},
  onRender : function(ct, position){
    Lino.HtmlBoxPanel.superclass.onRender.call(this, ct, position);
    this.ww.main_item.on('enable',this.enable,this);
    this.ww.main_item.on('disable',this.disable,this);
    this.el.on({
      dragenter:function(event){
        event.browserEvent.dataTransfer.dropEffect = 'move';
        return true;
      }
      ,dragover:function(event){
        event.browserEvent.dataTransfer.dropEffect = 'move';
        event.stopEvent();
        return true;
      }
      ,drop:{
        scope:this
        ,fn:function(event){
          event.stopEvent();
          console.log(20110516);
          var files = event.browserEvent.dataTransfer.files;
          if(files === undefined){
            return true;
          }
          var len = files.length;
          while(--len >= 0){
            console.log(files[len]);
            //~ this.processDragAndDropFileUpload(files[len]);
          }
          Lino.show_insert(this);
        }
      }
    });
  },
  refresh : function(after) {
    var record = this.ww.get_current_record();
    //~ console.log('HtmlBox.refresh()',this.title,record,record.title);
    var box = this.items.get(0);
    var todo = function() {
      if (this.disabled) return;
      //~ this.set_base_params(this.ww.get_base_params());
      this.set_base_params(this.ww.get_master_params());
      var el = box.getEl();
      if (el) {
        el.update(record ? this.format_data(record.data[this.name]) : '');
        //~ console.log('HtmlBox.refresh()',this.name);
      //~ } else {
        //~ console.log('HtmlBox.refresh() failed for',this.name);
      }
    };
    //~ Lino.do_when_visible(this,todo.createDelegate(this));
    Lino.do_when_visible(box,todo.createDelegate(this));
  }
});
Ext.override(Lino.HtmlBoxPanel,Lino.FieldBoxMixin);


Lino.RichTextPanel = Ext.extend(Ext.Panel,{
    
  initComponent : function(){
    Lino.RichTextPanel.superclass.initComponent.call(this);
  },
  constructor : function(ww,config,params) {
    //~ console.log('Lino.RichTextPanel.initComponent',this);
    //~ var url = TEMPLATES_URL + config.ls_url + "/" + String(rec.id) + "/" + config.name;
    //~ var url = TEMPLATES_URL + config.ls_url + "/" + config.name;
    var t = this;
    var tinymce_options = {
        theme : "advanced",
        content_css: ROOT_URL + '/media/lino/extjs/lino.css',
        language: 'en-us',
        //~ template_external_list_url : url,
        theme_advanced_toolbar_location : "top",
        theme_advanced_toolbar_align : "left",
        theme_advanced_statusbar_location : "bottom",
        template_popup_width : 700,
        template_popup_height : 500,
        template_replace_values : { 
            data_field : function(element){ 
                console.log(20110722,fieldName,t.ww.get_current_record()); 
                var fieldName = element.innerHTML;
                element.innerHTML = t.ww.get_current_record().data[fieldName];
            } 
        }
      };
      
    var editorConfig = {
      tinymceSettings: {
        plugins : "noneditable,template", 
        // Theme options - button# indicated the row# only
        theme_advanced_buttons1 : "bold,italic,underline,|,justifyleft,justifycenter,justifyright,|,bullist,numlist,|,outdent,indent,|,undo,redo,|,removeformat,template",
        theme_advanced_buttons2 : "",
        theme_advanced_buttons3 : "", // ,|,sub,sup,|,charmap",      
        theme_advanced_resizing : false
        //~ save_onsavecallback : save_callback,
        //~ save_enablewhendirty : true
        //~ save_oncancelcallback: on_cancel
        
    }};
    Ext.apply(editorConfig.tinymceSettings,tinymce_options);
    //~ editorConfig.name = config.action_name;
    editorConfig.name = config.name;
    delete config.name;
    //~ config.title = config.label;
    //~ delete config.label;
    this.before_init(ww,config,params);
    
    this.editor = new Ext.ux.TinyMCE(editorConfig);
    var t = this;
    config.tools = [{
                      qtip: "Edit text in own window", 
                      id: "up",
                      handler: function(){
                        if(t.editor.isDirty()) {
                            var record = t.ww.get_current_record();
                            record.data[t.editor.name] = t.editor.getValue();
                        }
                        Lino.edit_tinymce_text(t,tinymce_options)
                      }
                    }];
    
    config.items = this.editor;
    config.layout = "fit";
    Lino.RichTextPanel.superclass.constructor.call(this, config);
  },
  refresh : function(after) {
    var record = this.ww.get_current_record();
    //~ console.log('RichTextPanel.refresh()',this.title,record.title,record);
    var todo = function() {
      //~ this.set_base_params(this.ww.get_base_params());
      var url = ROOT_URL + '/templates' + this.ww.main_item.ls_url + "/" 
          + String(record.id) + "/" + this.editor.name;
      //~ console.log('RichTextPanel.refresh()',url);
      if (this.editor.ed) this.editor.ed.settings.template_external_list_url = url;
      this.set_base_params(this.ww.get_master_params());
      var v = record ? this.format_data(record.data[this.editor.name]) : ''
      this.editor.setValue(v);
    };
    Lino.do_when_visible(this,todo.createDelegate(this));
  }
});
Ext.override(Lino.RichTextPanel,Lino.FieldBoxMixin);


Lino.FormPanel = Ext.extend(Ext.form.FormPanel,{
  //~ trackResetOnLoad : true,
  //~ query_params : {},
  //~ 20110119b quick_search_text : '',
  constructor : function(ww,config,params){
    this.ww = ww;
    if (params) Ext.apply(config,params);
    //~ console.log(config);
    //~ console.log('FormPanel.constructor() 1',config)
    //~ Ext.applyIf(config,{base_params:{}});
    //~ console.log('FormPanel.constructor() 2',config)
    var actions = Lino.build_buttons(this,config.ls_bbar_actions);
    config.bbar = actions.bbar;
    //~ Ext.apply(config,Lino.build_buttons(this,config.ls_bbar_actions));
    //~ config.bbar = Lino.build_buttons(this,config.ls_bbar_actions);
    config.tbar = this.tbar_items();
    if (config.has_navigator) {
      config.tbar = config.tbar.concat([
        this.first = new Ext.Toolbar.Button({
          tooltip:"First",disabled:true,handler:this.moveFirst,scope:this,iconCls:'x-tbar-page-first'}),
        this.prev = new Ext.Toolbar.Button({
          tooltip:"Previous",disabled:true,handler:this.movePrev,scope:this,iconCls:'x-tbar-page-prev'}),
        this.next = new Ext.Toolbar.Button({
          tooltip:"Next",disabled:true,handler:this.moveNext,scope:this,iconCls:'x-tbar-page-next'}),
        this.last = new Ext.Toolbar.Button({
          tooltip:"Last",disabled:true,handler:this.moveLast,scope:this,iconCls:'x-tbar-page-last'})
      ]);
    }
    //~ console.log(20101117,this.ww.refresh);
    config.tbar = config.tbar.concat([
      {
        //~ text:'Refresh',
        handler:function(){ this.do_when_clean(this.refresh.createDelegate(this)) },
        iconCls: 'x-tbar-loading',
        tooltip:"Reload current record",
        scope:this}
    ]);
    config.tbar = config.tbar.concat([
        '->',
        this.displayItem = new Ext.Toolbar.TextItem({})
    ]);
    //~ if (config.can_config) {
    config.bbar = config.bbar.concat([
      '->',
      {text:'Layout Editor',handler:this.edit_detail_config,qtip:"Edit Detail Layout",scope:this}
    ])
    //~ }
    this.before_row_edit = config.before_row_edit.createDelegate(this);
      
    config.trackResetOnLoad = true;
    
    Lino.FormPanel.superclass.constructor.call(this, config);
      
    // let oosubmit replace submit:
    //~ this.form.oldSubmit=this.form.submit;
    //~ this.form.submit = function(options)
    //~ {
          //~ this.doAction('oosubmit', options);
          //~ return this;
    //~ };
      
    //~ console.log(20101222,this.form.trackResetOnLoad);
    //~ this.form.trackResetOnLoad = true;
      
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
  set_base_param : function(k,v) {
    this.ww.config.base_params[k] = v;
  },
  after_delete : function() {
    this.ww.close();
    //~ if (this.ww.caller) this.ww.caller.refresh();
  },
  moveFirst : function() {this.goto_record_id(this.current_record.navinfo.first)},
  movePrev : function() {this.goto_record_id(this.current_record.navinfo.prev)},
  moveNext : function() {this.goto_record_id(this.current_record.navinfo.next)},
  moveLast : function() {this.goto_record_id(this.current_record.navinfo.last)},
  
  get_record_url : function(record_id) {
      var url = ROOT_URL+'/api'+this.ls_url
      //~ var url = this.ww.config.url_data; // ls_url;
      url += '/' + String(record_id);
      return url;
  },
  
  refresh : function(after) { 
    //~ console.log('20110701 Lino.FormPanel.refresh()',this);
    if (this.current_record) {
        this.load_record_id(this.current_record.id,after);
    } else {
        this.set_current_record(undefined,after);
    }
  },
  
  do_when_clean : function(todo) {
    var this_ = this;
    if (this.form.isDirty()) {
        //~ console.log('20110701 do_when_clean() form is dirty');
        var config = {title:"Confirmation"};
        config.buttons = Ext.MessageBox.YESNOCANCEL;
        config.msg = "Save changes to current record ?";
        config.fn = function(buttonId,text,opt) {
          //~ console.log('do_when_clean',buttonId)
          if (buttonId == "yes") {
              //~ Lino.submit_detail(this_,undefined,todo);
              this_.ww.save(todo);
          } else if (buttonId == "no") { 
            todo();
          }
        }
        Ext.MessageBox.show(config);
    }else{
      //~ console.log('do_when_clean : now!')
      todo();
    }
  },
  
  goto_record_id : function(record_id) {
    //~ console.log('20110701 Lino.FormPanel.goto_record_id()',record_id);
    //~ var this_ = this;
    //~ this.do_when_clean(function() { this_.load_record_id(record_id) }
    this.do_when_clean(this.load_record_id.createDelegate(this,[record_id]));
  },
  
  load_record_id : function(record_id,after) {
    var this_ = this;
    //~ var p = { fmt: this.ww.config.action_name};
    var p = Ext.apply({},this.ww.config.base_params);
    //~ console.log('20110713 load_record_id',record_id,p);
    //~ console.log('20110713 action_name=',this.ww.config.action_name,
      //~ 'base_params=',this.ww.config.base_params);
    p.an = this.ww.config.action_name;
    p.fmt = 'json';
    //~ 20110119b p['query'] = this.quick_search_text;
    //~ Ext.apply(p,this.query_params);
    Ext.Ajax.request({ 
      waitMsg: 'Loading record...',
      method: 'GET',
      params: p,
      url: this_.get_record_url(record_id),
      success: function(response) {   
        // todo: convert to Lino.action_handler.... but result 
        if (response.responseText) {
          var rec = Ext.decode(response.responseText);
          //~ console.log('goto_record_id success',rec);
          if (rec.navinfo && rec.navinfo.recno == 0) {
              /* 
                recno 0 means "the requested pk exists but is not contained in the requested queryset".
                This can happen e.g. after search_change on a detail.
              */
              //~ this_.goto_record_id(rec.navinfo.first);
              if (rec.navinfo.first) {
                  this_.load_record_id(rec.navinfo.first);
              } else {
                  Ext.MessageBox.alert('Note',
                    "No more records to display. Detail window has been closed.");
                  this_.ww.close();
              }
                  
          } else {
              this_.set_current_record(rec,after);
          }
        }
      },
      failure: Lino.ajax_error_handler
    });
  },
  
  set_current_record : function(record,after) {
    this.current_record = record;
    //~ if (record) 
        //~ console.log('Lino.FormPanel.set_current_record',record.title,record);
    //~ else
        //~ console.log('Lino.FormPanel.set_current_record',record);
    //~ this.config.main_panel.form.load(record);    
    if (record) {
      this.enable();
      this.form.loadRecord(record);
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
    if (after) after();
  },
  unused_search_change : function(field,oldValue,newValue) {
    //~ console.log('FormPanel.search_change()');
    this.ww.config.base_params['query'] = field.getValue(); //~ 20110119b 
    //~ 20110119b this.quick_search_text = field.getValue(); 
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
      //~ console.log(20110609,arguments); 
      var params = {desc: editor.getValue()};
      Ext.apply(params,active_tab);
      var a = { 
        params: params, 
        method: 'PUT',
        url: '/detail_config'+_this.ls_url,
        failure : Lino.ajax_error_handler,
        success: Lino.action_handler( _this, function(result) {
          //~ console.log('detail_config/save success',result);
          win.close();
          document.location = _this.ww.get_permalink();
        })
      };
      //~ console.log('detail_config/save sent',a);
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
        if (response.responseText) {
          var result = Ext.decode(response.responseText);
          if (result.success) {
            editor.setValue(result.desc);
            save_btn.enable();
          }
        }
      }
    };
    Ext.Ajax.request(a);
    win.show();
  },
  //~ load_buttons_to : function(cmp,record) {
    //~ cmp.setButtons(record.data[cmp.name])
  //~ },
  //~ load_buttons_to : function(cmp,record) {
    //~ cmp.setButtons(record.data[cmp.name])
    //~ console.log('Lino.load_buttons_to()',cmp,record);
    //~ Lino.do_when_visible(cmp,function() {
      //~ cmp.setButtons(record.data[cmp.name])
      //~ var buttons = record.data[cmp.name]; // a list of button configs
      //~ var el = cmp.getEl();
      //~ for (i in buttons) {
          //~ buttons[i] = new Ext.Button(buttons[i])
      //~ };
      //~ console.log('load_buttons_to',buttons);
      //~ if (el) {
        //~ el.update(buttons);
      //~ }
      
    //~ });
    //~ cmp.on_master_changed();
  //~ },
  load_picture_to : function(cmp,record) {
    //~ console.log('FormPanel.load_picture_to()',record);
    var doit = function(src) {
        var f = function() {
          //~ console.log('Lino.load_picture()',src);
          cmp.el.dom.src = src;
        };
        Lino.do_when_visible(cmp,f);
    }
    if (record)
      //~ Ext.Ajax.request({
        //~ url: this.get_record_url(record.id),
        //~ params: {fmt:'image'},
        //~ success: function(result) {
          //~ var response = Ext.jsondecode
          //~ doit(response.open_url)
        //~ }
      //~ });
      //~ var src = this.get_record_url(record.id) + "?fmt=image"
      doit(this.get_record_url(record.id) + "?an=image");
      //~ var src = ROOT_URL+'/api'+this.ww.main_item.ls_url + "/" + record.id + "?fmt=image"
    else
      //~ doit('empty.jpg');
      doit(Ext.BLANK_IMAGE_URL);
  }
});


Lino.getRowClass = function(record, rowIndex, rowParams, store) {
  if (record.phantom) {
    //~ console.log(20101009);
    //~ rowParams.bodyStyle = "color:red;background-color:blue";
    return 'lino-phantom-row';
    }
  return '';
}
    
Lino.GridPanel = Ext.extend(Ext.grid.EditorGridPanel,{
  //~ quick_search_text : '',
  disabled_in_insert_window : true,
  clicksToEdit:2,
  enableColLock: false,
  autoHeight: false,
  //~ loadMask: true,
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
  loadMask: {msg:"Please wait..."},
  
  constructor : function(ww,config,params){
    this.ww = ww;
    if (params) Ext.apply(config,params);
    //~ Ext.applyIf(config,{base_params:{}});
    //~ this.ww = ww;
    var bp = { fmt:'json' }
    if (ww.main_item == this) { 
        // this gridpanel is the main component
        Ext.apply(bp,ww.config.base_params);    
    }
    //~ bp['fmt'] = 'json';
    
    //~ function on_proxy_load( proxy, transactionObject, callbackOptions ) {
      //~ console.log('on_proxy_load',transactionObject)
    //~ }
    var proxy = new Ext.data.HttpProxy({ 
      url: ROOT_URL+'/api'+config.ls_url, 
      method: "GET"
      //~ listeners: {load:on_proxy_load} 
    });
    //~ config.store = new Ext.data.JsonStore({ 
    //~ console.log('20110119 constructor',config.title,bp);
    config.store = new Ext.data.ArrayStore({ 
      listeners: { exception: Lino.on_store_exception }, 
      //~ proxy: new Ext.data.HttpProxy({ url: config.ls_data_url+'?fmt=json', method: "GET" }), remoteSort: true, 
      proxy: proxy, 
      //~ autoLoad: true,
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
        if (this.selModel.selection)
            return [ this.selModel.selection.record ];
        return [this.store.getAt(0)];
      };
      this.get_current_record = function() { 
        if (this.getSelectionModel().selection) 
          return this.selModel.selection.record;
        return this.store.getAt(0);
      };
    } else { 
      config.selModel = new Ext.grid.RowSelectionModel() 
      this.get_selected = function() {
        var sels = this.selModel.getSelections();
        if (sels.length == 0) sels = [this.store.getAt(0)];
        return sels
        //~ var sels = this.getSelectionModel().getSelections();
        //~ return Ext.pluck(sels,'id');
      };
      this.get_current_record = function() { 
        var rec = this.selModel.getSelected();
        if (rec == undefined) rec = this.store.getAt(0);
        return rec

      };
    };
    delete config.ls_quick_edit
    
    var tbar = this.tbar_items()
    
    var menu = [];
    var set_gc = function(index) {
      return function() {
        //~ console.log('set_gc() 20100812');
        this.getColumnModel().setConfig(
            this.apply_grid_config(index,this.ls_grid_configs,this.ls_columns));
      }
    }
    for (var i = 0; i < config.ls_grid_configs.length;i++) {
      var gc = config.ls_grid_configs[i];
      menu.push({text:gc.label,handler:set_gc(i),scope:this})
    }
    if(menu.length > 1) {
      tbar = tbar.concat([
        { text:"View",
          menu: menu,
          tooltip:"Select another view of this report"
        }
      ]);
    }
    
    if(false) {
      tbar = tbar.concat([
        { text:"Memo",
          xtype: 'button', 
          enableToggle: true, 
          listeners: { scope: this, 'toggle' : this.toggle_expand_memo},
          pressed : bp.expand,
          tooltip:"Expand memo fields"
        }
      ]);
    }
    
    config.tbar = new Ext.PagingToolbar({ 
      store: config.store, 
      prependButtons: true, 
      pageSize: config.page_length, 
      displayInfo: true, 
      beforePageText: "Page",
      afterPageText: "of {0}",
      displayMsg: "Displaying {0} - {1} of {2}",
      firstText: "First page",
      lastText: "Last page",
      prevText: "Previous page",
      nextText: "Next page",
      items: tbar
    });
    delete config.page_length
    
    var actions = Lino.build_buttons(this,config.ls_bbar_actions);
    config.cmenu = actions.cmenu;
    
    //~ Ext.apply(config,Lino.build_buttons(this,config.ls_bbar_actions));
    //~ config.bbar, this.cmenu = Lino.build_buttons(this,config.ls_bbar_actions);
    //~ this.cmenu = new Ext.menu.Menu({items: config.bbar});
    delete config.ls_bbar_actions
    
    //~ config.bbar = config.bbar.concat(['->']);
    //~ if(menu.length > 1) {
      //~ config.bbar = config.bbar.concat([
        //~ {text:'View',menu: menu,tooltip:"Select another view of this report"}
      //~ ]);
    //~ }
    //~ config.bbar = config.bbar.concat([
    //~ if (config.tools === undefined) config.tools = [];
    //~ config.tools = config.tools.concat([
      //~ {text:'GC',handler:this.manage_grid_configs,qtip:"Manage Grid Configurations",scope:this},
      //~ {handler:this.save_grid_config,qtip:"Save Grid Configuration",scope:this, id:"save"}
      //~ {text:'Save GC',handler:this.save_grid_config,qtip:"Save Grid Configuration",scope:this}
    //~ ]);
    
    //~ this.row_editor = new Ext.ux.grid.RowEditor();
    //~ config.plugins = [this.row_editor,new Lino.GridFilters()];
    
    config.plugins = [new Lino.GridFilters()];

    
    //~ this.row_editor.on({
      //~ scope: this,
      //~ afteredit: function(roweditor, changes, record, rowIndex) {
        //~ console.log(arguments);
      //~ }
    //~ });
    
    //~ config.colModel = new ext.grid.columnModel({defaultSortable:true,
      //~ columns:this.apply_grid_config(config.gc_name,config.ls_grid_configs,config.ls_columns)});
    config.columns = this.apply_grid_config(config.gc_name,config.ls_grid_configs,config.ls_columns);
    
    Lino.GridPanel.superclass.constructor.call(this, config);
    
    this.on('beforeedit',function(e) { this.before_row_edit(e.record)},this);
  },
  
  do_when_clean : function(todo) { todo() },
  
  onCellDblClick : function(g, row, col){
      if (this.ls_detail_handler) {
          //~ Lino.notify('show detail');
          Lino.show_detail(this);
          return false;
      }else{
        //~ console.log('startEditing');
        this.startEditing(row,col);
      }
  },
  
  get_record_url : function(record_id) {
      var url = ROOT_URL+'/api'+this.ls_url
      //~ var url = this.ww.config.url_data; // ls_url;
      url += '/' + String(record_id);
      return url;
  },
  
  get_base_params : function() {
    //~ return this.ww.config.base_params;
    return this.getStore().baseParams;
  },
  set_base_params : function(p) {
    //~ console.log('GridPanel.set_base_params',p)
    for (k in p) this.store.setBaseParam(k,p[k]);
  },
  set_base_param : function(k,v) {
    this.store.setBaseParam(k,v);
  },
  
  unused_search_change : function(field,oldValue,newValue) {
    //~ console.log('search_change',field.getValue(),oldValue,newValue)
    //~ 20110119
    //~ 20110119b this.quick_search_text = field.getValue();
    this.store.setBaseParam('query',field.getValue()); 
    this.refresh();
    //~ this.store.load({params: { 
      //~ start: 0, 
      //~ limit: this.getTopToolbar().pageSize,
      //~ query: this.quick_search_text
      //~ }});
  },
  
  apply_grid_config : function(index,grid_configs,rpt_columns) {
    //~ var rpt_columns = this.ls_columns;
    var gc = grid_configs[index];    
    //~ console.log('apply_grid_config() 20100812',name,gc);
    this.gc_name = index;
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
          col.hidden = gc.hiddens[i];
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
    
    //~ if (gc.hidden_cols) {
      //~ for (var i = 0; i < gc.hidden_cols.length; i++) {
        //~ var hc = gc.hidden_cols[i];
        //~ for (var j = 0; j < columns.length;j++) {
          //~ var col = columns[j];
          //~ if (col.dataIndex == hc) {
            //~ col.hidden = true;
            //~ break
          //~ }
        //~ }
      //~ }
    //~ }
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
    var hiddens = Array(cm.config.length);
    //~ var hiddens = Array(cm.config.length);
    var columns = Array(cm.config.length);
    //~ var columns = Array(cm.config.length);
    //~ var hidden_cols = [];
    //~ var filters = this.filters.getFilterValues();
    var p = this.filters.buildQuery(this.filters.getFilterData())
    for (var i = 0; i < cm.config.length; i++) {
      var col = cm.config[i];
      columns[i] = col.dataIndex;
      //~ hiddens[i] = col.hidden;
      widths[i] = col.width;
      hiddens[i] = col.hidden;
      //~ if (col.hidden) hidden_cols.push(col.dataIndex);
    }
    //~ p['hidden_cols'] = hidden_cols;
    p['widths'] = widths;
    p['hiddens'] = hiddens;
    p['columns'] = columns;
    p['name'] = this.gc_name;
    //~ var gc = this.ls_grid_configs[this.gc_name];
    //~ if (gc !== undefined) 
        //~ p['label'] = gc.label
    //~ console.log('20100810 save_grid_config',p);
    return p;
  },
  
  unused_manage_grid_configs : function() {
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
  
  unused_edit_grid_config : function(name) {
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
    var a = { 
      params:this.get_current_grid_config(), 
      method:'PUT',
      url:'/grid_config'+this.ls_url,
      success: Lino.action_handler(this),
      failure: Lino.ajax_error_handler
    };
    Ext.Ajax.request(a);
    //~ Lino.do_action(this,a);
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
    var p = {};
    //~ console.log('20101130 modified: ',e.record.modified);
    //~ console.log('20101130 value: ',e.value);
    //~ var p = e.record.getChanges();
    //~ console.log('20101130 getChanges: ',e.record.getChanges());
    //~ this.before_row_edit(e.record);
    for(k in e.record.getChanges()) {
        var v = e.record.get(k);
    //~ for(k in e.record.modified) {
        //~ console.log('20101130',k,'=',v);
        //~ var cm = e.grid.getColumnModel();
        //~ var di = cm.getDataIndex(k);
        var f = e.record.fields.get(k);
        //~ console.log('20101130 f = ',f);
        //~ var v = e.record.get(di);
        if (f.type.type == 'date') {
            p[k] = Ext.util.Format.date(v, f.dateFormat);
        }else{
            p[k] = v;
        }
        //~ var i = cm.findColumnIndex(k);
        //~ var r = cm.getRenderer(i);
        //~ var editor = cm.getCellEditor(i,e.row);
        //~ var col = e.grid.getColumnModel().getColumnById(k);
        //~ console.log('20101130 r = ',r(v));
        //~ var f = e.record.fields[k];
        //~ console.log('20101130 f = ',f);
        //~ console.log('20101130 editor = ',editor);
        //~ p[k] = f.getValue();
        //~ p[k] = r(v);
    }
    //~ console.log('20101130 p:',p);
    //~ var cm = e.grid.getColumnModel();
    //~ var di = cm.getDataIndex(e.column);
    //~ var f = e.record.fields.get(di);
    //~ console.log('20101130 f = ',f);
    //~ if (f.type.type == 'date') e.record.set(di,Ext.util.Format.date(e.value, f.dateFormat));
    
    
    //~ var p = e.record.data;
    
    // var p = {};
    //~ p['grid_afteredit_colname'] = e.field;
    //~ p[e.field] = e.value;
    //~ console.log('20100723 GridPanel.on_afteredit()',e);
    // add value used by ForeignKeyStoreField CHOICES_HIDDEN_SUFFIX
    // not sure whether this is still needed:
    p[e.field+'Hidden'] = e.value;
    // this one is needed so that this field can serve as choice context:
    e.record.data[e.field+'Hidden'] = e.value;
    // p[pk] = e.record.data[pk];
    // console.log("grid_afteredit:",e.field,'=',e.value);
    Ext.apply(p,this.get_base_params()); // needed for POST, ignored for PUT
    //~ Ext.apply(p,this.ww.config.base_params);
    //~ Ext.apply(p,this.store.baseParams);
    var self = this;
    var on_success = Lino.action_handler( this, function(result) {
      self.getStore().commitChanges(); // get rid of the red triangles
      self.getStore().reload();        // reload our datastore.
    },true);
    var req = {
        waitMsg: 'Saving your data...',
        success: on_success,
        params:p
    };
    if (e.record.phantom) {
      Ext.apply(req,{
        method: 'POST',
        url: ROOT_URL+'/api'+this.ls_url
      });
    } else {
      Ext.apply(req,{
        method: 'PUT',
        url: ROOT_URL+'/api'+this.ls_url+'/'+e.record.id
      });
    }
    //~ console.log('20110406 on_afteredit',req);
    Ext.Ajax.request(req);
  },

  initComponent : function(){
    //~ console.log('Lino.GridMixin.setup 1',this);
    //~ this.tbar = this.pager;
    Lino.GridPanel.superclass.initComponent.call(this);
    this.on('afteredit', this.on_afteredit);
    this.on('beforeedit', this.on_beforeedit);
    this.on('cellcontextmenu', Lino.cell_context_menu, this);
    //~ this.on('contextmenu', Lino.grid_context_menu, this);
    
    //~ this.on('resize', function(cmp,aw,ah,rw,rh) {
        //~ cmp.getTopToolbar().pageSize = cmp.calculatePageSize(this,aw,ah,rw,rh) || 10;
        //~ cmp.refresh();
      //~ }, this, {delay:500});
  },

  afterRender : function() {
    Lino.GridPanel.superclass.afterRender.call(this);
    // this.getView().mainBody.focus();
    // console.log(20100114,this.getView().getRows());
    // if (this.getView().getRows().length > 0) {
    //  this.getView().focusRow(1);
    // }
    //~ this.my_load_mask = new Ext.LoadMask(this.getEl(), {
        //~ msg:'Please wait...',
        //~ store:this.store});
      
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
  refresh : function(after) { 
    //~ Lino.notify('Lino.GridPanel.refresh');
    //~ Lino.notify('Lino.GridPanel.refresh '+this.store.proxy.url);
    var p = { params : {
        fmt : 'json',
        limit : this.getTopToolbar().pageSize,
        start : this.getTopToolbar().cursor
        //~ 20110119 query: this.quick_search_text
    } }
    if (after) {
        p.callback = function(r,options,success) {if(success) after()};
      }
    this.store.load(p);
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
    //~ if (! this.enabled) return;
    //~ cmp = this;
    //~ console.log('Lino.GridPanel.on_master_changed()',this.title);
    var todo = function() {
      if (this.disabled) return;
      //~ if (this.enabled) {
          //~ var src = caller.config.url_data + "/" + record.id + ".jpg"
          var p = this.ww.get_master_params();
          //~ for (k in p) this.getStore().setBaseParam(k,p[k]);
          //~ console.log('Lino.GridPanel.on_master_changed()',this.title,p);
          this.set_base_params(p);
          this.getStore().load(); 
      //~ }
    };
    Lino.do_when_visible(this,todo.createDelegate(this));
  }
});
  

Lino.MainPanelMixin = {
  tbar_items : function() {
      return [ 
        this.search_field = new Ext.form.TextField({ 
          fieldLabel: "Search", 
          listeners: { scope:this.ww, change:this.ww.search_change }
          //~ value: text
          //~ scope:this, 
          //~ enableKeyEvents: true, 
          //~ listeners: { keypress: this.search_keypress }, 
          //~ id: "seachString" 
        }), 
        { scope:this, 
          text: "csv", 
          handler: function() { 
            var p = Ext.apply({},this.get_base_params());
            p['fmt'] = 'csv';
            //~ url += "?" + Ext.urlEncode(p);
            window.open(ROOT_URL+'/api'+this.ls_url + "?" + Ext.urlEncode(p)) 
          } }
      ];
  }
};

Ext.override(Lino.GridPanel,Lino.MainPanelMixin);
Ext.override(Lino.FormPanel,Lino.MainPanelMixin);

//~ Lino.grid_context_menu = function(e) {
  //~ console.log('contextmenu',arguments);
//~ }

Lino.cell_context_menu = function(grid,row,col,e) {
  //~ console.log('cellcontextmenu',grid,row,col,e);
  e.stopEvent();
  //~ grid.getView().focusCell(row,col);
  grid.getSelectionModel().select(row,col);
  //~ console.log(grid.store.getAt(row));
  //~ grid.getView().focusRow(row);
  //~ return;
  if(!grid.cmenu.el){grid.cmenu.render(); }
  var xy = e.getXY();
  xy[1] -= grid.cmenu.el.getHeight();
  grid.cmenu.showAt(xy);
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
  forceSelection: true,
  triggerAction: 'all',
  autoSelect: false,
  submitValue: true,
  displayField: 'text', // 'text', 
  valueField: 'value', // 'value',
  
  //~ initComponent : Ext.form.ComboBox.prototype.initComponent.createSequence(function() {
  initComponent : function(){
      this.contextParams = {};
      //~ Ext.form.ComboBox.initComponent(this);
      Lino.ComboBox.superclass.initComponent.call(this);
  },
  setValue : function(v,record){
      /*
      Based on feature request developed in http://extjs.net/forum/showthread.php?t=75751
      */
      /* `record` is used to get the text corresponding to this value */
      //~ if(this.name == 'birth_country') 
        //~ console.log(this.name,'.setValue(', v ,') this=', this,'record=',record);
      var text = v;
      if(this.valueField){
        if(v == null || v == '') { 
            //~ if (this.name == 'birth_country') 
                //~ console.log(this.name,'.setValue',v,'no lookup needed, value is empty');
            //~ v = undefined;
            v = '';
        } else if (Ext.isDefined(record)) {
          text = record.data[this.name];
          //~ if (this.name == 'birth_country') 
            //~ console.log(this.name,'.setValue',v,'got text ',text,' from record ',record);
        } else {
          // if(this.mode == 'remote' && !Ext.isDefined(this.store.totalLength)){
          if(this.mode == 'remote' && ( this.lastQuery === null || (!Ext.isDefined(this.store.totalLength)))){
              //~ if (this.name == 'birth_country') console.log(this.name,'.setValue',v,'store not yet loaded');
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
                  //~ if (this.name == 'birth_country') 
                    //~ console.log(this.name,'.setValue',v,' : call load() with params ',params);
                  this.store.load({params: params});
              //~ }else{
                  //~ if (this.name == 'birth_country') 
                    //~ console.log(this.name,'.setValue',v,' : but store is loading',this.store.lastOptions);
              }
              return;
          //~ }else{
              //~ if (this.name == 'birth_country') 
                //~ console.log(this.name,'.setValue',v,' : store is loaded, lastQuery is "',this.lastQuery,'"');
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
          //~ this.hiddenField.originalValue = v;
          this.hiddenField.value = v;
      }
      Ext.form.ComboBox.superclass.setValue.call(this, text);
      this.value = v; // needed for grid.afteredit
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

Lino.ChoicesFieldElement = Ext.extend(Lino.ComboBox,{
  mode: 'local'
});


Lino.SimpleRemoteComboStore = Ext.extend(Ext.data.JsonStore,{
  forceSelection: true,
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
  //~ forceSelection:false,
  minChars: 2, // default 4 is to much
  queryDelay: 300, // default 500 is maybe slow
  queryParam: 'query', 
  //~ typeAhead: true,
  selectOnFocus: true, // select any existing text in the field immediately on focus.
  resizable: true
});

/*
Thanks to Animal for posting the basic idea:
http://www.sencha.com/forum/showthread.php?15842-2.0-SOLVED-Combobox-twintrigger-clear&p=76130&viewfull=1#post76130

*/
Lino.TwinCombo = Ext.extend(Lino.RemoteComboFieldElement,{
    trigger2Class : 'x-form-search-trigger',
    initComponent : function() {
        //~ Lino.TwinCombo.superclass.initComponent.call(this);
        Lino.ComboBox.prototype.initComponent.call(this);
        Ext.form.TwinTriggerField.prototype.initComponent.call(this);
    },
    onTrigger2Click : function() {
        //~ console.log('onTrigger2Click',this,arguments);
    }
  });
//~ Lino.TwinCombo.prototype.initComponent = Ext.form.TwinTriggerField.prototype.initComponent;
Lino.TwinCombo.prototype.getTrigger = Ext.form.TwinTriggerField.prototype.getTrigger;
Lino.TwinCombo.prototype.initTrigger = Ext.form.TwinTriggerField.prototype.initTrigger;
Lino.TwinCombo.prototype.onTrigger1Click = Ext.form.ComboBox.prototype.onTriggerClick;
//~ Lino.TwinCombo.prototype.onTrigger2Click = function() {
    //~ console.log('onTrigger2Click',arguments);
//~ };



Lino.SimpleRemoteComboFieldElement = Ext.extend(Lino.RemoteComboFieldElement,{
  displayField: 'value', 
  valueField: null,
  forceSelection: false
});









Lino.WindowWrapperBase = {

  setup : function() {
    //~ console.log('Lino.WindowWrapper.setup',this);
    //~ this.window.window_wrapper = this;
    //~ this.main_item.ww = this;
    //~ 20101021 this.main_item.set_base_params(this.base_params);
    //~ Ext.apply(this.window,{renderTo: 'main_area'});
    
    //~ 20110510
    //~ this.main_item.anchor = '100% 100%';
    //~ this.main_item.autoScroll = true;
    Ext.apply(this.window_config,{items: this.main_item});
    
    if (this.config.active_tab) {
      //~ console.log('active_tab',config.active_tab,this.main_item.items.get(0));
      this.main_item.items.get(0).activeTab = this.config.active_tab;
      //~ this.main_item.items.get(0).activate(config.active_tab);
    }
    if (this.config.base_params !== undefined) { // may be 0 
      //~ console.log('Lino.WindowWrapper with base_params',this.config.base_params);
      this.main_item.set_base_params(this.config.base_params);
      if (this.config.base_params.query) 
          this.main_item.search_field.setValue(this.config.base_params.query);
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
      //~ console.log('Lino.WindowWrapper with data_record',this.config.data_record.title);
      //~ this.main_item.on_master_changed.defer(2000,this.main_item,[config.data_record]);
      //~ Lino.do_when_visible(this.main_item,function(){this.on_master_changed(config.data_record)});
      //~ this.main_item.on('afterrender',function(){
      //~   this.main_item.on_master_changed(config.data_record)},this,{single:true});
      this.main_item.set_current_record(this.config.data_record);
      //~ return;
    } else if (this.config.record_id !== undefined) { // may be 0 
      //~ console.log('Lino.WindowWrapper with record_id',this.config.record_id);
      //~ this.main_item.goto_record_id(this.config.record_id);
      this.main_item.load_record_id(this.config.record_id);
    }
    
    //~ console.log('Lino.WindowWrapper.setup done',this);
  },
  show : function() {
      //~ console.time('WindowWrapper.show()');
      //~ Lino.load_mask.show();
      this.setup();
      this.window.show();
      //~ this.refresh();
      //~ Lino.load_mask.hide();
  },
  search_change : function(field,oldValue,newValue) {
    //~ console.log('search_change',field.getValue(),oldValue,newValue)
    this.main_item.set_base_param('query',field.getValue()); 
    this.main_item.refresh();
  },
  refresh : function(after) { 
    this.main_item.refresh(after);
  },
  close : function() { 
      this.window.close();
      if (this.caller) {
        if (this.caller.ww) {
            //~ console.log('20110110 gonna refresh ww:', this.caller.ww);
            this.caller.ww.refresh();
        } else {
            //~ console.log('20110110 refresh caller (no ww):', this.caller);
            this.caller.refresh();
        }
      //~ } else {
        //~ console.log('20110110 cannot refresh: no caller:', this);
      }
  }
};

Lino.WindowWrapper = function(caller,config,params,wc) {
  //~ console.log('Lino.WindowWrapper.constructor','config:',config,'params:',params);
  //~ console.time('WindowWrapper.constructor()');
  this.caller = caller;
  if (params) Ext.apply(config,params);
  //~ console.log('Lino.WindowWrapper.constructor 2','config:',config);
  Ext.applyIf(config,{base_params:{}});
  //~ console.log('Lino.WindowWrapper.constructor 3','config:',config);
  //~ config.base_params['fmt'] = config.action_name;
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
    //~ 20110510
    //~ layout: 'form', autoScroll: true,
    layout: "fit", 
    //~ maximized: true, 
    renderTo: 'main_area', constrain: true,
    //~ maximizable: true, 
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
  
  if (wc) 
      Ext.apply(this.window_config,wc);
  else 
      Ext.apply(this.window_config,{maximized: true});
  
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
    //~ var p = this.main_item.get_base_params() || {};
    var p = Ext.apply({},this.main_item.get_base_params());
    delete p.fmt;
    //~ if (p.fmt) delete p.fmt;
    Ext.apply(p,this.get_permalink_params());
     //~ p.fmt = 'html';
    //~ console.log('get_permalink',p,this.get_permalink_params());
    var url = this.get_permalink_url();
    if (Ext.urlEncode(p)) url = url + "?" + Ext.urlEncode(p);
    return url;
  },
  get_master_params : function() {
    var p = {}
    p['mt'] = this.config.content_type; 
    rec = this.get_current_record()
    if (rec) {
      if (rec.phantom) {
          p['mk'] = undefined; 
      }else{
          p['mk'] = rec.id; 
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
      return ROOT_URL+'/api' + this.main_item.ls_url;
  },
  get_permalink_params : function() {
      //~ return {an:'grid'};
      return {an:this.config.action_name};
  },
  on_render : function() {},
  //~ refresh : function() { },
  refresh : function(after) { 
    this.main_item.refresh(after);
  },
  
  hide : function() { this.window.hide() },
  get_window_config : function() { return {} }
  
});


Lino.GridMixin = {};

Lino.GridMasterWrapper = Ext.extend(Lino.WindowWrapper,Lino.GridMixin);
Lino.GridMasterWrapper.override({
  setup : function() {
    //~ this.main_item.store.proxy.on('load',
    //~ console.log('GridMasterWrapper.setup');
    var grid = this.main_item;
    this.main_item.store.on('load', function() {
        //~ console.log('GridMasterWrapper load',this.main_item.store.reader.arrayData);
        this.window.setTitle(grid.store.reader.arrayData.title);
        if(grid.selModel.getSelectedCell){         
            grid.selModel.select(0,0);
        }else{
            grid.selModel.selectFirstRow();
            grid.getView().focusEl.focus();
        }
      }, this
    );
    //~ if (this.main_item.tools === undefined) this.main_item.tools = [];
    this.window_config.tools = [
      //~ {text:'GC',handler:this.manage_grid_configs,qtip:"Manage Grid Configurations",scope:this},
      {handler:this.main_item.save_grid_config,qtip:"Save Grid Configuration",scope:this.main_item, id:"save"}
      //~ {text:'Save GC',handler:this.save_grid_config,qtip:"Save Grid Configuration",scope:this}
    ].concat(this.window_config.tools);
    
    Lino.WindowWrapper.prototype.setup.call(this);
    
  },
  show : function() {
      this.setup();
      this.window.show();
      this.refresh();
  },
  get_permalink_params : function() {
    var p = {};
    //~ var p = {an:this.config.action_name};
    return p;
  },
  add_row_listener : function(fn,scope) {
    // this.main_grid.add_row_listener(fn,scope);
    this.main_item.getSelectionModel().addListener('rowselect',fn,scope);
    //~ console.log(20100509,'Lino.GridMasterWrapper.add_row_listener',this.config.title);
  }
});



Lino.DetailWrapperBase = Ext.extend(Lino.WindowWrapper, {
  setup : function() {
    //~ setup active_fields();
    //~ Lino.DetailWrapperBase.prototype.setup.call(this);
    Lino.WindowWrapper.prototype.setup.call(this);
    var this_ = this;
    this.main_item.cascade(function(cmp){
      var active_field = false;
      for (i = 0; i < this_.config.active_fields.length; i++) {
        if (cmp.name == this_.config.active_fields[i]) {
            active_field = true; break;
        }
      };
      if (active_field) {
      //~ if (cmp instanceof Lino.GridPanel) {
          cmp.on("change",function() {this_.save()});
      }
    });
  }
});

Lino.DetailWrapper = Ext.extend(Lino.DetailWrapperBase, {
  get_permalink_url : function() {
      return ROOT_URL+'/api' + this.main_item.ls_url+'/'+this.get_current_record().id;
  },
  get_permalink_params : function() {
    var p = {};
    //~ var p = {an:'detail'};
    //~ var p = {an:this.config.action_name};
    var main = this.main_item.items.get(0);
    if (main.activeTab) {
      var tab = main.items.indexOf(main.activeTab);
      //~ console.log('main.activeTab',tab,main.activeTab);
      if (tab) p.tab = tab
    }
    return p;
  },
  save : function(after) {
      //~ console.log('20110701 DetailWrapper.save()',this);
      var panel = this.main_item;
      var rec = panel.get_current_record();
      //~ console.log('todo: Lino.submit_detail and Lino.submit_insert send also action name from btn',btn,panel.get_base_params())
      if (rec) {
        //~ Lino.notify('submit');
        //~ console.log('20110406 DetailWindow.save: panel.get_base_params() = <',panel.get_base_params(),'>');
        // 20110406
        panel.form.submit({
          url:ROOT_URL+'/api'+panel.ls_url + '/' + rec.id,
          method: 'PUT',
          //~ headers: { 'HTTP_X_REQUESTED_WITH' : 'XMLHttpRequest'},
          scope: panel,
          params: panel.get_base_params(), 
          success: function(form, action) {
            //~ panel.form.setValues(rec.data);
            //~ 20110701 panel.form.loadRecord(rec);
            Lino.notify(action.result.message);
            panel.refresh(after);
            //~ if (after) after(); else panel.refresh();
          },
          failure: Lino.on_submit_failure,
          clientValidation: true
        })
      } else Lino.notify("Sorry, no current record.");
  
  }
  
});

Lino.InsertWrapper = Ext.extend(Lino.DetailWrapperBase, {
  setup : function() {
    if (this.fileUpload) this.main_item.form.fileUpload = true;
    //~ this.config.base_params['fmt'] = 'insert';
    Lino.DetailWrapperBase.prototype.setup.call(this);
    this.main_item.cascade(function(cmp){
      //~ console.log('20110613 cascade',cmp);
      if (cmp.disabled_in_insert_window) {
      //~ if (cmp instanceof Lino.GridPanel) {
          cmp.disable();
      }
    });
  },
  get_permalink_url : function() {
      return ROOT_URL+'/api' + this.main_item.ls_url;
  },
  get_permalink_params : function() {
    return {an:this.config.action_name};      
    //~ return {an:'insert'};
  },
  save : function(after) {
    //~ console.log('InsertWrapper.save()',this);
    var panel = this.main_item;
    var _this = this;
    panel.form.submit({
      url:ROOT_URL+'/api'+panel.ls_url,
      method: 'POST',
      params: panel.get_base_params(), // 20101025
      scope: panel,
      success: function(form, action) {
        Lino.notify(action.result.message);
        if (_this.caller) {
          _this.close();
          if (_this.caller.ls_detail_handler) {
            //~ console.log(panel.ww.caller);
            _this.caller.ls_detail_handler(_this.caller,{
              record_id:action.result.record_id,
              base_params:_this.caller.get_base_params()});
            //~ Lino.show_detail_handler(panel.ww.caller.ls_detail_handler)(panel.ww.caller);
          //~ } else {
            // htmlbox doesn't have a detailwrapper
            //~ _this.caller.refresh();
          } 
        } else {
            // if there's no caller, then this was opened from a permalink.
            var p = Ext.apply({},_this.main_item.get_base_params());
            Ext.apply(p,{an:'detail'});
            var url = _this.get_permalink_url() + '/' + action.result.record_id + "?" + Ext.urlEncode(p);
            document.location = url;
        }
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
        /* Forward record to field.setValue(). 
        Lino never uses an array record here, so we can ignore this case. 
        */
        //~ console.log('20110214e loadRecord',record.data)
        var field, id;
        for(id in record.data){
            if(!Ext.isFunction(record.data[id]) && (field = this.findField(id))){
                field.setValue(record.data[id],record);
                if(this.trackResetOnLoad){
                    field.originalValue = field.getValue();
                    //~ if (field.hiddenField) {
                      //~ field.hiddenField.originalValue = field.hiddenField.value;
                    //~ }
                }
            }
        }
        return this;
    }
});




function initializeFooBarDropZone(cmp) {
    //~ console.log('initializeFooBarDropZone',cmp);
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


Ext.namespace('Lino.users.Users')
Lino.users.Users.grid = function(caller,params) { 
  var ww = new Lino.GridMasterWrapper(caller,{ "content_type": 2, "action_name": "grid" },params);
  var username1 = new Ext.form.TextField({ "allowBlank": false, "maxLength": 30 });
  var first_name2 = new Ext.form.TextField({ "maxLength": 30 });
  var last_name3 = new Ext.form.TextField({ "maxLength": 30 });
  var id8 = { "xtype": "numberfield" };
  var email9 = new Ext.form.TextField({ "maxLength": 75 });
  var last_login10 = new Ext.form.DisplayField({ "allowBlank": false });
  var date_joined11 = new Ext.form.DisplayField({ "allowBlank": false });
  var main_grid12 = new Lino.GridPanel(ww,{ "ls_url": "/users/Users", "ls_bbar_actions": [ { "text": "Delete", "panel_btn_handler": Lino.delete_selected } ], "gc_name": 0, "stripeRows": true, "ls_quick_edit": true, "ls_store_fields": [ { "name": "username" }, { "name": "first_name" }, { "name": "last_name" }, { "type": "boolean", "name": "is_active" }, { "type": "boolean", "name": "is_staff" }, { "type": "boolean", "name": "is_expert" }, { "type": "boolean", "name": "is_superuser" }, { "type": "int", "name": "id" }, { "name": "email" }, { "name": "last_login" }, { "name": "date_joined" } ], "pk_index": 7, "before_row_edit": function(record){  }, "ls_grid_configs": [  ], "ls_id_property": "id", "page_length": 30, "ls_columns": [ { "colIndex": 0, "sortable": true, "header": "username", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "username", "hidden": false, "editor": username1 }, { "colIndex": 1, "sortable": true, "header": "first name", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "first_name", "hidden": false, "editor": first_name2 }, { "colIndex": 2, "sortable": true, "header": "last name", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "last_name", "hidden": false, "editor": last_name3 }, { "colIndex": 3, "sortable": false, "xtype": "checkcolumn", "header": "is active", "editable": true, "filter": { "type": "boolean" }, "width": 90, "dataIndex": "is_active", "hidden": false }, { "colIndex": 4, "sortable": false, "xtype": "checkcolumn", "header": "is staff", "editable": true, "filter": { "type": "boolean" }, "width": 90, "dataIndex": "is_staff", "hidden": false }, { "colIndex": 5, "sortable": false, "xtype": "checkcolumn", "header": "is expert", "editable": true, "filter": { "type": "boolean" }, "width": 90, "dataIndex": "is_expert", "hidden": false }, { "colIndex": 6, "sortable": false, "xtype": "checkcolumn", "header": "is superuser", "editable": true, "filter": { "type": "boolean" }, "width": 90, "dataIndex": "is_superuser", "hidden": false }, { "colIndex": 7, "sortable": true, "header": "ID", "editable": true, "filter": { "type": "numeric" }, "width": 45, "renderer": Lino.id_renderer, "hidden": false, "editor": id8, "dataIndex": "id" }, { "colIndex": 8, "sortable": true, "header": "e-mail address", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "email", "hidden": false, "editor": email9 }, { "colIndex": 9, "sortable": true, "header": "last login", "editable": true, "width": 144, "dataIndex": "last_login", "hidden": false, "editor": last_login10 }, { "colIndex": 10, "sortable": true, "header": "date joined", "editable": true, "width": 144, "dataIndex": "date_joined", "hidden": false, "editor": date_joined11 } ] });
  ww.main_item = main_grid12;
  ww.show();
}

Ext.namespace('Lino.lino.SiteConfigs')
Lino.lino.SiteConfigs.grid = function(caller,params) { 
  var ww = new Lino.GridMasterWrapper(caller,{ "content_type": 3, "action_name": "grid" },params);
  var id35 = { "xtype": "numberfield" };
  var default_build_method36 = new Lino.ChoicesFieldElement({ "store": [ [ "appyodt", "AppyOdtBuildMethod" ], [ "appypdf", "AppyPdfBuildMethod" ], [ "appyrtf", "AppyRtfBuildMethod" ], [ "latex", "LatexBuildMethod" ], [ "pisa", "PisaBuildMethod" ], [ "rtf", "RtfBuildMethod" ] ] });
  var main_grid37 = new Lino.GridPanel(ww,{ "ls_url": "/lino/SiteConfigs", "ls_bbar_actions": [ { "text": "Delete", "panel_btn_handler": Lino.delete_selected } ], "gc_name": 0, "stripeRows": true, "ls_quick_edit": true, "ls_store_fields": [ { "type": "int", "name": "id" }, { "name": "default_build_method" },'default_build_methodHidden' ], "pk_index": 0, "before_row_edit": function(record){  }, "ls_grid_configs": [  ], "ls_id_property": "id", "page_length": 30, "ls_columns": [ { "colIndex": 0, "sortable": true, "header": "ID", "editable": true, "filter": { "type": "numeric" }, "width": 45, "renderer": Lino.id_renderer, "hidden": false, "editor": id35, "dataIndex": "id" }, { "colIndex": 1, "sortable": true, "header": "Default build method", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "default_build_method", "hidden": false, "editor": default_build_method36 } ] });
  ww.main_item = main_grid37;
  ww.show();
}

Ext.namespace('Lino.contenttypes.ContentTypes')
Lino.contenttypes.ContentTypes.grid = function(caller,params) { 
  var ww = new Lino.GridMasterWrapper(caller,{ "content_type": 1, "action_name": "grid" },params);
  var id42 = { "xtype": "numberfield" };
  var name43 = new Ext.form.TextField({ "allowBlank": false, "maxLength": 100 });
  var app_label44 = new Ext.form.TextField({ "allowBlank": false, "maxLength": 100 });
  var model45 = new Ext.form.TextField({ "allowBlank": false, "maxLength": 100 });
  var main_grid46 = new Lino.GridPanel(ww,{ "ls_url": "/contenttypes/ContentTypes", "ls_bbar_actions": [ { "text": "Delete", "panel_btn_handler": Lino.delete_selected } ], "gc_name": 0, "stripeRows": true, "ls_quick_edit": true, "ls_store_fields": [ { "type": "int", "name": "id" }, { "name": "name" }, { "name": "app_label" }, { "name": "model" } ], "pk_index": 0, "before_row_edit": function(record){  }, "ls_grid_configs": [  ], "ls_id_property": "id", "page_length": 30, "ls_columns": [ { "colIndex": 0, "sortable": true, "header": "ID", "editable": true, "filter": { "type": "numeric" }, "width": 45, "renderer": Lino.id_renderer, "hidden": false, "editor": id42, "dataIndex": "id" }, { "colIndex": 1, "sortable": true, "header": "name", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "name", "hidden": false, "editor": name43 }, { "colIndex": 2, "sortable": true, "header": "app label", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "app_label", "hidden": false, "editor": app_label44 }, { "colIndex": 3, "sortable": true, "header": "python model class name", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "model", "hidden": false, "editor": model45 } ] });
  ww.main_item = main_grid46;
  ww.show();
}

Ext.namespace('Lino.lino.TextFieldTemplates')
Lino.lino.TextFieldTemplates.grid = function(caller,params) { 
  var ww = new Lino.GridMasterWrapper(caller,{ "content_type": 5, "action_name": "grid" },params);
  var id55 = { "xtype": "numberfield" };
  var user56 = new Lino.RemoteComboFieldElement({ "store": new Lino.ComplexRemoteComboStore({ "proxy": new Ext.data.HttpProxy({ "url": "/choices/lino/TextFieldTemplates/user", "method": "GET" }) }), "pageSize": 30, "emptyText": "Select a User..." });
  var name57 = new Ext.form.TextField({ "allowBlank": false, "maxLength": 200 });
  var description58 = new Lino.RichTextPanel(ww,{ "ls_url": "/lino/TextFieldTemplates", "title": "Description" });
  var text59 = new Lino.RichTextPanel(ww,{ "ls_url": "/lino/TextFieldTemplates", "title": "Template Text" });
  var main_grid60 = new Lino.GridPanel(ww,{ "ls_url": "/lino/TextFieldTemplates", "ls_bbar_actions": [ { "text": "Delete", "panel_btn_handler": Lino.delete_selected } ], "gc_name": 0, "stripeRows": true, "ls_quick_edit": true, "ls_store_fields": [ { "type": "int", "name": "id" }, { "name": "user" },'userHidden', { "name": "name" }, { "name": "description" }, { "name": "text" } ], "pk_index": 0, "before_row_edit": function(record){ description58.refresh(); text59.refresh(); }, "ls_grid_configs": [  ], "ls_id_property": "id", "page_length": 30, "ls_columns": [ { "colIndex": 0, "sortable": true, "header": "ID", "editable": true, "filter": { "type": "numeric" }, "width": 45, "renderer": Lino.id_renderer, "hidden": false, "editor": id55, "dataIndex": "id" }, { "colIndex": 1, "sortable": true, "header": "user", "editable": true, "filter": { "type": "string" }, "width": 90, "dataIndex": "user", "hidden": false, "editor": user56 }, { "colIndex": 2, "sortable": true, "header": "Designation", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "name", "hidden": false, "editor": name57 }, { "colIndex": 3, "sortable": false, "header": "description", "editable": true, "filter": { "type": "string" }, "width": 540, "renderer": Lino.text_renderer, "hidden": false, "editor": description58, "dataIndex": "description" }, { "colIndex": 4, "sortable": false, "header": "text", "editable": true, "filter": { "type": "string" }, "width": 540, "renderer": Lino.text_renderer, "hidden": false, "editor": text59, "dataIndex": "text" } ] });
  ww.main_item = main_grid60;
  ww.show();
}

Ext.namespace('Lino.polls.Polls')
Lino.polls.Polls.FormPanel = Ext.extend(Lino.FormPanel,{
  constructor : function(ww,config) {
  var id74 = { "fieldLabel": "ID", "anchor": "100%", "name": "id", "xtype": "numberfield" };
  var id_ct_panel75 = new Ext.Container({ "flex": 12, "autoHeight": true, "labelWidth": 27, "items": [ id74 ], "frame": false, "border": false, "layout": "form" });
  var question76 = new Ext.form.TextField({ "allowBlank": false, "fieldLabel": "question", "anchor": "100%", "name": "question", "maxLength": 200 });
  var question_ct_panel77 = new Ext.Container({ "flex": 48, "autoHeight": true, "labelWidth": 81, "items": [ question76 ], "frame": false, "border": false, "layout": "form" });
  var pub_date78 = new Ext.form.DisplayField({ "disabled": true, "readOnly": true, "fieldLabel": "date published", "anchor": "100%", "name": "pub_date" });
  var pub_date_ct_panel79 = new Ext.Container({ "flex": 39, "autoHeight": true, "labelWidth": 135, "items": [ pub_date78 ], "frame": false, "border": false, "layout": "form" });
  var main_1_panel80 = new Ext.Container({ "border": false, "autoHeight": true, "layout": "hbox", "items": [ id_ct_panel75, question_ct_panel77, pub_date_ct_panel79 ], "frame": false, "layoutConfig": { "align": "stretchmax" } });
  var id81 = { "xtype": "numberfield" };
  var choice82 = new Ext.form.TextField({ "allowBlank": false, "maxLength": 200 });
  var votes83 = { "xtype": "numberfield", "allowBlank": false };
  var polls_ChoicesByPoll_grid85 = new Lino.GridPanel(ww,{ "flex": 83, "ls_url": "/polls/ChoicesByPoll", "ls_bbar_actions": [ { "text": "Delete", "panel_btn_handler": Lino.delete_selected } ], "title": "choices", "gc_name": 0, "stripeRows": true, "ls_quick_edit": true, "ls_store_fields": [ { "type": "int", "name": "id" }, { "name": "choice" }, { "type": "int", "name": "votes" } ], "pk_index": 0, "before_row_edit": function(record){  }, "ls_grid_configs": [  ], "ls_id_property": "id", "page_length": 30, "tools": [ Lino.report_window_button(ww,Lino.polls.ChoicesByPoll.grid) ], "ls_columns": [ { "colIndex": 0, "sortable": true, "header": "ID", "editable": true, "filter": { "type": "numeric" }, "width": 45, "renderer": Lino.id_renderer, "hidden": false, "editor": id81, "dataIndex": "id" }, { "colIndex": 1, "sortable": true, "header": "choice", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "choice", "hidden": false, "editor": choice82 }, { "colIndex": 2, "sortable": true, "header": "votes", "editable": true, "filter": { "type": "numeric" }, "width": 45, "dataIndex": "votes", "hidden": false, "editor": votes83 } ] });
  var main_panel86 = new Ext.Panel({ "border": false, "layout": "vbox", "autoScroll": true, "items": [ main_1_panel80, polls_ChoicesByPoll_grid85 ], "frame": true, "layoutConfig": { "align": "stretch" }, "bodyBorder": false, "labelAlign": "top" });
  config.items = main_panel86;
  config.before_row_edit = function(record){ polls_ChoicesByPoll_grid85.on_master_changed(); };
  Lino.polls.Polls.FormPanel.superclass.constructor.call(this, ww,config);
  }
});

Lino.polls.Polls.detail = function(caller,params) { 
  var ww = new Lino.DetailWrapper(caller,{ "content_type": 6, "name": "detail", "url_data": "/api/polls/Polls", "fk_name": null, "action_name": "detail", "active_fields": [  ] },params);
  var form_panel87 = new Lino.polls.Polls.FormPanel(ww,{ "ls_url": "/polls/Polls", "ls_bbar_actions": [ { "text": "Save", "handler": function() {ww.save()} }, { "text": "Insert", "must_save": true, "panel_btn_handler": function(panel){Lino.show_insert(panel)} }, { "text": "Delete", "panel_btn_handler": Lino.delete_selected } ], "ls_detail_handler": Lino.polls.Polls.detail, "has_navigator": true, "layout": "fit", "method": "PUT", "ls_insert_handler": Lino.polls.Polls.insert });
  ww.main_item = form_panel87;
  ww.show();
}

Lino.polls.Polls.insert = function(caller,params) { 
  var ww = new Lino.InsertWrapper(caller,{ "content_type": 6, "name": "insert", "url_data": "/api/polls/Polls", "record_id": -99999, "fk_name": null, "action_name": "insert", "active_fields": [  ] },params);
  var form_panel88 = new Lino.polls.Polls.FormPanel(ww,{ "ls_url": "/polls/Polls", "layout": "fit", "ls_detail_handler": Lino.polls.Polls.detail, "ls_bbar_actions": [ { "text": "Save", "handler": function() {ww.save()} } ], "method": "POST", "ls_insert_handler": Lino.polls.Polls.insert });
  ww.main_item = form_panel88;
  ww.show();
}

Lino.polls.Polls.grid = function(caller,params) { 
  var ww = new Lino.GridMasterWrapper(caller,{ "content_type": 6, "action_name": "grid" },params);
  var id71 = { "xtype": "numberfield" };
  var question72 = new Ext.form.TextField({ "allowBlank": false, "maxLength": 200 });
  var main_grid73 = new Lino.GridPanel(ww,{ "ls_url": "/polls/Polls", "ls_bbar_actions": [ { "text": "Detail", "panel_btn_handler": Lino.show_detail_handler }, { "text": "Insert", "must_save": true, "panel_btn_handler": function(panel){Lino.show_insert(panel)} }, { "text": "Delete", "panel_btn_handler": Lino.delete_selected } ], "ls_grid_configs": [  ], "gc_name": 0, "stripeRows": true, "ls_quick_edit": true, "ls_store_fields": [ { "type": "int", "name": "id" }, { "name": "question" } ], "pk_index": 0, "before_row_edit": function(record){  }, "ls_detail_handler": Lino.polls.Polls.detail, "ls_id_property": "id", "page_length": 30, "ls_columns": [ { "colIndex": 0, "sortable": true, "header": "ID", "editable": true, "filter": { "type": "numeric" }, "width": 45, "renderer": Lino.id_renderer, "hidden": false, "editor": id71, "dataIndex": "id" }, { "colIndex": 1, "sortable": true, "header": "question", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "question", "hidden": false, "editor": question72 } ], "ls_insert_handler": Lino.polls.Polls.insert });
  ww.main_item = main_grid73;
  ww.show();
}

Ext.namespace('Lino.polls.Choices')
Lino.polls.Choices.grid = function(caller,params) { 
  var ww = new Lino.GridMasterWrapper(caller,{ "content_type": 7, "action_name": "grid" },params);
  var id99 = { "xtype": "numberfield" };
  var poll100 = new Lino.TwinCombo({ "store": new Lino.ComplexRemoteComboStore({ "proxy": new Ext.data.HttpProxy({ "url": "/choices/polls/Choices/poll", "method": "GET" }) }), "onTrigger2Click": function(e){ Lino.show_fk_detail(this,e,Lino.polls.Polls.detail)}, "allowBlank": false, "pageSize": 30, "emptyText": "Select a poll..." });
  var choice101 = new Ext.form.TextField({ "allowBlank": false, "maxLength": 200 });
  var votes102 = { "xtype": "numberfield", "allowBlank": false };
  var main_grid103 = new Lino.GridPanel(ww,{ "ls_url": "/polls/Choices", "ls_bbar_actions": [ { "text": "Delete", "panel_btn_handler": Lino.delete_selected } ], "gc_name": 0, "stripeRows": true, "ls_quick_edit": true, "ls_store_fields": [ { "type": "int", "name": "id" }, { "name": "poll" },'pollHidden', { "name": "choice" }, { "type": "int", "name": "votes" } ], "pk_index": 0, "before_row_edit": function(record){  }, "ls_grid_configs": [  ], "ls_id_property": "id", "page_length": 30, "ls_columns": [ { "colIndex": 0, "sortable": true, "header": "ID", "editable": true, "filter": { "type": "numeric" }, "width": 45, "renderer": Lino.id_renderer, "hidden": false, "editor": id99, "dataIndex": "id" }, { "colIndex": 1, "sortable": true, "header": "poll", "editable": true, "filter": { "type": "string" }, "width": 90, "renderer": Lino.fk_renderer('pollHidden','Lino.polls.Polls.detail'), "hidden": false, "editor": poll100, "dataIndex": "poll" }, { "colIndex": 2, "sortable": true, "header": "choice", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "choice", "hidden": false, "editor": choice101 }, { "colIndex": 3, "sortable": true, "header": "votes", "editable": true, "filter": { "type": "numeric" }, "width": 45, "dataIndex": "votes", "hidden": false, "editor": votes102 } ] });
  ww.main_item = main_grid103;
  ww.show();
}

Ext.namespace('Lino.lino.DataControlListingReport')
Lino.lino.DataControlListingReport.FormPanel = Ext.extend(Lino.FormPanel,{
  constructor : function(ww,config) {
  config.items = new Ext.TabPanel({ "items": [  ], "activeTab": 0, "split": true });
  config.before_row_edit = function(record){  };
  Lino.lino.DataControlListingReport.FormPanel.superclass.constructor.call(this, ww,config);
  }
});

Lino.lino.DataControlListingReport.detail = function(caller,params) { 
  var ww = new Lino.DetailWrapper(caller,{ "content_type": 4, "name": "detail", "url_data": "/api/lino/DataControlListingReport", "fk_name": null, "action_name": "detail", "active_fields": [  ] },params);
  var form_panel115 = new Lino.lino.DataControlListingReport.FormPanel(ww,{ "ls_url": "/lino/DataControlListingReport", "layout": "fit", "ls_detail_handler": Lino.lino.DataControlListingReport.detail, "has_navigator": true, "ls_bbar_actions": [ { "text": "Save", "handler": function() {ww.save()} }, { "text": "Delete", "panel_btn_handler": Lino.delete_selected }, { "text": "Print", "must_save": true, "panel_btn_handler": Lino.row_action_handler('print') } ], "method": "PUT" });
  ww.main_item = form_panel115;
  ww.show();
}

Lino.lino.DataControlListingReport.listing = function(caller,params) { 
  var ww = new Lino.InsertWrapper(caller,{ "content_type": 4, "name": "listing", "url_data": "/api/lino/DataControlListingReport", "record_id": -99999, "fk_name": null, "action_name": "listing", "active_fields": [  ] },params);
  var form_panel116 = new Lino.lino.DataControlListingReport.FormPanel(ww,{ "ls_bbar_actions": [ { "text": "Save", "handler": function() {ww.save()} } ], "ls_url": "/lino/DataControlListingReport", "layout": "fit", "method": "POST", "ls_detail_handler": Lino.lino.DataControlListingReport.detail });
  ww.main_item = form_panel116;
  ww.show();
}

Lino.lino.DataControlListingReport.grid = function(caller,params) { 
  var ww = new Lino.GridMasterWrapper(caller,{ "content_type": 4, "action_name": "grid" },params);
  var id112 = { "xtype": "numberfield" };
  var date113 = new Lino.DateField({  });
  var main_grid114 = new Lino.GridPanel(ww,{ "ls_url": "/lino/DataControlListingReport", "ls_bbar_actions": [ { "text": "Detail", "panel_btn_handler": Lino.show_detail_handler }, { "text": "Delete", "panel_btn_handler": Lino.delete_selected }, { "text": "Print", "must_save": true, "panel_btn_handler": Lino.row_action_handler('print') } ], "gc_name": 0, "stripeRows": true, "ls_quick_edit": true, "ls_store_fields": [ { "type": "int", "name": "id" }, { "type": "date", "name": "date", "dateFormat": "d.m.Y" } ], "pk_index": 0, "before_row_edit": function(record){  }, "ls_detail_handler": Lino.lino.DataControlListingReport.detail, "ls_id_property": "id", "page_length": 30, "ls_columns": [ { "colIndex": 0, "sortable": true, "header": "ID", "editable": true, "filter": { "type": "numeric" }, "width": 45, "renderer": Lino.id_renderer, "hidden": false, "editor": id112, "dataIndex": "id" }, { "colIndex": 1, "sortable": true, "xtype": "datecolumn", "format": "d.m.Y", "editable": true, "filter": { "type": "date" }, "header": "Date", "dataIndex": "date", "hidden": false, "width": 72, "editor": date113 } ], "ls_grid_configs": [  ] });
  ww.main_item = main_grid114;
  ww.show();
}

Ext.namespace('Lino.lino.MyTextFieldTemplates')
Lino.lino.MyTextFieldTemplates.grid = function(caller,params) { 
  var ww = new Lino.GridMasterWrapper(caller,{ "content_type": 5, "action_name": "grid" },params);
  var id121 = { "xtype": "numberfield" };
  var name122 = new Ext.form.TextField({ "allowBlank": false, "maxLength": 200 });
  var description123 = new Lino.RichTextPanel(ww,{ "ls_url": "/lino/MyTextFieldTemplates", "title": "Description" });
  var text124 = new Lino.RichTextPanel(ww,{ "ls_url": "/lino/MyTextFieldTemplates", "title": "Template Text" });
  var main_grid125 = new Lino.GridPanel(ww,{ "ls_url": "/lino/MyTextFieldTemplates", "ls_bbar_actions": [ { "text": "Delete", "panel_btn_handler": Lino.delete_selected } ], "gc_name": 0, "stripeRows": true, "ls_quick_edit": true, "ls_store_fields": [ { "type": "int", "name": "id" }, { "name": "name" }, { "name": "description" }, { "name": "text" } ], "pk_index": 0, "before_row_edit": function(record){ description123.refresh(); text124.refresh(); }, "ls_grid_configs": [  ], "ls_id_property": "id", "page_length": 30, "ls_columns": [ { "colIndex": 0, "sortable": true, "header": "ID", "editable": true, "filter": { "type": "numeric" }, "width": 45, "renderer": Lino.id_renderer, "hidden": false, "editor": id121, "dataIndex": "id" }, { "colIndex": 1, "sortable": true, "header": "Designation", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "name", "hidden": false, "editor": name122 }, { "colIndex": 2, "sortable": false, "header": "description", "editable": true, "filter": { "type": "string" }, "width": 540, "renderer": Lino.text_renderer, "hidden": false, "editor": description123, "dataIndex": "description" }, { "colIndex": 3, "sortable": false, "header": "text", "editable": true, "filter": { "type": "string" }, "width": 540, "renderer": Lino.text_renderer, "hidden": false, "editor": text124, "dataIndex": "text" } ] });
  ww.main_item = main_grid125;
  ww.show();
}

Ext.namespace('Lino.polls.ChoicesByPoll')
Lino.polls.ChoicesByPoll.grid = function(caller,params) { 
  var ww = new Lino.GridMasterWrapper(caller,{ "content_type": 7, "action_name": "grid" },params);
  var id81 = { "xtype": "numberfield" };
  var choice82 = new Ext.form.TextField({ "allowBlank": false, "maxLength": 200 });
  var votes83 = { "xtype": "numberfield", "allowBlank": false };
  var main_grid84 = new Lino.GridPanel(ww,{ "ls_url": "/polls/ChoicesByPoll", "ls_bbar_actions": [ { "text": "Delete", "panel_btn_handler": Lino.delete_selected } ], "gc_name": 0, "stripeRows": true, "ls_quick_edit": true, "ls_store_fields": [ { "type": "int", "name": "id" }, { "name": "choice" }, { "type": "int", "name": "votes" } ], "pk_index": 0, "before_row_edit": function(record){  }, "ls_grid_configs": [  ], "ls_id_property": "id", "page_length": 30, "ls_columns": [ { "colIndex": 0, "sortable": true, "header": "ID", "editable": true, "filter": { "type": "numeric" }, "width": 45, "renderer": Lino.id_renderer, "hidden": false, "editor": id81, "dataIndex": "id" }, { "colIndex": 1, "sortable": true, "header": "choice", "editable": true, "filter": { "type": "string" }, "width": 180, "dataIndex": "choice", "hidden": false, "editor": choice82 }, { "colIndex": 2, "sortable": true, "header": "votes", "editable": true, "filter": { "type": "numeric" }, "width": 45, "dataIndex": "votes", "hidden": false, "editor": votes83 } ] });
  ww.main_item = main_grid84;
  ww.show();
}

