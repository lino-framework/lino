sap.ui.define([
   "sap/ui/core/mvc/Controller",
   "sap/m/MessageToast",
], function (Controller, MessageToast) {
   "use strict";
   return Controller.extend("sap.ui.demo.wt.controller.App", {

    	onOpenDialog : function () {
			this.getOwnerComponent().openHelloDialog();
		},

        // MenuItemEvent controlering
        onInit: function(){
            this._menus = {}
            var that=this;
            that.getView().byId('dashboard').getParent().setBusy(true);
            $.get( "/api/main_html", function( data ) {
                    that.getView().byId('dashboard').setContent(data.html);
                    that.getView().byId('dashboard').getParent().setBusy(false);
                });
            // highlights first item in menu if selected with Keyboard
//			this.byId("openMenu").attachBrowserEvent("tab keyup", function(oEvent){
//				this._bKeyboard = oEvent.type == "keyup";
//			}, this);
		},

		handlePressOpenMenu: function(oEvent) {
			var oButton = oEvent.getSource();
            var menu = oButton.data('menu');
            var parent = oButton.getParent();
            var target = oButton;
            var me = this;
            var fnOpenMenu;
			// create menu only once
			if (!this._menus[menu]) {
				this._menus[menu] = sap.ui.xmlfragment(
					"sap.ui.lino.menu." + menu,
					this
				);
				this.getView().addDependent(this._menus[menu]);
			}
            if (parent._getPopover().isOpen()){
                target=parent._getOverflowButton(); }

            var eDock = sap.ui.core.Popup.Dock;
            var openMenu = function() {me._menus[menu].open(me._bKeyboard, oButton, eDock.BeginTop, eDock.BeginBottom, target);}

            fnOpenMenu = function(oEvent) {
                oEvent.getSource().detachAfterClose(fnOpenMenu);
                setTimeout(openMenu,30);
              };
            if (target === oButton){
                openMenu();}
                else{
                    parent._getPopover().attachAfterClose(fnOpenMenu);
                    parent._getPopover().oPopup.setDurations("fast",0); // Make close animation quick
                    parent._getPopover().oPopup.setFollowOf(false) // Prevent focus switch and auto-closing of popover
                }

		},

		handleMenuItemPress: function(oEvent) {
		    var oButton = oEvent.getSource();
            var actor_id = oButton.data('actor_id');
            var action_name = oButton.data('action_name');
			var msg = "'" + oEvent.getParameter("item").getText() + actor_id +":" + action_name + "' pressed";
			MessageToast.show(msg);
			var vp = this.getView().byId('viewport')
			var content = sap.ui.getCore().byId(actor_id)
			if (content===undefined){
                content = new sap.ui.xmlview({id: actor_id,
                                    viewName : "sap.ui.lino." + action_name + "." + actor_id});

                var p = new sap.m.Page({
                    showHeader:true,
                    showNavButton:true,
                    content: content,
                    });
                p.attachNavButtonPress(null, function(oEvent){
                    vp.back();
                })

			    vp.addPage(p);
			    vp.to(p);
			    }
			else{
			    vp.to(content.getParent())
			    }


		},

		onBackPress: function(oEvent){
		    var vp = this.getView().byId('viewport')
			vp.back()
		},

   });
});