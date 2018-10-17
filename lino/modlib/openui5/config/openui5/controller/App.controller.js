sap.ui.define([
    "lino/controller/baseController",
    "sap/m/MessageToast",
    "sap/ui/model/json/JSONModel",
    "sap/ui/Device",
], function (baseController, MessageToast, JSONModel, Device) {
    "use strict";
    return baseController.extend("lino.controller.App", {
        onOpenDialog: function () {
            this.getOwnerComponent().openHelloDialog();
        },

        // MenuItemEvent controlering
        onInit: function () {
            this.initRouter();
            this._menus = {};
            var that = this;
            this._selectedDevice = 'desktop';
            if (Device.system.desktop === true) {
                this._connectedDevice = 'desktop';
            }
            else if (Device.system.phone === true) {
                this._connectedDevice = 'phone';
            }
            else if (Device.system.tablet === true) {
                this._connectedDevice = 'tablet';
            }

//            that.getView().byId('dashboard').getParent().setBusy(true);
//            $.get( "/api/main_html", function( data ) {
//                    that.getView().byId('dashboard').setContent(data.html);
//                    that.getView().byId('dashboard').getParent().setBusy(false);
//                });
            // highlights first item in menu if selected with Keyboard
//			this.byId("openMenu").attachBrowserEvent("tab keyup", function(oEvent){
//				this._bKeyboard = oEvent.type == "keyup";
//			}, this);
        },

        /**
         * Convenience method for getting the router for navigation.
         * @public
         * @returns {sap.ui.core.routing.Router or sap.m.routing.Router}
         */
        initRouter: function () {
            var oRouter = sap.ui.core.UIComponent.getRouterFor(this);
                oRouter.attachRouteMatched(this.routeMatched, this);
            return oRouter;
        },

        routeMatched: function(oEvent){
                var oParameters = oEvent.getParameters();
                    this.routeName = oParameters.name; // Yay! Our route name!
        },

        handlePressOpenMenu: function (oEvent) {
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
            if (parent._getPopover().isOpen()) {
                target = parent._getOverflowButton();
            }

            var eDock = sap.ui.core.Popup.Dock;
            var openMenu = function () {
                me._menus[menu].open(me._bKeyboard, oButton, eDock.BeginTop, eDock.BeginBottom, target);
            };

            fnOpenMenu = function (oEvent) {
                oEvent.getSource().detachAfterClose(fnOpenMenu);
                setTimeout(openMenu, 30);
            };
            if (target === oButton) {
                openMenu();
            }
            else {
                parent._getPopover().attachAfterClose(fnOpenMenu);
                parent._getPopover().oPopup.setDurations("fast", 0); // Make close animation quick
                parent._getPopover().oPopup.setFollowOf(false) // Prevent focus switch and auto-closing of popover
            }

        },

        handleMenuItemPress: function (oEvent) {
            var oButton = oEvent.getSource();
            var actor_id = oButton.data('actor_id');
            var action_name = oButton.data('action_name');
            var compressed_eval_js = oButton.data('eval_js');

            var s = atob(compressed_eval_js);

            var data = new Array(s.length);
            var i;
            for (i = 0; i < s.length; ++i) {
                data[i] = s.charCodeAt(i);
            }

            var inflate = new Zlib.Inflate(data);
            var decompress = inflate.decompress();
            var eval_js = new TextDecoder("utf-8").decode(decompress);

            var msg = "'" + oEvent.getParameter("item").getText() + actor_id + ":" + action_name + "' pressed";
            MessageToast.show(msg);
            eval(eval_js);
            // this.routeTo(action_name, actor_id);
        },

        // Todo: move into it's on controller
        onSignInButtonPress: function (oEvent) {
            var oView = this.getView();
            var oButton = oEvent.getSource();
            var oDialog = oView.byId("dialog");
            // create dialog lazily
            if (!oDialog) {
                // create dialog via fragment factory
                var form_data = {username: "", password: ""};
                var oModel = new JSONModel(form_data);
                this.getView().setModel(oModel, "form_data");
                oDialog = sap.ui.xmlfragment(oView.getId(), "lino.dialog.SignInActionFormPanel", this);
                oView.addDependent(oDialog);
            }
            oDialog.open();

        },
        /**
         * Change the device type (Desktop or Mobile)
         * @param oEvent
         */
        onChangeDeviceTypeButtonPress: function (oEvent) {
            var oView = this.getView();
            var oButton = oEvent.getSource();
            var newdevice = 'phone';
            if (this._selectedDevice === 'phone') {
                newdevice = 'desktop';
            }
            this._selectedDevice = newdevice;
            this.routeToAction(this.routeName,{}, true /*no history*/);
            // this.reload.apply(this, {'dt': newdevice});
        },

        onCloseDialog: function (oEvent) {
            var oDialog = this.getView().byId("dialog");
            oDialog.close();
        },

        onOkSignInDialog: function (oEvent) {
            var oModel = this.getView().getModel("form_data");
//            oModel.refresh(true) // Goes from data -> view only
            $.post("/auth", oModel.oData).done(function (data) {
                document.location = '/'; // Might work? Untested, might add refresh()
            }).fail(
                function (xhr, textStatus, errorThrown) {
                    MessageToast.show("Unable to log in as " + oModel.oData.username);
                });
            // seems that submitting the form as a normal form works, but the error handling is poor.
//            $("#__component0---MAIN_VIEW--authForm").submit();
        },

        onSignOutButtonPress: function (oEvent) {
            var oButton = oEvent.getSource();
            $.get("/auth?an=logout", function (data) {
                // Works, but might not be best method, the return should give a url to redirect to,
                document.location = '/';
            });
        },

        getNavport: function () {
            var vp = sap.ui.getCore().byId("__component0---MAIN_VIEW").byId('viewport');
            return vp
        }


    });
});