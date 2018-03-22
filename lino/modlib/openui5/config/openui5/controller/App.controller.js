sap.ui.define([
   "sap/ui/core/mvc/Controller",
   "sap/m/MessageToast",
   "sap/ui/model/json/JSONModel",
], function (Controller, MessageToast, JSONModel) {
   "use strict";
   return Controller.extend("lino.controller.App", {

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
					"lino.menu." + menu,
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
			var content = sap.ui.getCore().byId("grid." + actor_id)
			if (content===undefined){
                content = new sap.ui.xmlview({id: "grid." + actor_id,
                                    viewName : "lino." + action_name + "." + actor_id});

                var p = content /*new sap.m.Page({
                    showHeader:true,
                    showNavButton:true,
                    content: content,
                    });*/
                this.getView().addDependent(p)
//                this.getView().addDependent(content) // Unwanted, causes content not to render, parent object should be dependent,
                /*p.attachNavButtonPress(null, function(oEvent){
                    vp.back();
                })*/

			    vp.addPage(p);
			    vp.to(p);
			    }
			else{ vp.to(content/*.getParent()*/);}
		},

		onBackPress: function(oEvent){
		    var vp = this.getView().byId('viewport')
			vp.back()
		},

        onSignInButtonPress: function(oEvent){
            var oView = this.getView();
            var oButton = oEvent.getSource();
            var oDialog = oView.byId("dialog");
                     // create dialog lazily
             if (!oDialog) {
                // create dialog via fragment factory
                var form_data = {username:"", password:""}
                var oModel = new JSONModel(form_data);
                this.getView().setModel(oModel, "form_data");
                oDialog = sap.ui.xmlfragment(oView.getId(), "lino.dialog.SignInActionFormPanel", this);
                oView.addDependent(oDialog);
             }
             oDialog.open();

        },

        onCloseDialog: function(oEvent){
            var oDialog = this.getView().byId("dialog");
            oDialog.close()
        },

        onOkDialog: function(oEvent){
            var oModel = this.getView().getModel("form_data");
//            oModel.refresh(true) // Goes from data -> view only
            $.post( "/auth",oModel.oData).
                done( function( data ) {
                    document.location = '/'; // Might work? Untested, might add refresh()
                    }).
                fail(
                    function(xhr, textStatus, errorThrown){
                    MessageToast.show("Unable to log in as " + oModel.oData.username);
                    });
        },

        onSignOutButtonPress: function(oEvent){
            var oButton = oEvent.getSource();
            $.get( "/auth?an=logout", function( data ) {
                // Works, but might not be best method, the return should give a url to redirect to,
                document.location = '/';
            });
        },



   });
});