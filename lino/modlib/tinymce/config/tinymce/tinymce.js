/* Copyright 2009-2018 Rumma & Ko Ltd */
{% if site.plugins.tinymce.document_domain %}
document.domain = '{{site.plugins.tinymce.document_domain}}';
{% endif %}

Lino.edit_tinymce_text = function(panel, tinymce_options) {
  // edit the text in own window.
  // `panel` is the RichTextPanel
  // console.log(20150520, panel);
  //~ var rec = panel.get_current_record();
  var rec = panel.containing_panel.get_current_record();
  var value = rec ? rec.data[panel.editor.name] : '';
  var saving = false;
  var todo_after_save = false;
  var discard_changes = false;
  
  
  function save() {
    if (saving) {alert('tried to save again'); return; }
    var url = panel.containing_panel.get_record_url(rec.id);
    var params = Ext.apply({}, panel.containing_panel.get_base_params());
    params[panel.editor.name] = editor.getValue();
    //~ params.{{constants.URL_PARAM_SUBST_USER}} = Lino.subst_user;
    //~ Lino.insert_subst_user(params);

    // 20150325 http://trac.lino-framework.org/ticket/131
    var action_name = panel.containing_panel.save_action_name;
    if (!action_name) 
        action_name = panel.containing_panel.action_name;
    params.{{constants.URL_PARAM_ACTION_NAME}} = action_name;

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
        theme_advanced_buttons1 : "{{site.plugins.tinymce.window_buttons1}}",
        theme_advanced_buttons2 : "{{site.plugins.tinymce.window_buttons2}}",
        theme_advanced_buttons3 : "{{site.plugins.tinymce.window_buttons3}}",
        theme_advanced_resizing : false,
        convert_urls : false,
        save_onsavecallback : save_callback,
        save_enablewhendirty : true
        //~ save_oncancelcallback: on_cancel
  });
  Ext.apply(settings, tinymce_options);
  var editor = new Ext.ux.TinyMCE({
      value : value,
      tinymceSettings: settings
    });
  var win = new Ext.Window({
    title: rec.title, 
    //~ bbar: actions,
    layout: 'fit',
    items: editor,
    width: {{site.plugins.tinymce.window_width}}, 
    height: {{site.plugins.tinymce.window_height}},
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
        var config = {title:"{{_('Confirmation')}}"};
        config.buttons = Ext.MessageBox.YESNOCANCEL;
        config.msg = "{{_('Save changes to text ?')}}";
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


Lino.RichTextPanel = Ext.extend(Ext.Panel,Lino.PanelMixin);
Lino.RichTextPanel = Ext.extend(Lino.RichTextPanel,Lino.FieldBoxMixin);
Lino.RichTextPanel = Ext.extend(Lino.RichTextPanel,{
    
  //~ initComponent : function(){
    //~ Lino.RichTextPanel.superclass.initComponent.call(this);
  //~ },
  constructor : function(config, params) {
      // console.log('20150520a Lino.RichTextPanel.initComponent', this);
    //~ var url = TEMPLATES_URL + config.ls_url + "/" + String(rec.id) + "/" + config.name;
    //~ var url = TEMPLATES_URL + config.ls_url + "/" + config.name;
    var t = this;
    var tinymce_options = {
        theme : "advanced",
        content_css: '{{site.build_static_url("extjs/lino.css")}},{{site.build_static_url("tinymce_content.css")}}',

        theme_advanced_font_sizes : "12px,13px,14px,16px,18px,20px,24px",
        font_size_style_values : "12px,13px,14px,16px,18px,20px,24px",
        language: '{{language[:2]}}',
        //~ template_external_list_url : url,
        theme_advanced_toolbar_location : "top",
        theme_advanced_toolbar_align : "left",
        theme_advanced_statusbar_location : "bottom",
        template_popup_width : {{site.plugins.tinymce.window_width}},
        template_popup_height : {{site.plugins.tinymce.window_height}},
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
        theme_advanced_buttons1 : "{{site.plugins.tinymce.field_buttons}}",
        theme_advanced_buttons2 : "",
        theme_advanced_buttons3 : "", // ,|,sub,sup,|,charmap",      
        theme_advanced_resizing : false
        //~ save_onsavecallback : save_callback,
        //~ save_enablewhendirty : true
        //~ save_oncancelcallback: on_cancel
        
    }};
    Ext.apply(editorConfig.tinymceSettings, tinymce_options);
    //~ editorConfig.name = config.action_name;
    editorConfig.name = config.name;
    delete config.name;
    //~ config.title = config.label;
    //~ delete config.label;
    this.before_init(config,params);
    
    // console.log('20150520b Lino.RichTextPanel.initComponent', this);

    this.editor = new Ext.ux.TinyMCE(editorConfig);
    var t = this;
    function save_cmd() { 
        // console.log("20150902 save_cmd()", arguments);            
        var cw = t.get_containing_window();
        if (cw) {
            cw.main_item.save();
        }
    }
    this.editor.withEd(function(){
        if (!t.editor.ed.addShortcut(
            'ctrl+s', 'Save the content', save_cmd)) {
            console.log("20150902 addShortcut() failed");            
        };
        // t.editor.ed.onKeyDown.add(function(ed, e) {
        //     if (e.keyCode == 13 && e.ctrlKey) {
        //         save_cmd(); 
        //         return tinymce.dom.Event.cancel(e); 
        //         // e.preventDefault();
        //         // http://stackoverflow.com/questions/18971284/event-preventdefault-vs-return-false-no-jquery
        //     }
        // });
    });
    config.tools = [{
                      qtip: "{{_('Edit text in own window')}}", 
                      id: "up",
                      handler: function(){
                        if(t.editor.isDirty()) {
                            var record = t.containing_panel.get_current_record();
                            record.data[t.editor.name] = t.editor.getValue();
                        }
                        Lino.edit_tinymce_text(t, tinymce_options)
                      }
                    }];
    
    config.items = this.editor;
    config.layout = "fit";
    // console.log('20150520c Lino.RichTextPanel.initComponent', this);
    Lino.RichTextPanel.superclass.constructor.call(this, config);
    // console.log('20150520d Lino.RichTextPanel.initComponent', this);
  },
  getValue : function(v) {
      return this.editor.getValue(v);
  },
  refresh : function(unused) { 
      this.refresh_with_after();
  },
  /* RichTextPanel */
  refresh_with_after : function(after) {
    // when called from the dashboard:    
    if (!this.containing_panel.get_current_record) { return; }
    var record = this.containing_panel.get_current_record();
    // console.log('20140504 RichTextPanel.refresh()',
    //             this.title,record.title, record);
    var todo = function() {
      if (record) {
        var url = '{{site.plugins.tinymce.build_plain_url("templates")}}' 
              + this.containing_panel.ls_url + "/" 
              + String(record.id) + "/" + this.editor.name;
        // console.log('20150415 RichTextPanel.refresh()',url);
        if (this.editor.ed)
            this.editor.ed.settings.template_external_list_url = url;
            // else {console.log("20150415 no editor")}
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

