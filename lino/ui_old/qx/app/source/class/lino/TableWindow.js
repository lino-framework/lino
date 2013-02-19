/* ************************************************************************

   Copyright:

   License:

   Authors:

************************************************************************ */

/* ************************************************************************

#asset(lino/*)

************************************************************************ */

/**
 * This is the main application class of your custom application "lino"
 */
qx.Class.define("lino.TableWindow",
{
  extend : qx.ui.window.Window,
  //~ construct : function(app, caption) {
  construct : function(app) {
      //~ console.log('lino.TableWindow.construct()',this,app);
      this.base(arguments);
      //~ this.base(arguments, caption);
      //~ console.log('lino.TableWindow.construct.base ok');
      this.__app = app;
      //~ var tm = this.createTableModel();
      //~ this.__table = new qx.ui.table.Table(tm);
      this.__table = this.createTable();
      
      var toolbar = new qx.ui.toolbar.ToolBar();
      var part = new qx.ui.toolbar.Part();
      toolbar.add(part);
      var reload = new qx.ui.toolbar.Button('Reload');
      reload.addListener('execute',function(){
        var tm = this.__table.getTableModel();
        console.log("Reload. tm = ",tm);
        tm.reloadData();
      }, this);
      part.add(reload);
      this.setupToolbar(part);
      
      this.set({
        width: 600,
        height: 400,
        contentPadding : [ 0, 0, 0, 0 ]
        //~ showClose: false,
        //~ showMinimize: false
      });
      this.setLayout(new qx.ui.layout.VBox());
      this.add(toolbar);
      this.add(this.__table, {flex: 1});
      
  },
          
  members : {
      __app : null,
      __table : null,
      showWindow : function(cls) { 
        this.__app.showWindow(cls); 
      },
      createTableModel : function() {
        throw new Error("createTableModel is abstract");
      },
      setupToolbar: function(bar) { 
      }
  },
  events : {
    //~ "reload" : "qx.event.type.Event",
    //~ "post"   : "qx.event.type.Data"
  }
  
});