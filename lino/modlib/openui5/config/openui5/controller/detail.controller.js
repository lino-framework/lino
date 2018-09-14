sap.ui.define([
    "lino/controller/baseController",
    "sap/ui/model/json/JSONModel",
    "sap/ui/unified/Menu",
    "sap/ui/unified/MenuItem",
    "sap/m/MessageToast",
    "sap/ui/core/format/DateFormat",
    'sap/m/Button',
    'sap/m/Dialog',
    'sap/m/Text'
], function (baseController, JSONModel, Menu, MenuItem, MessageToast, DateFormat, Button, Dialog, Text) {
    "use strict";

    return baseController.extend("lino.controller.detail", {

        onInit: function () {
            var oView = this.getView();
            this.page_no = 0;
            this.page_limit = this.visibleRowCount;
            this.pv = []; // unused,
            this._PK = null;
            this._actor_id = this.getView().byId("MAIN_PAGE").data("actor_id");

            var oRouter = this.getRouter();
            oRouter.getRoute("detail." + this._actor_id).attachMatched(this._onRouteMatched, this);
        },


        _onRouteMatched: function (oEvent) {
            var oArgs, oView;
            oArgs = oEvent.getParameter("arguments");
            oView = this.getView();

            this.load_record(oArgs.record_id);

        },

        /**
         *  Used fot ajax action requests.
         */
        getSelectedRows: function (oEvent) {
            return this._PK
        },

        /**
         * Load data for a current object.
         * @public
         * @returns {sap.ui.model.json.JSONModel}
         */
        initSampleDataModel: function () {
            var oModel = new JSONModel();

            // var oDateFormat = DateFormat.getDateInstance({source: {pattern: "timestamp"}, pattern: "dd/MM/yyyy"});

            jQuery.ajax(this.getView().byId("MAIN_PAGE").data("url"), {
                dataType: "json",
                data: {limit: 15, fmt: 'json', an: "detail"},
                success: function (oData) {
                    oModel.setData(oData);
                },
                error: function () {
                    jQuery.sap.log.error("failed to load json");
                }
            });
            return oModel;
        },


        open_window_action: function (action, options, history) {
            this.getRouter().navTo(action,
                options, history);
        },

        /***
         * Close YesNoDialog
         */
        onNoDialog: function () {
            var dialog = this.getParent();
            dialog.close();
        },

        getNavport: function () {
            var vp = sap.ui.getCore().byId("__component0---MAIN_VIEW").byId('viewport');
            return vp
        },


        load_record: function (record_id) {
            var oModel = new JSONModel();
            var oView = this.getView();
            this._PK = record_id;
            MessageToast.show("Going to load item with PK of" + record_id);
            oView.setBusy(true);
            jQuery.ajax(oView.byId("MAIN_PAGE").data("url") + record_id, {
                dataType: "json",
                data: {
                    fmt: 'json',
                    an: 'detail'
                },
                success: function (oData) {
                    oModel.setData(oData);
                    oView.setModel(oModel, "record");
                    oView.setBusy(false);
                },
                error: function () {
                    jQuery.sap.log.error("failed to load json");
                }
            });
        },

        onLoaditems: function (oEvent) {
            console.log("loaditems");
        }

    });

});
