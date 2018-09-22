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
            this._content_type = this.getView().byId("MAIN_PAGE").data("content_type");

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
         *  Used for ajax action requests.
         */
        getSelectedRows: function (oEvent) {
            return this._PK
        },

        afterRecordDelete: function (data) {
            var oNavInfo = this.getView().oModels.record.getData().navinfo;
            var record_id = null;
            if (oNavInfo.next) {
                record_id = oNavInfo.next;
            }
            else if (oNavInfo.prev) {
                record_id = oNavInfo.next;
            }
            //todo Direct to grid if record_id === null
            var action = (record_id === null) ? "grid" : "detail";
            this.routeTo(action,
                data['detail_handler_name'].replace('.detail', ''),
                {record_id: record_id});
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

        /**

         * @returns record data
         */
        getRecordData: function () {
            let send_data = {}
            let data = this.getModel("record").getProperty("/data");
            console.log(data);
            let fields = this.getView().byId("MAIN_PAGE").data("save_fields").split(" ");
            let disabled = Object.keys(data.disabled_fields);
            fields.map(f => {
                if (!disabled.includes(f)) {
                    send_data[f] = data[f];
                    let fH = f + "Hidden";
                    if (data[fH]) {
                        send_data[fH] = data[fH];
                    }
                }
            });
            console.log(send_data);
            return send_data;
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

        refresh: function () {
            this.load_record(this._PK);
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
                    an: 'detail',
                    sr: record_id, // not needed, but have it anyway
                    rp: oView.getId(),
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
