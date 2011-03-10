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

    //~ construct : function(url,columns,title)
  construct : function(app) {
      console.log('lino.TableWindow.construct()',this,app);
      this.base(this.caption);
      //~ console.log('lino.TableWindow.construct.base ok');
      this.__app = app;
      var tm = this.createTableModel();
      var table = new qx.ui.table.Table(tm);
      
      var toolbar = new qx.ui.toolbar.ToolBar();
      var part = new qx.ui.toolbar.Part();
      toolbar.add(part);
      var reload = new qx.ui.toolbar.Button('Reload', "icon/22/actions/view-refresh.png");
      reload.addListener('execute',function(){
        this._tableModel.reloadData();
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
      this.add(table, {flex: 1});
      
  },
          
  members : {
      __app : null,
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