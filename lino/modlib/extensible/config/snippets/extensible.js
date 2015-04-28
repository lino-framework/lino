/*
  This is the `extensible.js` snippet. 
  Used in lino.modlib.extensible.App.site_js_snippets
*/

/*
Mappings towards lino.modlib.extensible.models.PanelCalendars
*/
// Sset SS = Ssite.modules.extensible.PanelCalendars.get_handle(Sui).store
Ext.ensible.cal.CalendarMappings = {
    CalendarId:   {name:'ID',       mapping: 'id', type: 'int'},
    Title:        {name:'CalTitle', mapping: 'summary', type: 'string'},
    Description:  {name:'Desc',     mapping: 'description', type: 'string'},
    ColorId:      {name:'Color',    mapping: 'color', type: 'int'},
    IsHidden:     {name:'Hidden',   mapping: 'is_hidden', type: 'boolean'},    
};
Ext.ensible.cal.CalendarRecord.reconfigure();  


/*
Mappings towards lino.modlib.extensible.models.PanelEvents 
*/
// Sset SS = Ssite.modules.extensible.PanelEvents.get_handle(Sui).store
Ext.ensible.cal.EventMappings = {
    EventId:     {name: 'ID',        mapping: 'id', type:'int'},
    CalendarId:  {name: 'CalID',     mapping: 'calendarHidden', type: 'int'},
    Title:       {name: 'EvtTitle',  mapping: 'summary'},
    StartDate:   {name: 'StartDt',   mapping: 'start_dt', 
      type: 'date', 
      dateFormat: "{{settings.SITE.datetime_format_extjs}}" },
    EndDate:     {name: 'EndDt',     mapping: 'end_dt', 
      type: 'date', 
      dateFormat: "{{settings.SITE.datetime_format_extjs}}"},
    RRule:       {name: 'RecurRule', mapping: 'rsetHidden'},
    Location:    {name: 'Location',  mapping: 'placeHidden'},
    Notes:       {name: 'Desc',      mapping: 'description'},
    Url:         {name: 'LinkUrl',   mapping: 'url'},
    IsAllDay:    {name: 'AllDay',    mapping: 'all_day', type: 'boolean'},
    Reminder:    {name: 'Reminder',  mapping: 'reminder'}
    
};
Ext.ensible.cal.EventRecord.reconfigure();


//~ Lino.on_eventclick = 
    
Lino.on_editdetails = 

Lino.format_time = function(dt) {
    return dt.getHours() + ':' + dt.getMinutes();
}
    
Lino.on_eventdelete = function() {
  //~ console.log("Lino.on_eventdelete",arguments);
};

Lino.on_eventadd  = function(cp,rec,el) {
  //~ console.log("Lino.on_eventadd ",arguments);
  return false;
}
    
Lino.on_eventresize  = function(cp,rec,el) {
  //~ console.log("Lino.on_eventresize ",arguments);
  //~ Lino.cal.Events.insert(cp);
  //~ return false;
}
    
Lino.on_eventupdate  = function(cp,rec,el) {
  //~ console.log("Lino.on_eventupdate",arguments);
  //~ Lino.cal.Events.insert(cp);
  //~ return false;
}
    

//~ Lino.eventStore = new Ext.ensible.cal.EventStore({ 
//~ Lino.eventStore = new Ext.data.ArrayStore({ 
Lino.unused_eventStore = new Ext.data.JsonStore({ 
  listeners: { exception: Lino.on_store_exception }
  ,url: '{{extjs.build_plain_url("restful/extensible/PanelEvents")}}'
  ,restful : true
  ,proxy: new Ext.data.HttpProxy({ 
      url: '{{extjs.build_plain_url("restful/extensible/PanelEvents")}}', 
      disableCaching: false // no need for cache busting when loading via Ajax
      //~ disableCaching:true,
  })
  ,fields: Ext.ensible.cal.EventRecord.prototype.fields.getRange()
  ,totalProperty: "count"
  ,root: "rows"
  ,idProperty: Ext.ensible.cal.EventMappings.EventId.mapping
  ,writer : new Ext.data.JsonWriter({
    writeAllFields: false
  })
  ,load: function(options) {
    //~ foo.bar = baz; // 20120213
      if (!options) options = {};
      if (!options.params) options.params = {};
      //~ options.params.$constants.URL_PARAM_TEAM_VIEW = Lino.calendar_app.team_view_button.pressed;
      
      var view = this.cal_panel.getActiveView();
      var bounds = view.getViewBounds();
      //~ var p = {sd:'05.02.2012',ed:'11.02.2012'};
      //~ var p = {};
      options.params[view.dateParamStart] = bounds.start.format(view.dateParamFormat);
      options.params[view.dateParamEnd] = bounds.end.format(view.dateParamFormat);
      Lino.insert_subst_user(options.params);
      //~ Ext.apply(options.params,p)
      //~ console.log('20120710 eventStore.load()',this.baseParams,options);
    
    return Ext.data.JsonStore.prototype.load.call(this,options);
  }
});


Lino.CalendarCfg = {
    dateParamFormat: '{{settings.SITE.date_format_extjs}}',
    dateParamStart:'sd',
    dateParamEnd:'ed'
};
//~ 20120704 Lino.CalendarPanel = Ext.extend(Ext.ensible.cal.CalendarPanel,Lino.MainPanel);
//~ Lino.CalendarPanel = Ext.extend(Lino.CalendarPanel,{
Ext.override(Ext.ensible.cal.CalendarPanel,Lino.MainPanel);
Ext.override(Ext.ensible.cal.CalendarPanel,{
  //~ empty_title : "\$ui.get_actor('cal.Panel').report.label",
  empty_title : "{{site.modules.extensible.CalendarPanel.label}}"
  ,activeItem: 1 // 0: day, 1: week
  ,ls_url: '/extensible/CalendarPanel'
  //~ ,disableCaching:true
  //~ ,eventStore: Lino.eventStore
  //~ ,calendarStore: Lino.calendarStore
  //~ ,initComponent : function(){
    //~ Ext.ensible.cal.CalendarPanel.superclass.initComponent.call(this);
    //~ this.eventStore.on('load',function(){
      //~ console.log("20130808",Lino.eventStore);
      //~ if (this.eventStore.reader.jsonData) {
        //~ console.log("20130808 b",this.eventStore.reader.jsonData.title);
        //~ this.set_window_title(this.eventStore.reader.jsonData.title);
      //~ }
    //~ },this);
  //~ }
  ,listeners: { 
    editdetails: function(cp,rec,el) {
      //~ console.log("Lino.on_editdetails",arguments);
      if (rec.data.ID)
          Lino.extensible.PanelEvents.detail.run(null,{
              record_id:rec.data.ID,
              base_params:this.app_instance.event_store.baseParams});
      return false;
    }
    ,eventclick: function(cp,rec,el) {
      //~ console.log("Lino.on_eventclick",arguments);
      //~ Lino.cal.Events.detail_action.run({record_id:rec.data.ID});
      Lino.extensible.PanelEvents.detail.run(null,{
            record_id:rec.data.ID,
                base_params:this.app_instance.event_store.baseParams});
      return false;
    }
    //~ ,eventadd: Lino.on_eventadd
    //~ ,eventdelete: Lino.on_eventdelete
    //~ ,eventresize: Lino.on_eventresize
    ,afterrender : function(config) {
      // console.log("20140402 CalendarPanel.afterrender");
      this.app_instance.calendar_store.cal_panel = this;
      // 20140402 this.app_instance.calendar_store.load();
      //~ console.log("20120704 afterrender calls eventStore.load()",p);
      this.app_instance.event_store.cal_panel = this;
      //~ Lino.eventStore.load({params:p});
      //~ 20130905 removed: this.app_instance.event_store.load();
      //~ Lino.CalendarPanel.superclass.constructor.call(this, config);
      //~ console.log(20120118, config,this);
    }
    }
  ,enableEditDetails: false
  //~ ,monthViewCfg: Lino.CalendarCfg
  //~ ,weekViewCfg: Lino.CalendarCfg
  //~ ,multiDayViewCfg: Lino.CalendarCfg
  //~ ,multiWeekViewCfg: Lino.CalendarCfg
  //~ ,dayViewCfg: Lino.CalendarCfg
  //~ ,initComponent : function() {
    //~ // this.on('eventadd',Lino.on_eventadd);
    //~ Lino.CalendarPanel.superclass.initComponent.call(this);
  //~ }
});




Lino.CalendarAppPanel = Ext.extend(Ext.Panel,Lino.MainPanel);
Lino.CalendarAppPanel = Ext.extend(Lino.CalendarAppPanel,Lino.PanelMixin);
Lino.CalendarAppPanel = Ext.extend(Lino.CalendarAppPanel,{
  app_instance : null
  //~ empty_title : "\$ui.get_actor('cal.Panel').report.label",
  ,empty_title : "{{site.modules.extensible.CalendarPanel.label}}"
  ,ls_url: '/extensible/CalendarPanel'
  ,set_status : function(status,rp) { 
      // console.log('20140402 CalendarAppPanel.set_status()', status);
      this.requesting_panel = Ext.getCmp(rp);
      this.clear_base_params();
      if (status == undefined) status = {};
      //~ if (status.param_values) 
      //~ this.set_field_values(status.field_values);
      if (status.base_params) this.set_base_params(status.base_params);
      this.refresh();
      }
  ,refresh : function() {
      //~ this.app_instance.event_store.reload(); 20130905
      this.app_instance.calendar_store.load();  // added 20140402
      this.app_instance.event_store.load();
  }
  ,layout: 'fit'
  ,get_base_params : function() {
    // console.log('20140402 getbase_params has', this.base_params);
    var p = Ext.apply({}, this.base_params);
    Lino.insert_subst_user(p);
    // console.log('20140402 getbase_params returns', p);
    return p;
  }
  ,set_base_params : function(p) {
    this.base_params = Ext.apply(this.app_instance.event_store.baseParams,p);
    this.app_instance.event_store.baseParams = this.base_params;
    // console.log('20140402 this.base_params is', this.base_params);
  }
  ,clear_base_params : function() {
      this.base_params = {};
      Lino.insert_subst_user(this.base_params);
  }
  ,set_base_param : function(k,v) {
      if (!this.base_params) this.base_params = {};
      this.base_params[k] = v;
  }
});

Lino.CalendarApp = function() { return {
  team_view_button : null 
  ,get_main_panel : function() {
      var cap = null;
      this.event_store = new Ext.data.JsonStore({ 
          listeners: { exception: Lino.on_store_exception }
          ,url: '{{extjs.build_plain_url("restful/extensible/PanelEvents")}}'
          ,restful : true
          ,proxy: new Ext.data.HttpProxy({ 
              url: '{{extjs.build_plain_url("restful/extensible/PanelEvents")}}', 
              disableCaching: false // no need for cache busting when loading via Ajax
              //~ disableCaching:true,
          })
          ,fields: Ext.ensible.cal.EventRecord.prototype.fields.getRange()
          ,totalProperty: "count"
          ,root: "rows"
          ,idProperty: Ext.ensible.cal.EventMappings.EventId.mapping
          ,writer : new Ext.data.JsonWriter({
            writeAllFields: false
          })
          ,load: function(options) {
            //~ foo.bar = baz; // 20120213
              if (!options) options = {};
              if (!options.params) options.params = {};
              //~ options.params.$constants.URL_PARAM_TEAM_VIEW = Lino.calendar_app.team_view_button.pressed;
              
              var view = this.cal_panel.getActiveView();
              var bounds = view.getViewBounds();
              //~ var p = {sd:'05.02.2012',ed:'11.02.2012'};
              //~ var p = {};
              options.params[view.dateParamStart] = bounds.start.format(view.dateParamFormat);
              options.params[view.dateParamEnd] = bounds.end.format(view.dateParamFormat);
              Lino.insert_subst_user(options.params);
              Ext.apply(options.params, cap.get_base_params());
              //~ this.cal_panel.base_params.su.toString();
              //~ if (this.cal_panel) {
                  // Ext.apply(options.params,this.cal_panel.base_params);
              //~ }
              //~ Ext.apply(options.params,p)
              //~ console.log('20130905 eventStore.load()',this.cal_panel,this.baseParams,options.params);
            
            return Ext.data.JsonStore.prototype.load.call(this,options);
          }
      });

      //~ Lino.calendarStore
      this.calendar_store = new Ext.data.JsonStore({ 
          listeners: { exception: Lino.on_store_exception }
          ,restful : true
          ,proxy: new Ext.data.HttpProxy({ 
              url: '{{extjs.build_plain_url("restful/extensible/PanelCalendars",fmt=constants.URL_FORMAT_JSON)}}', 
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
          ,load: function(options) {
              // new since 20140402 add substitute user when calling
              // calendars
              if (!options) options = {};
              if (!options.params) options.params = {};
              // Lino.insert_subst_user(options.params);
              Ext.apply(options.params, cap.get_base_params());
              // console.log("20140402 calendar_store.load", options.params, 
              //             this.cal_panel, cap.get_base_params());
            return Ext.data.JsonStore.prototype.load.call(this,options);
          }
      });
      
      cap = new Lino.CalendarAppPanel({ 
          app_instance: this, 
          items : 
        //~ [{
          //~ id: 'app-header',
          //~ region: 'north',
          //~ height: 35,
          //~ border: false,
          // contentEl: 'app-header-content'
        //~ },
      {
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
                              // console.log("20131017",dp);
                              //~ Lino.calendarPanel.setStartDate(dt);
                              //~ cap.setStartDate(dt);
                              Ext.getCmp('app-calendar').setStartDate(dt);
                          },
                          //~ scope: this
                      }
                  }
              //~ },{ 
                //~ layout:'fit',
                //~ items: [
                  //~ new Ext.form.Checkbox({
                    //~ boxLabel:"$_('Team view')",
                    //~ hideLabel:true
                    //~ listeners: { click: }
                  //~ })
                //~ ]
              //~ },{ 
                //~ layout:'form',
                //~ items: [
                  //~ this.team_view_button = new Ext.Button({
                    //~ text:"{{_('Team view')}}",
                    //~ enableToggle:true,
                    //~ pressed:false,
                    //~ toggleHandler: function(btn,state) { 
                      //~ // console.log('20120716 teamView.toggle()');
                      //~ this.event_store.setBaseParam('{{constants.URL_PARAM_TEAM_VIEW}}',state);
                      //~ this.event_store.load();
                      //~ // console.log("team view",state);
                    //~ }
                  //~ })
                //~ ]
              },{
                  xtype: 'extensible.calendarlist',
                  store: this.calendar_store,
                  border: false,
                  width: 175
              }]
          },{
              xtype: 'extensible.calendarpanel', // Ext.ensible.cal.CalendarPanel
              eventStore: this.event_store,
              app_instance: this,
              calendarStore: this.calendar_store,
              border: false,
              id:'app-calendar',
              region: 'center',
              //~ activeItem: 3, // month view
              
              // Any generic view options that should be applied to all sub views:
              viewConfig: {
                  // Lino.CalendarCfg
                  dateParamFormat: '{{settings.SITE.date_format_extjs}}',
                  dateParamStart:'sd',
                  dateParamEnd:'ed',
                
                  //enableFx: false,
                  //ddIncrement: 10, //only applies to DayView and subclasses, but convenient to put it here
                  viewStartHour: {{settings.SITE.plugins.extensible.calendar_start_hour}}, // 8
                  viewEndHour: {{settings.SITE.plugins.extensible.calendar_end_hour}} // 18
                  //minEventDisplayMinutes: 15
              },
              
              // View options specific to a certain view (if the same options exist in viewConfig
              // they will be overridden by the view-specific config):
              monthViewCfg: {
                  showHeader: true,
                  showWeekLinks: true,
                  showWeekNumbers: true,
                  eventBodyMarkup: ['{Title}',
                    //~ '<tpl if="url">',
                        //~ '<a href="{url}">XX</a>',
                    //~ '</tpl>',
                    '<tpl if="_isReminder">',
                        '<i class="ext-cal-ic ext-cal-ic-rem">&#160;</i>',
                    '</tpl>',
                    '<tpl if="_isRecurring">',
                        '<i class="ext-cal-ic ext-cal-ic-rcr">&#160;</i>',
                    '</tpl>',
                    '<tpl if="spanLeft">',
                        '<i class="ext-cal-spl">&#160;</i>',
                    '</tpl>',
                    '<tpl if="spanRight">',
                        '<i class="ext-cal-spr">&#160;</i>',
                    '</tpl>'
                ].join('')
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
              //~ initComponent: function() {
                  //~ Lino.calendarPanel = this;
                  //~ this.constructor.prototype.initComponent.apply(this, arguments);
              //~ },
              
              listeners: {
                  //~ 'eventclick': {
                      //~ fn: function(vw, rec, el){
                          //~ this.clearMsg();
                      //~ },
                      //~ scope: this
                  //~ },
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
                          this.event_store.remove(rec);
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
        }
        //~ ]
        
      });
      
      this.event_store.on('load',function(){
        //~ console.log("20130905 on event_store load",this.event_store.reader.jsonData);
        if (this.event_store.reader.jsonData) {
          //~ console.log("20130808 b",this.event_store.reader.jsonData.title);
          //~ console.log("20130808 c",this);
          cap.set_window_title(this.event_store.reader.jsonData.title);
        }
      },this);
      
      //~ cap.app_instance = this;
      return cap;
      
  }
  ,updateTitle: function(startDt, endDt){
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
  }
  // This is an application-specific way to communicate CalendarPanel event messages back to the user.
  // This could be replaced with a function to do "toast" style messages, growl messages, etc. This will
  // vary based on application requirements, which is why it's not baked into the CalendarPanel.
  ,showMsg: function(msg){
      Lino.notify(msg);
      //~ Ext.fly('app-msg').update(msg).removeClass('x-hidden');
  }
  
  ,clearMsg: function(){
      Lino.notify('');
      //~ Ext.fly('app-msg').update('').addClass('x-hidden');
  }
}
};

