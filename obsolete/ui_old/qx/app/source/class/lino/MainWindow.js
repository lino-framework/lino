qx.Class.define("lino.MainWindow",
{
  extend : qx.ui.window.Window,

    construct : function()
    {
      //~ this.base(arguments, "Hello")
      // tutorial-part-2.html#finishing-touches
      this.base(arguments, "Lino", "lino/lino.ico");

      // hide the window buttons
      this.maximize();
      //~ this.setShowClose(false);
      //~ this.setShowMaximize(true);
      //~ this.setShowMinimize(false);
      
      //~ // adjust size
      //~ this.setWidth(250);
      //~ this.setHeight(300);    
      
      var layout = new qx.ui.layout.Grid(0, 0);
      //~ layout.setRowFlex(1, 1);
      //~ layout.setColumnFlex(0, 1);
      this.setLayout(layout);      
      this.setContentPadding(0);
      
      var menubar = new qx.ui.menubar.MenuBar();
      this.add(menubar, {row: 0, column: 0, colSpan: 2});
      
      var m1 = new qx.ui.menu.Menu(this.tr("Contacts"));
      menubar.add(m1);
      
      var btn = new qx.ui.menubar.Button(this.tr("Persons"));
      m1.add(btn)
      btn.setToolTipText(this.tr("Reload the tweets."));
      btn.addListener("execute", function() {
          this.fireEvent("reload");
      }, this); 
      // spacer
      //~ toolbar.addSpacer();
          
    }
    //~ members : {
      //~ __list : null,
      //~ __textarea : null,
      
      //~ getList : function() {
        //~ return this.__list;
      //~ },
      //~ clearPostMessage : function() {
        //~ this.__textarea.setValue(null);
      //~ }
    //~ },
    //~ events :
    //~ {
      //~ "reload" : "qx.event.type.Event",
      //~ "post"   : "qx.event.type.Data"
    //~ }
});