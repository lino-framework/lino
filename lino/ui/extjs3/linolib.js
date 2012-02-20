/*
 Copyright 2009-2012 Luc Saffre
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

$ui.linolib_intro()

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

Added special handling for checkbox inputs. 
ExtJS defines disabled checkboxes `readonly`, not `disabled` as for other inputs.

*/
Ext.lib.Ajax.serializeForm = function(form) {
    //~ console.log('20120203 linolib.js serializeForm',form);
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

        if (!element.disabled && name && !(type == 'checkbox' && element.readonly)) {
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
                    if (type == 'checkbox') {
                        //~ console.log('20111001',element,'data += ',encoder(name) + '=' + (element.checked ? 'on' : 'off') + '&');
                        data += encoder(name) + '=' + (element.checked ? 'on' : 'off') + '&';
                    } else {
                        //~ console.log('20111001',element,'data += ',encoder(name) + '=' + encoder(element.value) + '&');
                        data += encoder(name) + '=' + encoder(element.value) + '&';
                    }
                    hasSubmit = /submit/i.test(type);
                }
            }
        //~ } else {
            //~ console.log(name,type,element.readonly);
        }
    });
    return data.substr(0, data.length - 1);
};

Ext.namespace('Lino');

/*
Instead of serializing the fields of a params_panel, we want their values be stored into an object.

The following code is a collage of serializeForm and Action.Submit.run()
*/
Lino.unused_form2dict = function(pp) {
  
    if(!pp.form.isValid()) {
        console.log('20120203 WARNING form2dict found invalid data',pp);
        //~ return;
    }
      
    var frm = Ext.getDom(pp.form.el.dom)
      //~ var frm = this.params_panel.form.el.dom
    if (!frm) {
        console.log('20120203 form2dict no frm',pp);
        return;
    }
    
    var fields = pp.form.items,
        emptyFields = [],
        setupEmptyFields = function(f){
            if (f.el.getValue() == f.emptyText) {
                emptyFields.push(f);
                f.el.dom.value = "";
            }
            if(f.isComposite && f.rendered){
                f.items.each(setupEmptyFields);
            }
        };
        
    fields.each(setupEmptyFields);
        
    var data = {};
      
    var fElements = frm.elements,
        hasSubmit = false, 
        name, 
        type, 
        hasValue;

    Ext.each(fElements, function(element){
        name = element.name;
        type = element.type;
        if (!element.disabled && name && !(type == 'checkbox' && element.readonly)) {
            if (/select-(one|multiple)/i.test(type)) {
                Ext.each(element.options, function(opt){
                    if (opt.selected) {
                        hasValue = opt.hasAttribute ? opt.hasAttribute('value') : opt.getAttributeNode('value').specified;
                        data[name] = hasValue ? opt.value : opt.text;
                    }
                });
            } else if (!(/file|undefined|reset|button/i.test(type))) {
                //~ if (!(/radio|checkbox/i.test(type) && !element.checked) && !(type == 'submit' && hasSubmit)) {
                if (!(type == 'submit' && hasSubmit)) {
                    if (type == 'checkbox') {
                        //~ console.log('20111001',element,'data += ',encoder(name) + '=' + (element.checked ? 'on' : 'off') + '&');
                        data[name] = (element.checked ? 'on' : 'off')
                    } else {
                        //~ console.log('20111001',element,'data += ',encoder(name) + '=' + encoder(element.value) + '&');
                        data[name] = element.value
                    }
                    hasSubmit = /submit/i.test(type);
                }
            }
        }
    });
    
    Ext.each(emptyFields, function(f) {
        if (f.applyEmptyText) {
            f.applyEmptyText();
        }
    });
      
    return data;
};




Lino.current_window = null;
Lino.window_history = Array();

Lino.open_window = function(win,st) {
  //~ console.log("20120203 Lino.open_window()",win,st);
  var cw = Lino.current_window;
  if (cw) {
    Lino.window_history.push({
      window:cw,
      status:cw.main_item.get_status()
    });
  }
  Lino.current_window = win;
  win.main_item.set_status(st);
  win.show();
};

Lino.close_window = function(status_update) {
  var cw = Lino.current_window;
  var ww = Lino.window_history.pop();
  if (ww) {
    //~ if (status_update) Ext.apply(ww.status,status_update);
    if (status_update) status_update(ww);
    ww.window.main_item.set_status(ww.status);
    Lino.current_window = ww.window;
  } else {
    Lino.current_window = null;
  }
  if (cw) cw.hide_really();
};

Lino.kill_current_window = function() {
  var cw = Lino.current_window;
  Lino.current_window = null;
  if (cw) cw.hide_really();
};

Lino.calling_window = function() {
    if (Lino.window_history.length) return Lino.window_history[Lino.window_history.length-1];
}

Lino.PanelMixin = {
  get_containing_window : function (){
      if (this.containing_window) return this.containing_window;
      return this.containing_panel.get_containing_window();
  }
  ,set_window_title : function(title) {
    //~ this.setTitle(title);
    var cw = this.get_containing_window();

    //~ if (cw) {
    //~ if (cw && cw.closable) {
    if (cw && !cw.main_item.hide_window_title) {
      //~ console.log('20111202 set_window_title(',title,') for',this.containing_window);
      //~ if (! this.containing_window.rendered) console.log("WARNING: not rendered!");
      cw.setTitle(title);
    //~ } else {
      //~ document.title = title;
    }
    //~ else console.log('20111202 not set_window_title(',title,') for',this);
  }
  
};


Lino.status_bar = new Ext.ux.StatusBar({defaultText:'Lino version $(lino.__version__).'});

#if $settings.LINO.use_tinymce

Lino.edit_tinymce_text = function(panel,options) {
  // `panel` is the RichTextPanel
  //~ console.log(20111220,panel);
  //~ var rec = panel.get_current_record();
  var rec = panel.containing_panel.get_current_record();
  var value = rec ? rec.data[panel.editor.name] : '';
  var saving = false;
  var todo_after_save = false;
  var discard_changes = false;
  
  
  function save() {
    //~ if (todo_after_save) {alert('tried to save again'); return; }
    if (saving) {alert('tried to save again'); return; }
    //~ var url = panel.containing_window.main_item.get_record_url(rec.id);
    var url = panel.containing_panel.get_record_url(rec.id);
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
        //~ panel.containing_window.set_current_record(rec);
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
    //~ closeAction: "close"
    closeAction: "hide"
    //~ hideMode: "offsets",
    //~ constrainHeader: true,
    //~ bodyStyle: 'padding: 10px'
  });

  //~ win.on('beforeclose',function() {
  win.on('beforehide',function() {
    if (todo_after_save) return false;
    if (discard_changes) return true;
    if (editor.isDirty()) {
        //~ var ok = false;
        //~ var allowClose = true;
        var config = {title:"$_('Confirmation')"};
        config.buttons = Ext.MessageBox.YESNOCANCEL;
        config.msg = "$_('Save changes to text ?')";
        config.modal = true;
        config.fn = function(buttonId,text,opt) {
          //~ console.log('do_when_clean',buttonId)
          if (buttonId == "yes") {
              /* we cancel this close, but save()'s onSuccess will call again.*/
              //~ allowClose = false;
              todo_after_save = function(){win.hide();}
              editor.ed.execCommand('mceSave');
              //~ editor.ed.save(function(){win.close();});
          } else if (buttonId == "no") { 
              discard_changes = true;
              win.hide()
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

#end if

#if $settings.LINO.use_vinylfox
Lino.VinylFoxPlugins = function(){
    return [
        new Ext.ux.form.HtmlEditor.Link(),
        new Ext.ux.form.HtmlEditor.Divider(),
        new Ext.ux.form.HtmlEditor.Word(),
        //~ new Ext.ux.form.HtmlEditor.FindAndReplace(),
        //~ new Ext.ux.form.HtmlEditor.UndoRedo(),
        new Ext.ux.form.HtmlEditor.Divider(),
        //~ new Ext.ux.form.HtmlEditor.Image(),
        //~ new Ext.ux.form.HtmlEditor.Table(),
        new Ext.ux.form.HtmlEditor.HR(),
        new Ext.ux.form.HtmlEditor.SpecialCharacters(),
        new Ext.ux.form.HtmlEditor.HeadingMenu(),
        new Ext.ux.form.HtmlEditor.IndentOutdent(),
        new Ext.ux.form.HtmlEditor.SubSuperScript(),
        new Ext.ux.form.HtmlEditor.RemoveFormat()
    ];
};
#end if



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
  format: '$settings.LINO.time_format_extjs',
  increment: 15
  });
Lino.DateField = Ext.extend(Ext.form.DateField,{
  format: '$settings.LINO.date_format_extjs',
  altFormats: '$settings.LINO.alt_date_formats_extjs'
  });
Lino.DateTimeField = Ext.extend(Ext.ux.form.DateTime,{
  dateFormat: '$settings.LINO.date_format_extjs',
  timeFormat: '$settings.LINO.time_format_extjs',
  //~ hiddenFormat: '$settings.LINO.date_format_extjs $settings.LINO.time_format_extjs'
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
Lino.IncompleteDateField = Ext.extend(Ext.form.TextField,{
  //~ regex: /^-?\d+-[01]\d-[0123]\d$/,
  //~ regex: /^[0123]\d\.[01]\d\.-?\d+$/,
  regex: $settings.LINO.date_format_regex,
  regexText: '$_("Enter a date in format YYYY-MM-DD (use zeroes for unknown parts).")'
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
            //~ console.log(20110516);
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

Lino.file_field_handler = function(panel,config) {
  //~ if (instanceof Lino.DetailWrapper) {
  if (panel.action_name == 'insert') {
  //~ if (panel.get_current_record().phantom) {
      panel.has_file_upload = true;
#if $settings.LINO.use_awesome_uploader
      return { xtype:'button', text: 'Upload', handler: Lino.show_uploader }
#else      
      var f = new Lino.FileUploadField(config);
      //~ Lino.make_dropzone(f);
      return f;
      //~ return new Ext.ux.form.FileUploadField(config);
      //~ return new Lino.FileField(config);
#end if      
  } else {
      //~ return new Lino.URLField(config);
      return new Lino.FileField(config);
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
      if (this.isVisible()) { // to avoid "Uncaught TypeError: Cannot call method 'getHeight' of undefined."
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


//~ Lino.show_about = function() {
  //~ new Ext.Window({
    //~ width: 400, height: 400,
    //~ title: "About",
    //~ html: '<a href="http://www.extjs.com" target="_blank">ExtJS</a> version ' + Ext.version
  //~ }).show();
//~ };

Lino.on_store_exception = function (store,type,action,options,reponse,arg) {
  console.log("on_store_exception: store=",store,
    "type=",type,
    "action=",action,
    "options=",options,
    "reponse=",reponse,
    "arg=",arg);
  if (arg) { console.log(arg.stack)};
};

//~ Lino.on_submit_success = function(form, action) {
   //~ Lino.notify(action.result.message);
   //~ this.close();
//~ };

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

Lino.show_in_own_window_button = function(handler) {
  return {
    qtip: "$_("Show this panel in own window")", 
    id: "up",
    handler: function(event,toolEl,panel, tc) {
      //~ console.log('20111206 report_window_button',panel,handler);
      //~ var bp = ww.get_master_params();
      //~ panel.containing_window = ww; // for HtmlBox. see blog/2010/1022
      //~ handler(panel,{base_params:bp});
      //~ handler(panel,{base_params:panel.get_master_params()});
      handler({},{base_params:panel.containing_panel.get_master_params()});
      //~ handler(panel,{master_panel:panel.containing_window.main_item});
    }
  }
}




Lino.delete_selected = function(panel) {
  //~ console.log("Lino.delete_selected",panel);
  var recs1 = panel.get_selected();
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
          Lino.do_action(panel,{
              method:'DELETE',
              url: ROOT_URL + '/api' + panel.ls_url + '/' + recs[i].id,
              after_success: panel.after_delete.createDelegate(panel)
          })
        }
        //~ caller.after_delete();
      }
      else Lino.notify("Dann eben nicht.");
    }
  });
};

Lino.action_handler = function (panel,on_success,gridmode,on_confirm) {
  return function (response) {
    panel.loadMask.hide(); // 20120211
    if (response.responseText) {
      var result = Ext.decode(response.responseText);
      //~ console.log('Lino.action_handler()','result is',result,'on_confirm is',on_confirm);
      if (on_success && result.success) on_success(result);
      if (on_confirm && result.confirm_message) {
          var config = {title:"$_('Confirmation')"};
          config.buttons = Ext.MessageBox.YESNOCANCEL;
          config.msg = result.confirm_message;
          config.fn = function(buttonId,text,opt) {
            if (buttonId == "yes") {
                on_confirm(panel,undefined,result.step);
            }
          }
          Ext.MessageBox.show(config);
          return;
      }
      if (result.message) {
          if (result.alert && ! gridmode) {
              //~ Ext.MessageBox.alert('Alert',result.alert_msg);
              if (result.alert === true) result.alert = "$_('Alert')";
              Ext.MessageBox.alert(result.alert,result.message);
          } else {
              Lino.notify(result.message);
          }
      }
      if (result.refresh_all) {
          var cw = panel.get_containing_window();
          //~ console.log("20120123 refresh_all");
          if (cw) {
            cw.main_item.refresh();
          }
          else console.log("20120123 cannot refresh_all",panel);
      } else {
          if (result.refresh) panel.refresh();
      }
      #if $settings.LINO.use_davlink
      if (result.open_davlink_url) {
         Lino.davlink_open(result.open_davlink_url);
      }
      #end if
      if (result.open_url) {
          //~ console.log(20111126,result.open_url);
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
    //~ console.log('Lino.do_action()',action,'action success',response);
    if (action.after_success) {
        //~ console.log('Lino.do_action() calling after_success');
        action.after_success();
    }
    if (response.responseText) {
      var result = Ext.decode(response.responseText);
      //~ console.log('Lino.do_action()',action.name,'result is',result);
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
    failure: Lino.ajax_error_handler(caller)
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

//~ Lino.tools_close_handler = function (ww) {
  //~ return function() { 
      //~ ww.close();
  //~ }
//~ };
Lino.permalink_handler = function (ww) {
  return function() { 
    //~ console.log(20100923,ww.get_permalink());
    //~ document.location = ww.main_item.get_permalink();
    location.replace(ww.main_item.get_permalink());
    //~ document.location = "?permalink=" + ww.get_permalink();
    //~ document.location = "?permalink=" + ww.config.permalink_name +'()';
  }
};
//~ Lino.run_permalink = function() {
  //~ var plink = Lino.gup('permalink');
  //~ if(plink) { eval('Lino.'+plink); }
//~ }

Lino.MainPanel = {
  config_containing_window : function(wincfg) { }
  ,init_containing_window : function(win) { }
  ,do_when_clean : function(todo) { todo() }
  ,get_master_params : function() {
    var p = {}
    p['$URL_PARAM_MASTER_TYPE'] = this.content_type; 
    rec = this.get_current_record()
    if (rec) {
      if (rec.phantom) {
          p['$URL_PARAM_MASTER_PK'] = undefined; 
      }else{
          p['$URL_PARAM_MASTER_PK'] = rec.id; 
      }
    } else {
      p['mk'] = undefined;
    }
    //~ console.log('get_master_params returns',p,'using record',rec);
    return p;
  }
  ,get_permalink : function() {
    //~ var p = this.main_item.get_base_params() || {};
    var p = Ext.apply({},this.get_base_params());
    delete p.fmt;
    //~ if (p.fmt) delete p.fmt;
    Ext.apply(p,this.get_permalink_params());
     //~ p.fmt = 'html';
    //~ console.log('get_permalink',p,this.get_permalink_params());
    var url = this.get_permalink_url();
    if (Ext.urlEncode(p)) url = url + "?" + Ext.urlEncode(p);
    return url;
  }
  ,get_record_url : function(record_id) {
      var url = ROOT_URL + '/api' + this.ls_url
      //~ var url = this.containing_window.config.url_data; // ls_url;
      url += '/' + (record_id === undefined ? '-99999' : String(record_id));
      //~ if (record_id !== undefined) url += '/' + String(record_id);
      //~ url += '/' + String(record_id);
      return url;
  }
  ,get_permalink_url : function() {
      return ROOT_URL+'/api' + this.ls_url;
  }
  ,get_permalink_params : function() {
      //~ return {an:'grid'};
      var p = {};
      if (this.action_name)
          p['$ext_requests.URL_PARAM_ACTION_NAME'] = this.action_name;
      this.add_param_values(p)
      return p;
  }
  ,set_status : function(status) {}
  ,get_status : function() { return {}}
  ,refresh : function() {}
  ,get_base_params : function() { return {}}
  ,add_params_panel : function (tbar) {
      if (this.params_panel) {
        tbar = tbar.concat([{ scope:this, 
          text: "$_("[parameters]")", // gear
          enableToggle: true,
          pressed: ! this.params_panel_hidden,
          toggleHandler: function(btn,state) { 
            //~ if (this.params_panel.isVisible()) 
                //~ this.params_panel.hide();
            //~ else
                //~ this.params_panel.show();
            //~ console.log("20120210 add_params_panel",state,this.params_panel);
            if (state) this.params_panel.show();
            else this.params_panel.hide();
            this.get_containing_window().doLayout();
          }
        }]);
        var t = this;
        Ext.each(this.params_panel.fields,function(f) {
          //~ f.on('valid',function() {t.refresh()});
          if (f instanceof Ext.form.Checkbox)
              f.on('check',function() {t.refresh()});
          else if (f instanceof Ext.form.TriggerField)
              f.on('select',function() {t.refresh()});
          else
              f.on('change',function() {t.refresh()});
          });
      }
      return tbar;
  }
  ,add_param_values : function (p) {
    if (this.params_panel) {
      //~ var formdata = Lino.form2dict(this.params_panel);
      //~ console.log('20120203 add_param_values formdata', formdata);
      //~ p.$ext_requests.URL_PARAM_PARAM_VALUES = formdata;
      //~ return;
      //~ var formdata = Ext.lib.Ajax.serializeForm(frm);
      var fields = this.params_panel.fields;
      //~ console.log('20120116 gonna loop on', fields);
      var pv = Array(fields.length);
      for(var i=0; i < fields.length;i++) {
          var f = fields[i]
          if (f.formatDate) {
              pv[i] = f.formatDate(f.getValue()); 
          } else {
              pv[i] = f.getValue(); 
          }
      }
      p.$ext_requests.URL_PARAM_PARAM_VALUES = pv;
      //~ console.log("20120203 add_param_values added pv",pv,"to",p);
    }
    
  },
  set_param_values : function(pv) {
    //~ console.log('20120203 set_param_values', pv);
    if (this.params_panel) {
      if (pv) this.params_panel.form.my_loadRecord(pv);
      else this.params_panel.form.reset(); 
      
      //~ var fields = this.params_panel.fields;
      //~ console.log('20120116 gonna loop on', fields);
      //~ for(var i=0; i < fields.length;i++) {
          //~ var f = fields[i]
          //~ f.setValue(pv[i]); 
      //~ }
      //~ this.refresh();
      //~ console.log(20120113,options);
    }
    //~ var test = {test:"foo"};
    //~ this.add_param_values(test);
    //~ console.log('20120203 set_param_values test is ', test);
  }
};


Lino.ajax_error_handler = function(panel) {
  return function(response,options) {
    console.log('Ajax failure:',response,options);
    if (panel.loadMask) panel.loadMask.hide();
    if (response.responseText) {
      var lines = response.responseText.split('\n');
      if (lines.length > 10) {
          line = lines.splice(5,lines.length-10,"(...)");
      }
      Ext.MessageBox.alert(
        response.statusText,
        lines.join('<br/>')
        //~ response.responseText.replace(/\n/g,'<br/>'))
      )
    } else {
      Ext.MessageBox.alert('Action failed',
        'Lino server did not respond to Ajax request');
    }
  }
}
// Ext.Ajax.on('requestexception',Lino.ajax_error_handler)

//~ Lino.main_menu = new Ext.Toolbar({});
  
#if $settings.LINO.use_quicktips

Ext.QuickTips.init();
  
Lino.quicktip_renderer = function(title,body) {
  return function(c) {
    Ext.QuickTips.register({
      target: c.getEl(),
      title: title,
      text: body
    });
  }
};

#end if
  
Lino.help_text_editor = function() {
  //~ var bp = {
      //~ mk:this.content_type,
      //~ mt:1
    //~ };
    //~ console.log(20120202,bp);
  //~ Lino.lino.ContentTypes.detail({},{base_params:bp});
  Lino.lino.ContentTypes.detail({},{record_id:this.content_type});
}

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
    //~ if (record.phantom) return '';
    if (value) {
        var s = '<a href="javascript:' ;
        s += handlername + '({},{record_id:\'' + String(record.data[fkname]) + '\'})">';
        s += value + '</a>';
        //~ console.log('Lino.fk_renderer',value,'-->',s);
        return s
    }
    return '';
  }
};

Lino.lfk_renderer = function(panel,fkname) {
  //~ console.log('Lino.fk_renderer handler=',handler);
  var handlername = 'console.log';
  return function(value, metaData, record, rowIndex, colIndex, store) {
    //~ console.log('Lino.fk_renderer',fkname,rowIndex,colIndex,record,metaData,store);
    if (record.phantom) return '';
    if (value) {
        var s = '<a href="javascript:' ;
        s += handlername + '({},{record_id:\'' + String(record.data[fkname]) + '\'})">';
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
  //~ } else {
      //~ cmp.on('resize',todo,cmp,{single:true});
  //~ }
  //~ if (false) { // 20120213
  } else { 
    //~ console.log('Lino.do_when_visible() must defer because not isVisible()',todo,cmp);
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
      Lino.notify("$_('Action not available on phantom record.')");
    }
    return;
  }
  return fn(rec);
};

Lino.row_action_handler = function(actionName,gridmode) {
  var fn = function(panel,btn,step) {
    Lino.do_on_current_record(panel,function(rec) {
      //~ console.log(panel);
      var url = panel.get_record_url(rec.id);
      var p = Ext.apply({},panel.get_base_params());
      //~ var p = Ext.apply({},panel.get_master_params());
      p['$ext_requests.URL_PARAM_ACTION_NAME'] = actionName;
      if (step) p['$ext_requests.URL_PARAM_ACTION_STEP'] = step;
      //~ p.an = action_name;
      //~ url += "?" + Ext.urlEncode(p);
      //~ window.open(url);
      panel.loadMask.show(); // 20120211
      Ext.Ajax.request({
        method: 'GET',
        url: url,
        params: p,
        success: Lino.action_handler(panel,function(result){},gridmode,fn)
      });
    });
  };
  return fn;
};

Lino.list_action_handler = function(actionName,gridmode) {
  var fn = function(panel,btn,step) {
    //~ console.log(panel);
    var url = ROOT_URL + '/api' + panel.ls_url ;
    var p = Ext.apply({},panel.get_base_params());
    p['$ext_requests.URL_PARAM_ACTION_NAME'] = actionName;
    if (step) p['$ext_requests.URL_PARAM_ACTION_STEP'] = step;
    panel.loadMask.show(); // 20120211
    Ext.Ajax.request({
      method: 'GET',
      url: url,
      params: p,
      success: Lino.action_handler(panel,function(result){},gridmode,fn)
    });
  };
  return fn;
};

Lino.show_detail = function(panel,btn) {
  Lino.do_on_current_record(panel, function(rec) {
      //~ panel.loadMask.show();
      panel.ls_detail_handler({
        //~ listeners: {show: function() {panel.loadMask.hide();}}
        },{
        record_id:rec.id,
        base_params:panel.get_base_params()
      });
      //~ panel.loadMask.hide();
      //~ panel.containing_window.window.hideMask();
      //~ panel.el.unmask();
    },
    Lino.show_insert
  );
};

Lino.show_fk_detail = function(combo,handler) {
    //~ console.log("Lino.show_fk_detail",combo,e,handler);
    pk = combo.getValue();
    if (pk) {
        handler({},{record_id: pk})
      } else {
        Lino.notify("$_('Cannot show detail for empty foreign key.')");
      }
};

Lino.show_insert = function(panel,btn) {
  var bp = panel.get_base_params();
  //~ console.log('20120125 Lino.show_insert',bp)
  panel.ls_insert_handler({},{record_id:-99999,base_params:bp});
};

Lino.show_insert_duplicate = function(panel,btn) {
  Lino.do_on_current_record(panel,
    function(rec) {
      var newRec = {};
      Ext.apply(newRec,rec);
      newRec.id = -99999;
      panel.ls_insert_handler({data_record:rec});
    });
};

//~ Lino.update_row_handler = function(action_name) {
  //~ return function(panel,btn) {
    //~ Lino.notify("Sorry, " + action_name + " is not implemented.");
  //~ }
//~ };


#if $settings.LINO.use_gridfilters

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

#end if

//~ Lino.ButtonField = Ext.extend(Ext.form.TextField,{
//~ Lino.ButtonField = Ext.extend(Ext.form.Field,{
    //~ editable : false,
    //~ constructor : function(ww,config,params){
      //~ this.containing_window = ww;
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
  before_init : function(config,params) {
    if (params) Ext.apply(config,params);
    var actions = Lino.build_buttons(this,config.ls_bbar_actions);
    if (actions) config.bbar = actions.bbar;
  },
  //~ constructor : function(ww,config,params){
    //~ this.containing_window = ww;
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
    this.base_params = Ext.apply({},p);
    //~ if (p.param_values) this.set_param_values(p.param_values);  
  },
  clear_base_params : function() {
      this.base_params = {};
  },
  set_base_param : function(k,v) {
    this.base_params[k] = v;
  }
};



Lino.HtmlBoxPanel = Ext.extend(Ext.Panel,Lino.PanelMixin);
Lino.HtmlBoxPanel = Ext.extend(Lino.HtmlBoxPanel,Lino.FieldBoxMixin);
Lino.HtmlBoxPanel = Ext.extend(Lino.HtmlBoxPanel,{
  disabled_in_insert_window : true,
  constructor : function(config,params) {
    this.before_init(config,params);
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
    //~ console.log(20111125,this.containing_window);
    if (this.containing_panel) {
      this.containing_panel.on('enable',this.enable,this);
      this.containing_panel.on('disable',this.disable,this);
    }
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
  refresh : function(unused) { 
      this.refresh_with_after();
  },
  refresh_with_after : function(after) {
    //~ if (this.master_panel) {
      var record = this.containing_panel.get_current_record();
      //~ console.log('HtmlBox.refresh()',this.title,record,record.title);
      var box = this.items.get(0);
      var todo = function() {
        if (this.disabled) return;
        //~ this.set_base_params(this.containing_window.get_base_params());
        this.set_base_params(this.containing_panel.get_master_params());
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
    //~ }
  }
});
//~ Ext.override(Lino.HtmlBoxPanel,Lino.FieldBoxMixin);

#if $settings.LINO.use_tinymce

Lino.RichTextPanel = Ext.extend(Ext.Panel,Lino.PanelMixin);
Lino.RichTextPanel = Ext.extend(Lino.RichTextPanel,Lino.FieldBoxMixin);
Lino.RichTextPanel = Ext.extend(Lino.RichTextPanel,{
    
  //~ initComponent : function(){
    //~ Lino.RichTextPanel.superclass.initComponent.call(this);
  //~ },
  constructor : function(config,params) {
    //~ console.log('Lino.RichTextPanel.initComponent',this);
    //~ var url = TEMPLATES_URL + config.ls_url + "/" + String(rec.id) + "/" + config.name;
    //~ var url = TEMPLATES_URL + config.ls_url + "/" + config.name;
    var t = this;
    var tinymce_options = {
        theme : "advanced",
        content_css: ROOT_URL + '/media/lino/extjs/lino.css',
        language: '$settings.LANGUAGE_CODE',
        //~ template_external_list_url : url,
        theme_advanced_toolbar_location : "top",
        theme_advanced_toolbar_align : "left",
        theme_advanced_statusbar_location : "bottom",
        template_popup_width : 700,
        template_popup_height : 500,
        template_replace_values : { 
            data_field : function(element){ 
                //~ console.log(20110722,fieldName,t.containing_window.get_current_record()); 
                var fieldName = element.innerHTML;
                element.innerHTML = t.containing_panel.get_current_record().data[fieldName];
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
    this.before_init(config,params);
    
    this.editor = new Ext.ux.TinyMCE(editorConfig);
    var t = this;
    config.tools = [{
                      qtip: "$_('Edit text in own window')", 
                      id: "up",
                      handler: function(){
                        if(t.editor.isDirty()) {
                            var record = t.containing_panel.get_current_record();
                            record.data[t.editor.name] = t.editor.getValue();
                        }
                        Lino.edit_tinymce_text(t,tinymce_options)
                      }
                    }];
    
    config.items = this.editor;
    config.layout = "fit";
    Lino.RichTextPanel.superclass.constructor.call(this, config);
  },
  refresh : function(unused) { 
      this.refresh_with_after();
  },
  refresh_with_after : function(after) {
    var record = this.containing_panel.get_current_record();
    //~ console.log('RichTextPanel.refresh()',this.title,record.title,record);
    var todo = function() {
      //~ this.set_base_params(this.containing_window.get_base_params());
      if (record) {
        var url = ROOT_URL + '/templates' + this.containing_panel.ls_url + "/" 
            + String(record.id) + "/" + this.editor.name;
        //~ console.log('RichTextPanel.refresh()',url);
        if (this.editor.ed) this.editor.ed.settings.template_external_list_url = url;
        this.set_base_params(this.containing_panel.get_master_params());
        //~ var v = record ? this.format_data(record.data[this.editor.name]) : ''
        var v = this.format_data(record.data[this.editor.name])
        this.editor.setValue(v);
      } else {
        this.editor.setValue('(no data)');
      }
    };
    Lino.do_when_visible(this,todo.createDelegate(this));
  }
});
//~ Ext.override(Lino.RichTextPanel,Lino.FieldBoxMixin);

#end if

Lino.FormPanel = Ext.extend(Ext.form.FormPanel,Lino.MainPanel);
Lino.FormPanel = Ext.extend(Lino.FormPanel,Lino.PanelMixin);
Lino.FormPanel = Ext.extend(Lino.FormPanel,{
  params_panel_hidden : false,
  base_params : {},
  //~ trackResetOnLoad : true,
  //~ query_params : {},
  //~ 20110119b quick_search_text : '',
  constructor : function(config,params){
    if (params) Ext.apply(config,params);
    //~ ww.config.base_params.query = ''; // 20111018
    //~ console.log(config);
    //~ console.log('FormPanel.constructor() 1',config)
    //~ Ext.applyIf(config,{base_params:{}});
    //~ console.log('FormPanel.constructor() 2',config)
      
    config.trackResetOnLoad = true;
    
    Lino.FormPanel.superclass.constructor.call(this, config);
      
    this.set_base_param('$URL_PARAM_FILTER',''); // 20111018
      
  },
  initComponent : function(){
    
    //~ console.log("20111201 containing_window",this.containing_window,this);
    
    var actions = Lino.build_buttons(this,this.ls_bbar_actions);
    this.bbar = actions.bbar;
    //~ Ext.apply(config,Lino.build_buttons(this,config.ls_bbar_actions));
    //~ config.bbar = Lino.build_buttons(this,config.ls_bbar_actions);
    var config = this;
    
    //~ if (this.containing_window instanceof Lino.DetailWrapper) {
    
    //~ console.log('20120121 initComponent', this.action_name);
    //~ if (this.action_name == 'detail' | this.action_name == 'show') {
    //~ if (this.action_name != 'insert') {
    if (! this.hide_top_toolbar) {
      this.tbar = [];
      // 20111015    
      if (! this.hide_navigator) {
        this.record_selector = new Lino.RemoteComboFieldElement({
          store: new Lino.ComplexRemoteComboStore({
            //~ baseParams: config.containing_window.config.base_params,
            baseParams: this.get_base_params(),
            //~ value: this.containing_window.config.base_params.query,
            proxy: new Ext.data.HttpProxy({
              url: ROOT_URL + '/choices' + config.ls_url,
              method:'GET'
            })
          }),
          pageSize:25,
          listeners: { 
            scope:this, 
            select:function(combo,record,index) {
              //~ console.log('jumpto_select',arguments);
              this.goto_record_id(record.id);
            }
          },
          emptyText: "$_('Go to record')"
        })
        config.tbar = config.tbar.concat([this.record_selector]);
        
        config.tbar = config.tbar.concat([
          this.first = new Ext.Toolbar.Button({
            tooltip:"$_('First')",disabled:true,handler:this.moveFirst,scope:this,iconCls:'x-tbar-page-first'}),
          this.prev = new Ext.Toolbar.Button({
            tooltip:"$_('Previous')",disabled:true,handler:this.movePrev,scope:this,iconCls:'x-tbar-page-prev'}),
          this.next = new Ext.Toolbar.Button({
            tooltip:"$_('Next')",disabled:true,handler:this.moveNext,scope:this,iconCls:'x-tbar-page-next'}),
          this.last = new Ext.Toolbar.Button({
            tooltip:"$_('Last')",disabled:true,handler:this.moveLast,scope:this,iconCls:'x-tbar-page-last'})
        ]);
      }
      config.tbar = this.add_params_panel(config.tbar);
      
      //~ console.log(20101117,this.containing_window.refresh);
      config.tbar = config.tbar.concat([
        {
          //~ text:'Refresh',
          handler:function(){ this.do_when_clean(this.refresh.createDelegate(this)) },
          iconCls: 'x-tbar-loading',
          tooltip:"$_('Reload current record')",
          scope:this}
      ]);
          
      config.tbar = config.tbar.concat([
          '->',
          this.displayItem = new Ext.Toolbar.TextItem({})
      ]);
          
    }
    if (config.content_type) {
      config.bbar = config.bbar.concat([
        '->',
        { text: '[$_("Help Text Editor")]',
          handler: Lino.help_text_editor,
          qtip: "$_('Edit help texts for fields on this model.')",
          scope: this}
        //~ ,{ text: '[$_("Layout Editor")]',
          //~ handler: this.edit_detail_config,
          //~ qtip: "$_("Edit Detail layout")",
          //~ scope: this}
      ])
    }
    //~ this.before_row_edit = config.before_row_edit.createDelegate(this);
      
    //~ if (this.master_panel) {
        //~ this.set_base_params(this.master_panel.get_master_params());
    //~ }
      
    Lino.FormPanel.superclass.initComponent.call(this);
    
    this.on('render',function(){
      this.loadMask = new Ext.LoadMask(this.bwrap,{msg:"$_('Please wait...')"});
    },this);
    
    
    //~ var this_ = this;
    //~ this.cascade(function(cmp){
      //~ // var active_field = false;
      //~ for (i = 0; i < this_.active_fields.length; i++) {
        //~ if (cmp.name == this_.active_fields[i]) {
            //~ // active_field = true; break;
            //~ cmp.on("change",function() {this_.save()});
        //~ }
      //~ };
      //~ if (active_field) {
      // if (cmp instanceof Lino.GridPanel) {
          //~ cmp.on("change",function() {this_.save()});
      //~ }
    //~ });
    
    if (this.action_name == 'insert') {
      this.cascade(function(cmp){
        //~ console.log('20110613 cascade',cmp);
        if (cmp.disabled_in_insert_window) {
        //~ if (cmp instanceof Lino.GridPanel) {
            cmp.disable();
        }
      });
      
    }
    
  },
  
  get_status : function(){
      var st = {
        base_params: this.get_base_params(),
        data_record : this.get_current_record()
        }
      var tp = this.items.get(0);
      if (tp instanceof Ext.TabPanel) {
        st.active_tab = tp.getActiveTab();
      }
      return st;
  },
  set_status : function(status){
    //~ console.log('20120208 FormPanel.set_status()',this,status);
    this.clear_base_params();
    if (status == undefined) status = {};
    if (status.param_values) this.set_param_values(status.param_values);
    if (status.base_params) this.set_base_params(status.base_params);
    var tp = this.items.get(0);
    if (tp instanceof Ext.TabPanel) {
      if (status.active_tab) {
        //~ console.log('20111201 active_tab',this.active_tab,this.items.get(0));
        //~ tp.activeTab = status.active_tab;
        tp.setActiveTab(status.active_tab);
        //~ this.main_item.items.get(0).activate(status.active_tab);
      } else {
        tp.setActiveTab(0);
      }
      }
    
    if (status.data_record) {
      //~ console.log('20111201 Lino.FormPanel with data_record',this.data_record.title,this.containing_window);
      //~ this.main_item.on_master_changed.defer(2000,this.main_item,[status.data_record]);
      //~ Lino.do_when_visible(this.main_item,function(){this.on_master_changed(status.data_record)});
      //~ this.main_item.on('afterrender',function(){
      //~   this.main_item.on_master_changed(status.data_record)},this,{single:true});
      /* must defer because because set_window_title() didn't work otherwise */
      this.set_current_record.createDelegate(this,[status.data_record]).defer(100);
      //~ this.set_current_record(this.data_record);
      //~ return;
    } else if (status.record_id != undefined) { 
      /* possible values include 0 and null, 0 being a valid record id, 
      null the equivalent of undefined
      */
      //~ this.main_item.goto_record_id(this.status.record_id);
      this.load_record_id(status.record_id);
    } else {
      this.set_current_record(undefined);
    }
  },
    
  get_base_params : function() {
    // needed for insert action
    return this.base_params;
  },
  set_base_params : function(p) {
    //~ this.base_params = Ext.apply({},p);
    Ext.apply(this.base_params,p);
    //~ if (p.param_values) this.set_param_values(p.param_values);  
  },
  clear_base_params : function() {
      this.base_params = {};
  },
  set_base_param : function(k,v) {
    this.base_params[k] = v;
  },
  
  after_delete : function() {
    if (this.current_record.navinfo.next)
      this.moveNext();
    else if (this.current_record.navinfo.prev)
      this.movePrev();
    else 
      this.abandon();
  },
  moveFirst : function() {this.goto_record_id(this.current_record.navinfo.first)},
  movePrev : function() {this.goto_record_id(this.current_record.navinfo.prev)},
  moveNext : function() {this.goto_record_id(this.current_record.navinfo.next)},
  moveLast : function() {this.goto_record_id(this.current_record.navinfo.last)},
  
  
  refresh : function(unused) { 
      this.refresh_with_after();
  },
  refresh_with_after : function(after) { 
    //~ console.log('20120121 Lino.FormPanel.refresh()',this);
    if (this.current_record) {
        this.load_record_id(this.current_record.id,after);
    } else {
        this.set_current_record(undefined,after);
    }
  },
  
  do_when_clean : function(todo) {
    var this_ = this;
    if (this.form.isDirty()) {
        //~ console.log('20111217 do_when_clean() form is dirty',this.form);
        var config = {title:"$_('Confirmation')"};
        config.buttons = Ext.MessageBox.YESNOCANCEL;
        config.msg = "$_('Save changes to current record ?')";
        config.fn = function(buttonId,text,opt) {
          //~ console.log('do_when_clean',buttonId)
          if (buttonId == "yes") {
              //~ Lino.submit_detail(this_,undefined,todo);
              //~ this_.containing_window.save(todo);
              this_.save(todo);
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
    //~ var p = { fmt: this.containing_window.config.action_name};
    //~ var p = Ext.apply({},this.containing_window.config.base_params);
    var p = Ext.apply({},this.get_base_params());
    //~ console.log('20110713 load_record_id',record_id,p);
    //~ console.log('20110713 action_name=',this.containing_window.config.action_name,
      //~ 'base_params=',this.containing_window.config.base_params);
    if (this.action_name)
        p.$ext_requests.URL_PARAM_ACTION_NAME = this.action_name;
    //~ p.an = this.action_name;
    //~ p.an = this.containing_window.config.action_name;
    //~ p.fmt = 'json';
    //~ p.fmt = '$ext_requests.URL_FORMAT_JSON';
    p.$ext_requests.URL_PARAM_FORMAT = '$ext_requests.URL_FORMAT_JSON';
    //~ 20110119b p['$URL_PARAM_FILTER'] = this.quick_search_text;
    //~ Ext.apply(p,this.query_params);
    this.add_param_values(p);
    if (this.loadMask) this.loadMask.show();
    Ext.Ajax.request({ 
      waitMsg: 'Loading record...',
      method: 'GET',
      params: p,
      scope: this,
      url: this.get_record_url(record_id),
      success: function(response) {   
        // todo: convert to Lino.action_handler.... but result 
        if (this.loadMask) this.loadMask.hide();
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
                  this.load_record_id(rec.navinfo.first);
              } else this.abandon();
                  
          } else {
              this.set_current_record(rec,after);
          }
        }
      },
      failure: Lino.ajax_error_handler(this)
    });
  },

  abandon : function () {
    Ext.MessageBox.alert('Note',
      "$_('No more records to display. Detail window has been closed.')");
    Lino.close_window();
    //~ if (this.containing_window) {
        //~ this.containing_window.hide();
    //~ }
  },
  
  set_current_record : function(record,after) {
    //~ console.log('20111201 Lino.FormPanel.set_current_record',record.title,record);
    if (this.record_selector) {
        this.record_selector.clearValue();
        // e.g. InsertWrapper FormPanel doesn't have a record_selector
    }
    this.current_record = record;
    //~ if (record) 
        //~ console.log('Lino.FormPanel.set_current_record',record.title,record);
    //~ else
        //~ console.log('Lino.FormPanel.set_current_record',record);
    //~ this.config.main_panel.form.load(record);    
    if (record) {
      this.enable();
      this.form.my_loadRecord(record.data);
      this.set_window_title(record.title);
      this.getBottomToolbar().enable();
      if (record.disabled_actions) {
          //~ console.log('disabled_actions =',record.disabled_actions,this.getBottomToolbar());
          this.getBottomToolbar().items.each(function(item,index,length){
              if (record.disabled_actions[item.name]) 
                item.disable();
              else item.enable();
          });
      };
      if (record.data.disable_editing) {
          //~ console.log("20120202 disable_editing",record.title);
          this.form.items.each(function(cmp){
            cmp.disable();
          },this);
      } else {
          this.form.items.each(function(cmp){
            //~ console.log("20120202",cmp);
            if (record.data.disabled_fields[cmp.name]) cmp.disable();
            else cmp.enable();
          },this);
        
          //~ if (record.data.disabled_fields) {
              //~ for (i = 0; i < record.data.disabled_fields.length; i++) {
                  //~ var flds = this.find('name',record.data.disabled_fields[i]);
                  //~ if (flds.length == 1) { 
                    //~ flds[0].disable(); 
                  //~ }
              //~ }
          //~ }
      };
      if (! this.hide_navigator && record.navinfo) {
        this.first.setDisabled(!record.navinfo.first);
        this.prev.setDisabled(!record.navinfo.prev);
        this.next.setDisabled(!record.navinfo.next);
        this.last.setDisabled(!record.navinfo.last);
        this.displayItem.setText(record.navinfo.message);
      }
    } else {
      if (this.form.rendered) 
        this.form.reset(); /* FileUploadField would fail when resetting a non-rendered form */
      //~ this.disable();
      this.getBottomToolbar().disable();
      this.form.items.each(function(cmp){
        cmp.disable();
      },this);
      this.set_window_title(this.empty_title);
      //~ this.containing_window.window.setTitle(this.empty_title);
      if (!this.hide_navigator) {
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
  
  before_row_edit : function(record) {},
  search_change : function(field,oldValue,newValue) {
    //~ console.log('search_change',field.getValue(),oldValue,newValue)
    this.set_base_param('$URL_PARAM_FILTER',field.getValue()); 
    this.refresh();
  },
  
  get_selected : function() { return [ this.current_record ] },
  get_current_record : function() {  
    //~ console.log(20100714,this.current_record);
    return this.current_record 
  },
  
  get_permalink_url : function() {
      var rec = this.get_current_record();
      if (rec && ! rec.phantom && rec.id != -99998)
          return ROOT_URL + '/api' + this.ls_url + '/' + rec.id;
      return ROOT_URL + '/api' + this.ls_url;
    
  },
  get_permalink_params : function() {
    var p = {};
    //~ var p = {an:'detail'};
    if (this.action_name)
        p.$ext_requests.URL_PARAM_ACTION_NAME = this.action_name;
    //~ var p = {an:this.action_name};
    var main = this.items.get(0);
    if (main.activeTab) {
      var tab = main.items.indexOf(main.activeTab);
      //~ console.log('main.activeTab',tab,main.activeTab);
      if (tab) p.$ext_requests.URL_PARAM_TAB = tab;
    }
    this.add_param_values(p)
    return p;
  },
  
  /* 
  Lino.FormPanel.save() 
  */
  save : function(after) {
    //~ var panel = this;
    this.loadMask.show();
    var rec = this.get_current_record();
    if (this.has_file_upload) this.form.fileUpload = true;
    //~ console.log('FormPanel.save()',rec);
    if (rec) {
      if (rec.phantom) {
        if (this.action_name != 'insert') 
            console.log("Warning: phantom record, but action_name is",this.action_name)
        this.form.submit({
          url: ROOT_URL + '/api' + this.ls_url,
          method: 'POST',
          params: this.get_base_params(), // 20101025
          scope: this,
          success: function(form, action) {
            this.loadMask.hide();
            Lino.notify(action.result.message);
            /***
            Close this window, but update the status of the 
            calling window.
            If the calling window is a detail on the same table,
            then it should skip to the new record. But only then.
            A successful response usually has a data_record,
            except if it is a fileupload form where some mysterious 
            decoding problems (20120209) force us to return a record_id 
            which will lead to an additional GET.
            ***/
            var url = this.ls_url;
            var ww = Lino.calling_window();
            if (ww && ww.window.main_item instanceof Lino.FormPanel 
                   && ww.window.main_item.ls_url == this.ls_url) {
                //~ console.log("20120217 case 1");
                ww.status.record_id = action.result.record_id;
                ww.status.data_record = action.result.data_record;
                Lino.close_window();
            } else if (this.ls_detail_handler) {
                //~ console.log("20120217 case 2");
                Lino.kill_current_window();
                this.ls_detail_handler(null,{
                    record_id:action.result.record_id,
                    data_record: action.result.data_record,
                    base_params:this.get_base_params()
                });
            } else {
                //~ console.log("20120217 case 3");
                Lino.close_window();
            }
            //~ Lino.close_window(function(ww){
                //~ if (ww.window.main_item instanceof Lino.FormPanel 
                    //~ && ww.window.main_item.ls_url == url) {
                  //~ ww.status.record_id = action.result.record_id,
                  //~ ww.status.data_record = action.result.data_record
                //~ }
            //~ });
          },
          failure: function() { 
            this.loadMask.hide();
            Lino.on_submit_failure(arguments)},
          clientValidation: true
        })
      } else {
        if (this.action_name != 'detail') 
            console.log("Warning: non-phantom record, but action_name is",this.action_name)
        this.form.submit({
          url: ROOT_URL + '/api' + this.ls_url + '/' + rec.id,
          method: 'PUT',
          //~ headers: { 'HTTP_X_REQUESTED_WITH' : 'XMLHttpRequest'},
          scope: this,
          params: this.get_base_params(), 
          success: function(form, action) {
            //~ panel.form.setValues(rec.data);
            //~ 20110701 panel.form.my_loadRecord(rec);
            this.loadMask.hide();
            Lino.notify(action.result.message);
            this.set_current_record(action.result.data_record,after);
            //~ this.refresh_with_after(after);
            //~ if (after) after(); else panel.refresh();
          },
          failure: function() { 
            this.loadMask.hide();
            Lino.on_submit_failure(arguments)},
          clientValidation: true
        })
      }
    } else Lino.notify("Sorry, no current record.");
  },
  
  edit_detail_config : function () {
    var active_tab = {};
    var main = this.items.get(0);
    if (main.getActiveTab !== undefined) {
      var tabitem = main.getActiveTab();
      Ext.apply(active_tab,{$ext_requests.URL_PARAM_TAB : main.items.indexOf(tabitem)});
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
        url: ROOT_URL + '/detail_config' + _this.ls_url,
        failure : Lino.ajax_error_handler(this),
        success: Lino.action_handler( _this, function(result) {
          //~ console.log('detail_config/save success',result);
          win.close();
          document.location = _this.get_permalink();
        })
      };
      //~ console.log('detail_config/save sent',a);
      _this.loadMask.show(); // 20120211
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
      url:ROOT_URL+'/detail_config'+_this.ls_url,
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
  }
});



Lino.getRowClass = function(record, rowIndex, rowParams, store) {
  if (record.phantom) {
    //~ console.log(20101009,record);
    //~ rowParams.bodyStyle = "color:red;background-color:blue";
    return 'lino-phantom-row';
    }
  //~ console.log('20101009 not a phantom:',record);
  return '';
}

//~ FOO = 0;

Lino.GridStore = Ext.extend(Ext.data.ArrayStore,{ 
  autoLoad: false,
  load: function(options) {
    //~ foo.bar = baz; // 20120213
    if (!options) options = {};
    if (!options.params) options.params = {};
    options.params.$URL_PARAM_FORMAT = '$ext_requests.URL_FORMAT_JSON';
      
    var ps = this.grid_panel.calculatePageSize();
    
    if (!ps) {
        //~ this.gridpanel.on('render',this.load())
      //~ console.log("20120213 GridStore.load() failed to calculate pagesize");
      return false;
        //~ params.$URL_PARAM_LIMIT = 1;
        //~ this.grid_panel.on('render',this.load.createDelegate(this,options))
        //~ return;
    } 
    
    options.params.$URL_PARAM_LIMIT = ps;
      
    if (this.grid_panel.hide_top_toolbar) {
        //~ console.log("20120206 GridStore.load() toolbar is hidden");
        options.params.$URL_PARAM_START = 0;
    } else {
        //~ options.params.$URL_PARAM_START = this.grid_panel.getTopToolbar().cursor;
        //~ if (this.grid_panel.getTopToolbar().pageSize !=  ps) {
          //~ console.log("20120206 abort load because toolbar says pagesize",
            //~ this.grid_panel.getTopToolbar().pageSize,
            //~ "while actual pagesize is",ps);
            //~ return;
        //~ }
        
        this.grid_panel.getTopToolbar().pageSize =  ps;
        if (options.params.$URL_PARAM_START == undefined)
            options.params.$URL_PARAM_START = this.grid_panel.getTopToolbar().cursor;
      
    }
      
    this.grid_panel.add_param_values(options.params);
    //~ console.log("20120213 GridStore.load()",options.params);
    //~ if (FOO > 0) {
        //~ foo.bar = baz;
    //~ } else FOO += 1;
    return Lino.GridStore.superclass.load.call(this,options);
  }
});

    
Lino.GridPanel = Ext.extend(Ext.grid.EditorGridPanel,Lino.MainPanel);
Lino.GridPanel = Ext.extend(Lino.GridPanel,Lino.PanelMixin);
Lino.GridPanel = Ext.extend(Lino.GridPanel,{
  //~ quick_search_text : '',
  disabled_in_insert_window : true,
  clicksToEdit:2,
  enableColLock: false,
  autoHeight: false,
  params_panel_hidden : false,
  //~ loadMask: true,
  //~ viewConfig: {
          //~ getRowClass: Lino.getRowClass,
          //~ emptyText:"$_('No data to display.')"
        //~ },
  loadMask: {msg:"$_('Please wait...')"},
  
  constructor : function(config){
#if $settings.LINO.use_gridfilters
    config.plugins = [new Lino.GridFilters()];
#end if    
#if $settings.LINO.use_filterRow
    config.plugins = [new Ext.ux.grid.FilterRow()];
#end if    
    Lino.GridPanel.superclass.constructor.call(this,config);
    
    //~ if (this.containing_window) {
        //~ console.log("20111206 install refresh");
        //~ this.containing_window.on('show',this.refresh,this);
    //~ }
    
  },
  
  config_containing_window : function(wincfg) { 
      if (wincfg.tools != undefined) 
        wincfg.tools = [
          {handler:this.save_grid_config,
            qtip:"$_("Save Grid Configuration")",
            scope:this, id:"save"}
        ].concat(wincfg.tools);
      //~ wincfg.listeners = { show: ... };
  },
  init_containing_window : function(win) { 
    //~ console.log("20111206 install refresh");
    //~ win.on('show',this.refresh,this);
  },
  
  initComponent : function(){
    
    /* 
    Problem 20111206:
    When a GridPanel is the main item of the window, then it doesn't 
    have it's own header but uses the window's header bar.
    We must do this in initComponent because e.g. in beforerender 
    it's already to late: a header element has been created because 
    there was a title.
    But Lino.Window adds itself as `this.containing_window` 
    only after the GridPanel has been initialized.
    Workaround is to generate a line "params.containing_window = true;" 
    in the handler function.
    */ 
    //~ if (this.containing_window) {
    if (this.is_main_window) {
        //~ console.log(20111206, 'delete title',this.title,'from',this);
        //~ delete this.title;
        this.tools = undefined;  
        this.title = undefined;  /* simply deleting it 
          isn't enough because that would only 
          unhide the title defined in some base class. */
    } 
    //~ else console.log(20111206, 'dont delete title',this.title,'from',this);
    
    /* e.g. when slave gridwindow called from a permalink */
    //~ if (this.base_params) Ext.apply(bp,this.base_params);  
    //~ bp['fmt'] = 'json';
    
    //~ function on_proxy_load( proxy, transactionObject, callbackOptions ) {
      //~ console.log('on_proxy_load',transactionObject)
    //~ }
    var proxy = new Ext.data.HttpProxy({ 
      url: ROOT_URL + '/api' + this.ls_url, 
      method: "GET"
      //~ listeners: {load:on_proxy_load} 
    });
    //~ config.store = new Ext.data.JsonStore({ 
    //~ this.store = new Ext.data.ArrayStore({ 
    this.store = new Lino.GridStore({ 
      listeners: { exception: Lino.on_store_exception }, 
      grid_panel: this,
      proxy: proxy, 
      //~ autoLoad: this.containing_window ? true : false,
      idIndex: this.pk_index,
      remoteSort: true, 
      //~ baseParams: bp, 
      fields: this.ls_store_fields, 
      totalProperty: "count", 
      root: "rows", 
      //~ id: "id" });
      idProperty: this.ls_id_property });
      
    //~ console.log('config.pk_index',config.pk_index,config.store),
    delete this.ls_store_fields;
      
    var this_ = this;
    //~ var grid = this;
    this.store.on('load', function() {
        //~ console.log('GridMasterWrapper setup',this_.store.reader.arrayData.title);
        var da = this_.store.reader.arrayData.disabled_actions
        if (da) {
            this.cmenu.cascade(function(item){ 
              if(da[item.name]) item.disable();
              else item.enable();
            });
        };
        if (this_.containing_window)
            this_.set_window_title(this_.store.reader.arrayData.title);
            //~ this_.containing_window.setTitle(this_.store.reader.arrayData.title);
        if (this_.selModel.getSelectedCell){
            if (this_.getStore().getCount()) // there may be no data
                this_.selModel.select(0,0); 
        } else {
            this_.selModel.selectFirstRow();
            this_.getView().focusEl.focus();
        }
      }, this
    );
    if (!this.hide_top_toolbar) {  
      var tbar = [ 
        this.search_field = new Ext.form.TextField({ 
          fieldLabel: "Search", 
          listeners: { scope:this_, change:this_.search_change }
          //~ value: text
          //~ scope:this, 
          //~ enableKeyEvents: true, 
          //~ listeners: { keypress: this.search_keypress }, 
          //~ id: "seachString" 
      })];
      tbar = this.add_params_panel(tbar);
      tbar = tbar.concat([
        { scope:this, 
          text: "[csv]", 
          handler: function() { 
            var p = Ext.apply({},this.get_base_params());
            p['fmt'] = 'csv';
            //~ url += "?" + Ext.urlEncode(p);
            window.open(ROOT_URL+'/api'+this.ls_url + "?" + Ext.urlEncode(p)) 
          } },
        { scope:this, 
          text: "[html]", 
          handler: function() { 
            var p = this.get_current_grid_config();
            Ext.apply(p,this.get_base_params());
            //~ var p = Ext.apply({},this.get_base_params());
            p.$ext_requests.URL_PARAM_FORMAT = "$ext_requests.URL_FORMAT_PRINTER";
            //~ p['fmt'] = 'printer';
            this.add_param_values(p);
            //~ url += "?" + Ext.urlEncode(p);
            window.open(ROOT_URL+'/api'+this.ls_url + "?" + Ext.urlEncode(p)) 
          } },
        { scope:this, 
          text: "[pdf]", 
          handler: function() { 
            var p = this.get_current_grid_config();
            Ext.apply(p,this.get_base_params());
            //~ var p = Ext.apply({},this.get_base_params());
            //~ p['fmt'] = 'pdf';
            p.$ext_requests.URL_PARAM_FORMAT = "$ext_requests.URL_FORMAT_PDF";
            this.add_param_values(p);
            //~ url += "?" + Ext.urlEncode(p);
            window.open(ROOT_URL+'/api'+this.ls_url + "?" + Ext.urlEncode(p)) 
          } }
      ]);
    
    
      var menu = [];
      var set_gc = function(index) {
        return function() {
          //~ console.log('set_gc() 20100812');
          this.getColumnModel().setConfig(
              this.apply_grid_config(index,this.ls_grid_configs,this.ls_columns));
        }
      }
      for (var i = 0; i < this.ls_grid_configs.length;i++) {
        var gc = this.ls_grid_configs[i];
        menu.push({text:gc.label,handler:set_gc(i),scope:this})
      }
      if(menu.length > 1) {
        tbar = tbar.concat([
          { text:"$_('View')",
            menu: menu,
            tooltip:"$_('Select another view of this report')"
          }
        ]);
      }
      this.tbar = new Ext.PagingToolbar({ 
        store: this.store, 
        prependButtons: true, 
        //~ pageSize: this.page_length, 
        pageSize: 1, 
        displayInfo: true, 
        beforePageText: "$_('Page')",
        afterPageText: "$_('of {0}')",
        displayMsg: "$_('Displaying {0} - {1} of {2}')",
        firstText: "$_('First page')",
        lastText: "$_('Last page')",
        prevText: "$_('Previous page')",
        nextText: "$_('Next page')",
        items: tbar
      });
      //~ this.on('resize', function(cmp,aw,ah,rw,rh) {
          //~ var ps = this.calculatePageSize();
          //~ if (ps && ps != this.getTopToolbar().pageSize) {
              //~ // console.log('20120203 resize : pageSize',this.getTopToolbar().pageSize,'->',ps);
              //~ // this.getTopToolbar().pageSize =  ps;
              //~ cmp.refresh();
              //~ // this.getTopToolbar().doRefresh();
          //~ }
        //~ }, this);
      //~ this.on('resize', function(cmp,aw,ah,rw,rh) {
          //~ cmp.getTopToolbar().pageSize = this.calculatePageSize(aw,ah,rw,rh) || 10;
          //~ cmp.refresh();
        //~ }, this, {delay:500});
    }
    
    delete this.page_length
    
    var actions = Lino.build_buttons(this,this.ls_bbar_actions);
    this.cmenu = actions.cmenu;
    
    //~ Ext.apply(config,Lino.build_buttons(this,config.ls_bbar_actions));
    //~ config.bbar, this.cmenu = Lino.build_buttons(this,config.ls_bbar_actions);
    //~ this.cmenu = new Ext.menu.Menu({items: config.bbar});
    delete this.ls_bbar_actions
    
    
      
    if (this.ls_quick_edit) {
      this.selModel = new Ext.grid.CellSelectionModel()
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
      this.selModel = new Ext.grid.RowSelectionModel() 
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
    delete this.ls_quick_edit;
    
    Lino.GridPanel.superclass.initComponent.call(this);
    
    //~ if (this.containing_window) 
        //~ this.on('afterlayout', this.refresh, this);
        //~ this.on('afterrender', this.refresh,this);
    //~ else
        //~ this.on('show', this.refresh,this);
    //~ this.on('afterlayout', function() {
      //~ if (this.id == "ext-comp-1157") 
        //~ console.log("20120213 afterlayout",this); 
      //~ // this.refresh();
      //~ },this);
    //~ this.on('afterrender', this.refresh);
    //~ this.on('resize', this.refresh,this,{delay:500});
    //~ this.on('resize', function(){console.log("20120213 resize",arguments)},this);
    this.on('resize', function(){
      //~ console.log("20120213 resize",arguments)
      this.refresh();
      },this);
    this.on('viewready', function(){
      //~ console.log("20120213 resize",arguments);
      this.view_is_ready = true;
      this.refresh();
      },this);
    this.on('afteredit', this.on_afteredit);
    this.on('beforeedit', this.on_beforeedit);
    this.on('cellcontextmenu', Lino.cell_context_menu, this);
    //~ this.on('contextmenu', Lino.grid_context_menu, this);
    
    this.on('beforeedit',function(e) { this.before_row_edit(e.record)},this);
    
    //~ if (this.id == "ext-comp-1157") captureEvents(this);    
    
  },
  
  //~ onResize : function(){
      //~ console.log("20120206 GridPanel.onResize",arguments);
      //~ Lino.GridPanel.superclass.onResize.apply(this, arguments);
      //~ this.refresh();
  //~ },
  
  
  get_status : function(){
    var p = { base_params : this.get_base_params()};
    if (!this.hide_top_toolbar) {
        p.current_page = this.getTopToolbar().current;
    }
    //~ console.log("20120213 GridPanel.get_status",p);
    return p;
  },
  set_status : function(status){
    //~ console.log("20120213 GridPanel.set_status",status);
    this.clear_base_params();
    if (status == undefined) status = {};
    if (status.param_values) this.set_param_values(status.param_values);
    if (status.base_params) { 
      this.set_base_params(status.base_params);
    }
    if (!this.hide_top_toolbar) {
      //~ console.log("20120213 GridPanel.getTopToolbar().changePage",
          //~ status.current_page || 1);
      this.getTopToolbar().changePage(status.current_page || 1);
    }
    //~ this.fireEvent('resize');
    //~ this.refresh.defer(100,this); 
    //~ this.onResize.defer(100,this); 
    //~ this.refresh(); 
    //~ this.doLayout(); 
    //~ this.onResize(); 
    //~ this.store.load();
  },
  
  refresh : function(unused) { 
    this.refresh_with_after();
  },
  refresh_with_after : function(after) { 
    //~ Lino.notify('20120204 Lino.GridPanel.refresh');
    //~ Lino.notify('Lino.GridPanel.refresh '+this.store.proxy.url);
    //~ var bp = { fmt:'json' }
    if (this.containing_panel) {
        //~ Ext.apply(p,this.master_panel.get_master_params());
        //~ Ext.apply(options.params,this.containing_panel.get_master_params());
        this.set_base_params(this.containing_panel.get_master_params());
    }
    
    if (! this.view_is_ready) return;
    
    var options = {};
    if (after) {
        options.callback = function(r,options,success) {if(success) after()}
    }
    
      
    //~ if (!this.rendered) {
        //~ console.log("20120206 GridPanel.refresh() must wait until rendered",options);
        //~ this.grid_panel.on('render',this.load.createDelegate(this,options))
        //~ return;
    //~ }
    
    this.store.load(options);
  },
  
  /* pageSize depends on grid height (Trying to remove scrollbar)
  Thanks to 
  - Christophe Badoit on http://www.sencha.com/forum/showthread.php?82647
  - http://www.sencha.com/forum/archive/index.php/t-37231.html
  */
  calculatePageSize : function(second_attempt) {
    //~ if (!this.rendered) { 
    if (!this.view_is_ready) { 
      //~ console.log('Cannot calculatePageSize() : not rendered');
      return false; }
    //~ if (!this.isVisible()) { 
      //~ console.log('calculatePageSize : not visible');
      //~ return false; }
      
    //~ console.log('getFrameHeight() is',this.getFrameHeight());
    //~ console.log('getView().scroller.getHeight() is',this.getView().scroller.getHeight());
    //~ console.log('mainBody.getHeight() is',this.getView().mainBody.getHeight());
    //~ console.log('getInnerHeight() is',this.getInnerHeight());
    //~ console.log('getHeight() is',this.getHeight());
    //~ console.log('el.getHeight() is',this.getEl().getHeight());
    //~ console.log('getGridEl().getHeight() is',this.getGridEl().getHeight());
    //~ console.log('getOuterSize().height is',this.getOuterSize().height);
    //~ console.log('getBox().height is',this.getBox().height);
    //~ console.log('getResizeEl.getHeight() is',this.getResizeEl().getHeight());
    //~ console.log('getLayoutTarget().getHeight() is',this.getLayoutTarget().getHeight());
      
    var rowHeight = this.getFrameHeight();
    //~ var rowHeight = 52; // experimental value
    var row = this.view.getRow(0);
    if (row) {
      //~ console.log('20120213 yes');
      rowHeight = Ext.get(row).getHeight();
    }
    //~ console.log('rowHeight is ',rowHeight,this,caller);
    //~ this.getView().syncScroll();
    //~ this.getView().initTemplates();
    var height = this.getView().scroller.getHeight();
    //~ console.log('getView().scroller.getHeight() is',this.getView().scroller.getHeight());
    //~ console.log('getInnerHeight() - getFrameHeight() is',
      //~ this.getInnerHeight(), '-',
      //~ this.getFrameHeight(), '=',
      //~ this.getInnerHeight() - this.getFrameHeight());
    //~ var height = this.getView().mainBody.getHeight();
    //~ var height = this.getView().mainWrap.getHeight();
    //~ var height = this.getView().resizeMarker.getHeight();
    //~ this.syncSize();
    //~ var height = this.getInnerHeight() - this.getFrameHeight();
    //~ var height = this.getHeight() - this.getFrameHeight();
    height -= Ext.getScrollBarWidth(); // leave room for a possible horizontal scrollbar... 
    //~ height -= this.getView().scrollOffset;
    var ps = Math.floor(height / rowHeight);
    //~ console.log('20120203 calculatePageSize():',height,'/',rowHeight,'->',ps);
    ps -= 1; // leave room for a possible phantom row
    //~ return (ps > 1 ? ps : false);
    if (ps > 1) return ps;
    //~ console.log('calculatePageSize() found less than 1 row:',height,'/',rowHeight,'->',ps);
    //~ foo.bar = baz; // 20120213
    return 5;
    //~ if (second_attempt) {
        //~ console.log('calculatePageSize() abandons after second attempt:',
          //~ height,'/',rowHeight,'->',ps);
      //~ return 5;
    //~ }
    //~ return this.calculatePageSize.defer(500,this,[true]);
  },
  
  onCellDblClick : function(grid, row, col){
      //~ console.log("onCellDblClick",grid, row, col);
      if (this.ls_detail_handler) {
          //~ Lino.notify('show detail');
          Lino.show_detail(this);
          return false;
      }else{
        //~ console.log('startEditing');
        this.startEditing(row,col);
      }
  },
  
  get_base_params : function() {
    //~ return this.containing_window.config.base_params;
    return this.store.baseParams;
  },
  set_base_params : function(p) {
    //~ console.log('GridPanel.set_base_params',p)
    for (k in p) this.store.setBaseParam(k,p[k]);
    //~ this.store.baseParams = p;
    if (p.query) 
        this.search_field.setValue(p.query);
    //~ if (p.param_values) 
        //~ this.set_param_values(p.param_values);  
  },
  clear_base_params : function() {
      this.store.baseParams = {};
  },
  set_base_param : function(k,v) {
    this.store.setBaseParam(k,v);
  },
  
  //~ get_permalink_params : function() {
    //~ var p = {};
    //~ return p;
  //~ },
  
  before_row_edit : function(record) {},
  search_change : function(field,oldValue,newValue) {
    //~ console.log('search_change',field.getValue(),oldValue,newValue)
    this.set_base_param('$URL_PARAM_FILTER',field.getValue()); 
    this.getTopToolbar().moveFirst();
    //~ this.refresh();
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
        if (col.dataIndex == gc.$(ext_requests.URL_PARAM_COLUMNS)[i]) {
          col.width = gc.$(ext_requests.URL_PARAM_WIDTHS)[i];
          col.hidden = gc.$(ext_requests.URL_PARAM_HIDDENS)[i];
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
    p.$ext_requests.URL_PARAM_WIDTHS = widths;
    p.$ext_requests.URL_PARAM_HIDDENS = hiddens;
    p.$ext_requests.URL_PARAM_COLUMNS = columns;
    //~ p['widths'] = widths;
    //~ p['hiddens'] = hiddens;
    //~ p['columns'] = columns;
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
      url:ROOT_URL + '/grid_config' + this.ls_url,
      success: Lino.action_handler(this),
      scope: this,
      failure: Lino.ajax_error_handler(this)
    };
    this.loadMask.show(); // 20120211
    Ext.Ajax.request(a);
    //~ Lino.do_action(this,a);
  },
  
  on_beforeedit : function(e) {
    //~ console.log('20120202 GridPanel.on_beforeedit()',e,e.record.data.disabled_fields);
    if(e.record.data.disabled_fields && e.record.data.disabled_fields[e.field]) {
      e.cancel = true;
      Lino.notify(String.format("$_("Field '{0}' is disabled")",e.field));
    }
    //~ if (e.record.data.disabled_fields) {
      //~ for (i in e.record.data.disabled_fields) {
        //~ if(e.record.data.disabled_fields[i] == e.field) {
          //~ e.cancel = true;
          //~ Lino.notify(String.format('Field "{0}" is disabled for this record',e.field));
          //~ return
        //~ }
      //~ }
    //~ }
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
    p[e.field+'$ext_requests.CHOICES_HIDDEN_SUFFIX'] = e.value;
    // this one is needed so that this field can serve as choice context:
    e.record.data[e.field+'$ext_requests.CHOICES_HIDDEN_SUFFIX'] = e.value;
    // p[pk] = e.record.data[pk];
    // console.log("grid_afteredit:",e.field,'=',e.value);
    Ext.apply(p,this.get_base_params()); // needed for POST, ignored for PUT
    //~ Ext.apply(p,this.containing_window.config.base_params);
    p['$ext_requests.URL_PARAM_ACTION_NAME'] = 'grid';
    var self = this;
    var req = {
        params:p,
        waitMsg: 'Saving your data...',
        success: Lino.action_handler( this, function(result) {
          self.getStore().commitChanges(); // get rid of the red triangles
          self.getStore().reload();        // reload our datastore.
          },true),
        scope: this,
        failure: Lino.ajax_error_handler(this)
    };
    if (e.record.phantom) {
      Ext.apply(req,{
        method: 'POST',
        url: ROOT_URL + '/api' + this.ls_url
      });
    } else {
      Ext.apply(req,{
        method: 'PUT',
        url: ROOT_URL + '/api' + this.ls_url + '/' + e.record.id
      });
    }
    //~ console.log('20110406 on_afteredit',req);
    this.loadMask.show(); // 20120211
    Ext.Ajax.request(req);
  },

  afterRender : function() {
    Lino.GridPanel.superclass.afterRender.call(this);
    // this.getView().mainBody.focus();
    // console.log(20100114,this.getView().getRows());
    // if (this.getView().getRows().length > 0) {
    //  this.getView().focusRow(1);
    // }
    //~ this.my_load_mask = new Ext.LoadMask(this.getEl(), {
        //~ msg:'$_("Please wait...")',
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
  after_delete : function() {
    console.log('Lino.GridPanel.after_delete');
    this.refresh();
  },
  add_row_listener : function(fn,scope) {
    this.getSelectionModel().addListener('rowselect',fn,scope);
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
    //~ if (! this.rendered) return; // 20120213
    var todo = function() {
      if (this.disabled) return;
      //~ if (this.enabled) {
          //~ var src = caller.config.url_data + "/" + record.id + ".jpg"
          //~ console.log(20111125, this.containing_window);
          //~ for (k in p) this.getStore().setBaseParam(k,p[k]);
          //~ console.log('Lino.GridPanel.on_master_changed()',this.title,p);
          this.refresh()
          //~ this.set_base_params(this.master_panel.get_master_params());
          //~ this.getStore().load(); 
      //~ }
    };
    Lino.do_when_visible(this,todo.createDelegate(this));
  }
});
  

//~ Lino.MainPanelMixin = {
  //~ tbar_items : function() {
      //~ return ;
  //~ }
//~ };

//~ Ext.override(Lino.GridPanel,Lino.MainPanelMixin);
//~ Ext.override(Lino.FormPanel,Lino.MainPanelMixin);

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


//~ Lino.load_main_menu = function() {
  //~ Ext.Ajax.request({
    //~ waitMsg: 'Loading main menu...',
    //~ method: 'GET',
    //~ url: '/menu',
    //~ success: Lino.on_load_menu,
    //~ failure: Lino.ajax_error_handler
  //~ });
//~ };



//~ Lino.SlavePlugin = function(caller) {
  //~ this.caller = caller;
//~ };

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
  displayField: '$ext_requests.CHOICES_TEXT_FIELD', // 'text', 
  valueField: '$ext_requests.CHOICES_VALUE_FIELD', // 'value',
  
  //~ initComponent : Ext.form.ComboBox.prototype.initComponent.createSequence(function() {
  initComponent : function(){
      this.contextParams = {};
      //~ Ext.form.ComboBox.initComponent(this);
      Lino.ComboBox.superclass.initComponent.call(this);
  },
  setValue : function(v,record_data){
      /*
      Based on feature request developed in http://extjs.net/forum/showthread.php?t=75751
      */
      /* `record_data` is used to get the text corresponding to this value */
      //~ if(this.name == 'city') 
      //~ console.log('20120203', this.name,'.setValue(', v ,') this=', this,'record_data=',record_data);
      var text = v;
      if(this.valueField){
        if(v == null || v == '') { 
            //~ if (this.name == 'birth_country') 
                //~ console.log(this.name,'.setValue',v,'no lookup needed, value is empty');
            //~ v = undefined;
            v = '';
            //~ text = '';
        } else if (Ext.isDefined(record_data)) {
          text = record_data[this.name];
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
      //~ this.lastSelectionText = v;
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
        //~ p.start = 0;
        //~ p.limit = this.pageSize;
        p['$URL_PARAM_START'] = 0;
        p['$URL_PARAM_LIMIT'] = this.pageSize;
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
  queryParam: '$URL_PARAM_FILTER', 
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




Lino.Window = Ext.extend(Ext.Window,{
  //~ layout: "fit", 
  closeAction : 'hide',
  renderTo: 'main_area', 
  constrain: true,
  maximized: true,
  draggable: false,
  width: 700,
  height: 500,
  maximizable: false,
  constructor : function (config) {
    if (config.main_item.params_panel) {
        config.layout = 'border';
        config.main_item.region = 'center';
        config.main_item.params_panel.region = 'north';
        //~ config.main_item.params_panel.hidden = config.main_item.params_panel_hidden;
        config.items = [config.main_item.params_panel, config.main_item];
    } else {
        config.layout = 'fit';
        config.items = config.main_item;
    }
    this.main_item = config.main_item; 
    
    delete config.main_item;
    //~ delete config.params_item;
    
    //~ this.main_item = config.items.get(0);
    this.main_item.containing_window = this;
    
    //~ console.log('20120110 Lino.Window.constructor() 1');
    //~ if (Lino.current_window) { // all windows except the top are closable
    if (this.main_item.hide_window_title) { 
      config.closable = false;
      config.frame = false;
      config.shadow = false;
      //~ config.border = true;
      //~ config.title = undefined;
      //~ config.tools = null;
      delete config.title;
      delete config.tools;
    } else {
      config.title = this.main_item.empty_title;
      config.closable = true;
      config.tools = [ 
        { qtip: 'permalink', handler: Lino.permalink_handler(this), id: "pin" }
      ];
    //~ { qtip: this.config.qtip, handler: Lino.save_wc_handler(this), id: "save" }, 
    //~ { qtip: 'Call doLayout() on main Container.', handler: Lino.refresh_handler(this), id: "refresh" },
    //~ if (this.main_item.params_panel) {
        //~ config.tools = config.tools.concat([ 
          //~ { qtip: 'Show/hide parameter panel', handler: this.toggle_params_panel, id: "gear", scope:this } 
        //~ ]);
    //~ }
    //~ if (config.closable !== false) {
      // if undefined, will take default behaviour
      config.tools = config.tools.concat([ 
        { qtip: 'close', handler: this.hide, id: "close", scope:this } 
      ]);
    }
    
    this.main_item.config_containing_window(config);
    
    //~ console.log('20120110 Lino.Window.constructor() 2');
    Lino.Window.superclass.constructor.call(this,config);
    
    //~ console.log('20120110 Lino.Window.constructor() 3');
    
  },
  initComponent : function() {
    this.main_item.init_containing_window(this);
    Lino.Window.superclass.initComponent.call(this);
  
  },
  //~ toggle_params_panel : function() {
      //~ if (this.main_item.params_panel.isVisible()) 
          //~ this.main_item.params_panel.hide();
      //~ else
          //~ this.main_item.params_panel.show();
      //~ this.doLayout();
  //~ },
  unused_show : function(animateTarget,callback,scope,after_show) {
      //~ console.log('20120110 Lino.Window.show()',after_show);
      if (this.caller && !this.caller.get_containing_window) 
          console.log('20120124 WARNING: no get_containing_window in caller', this.caller);
    
      Lino.Window.superclass.show.call(this,animateTarget,callback,scope);
      Lino.current_window = this;
      if (!after_show) after_show = {};
      this.main_item.after_show(after_show);
      //~ this.window.show();
      //~ this.refresh();
      //~ Lino.load_mask.hide();
      //~ console.log('20120110 Lino.Window.show() 2');
      return this;
  },
  //~ kill : function() {
    //~ Lino.Window.superclass.hide.call(this);
    //~ Lino.current_window = this;
  //~ },
  hide : function() { 
      //~ var t = this;
      this.main_item.do_when_clean(function() { 
        //~ Lino.close_window(t); });
        Lino.close_window(); });
  },
  hide_really : function() { 
    Lino.Window.superclass.hide.call(this);
  },
  unused_hide : function() { 
      //~ console.log("Gonna close");
      var this_ = this;
      var caller = this.caller;
      this.main_item.do_when_clean(function() {
        Lino.Window.superclass.hide.call(this_);
        Lino.current_window = null;
        if (caller) {
          //~ console.log('20120124 caller is', caller);
          var cw = caller.get_containing_window();
          if (cw) {
              //~ console.log("20120118 refresh caller's window", cw);
              Lino.current_window = cw;
              cw.main_item.refresh();
          //~ } else {
              //~ console.log('20120124 caller had no containing window', caller);
              //~ caller.refresh();
          }
        //~ } else {
          //~ console.log('20120124 cannot refresh: no caller');
        }
      });
  },
  onRender : function(ct, position){
    //~ console.log('20120110 Lino.Window.onRender() 1');
    Lino.Window.superclass.onRender.call(this, ct, position);
    var main_area = Ext.getCmp('main_area')
    //~ console.log('20120110 Lino.Window.onRender() 2');
  
    this.on('show', function(win) {
        //~ console.log('20120110 Lino.Window.on show 1');
        main_area.on('resize', win.onWindowResize, win);
    });
    this.on('hide', function(win) {
        main_area.un('resize', win.onWindowResize, win);
    });
    //~ console.log('20120110 Lino.Window.onRender() 3');
  }
});


Lino.unused_ParamWindow = Ext.extend(Lino.Window,{
  //~ layout: "border", 
  constructor : function (config) {
    Lino.ParamWindow.superclass.constructor.call(this,config);
    this.main_item = config.items; // `items` must be a single component
    config.layout = 'border';
    this.main_item.region = 'center';
    config.params.region = 'north';
    config.items = [config.params, config.items];
    //~ delete config.params;
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
    my_loadRecord : function(record_data){
    //~ loadRecord : function(record){
        /* Forward also `record` to field.setValue() 
        so that Lino.Combobox can use it. 
        Lino never uses an array record here, so we can ignore this case. 
        */
        //~ console.log('20110214e loadRecord',record.data)
        var field, id;
        for(id in record_data){
            if(!Ext.isFunction(record_data[id]) && (field = this.findField(id))){
                field.setValue(record_data[id],record_data);
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
        //~ formPanel.getForm().my_loadRecord(selectedRecord);


        // Delete record from the grid.  not really required.
        //~ ddSource.grid.store.remove(selectedRecord);

        return(true);
      }
    })
}

#if $settings.LINO.use_awesome_uploader
Lino.AwesomeUploaderWindow = new Ext.Window({
		title:'Awesome Uploader in a Window!'
		,closeAction:'hide'
		,frame:true
		,width:500
		,height:200
		,items:{
			xtype:'awesomeuploader'
			,gridHeight:100
			,height:160
			,awesomeUploaderRoot:MEDIA_URL+'/lino/AwesomeUploader/'
			,listeners:{
				scope:this
				,fileupload:function(uploader, success, result){
					if(success){
						Ext.Msg.alert('File Uploaded!','A file has been uploaded!');
					}
				}
			}
		}
});
Lino.show_uploader = function () {
  Lino.AwesomeUploaderWindow.show();
};
#end if

Lino.show_mti_child = function(fieldname,detail_handler) {
  //~ console.log('show_mti_child',this);
  //~ console.log('show_mti_child',panel.find("main_area"));
  rec = Lino.current_window.main_item.get_current_record();
  //~ rec = panel.get_current_record();
  if (rec) {
    //~ console.log('show_mti_child',Lino.current_window,rec);
    if (rec.phantom) {
      Lino.notify('Not allowed on phantom record.');
    }else if (rec.data[fieldname]) {
      //~ console.log('show_mti_child',rec.id);
      detail_handler(Lino.current_window.main_item,{},{record_id:rec.id});
      //~ window.open(urlroot + '/' + rec.id);
      //~ document.location = urlroot + '/' + rec.id;
      //~ window.open(urlroot + '/' + rec.id,'_blank');
    } else {
      Lino.notify('$_("Cannot show MTI child if checkbox is off.")');
    }
  } else {
    Lino.notify('No current record.');
  }
};

#if $settings.LINO.use_davlink

Lino.davlink_open = function(webdavURL) {
  /* Calls lino.applets.davlink.DavLink.open()
  */
  //~ console.log('Going to call document.applets.DavLink.open(',webdavURL,')');
  document.applets.DavLink.open(webdavURL);
}

#end if

#if $settings.LINO.use_extensible and $settings.LINO.has_module('lino.modlib.cal')


/*
Mappings towards lino.modlib.cal.models.PanelCalendars
*/
#set $S = $site.modules.cal.PanelCalendars.get_handle($ui).store
//~ Ext.ensible.cal.CalendarMappings = {
    //~ CalendarId:   {name:'ID', mapping: $S.column_index('id'), type: 'int'},
    //~ Title:        {name:'CalTitle', mapping: $S.column_index('name'), type: 'string'},
    //~ Description:  {name:'Desc', mapping: $S.column_index('description'), type: 'string'},
    //~ ColorId:      {name:'Color', mapping: $S.column_index('color'), type: 'int'},
    //~ IsHidden:     {name:'Hidden', mapping: $S.column_index('is_hidden'), type: 'boolean'},    
//~ };
Ext.ensible.cal.CalendarMappings = {
    CalendarId:   {name:'ID',       mapping: 'id', type: 'int'},
    Title:        {name:'CalTitle', mapping: 'name', type: 'string'},
    Description:  {name:'Desc',     mapping: 'description', type: 'string'},
    ColorId:      {name:'Color',    mapping: 'color', type: 'int'},
    IsHidden:     {name:'Hidden',   mapping: 'is_hidden', type: 'boolean'},    
};
Ext.ensible.cal.CalendarRecord.reconfigure();  


/*
Mappings towards lino.modlib.cal.models.PanelEvents 
*/
#set $S = $site.modules.cal.PanelEvents.get_handle($ui).store
//~ Ext.ensible.cal.EventMappings = {
    //~ EventId:     {name: 'ID', mapping: $S.column_index('id'), type:'int'},
    //~ CalendarId:  {name: 'CalID', mapping: $S.column_index('calendarHidden'), type: 'int'},
    //~ Title:       {name: 'EvtTitle', mapping: $S.column_index('summary')},
    //~ StartDate:   {name: 'StartDt', mapping: $S.column_index('start_dt'), type: 'date', dateFormat: 'c'},
    //~ EndDate:     {name: 'EndDt', mapping: $S.column_index('end_dt'), type: 'date', dateFormat: 'c'},
    //~ RRule:       {name: 'RecurRule', mapping: $S.column_index('rsetHidden')},
    //~ Location:    {name: 'Location', mapping: $S.column_index('placeHidden')},
    //~ Notes:       {name: 'Desc', mapping: $S.column_index('description')},
    //~ Url:         {name: 'LinkUrl', mapping: $S.column_index('url')},
    //~ IsAllDay:    {name: 'AllDay', mapping: $S.column_index('all_day'), type: 'boolean'},
    //~ Reminder:    {name: 'Reminder', mapping: $S.column_index('reminder')}
    
//~ };
Ext.ensible.cal.EventMappings = {
    EventId:     {name: 'ID',        mapping: 'id', type:'int'},
    CalendarId:  {name: 'CalID',     mapping: 'calendarHidden', type: 'int'},
    Title:       {name: 'EvtTitle',  mapping: 'summary'},
    StartDate:   {name: 'StartDt',   mapping: 'start_dt', 
      type: 'date', 
      dateFormat: "$settings.LINO.datetime_format_extjs" },
    EndDate:     {name: 'EndDt',     mapping: 'end_dt', 
      type: 'date', 
      dateFormat: "$settings.LINO.datetime_format_extjs"},
    RRule:       {name: 'RecurRule', mapping: 'rsetHidden'},
    Location:    {name: 'Location',  mapping: 'placeHidden'},
    Notes:       {name: 'Desc',      mapping: 'description'},
    Url:         {name: 'LinkUrl',   mapping: 'url'},
    IsAllDay:    {name: 'AllDay',    mapping: 'all_day', type: 'boolean'},
    Reminder:    {name: 'Reminder',  mapping: 'reminder'}
    
};
Ext.ensible.cal.EventRecord.reconfigure();


Lino.on_eventclick = function(cp,rec,el) {
  console.log("Lino.on_eventclick",arguments);
  Lino.cal.Events.detail({},{record_id:rec.data.ID});
  return false;
}
    
Lino.on_editdetails = function(cp,rec,el) {
  console.log("Lino.on_editdetails",arguments);
  if (rec.data.ID)
      Lino.cal.Events.detail({},{record_id:rec.data.ID});
  return false;
}

Lino.format_time = function(dt) {
    return dt.getHours() + ':' + dt.getMinutes();
}
    
Lino.on_eventdelete = function() {
  console.log("Lino.on_eventdelete",arguments);
};

Lino.unused_on_eventadd  = function(cp,rec,el) {
  var M = Ext.ensible.cal.EventMappings;
  var params = {
    //~ id: rec.data[M.EventId.name],
    calendarHidden: rec.data[M.CalendarId.name],
    summary: rec.data[M.Title.name],
    start_date: rec.data[M.StartDate.name].dateFormat("$settings.LINO.date_format_extjs"),
    start_time: Lino.format_time(rec.data[M.StartDate.name]),
    end_date: rec.data[M.EndDate.name].dateFormat("$settings.LINO.date_format_extjs"),
    end_time: Lino.format_time(rec.data[M.EndDate.name]),
    description: rec.data[M.Notes.name]
    //~ StartDate:   {name: 'StartDt', mapping: $S.column_index('start_dt'), type: 'date', dateFormat: 'c'},
    //~ EndDate:     {name: 'EndDt', mapping: $S.column_index('end_dt'), type: 'date', dateFormat: 'c'},
    //~ RRule:       {name: 'RecurRule', mapping: $S.column_index('rsetHidden')},
    //~ Location:    {name: 'Location', mapping: $S.column_index('placeHidden')},
    //~ Notes:       {name: 'Desc', mapping: $S.column_index('description')},
    //~ Url:         {name: 'LinkUrl', mapping: $S.column_index('url')},
    //~ IsAllDay:    {name: 'AllDay', mapping: $S.column_index('all_day'), type: 'boolean'},
    //~ Reminder:    {name: 'Reminder', mapping: $S.column_index('reminder')}
    };
  console.log("Lino.on_eventadd ",rec,M,params);
  return params;
  //~ var a = {
    //~ url: ROOT_URL + '/api/cal/Events',
    //~ method: 'POST',
    //~ params: params, 
    //~ success: function(form, action) {
    //~ }
  //~ }
  //~ console.log("Lino.on_eventadd ",a);
  //~ return a;
  //~ Ext.Ajax.request(a);
  //~ Lino.cal.Events.insert(cp,{});
  //~ return false;
}
Lino.on_eventadd  = function(cp,rec,el) {
  console.log("Lino.on_eventadd ",arguments);
  return false;
}
    
Lino.on_eventresize  = function(cp,rec,el) {
  console.log("Lino.on_eventresize ",arguments);
  //~ Lino.cal.Events.insert(cp);
  //~ return false;
}
    
Lino.on_eventupdate  = function(cp,rec,el) {
  console.log("Lino.on_eventupdate",arguments);
  //~ Lino.cal.Events.insert(cp);
  //~ return false;
}
    

//~ Lino.eventStore = new Ext.ensible.cal.EventStore({ 
//~ Lino.eventStore = new Ext.data.ArrayStore({ 
Lino.eventStore = new Ext.data.JsonStore({ 
      listeners: { exception: Lino.on_store_exception }
      ,url: ROOT_URL + '/restful/cal/PanelEvents'
      ,restful : true
      ,proxy: new Ext.data.HttpProxy({ 
          url: ROOT_URL + '/restful/cal/PanelEvents', 
          disableCaching: false // no need for cache busting when loading via Ajax
          //~ disableCaching:true,
      })
      //~ ,reader : new Ext.data.JsonReader({
        ,fields: Ext.ensible.cal.EventRecord.prototype.fields.getRange()
        ,totalProperty: "count"
        ,root: "rows"
        ,idProperty: Ext.ensible.cal.EventMappings.EventId.mapping
        //~ ,idIndex: Ext.ensible.cal.EventMappings.EventId.mapping
      //~ })
      ,writer : new Ext.data.JsonWriter({
          writeAllFields: false
          //~ ,encode: false
          //~ ,createRecord : function(rec) {
              //~ return Lino.on_eventadd(null,rec);
          //~ }
          //~ ,destroyRecord : function(rec) {
              //~ return Lino.on_eventdelete(null,rec);
          //~ }
          //~ ,updateRecord : function(rec) {
              //~ return Lino.on_eventupdate(null,rec);
          //~ }
        
      })
      //~ ,disableCaching:true
      //~ ,autoLoad: true
      //~ ,remoteSort: true
      //~ ,baseParams: bp
    });

//~ Lino.calendarStore = new Ext.data.ArrayStore({ 
Lino.calendarStore = new Ext.data.JsonStore({ 
      listeners: { exception: Lino.on_store_exception }
      ,restful : true
      ,proxy: new Ext.data.HttpProxy({ 
          url: ROOT_URL + '/restful/cal/PanelCalendars?fmt=$ext_requests.URL_FORMAT_JSON', 
          disableCaching: false // no need for cache busting when loading via Ajax
          //~ restful : true
          //~ method: "GET"
      })
      //~ ,autoLoad: true
      //~ ,remoteSort: true
      //~ ,baseParams: bp
      ,totalProperty: "count"
      ,root: "rows"
      ,fields: Ext.ensible.cal.CalendarRecord.prototype.fields.getRange()
      ,idProperty: Ext.ensible.cal.CalendarMappings.CalendarId.mapping
      //~ ,idIndex: Ext.ensible.cal.CalendarMappings.CalendarId.mapping
    });


Lino.CalendarCfg = {
    dateParamFormat: '$settings.LINO.date_format_extjs',
    dateParamStart:'sd',
    dateParamEnd:'ed'
};
Lino.CalendarPanel = Ext.extend(Ext.ensible.cal.CalendarPanel,Lino.MainPanel);
//~ Ext.override(Lino.CalendarPanel,Lino.FieldBoxMixin);
Lino.CalendarPanel = Ext.extend(Lino.CalendarPanel,{
  //~ empty_title : "\$ui.get_actor('cal.Panel').report.label",
  empty_title : "$site.modules.cal.Panel.label"
  ,activeItem: 1 // 0: day, 1: week
  ,eventStore: Lino.eventStore
  ,ls_url: '/cal/Panel'
  //~ ,disableCaching:true
  ,calendarStore: Lino.calendarStore
  ,listeners: { 
    editdetails: Lino.on_editdetails
    ,eventclick: Lino.on_eventclick
    //~ ,eventadd: Lino.on_eventadd
    //~ ,eventdelete: Lino.on_eventdelete
    //~ ,eventresize: Lino.on_eventresize
    ,afterrender : function(config) {
      //~ console.log("20120211 render");
      Lino.calendarStore.load();
      var view = this.getActiveView();
      var bounds = view.getViewBounds();
      //~ var p = {sd:'05.02.2012',ed:'11.02.2012'};
      var p = {};
      p[view.dateParamStart] = bounds.start.format(view.dateParamFormat);
      p[view.dateParamEnd] = bounds.end.format(view.dateParamFormat);
      //~ console.log("20120211",p);
      Lino.eventStore.load({params:p});
      //~ Lino.CalendarPanel.superclass.constructor.call(this, config);
      //~ console.log(20120118, config,this);
    }
    }
  ,enableEditDetails: false
  ,monthViewCfg: Lino.CalendarCfg
  ,weekViewCfg: Lino.CalendarCfg
  ,multiDayViewCfg: Lino.CalendarCfg
  ,multiWeekViewCfg: Lino.CalendarCfg
  ,dayViewCfg: Lino.CalendarCfg
  //~ ,initComponent : function() {
    //~ // this.on('eventadd',Lino.on_eventadd);
    //~ Lino.CalendarPanel.superclass.initComponent.call(this);
  //~ }
});

/**
Lino.CalendarAppPanel = Ext.extend(Ext.Panel,Lino.MainPanel);
Lino.CalendarAppPanel = Ext.extend(CalendarAppPanel,{
  //~ empty_title : "\$ui.get_actor('cal.Panel').report.label",
  empty_title : "$site.modules.cal.Panel.label"
  ,activeItem: 1 // 0: day, 1: week
  ,eventStore: Lino.eventStore
  ,ls_url: '/cal/Panel'
  //~ ,disableCaching:true
  ,calendarStore: Lino.calendarStore
  ,listeners: { 
    editdetails: Lino.on_editdetails
    ,eventclick: Lino.on_eventclick
    //~ ,eventadd: Lino.on_eventadd
    //~ ,eventdelete: Lino.on_eventdelete
    //~ ,eventresize: Lino.on_eventresize
    ,afterrender : function(config) {
      //~ console.log("20120211 render");
      Lino.calendarStore.load();
      var view = this.getActiveView();
      var bounds = view.getViewBounds();
      //~ var p = {sd:'05.02.2012',ed:'11.02.2012'};
      var p = {};
      p[view.dateParamStart] = bounds.start.format(view.dateParamFormat);
      p[view.dateParamEnd] = bounds.end.format(view.dateParamFormat);
      //~ console.log("20120211",p);
      Lino.eventStore.load({params:p});
      //~ Lino.CalendarPanel.superclass.constructor.call(this, config);
      //~ console.log(20120118, config,this);
    }
    }
  ,enableEditDetails: false
  ,monthViewCfg: Lino.CalendarCfg
  ,weekViewCfg: Lino.CalendarCfg
  ,multiDayViewCfg: Lino.CalendarCfg
  ,multiWeekViewCfg: Lino.CalendarCfg
  ,dayViewCfg: Lino.CalendarCfg
  
            // This is the app UI layout code.  All of the calendar views are subcomponents of
            // CalendarPanel, but the app title bar and sidebar/navigation calendar are separate
            // pieces that are composed in app-specific layout code since they could be omitted
            // or placed elsewhere within the application.
            new Ext.Viewport({
                layout: 'border',
                items: [{
                    id: 'app-header',
                    region: 'north',
                    height: 35,
                    border: false,
                    contentEl: 'app-header-content'
                },{
                    id: 'app-center',
                    title: '...', // will be updated to the current view's date range
                    region: 'center',
                    layout: 'border',
                    listeners: {
                        'afterrender': function(){
                            Ext.getCmp('app-center').header.addClass('app-center-header');
                        }
                    },
                    items: [{
                        id:'app-west',
                        region: 'west',
                        width: 176,
                        border: false,
                        items: [{
                            xtype: 'datepicker',
                            id: 'app-nav-picker',
                            cls: 'ext-cal-nav-picker',
                            listeners: {
                                'select': {
                                    fn: function(dp, dt){
                                        App.calendarPanel.setStartDate(dt);
                                    },
                                    scope: this
                                }
                            }
                        },{
                            xtype: 'extensible.calendarlist',
                            store: this.calendarStore,
                            border: false,
                            width: 175
                        }]
                    },{
                        xtype: 'extensible.calendarpanel',
                        eventStore: this.eventStore,
                        calendarStore: this.calendarStore,
                        border: false,
                        id:'app-calendar',
                        region: 'center',
                        activeItem: 3, // month view
                        
                        // Any generic view options that should be applied to all sub views:
                        viewConfig: {
                            //enableFx: false,
                            //ddIncrement: 10, //only applies to DayView and subclasses, but convenient to put it here
                            //viewStartHour: 6,
                            //viewEndHour: 18,
                            //minEventDisplayMinutes: 15
                        },
                        
                        // View options specific to a certain view (if the same options exist in viewConfig
                        // they will be overridden by the view-specific config):
                        monthViewCfg: {
                            showHeader: true,
                            showWeekLinks: true,
                            showWeekNumbers: true
                        },
                        
                        multiWeekViewCfg: {
                            //weekCount: 3
                        },
                        
                        // Some optional CalendarPanel configs to experiment with:
                        //readOnly: true,
                        //showDayView: false,
                        //showMultiDayView: true,
                        //showWeekView: false,
                        //showMultiWeekView: false,
                        //showMonthView: false,
                        //showNavBar: false,
                        //showTodayText: false,
                        //showTime: false,
                        //editModal: true,
                        //enableEditDetails: false,
                        //title: 'My Calendar', // the header of the calendar, could be a subtitle for the app
                        
                        // Once this component inits it will set a reference to itself as an application
                        // member property for easy reference in other functions within App.
                        initComponent: function() {
                            App.calendarPanel = this;
                            this.constructor.prototype.initComponent.apply(this, arguments);
                        },
                        
                        listeners: {
                            'eventclick': {
                                fn: function(vw, rec, el){
                                    this.clearMsg();
                                },
                                scope: this
                            },
                            'eventover': function(vw, rec, el){
                                //console.log('Entered evt rec='+rec.data[Ext.ensible.cal.EventMappings.Title.name]', view='+ vw.id +', el='+el.id);
                            },
                            'eventout': function(vw, rec, el){
                                //console.log('Leaving evt rec='+rec.data[Ext.ensible.cal.EventMappings.Title.name]+', view='+ vw.id +', el='+el.id);
                            },
                            'eventadd': {
                                fn: function(cp, rec){
                                    this.showMsg('Event '+ rec.data[Ext.ensible.cal.EventMappings.Title.name] +' was added');
                                },
                                scope: this
                            },
                            'eventupdate': {
                                fn: function(cp, rec){
                                    this.showMsg('Event '+ rec.data[Ext.ensible.cal.EventMappings.Title.name] +' was updated');
                                },
                                scope: this
                            },
                            'eventdelete': {
                                fn: function(cp, rec){
                                    //this.eventStore.remove(rec);
                                    this.showMsg('Event '+ rec.data[Ext.ensible.cal.EventMappings.Title.name] +' was deleted');
                                },
                                scope: this
                            },
                            'eventcancel': {
                                fn: function(cp, rec){
                                    // edit canceled
                                },
                                scope: this
                            },
                            'viewchange': {
                                fn: function(p, vw, dateInfo){
                                    if(this.editWin){
                                        this.editWin.hide();
                                    };
                                    if(dateInfo !== null){
                                        // will be null when switching to the event edit form so ignore
                                        Ext.getCmp('app-nav-picker').setValue(dateInfo.activeDate);
                                        this.updateTitle(dateInfo.viewStart, dateInfo.viewEnd);
                                    }
                                },
                                scope: this
                            },
                            'dayclick': {
                                fn: function(vw, dt, ad, el){
                                    this.clearMsg();
                                },
                                scope: this
                            },
                            'rangeselect': {
                                fn: function(vw, dates, onComplete){
                                    this.clearMsg();
                                },
                                scope: this
                            },
                            'eventmove': {
                                fn: function(vw, rec){
                                    rec.commit();
                                    var time = rec.data[Ext.ensible.cal.EventMappings.IsAllDay.name] ? '' : ' \\a\\t g:i a';
                                    this.showMsg('Event '+ rec.data[Ext.ensible.cal.EventMappings.Title.name] +' was moved to '+
                                        rec.data[Ext.ensible.cal.EventMappings.StartDate.name].format('F jS'+time));
                                },
                                scope: this
                            },
                            'eventresize': {
                                fn: function(vw, rec){
                                    rec.commit();
                                    this.showMsg('Event '+ rec.data[Ext.ensible.cal.EventMappings.Title.name] +' was updated');
                                },
                                scope: this
                            },
                            'eventdelete': {
                                fn: function(win, rec){
                                    this.eventStore.remove(rec);
                                    this.showMsg('Event '+ rec.data[Ext.ensible.cal.EventMappings.Title.name] +' was deleted');
                                },
                                scope: this
                            },
                            'initdrag': {
                                fn: function(vw){
                                    if(this.editWin && this.editWin.isVisible()){
                                        this.editWin.hide();
                                    }
                                },
                                scope: this
                            }
                        }
                    }]
                }]
            });
        },
        
        // The CalendarPanel itself supports the standard Panel title config, but that title
        // only spans the calendar views.  For a title that spans the entire width of the app
        // we added a title to the layout's outer center region that is app-specific. This code
        // updates that outer title based on the currently-selected view range anytime the view changes.
        updateTitle: function(startDt, endDt){
            var p = Ext.getCmp('app-center');
            
            if(startDt.clearTime().getTime() == endDt.clearTime().getTime()){
                p.setTitle(startDt.format('F j, Y'));
            }
            else if(startDt.getFullYear() == endDt.getFullYear()){
                if(startDt.getMonth() == endDt.getMonth()){
                    p.setTitle(startDt.format('F j') + ' - ' + endDt.format('j, Y'));
                }
                else{
                    p.setTitle(startDt.format('F j') + ' - ' + endDt.format('F j, Y'));
                }
            }
            else{
                p.setTitle(startDt.format('F j, Y') + ' - ' + endDt.format('F j, Y'));
            }
        },
        
        // This is an application-specific way to communicate CalendarPanel event messages back to the user.
        // This could be replaced with a function to do "toast" style messages, growl messages, etc. This will
        // vary based on application requirements, which is why it's not baked into the CalendarPanel.
        showMsg: function(msg){
            Ext.fly('app-msg').update(msg).removeClass('x-hidden');
        },
        
        clearMsg: function(){
            Ext.fly('app-msg').update('').addClass('x-hidden');
        }
    }



****/





#end if

/*
captureEvents utility by Aaron Conran
<http://www.sencha.com/learn/grid-faq/>

Ext.onReady(function(){
    var grid = new Ext.grid.GridPanel({
        ... 
    });
 
    captureEvents(grid);
});

*/
function captureEvents(observable) {
    Ext.util.Observable.capture(
        observable,
        function(eventName) {
            console.info(eventName);
        },
        this
    );		
}
 
