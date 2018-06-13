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
], function (baseController,JSONModel, Menu, MenuItem, MessageToast, DateFormat,Button,Dialog,Text) {
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


        initSampleDataModel: function () {
            var oModel = new JSONModel();

            var oDateFormat = DateFormat.getDateInstance({source: {pattern: "timestamp"}, pattern: "dd/MM/yyyy"});

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
            console.log(this.count++)

            return oModel;
        },

        onPressAction: function (oEvent) {
            var button = oEvent.getSource();
            var oView = this.getView();
            var action_name = button.data('action_name');
            var action_url = button.data('action_url');
            var action_method = button.data('action_method');
            var msg = action_name + "' pressed";
            // action_url = 'tickets/Tickets/';
            var url = '/api/' + action_url  + this._PK;
            MessageToast.show(msg);
            jQuery.ajax({
              url:url,
              type: action_method,
              data: jQuery.param({an: action_name}),
              success: function(data){
                  if (data && data['success'] && data['xcallback'] !== undefined){
                    var  xcallback = data['xcallback'];
                    /* TODO: Refactor this indo it's own view where you use data binding for the message and callback_ID
                    *      We will be doing such things for other actions (Ones that require parameters)
                    *      it will be a good exercise.and we might need this exact same thing with other events.
                           For example asking if you want to save unsaved data when leaving a page.
                    */
                    var dialog = new Dialog({
                        title: xcallback['title'],
                        type: 'Message',
                        content: new Text({ text: data['message']}),
                        beginButton: new Button({
                            text: xcallback['buttons']['yes'],
                            press: function () {
                                MessageToast.show('Yes pressed!');
                                jQuery.ajax({
                                    url:'/callbacks/'+ xcallback['id'] +'/yes',
                                    type: 'GET',
                                    success: function(data){
                                      MessageToast.show(data['message']);
                                    },
                                    error: function(e){
                                          MessageToast.show("error: "+e);
                                      }
                                    });
                                dialog.close();
                            }
                        }),
                        endButton: new Button({
                            text:  xcallback['buttons']['no'],
                            press: function () {
                                dialog.close();
                            }
                        }),
                        afterClose: function() {
                            dialog.destroy();
                        }
                    });

                    dialog.open();
                  }
                  MessageToast.show(data['message']);
              },
              error: function(e){
                  MessageToast.show("error: "+e);
              }
            });
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
        },

    });

});
