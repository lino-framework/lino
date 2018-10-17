sap.ui.define([
    "lino/controller/baseController",
    "sap/ui/model/json/JSONModel",
    "sap/ui/unified/Menu",
    "sap/ui/unified/MenuItem",
    "sap/m/MessageToast",
    "sap/ui/core/format/DateFormat",
    "sap/ui/model/Filter",
    "sap/ui/model/FilterOperator"
], function (baseController, JSONModel, Menu, MenuItem, MessageToast, DateFormat, Filter, FilterOperator) {
    "use strict";

    return baseController.extend("lino.controller.table", {

        log_rows: function (sMsg) {
            console.log(sMsg,
                this._table.getVisibleRowCount())
        },

        onInit: function () {
            var me = this;
            var oView = this.getView();
            var oMainTable = this.getView().byId("MAIN_TABLE");
            this._is_rendered = false;
            this._table = oMainTable;
            this.page_limit = this.visibleRowCount;
            this._PK = oMainTable.data("PK");
            this._actor_id = oMainTable.data("actor_id");
            this._content_type = oMainTable.data("mt"); // null or int
            this._MT = oMainTable.data("mt"); // null or int

            this._is_slave = oMainTable.data("is_slave"); // null or int

            var oRouter = this.getRouter();

			oRouter.getRoute("grid."+ this._actor_id).attachMatched(this._onRouteMatched, this);


            this._table.setBusy(true);

            this._table.addEventDelegate({
                afterRendering: function () {
                    me.log_rows("tableAfterRender");
                }
            });

            // override after rendering event handler to find out how many rows are rendered and how many should be per page
            // Is run twice on inital loading of view, second time has the correct values
            // view after render event is fired after first firing of this event, but before second firing of table event
            // this._table.onAfterRendering = function () {
            //     sap.ui.table.Table.prototype.onAfterRendering.apply(this, arguments);
            //     me.reload.apply(me, arguments);
            // };

            // Set values for table conf
            oView.setModel(new JSONModel({
//				showVisibilityMenuEntry: false,
                showFreezeMenuEntry: false,
                enableCellFilter: false
            }), "ui");

            // Set meta data for table/actor
            oView.setModel(new JSONModel({
                page: 1,
                page_old: 1, // Todo: implement correctly for setting on invalid page number value
                page_total: "N/A"
            }), "meta");

            // Param values (unused ATM)
            oView.setModel(new JSONModel({}), "pv");


        },
        /***
         * Read query passed with the route.
         * @param oEvent
         * @private
         */
        _onRouteMatched : function (oEvent) {
			var oArgs, oView;

			oArgs = oEvent.getParameter("arguments");
            if (oArgs["?query"] !== undefined){
                this._query = oArgs["?query"];
            }
		},

        onAfterRendering: function (oEvent) {
            // to prevent second loading of data on init,
            //this._is_rendered = true;
            this.refresh()
        },

        refresh: Lino.debounce(
            function (oEvent) {
            // Fetches the page that's set in {meta>page} or if that's not a valid page page_old
            // Called on page-resize and load, after the table has rendered and knows it's row count.
            // oEvent is from table afterendering event
            console.log("...Reloading...");
            this._table.setBusy(true);
            this.page_limit = this._table.getVisibleRowCount();
            if (true) {
                var oJSONModel = this.initSampleDataModel();
                this.getView().setModel(oJSONModel);
            }

        },500),

        getSelectedRows: function (oEvent) {
            var me = this;
            var selections = this._table.getSelectedIndices();
            return selections.map(
                function (index) {
                    var model = me.getView().getModel();
                    return model.getProperty(me._PK, model.mContexts["/rows/"+index] );
                }).filter(num => num != null );
        },

        afterRecordDelete: function(data) {
            this.refresh();
        },

//        beforeExit: function(){console.log("beforeExit")},


        initSampleDataModel: function () {
            var me = this;
            this._table.setBusy(true);
            var oRecordDataModel = new JSONModel();
            var oModel = me.getView().getModel("meta");
            var data = {
                limit: this.page_limit,
                fmt: 'json',
                mt: this._content_type,
                start: (oModel.getProperty("/page") - 1) * this.page_limit,
                rp: this.getView().getId()
            };
            if (this._query !==  undefined){
                jQuery.extend(data, this._query);
            }
            var oDateFormat = DateFormat.getDateInstance({source: {pattern: "timestamp"}, pattern: "dd/MM/yyyy"});
            if (this._is_slave) {
                data.mk = this.getParentView().getController()._PK;
            }

            jQuery.ajax(this.getView().byId("MAIN_TABLE").data("url"), {
                dataType: "json",
                data: data,
                success: function (oData) {
                    var iPage = Math.ceil(oData.count / me.page_limit);
                    oModel.setProperty("/page_total", iPage);
                    oModel.setProperty("/page_old", iPage);

                    oRecordDataModel.setData(oData);
                    me._table.setBusy(false)
                },
                error: function () {
                    jQuery.sap.log.error("failed to load json");
                }
            });

            return oRecordDataModel;
        },


        onRowNavPress: function (oEvent) {
            // todo refactor into open_window method of app controller
            var oRow = oEvent.getParameter("row");
            var oBindingContext = oRow.getBindingContext();
            var oItem = oEvent.getParameter("item");
            var record_id = this.getView().getModel().getProperty(this._PK, oBindingContext);
            console.log("Opening detail for: " + this._actor_id + "/" + record_id);

            var msg = "'" + oEvent.getParameter("item").getText() + this._actor_id + ":" + "detail" + "' pressed";
            MessageToast.show(msg);

            this.routeTo("detail", this._actor_id, {"record_id": record_id});

        },


        onColumnSelect: function (oEvent) {
            var oCurrentColumn = oEvent.getParameter("column");
            var oImageColumn = this.getView().byId("image");
            if (oCurrentColumn === oImageColumn) {
                MessageToast.show("Column header " + oCurrentColumn.getLabel().getText() + " pressed.");
            }
        },

        onColumnMenuOpen: function (oEvent) {
            var oCurrentColumn = oEvent.getSource();
            var oImageColumn = this.getView().byId("image");
            if (oCurrentColumn !== oImageColumn) {
                return;
            }

            //Just skip opening the column Menu on column "Image"
            oEvent.preventDefault();
        },

        onProductIdCellContextMenu: function (oEvent) {
            if (sap.ui.Device.support.touch) {
                return; //Do not use context menus on touch devices
            }

            if (oEvent.getParameter("columnId") !== this.getView().createId("productId")) {
                return; //Custom context menu for product id column only
            }

            oEvent.preventDefault();

            var oRowContext = oEvent.getParameter("rowBindingContext");

            if (!this._oIdContextMenu) {
                this._oIdContextMenu = new Menu();
                this.getView().addDependent(this._oIdContextMenu);
            }

            this._oIdContextMenu.destroyItems();
            this._oIdContextMenu.addItem(new MenuItem({
                text: "My Custom Cell Action",
                select: function () {
                    MessageToast.show("Context action triggered on Column 'Product ID' on id '" + oRowContext.getProperty("ProductId") + "'.");
                }
            }));

            //Open the menu on the cell
            var oCellDomRef = oEvent.getParameter("cellDomRef");
            var eDock = sap.ui.core.Popup.Dock;
            this._oIdContextMenu.open(false, oCellDomRef, eDock.BeginTop, eDock.BeginBottom, oCellDomRef, "none none");
        },

        onQuantityCustomItemSelect: function (oEvent) {
            MessageToast.show("Some custom action triggered on column 'Quantity'.");
        },

        onQuantitySort: function (oEvent) {
            var bAdd = oEvent.getParameter("ctrlKey") === true;
            var oColumn = this.getView().byId("quantity");
            var sOrder = oColumn.getSortOrder() === "Ascending" ? "Descending" : "Ascending";

            this.getView().byId("table").sort(oColumn, sOrder, bAdd);
        },

        // Unused, from ui5 sample docs
        showInfo: function (oEvent) {
            try {
                jQuery.sap.require("sap.ui.table.sample.TableExampleUtils");
                sap.ui.table.sample.TableExampleUtils.showInfo(jQuery.sap.getModulePath("sap.ui.table.sample.Menus", "/info.json"), oEvent.getSource());
            } catch (e) {
                // nothing
            }
        },

        // Todo disable prev and first on first page, and next and last on last page.
        onFirstPress: function (oEvent) {
            var oModel = this.getView().getModel("meta");
            oModel.setProperty("/page", 1);
            this.refresh();
        },
        onPrevPress: function (oEvent) {
            var oModel = this.getView().getModel("meta");
            oModel.setProperty("/page", Math.max(1, oModel.getProperty("/page") - 1));
            this.refresh();
        },
        onPagerInputChange: function (oEvent) {
            var oModel = this.getView().getModel("meta");
            var sPage = +oEvent.getParameters().value; //+ converts value into int or NaN // value is same as {meta>page}
            var sOldPage = oModel.getProperty("/page_old");
            var input = oEvent.getSource();
            console.log(sPage, sOldPage, input);
            if (sPage !== sOldPage) {
                input.setValueState("None");
                MessageToast.show("Should load page:" + sPage);
                this.refresh()
            }
            else if (isNaN(sPage)) {
                input.setValueState("Error");
            }
        },
        onNextPress: function (oEvent) {
            var oModel = this.getView().getModel("meta");
            oModel.setProperty("/page", Math.min(oModel.getProperty("/page") + 1, oModel.getProperty("/page_total")))
            this.refresh();
        },
        onLastPress: function (oEvent) {
            var oModel = this.getView().getModel("meta");
            oModel.setProperty("/page", oModel.getProperty("/page_total"));
            this.refresh();
        },

        /**
         * Event handler when a table item gets pressed
         * @param {sap.ui.base.Event} oEvent the table selectionChange event
         * @public
         */
        onPress: function (oEvent) {
            // The source is the list item that got pressed
            this._showObject(oEvent.getSource());
        },
        /* =========================================================== */
        /* internal methods                                            */
        /* =========================================================== */

        /**
         * Shows the selected item on the object page
         * On phones a additional history entry is created
         * @param {sap.m.ObjectListItem} oItem selected Item
         * @private
         */
        _showObject: function (oItem) {
            this.getRouter().navTo("object", {
                objectId: oItem.getBindingContext().getProperty("ProductID")
            });
        },
        onSearch: function (oEvent) {
            if (oEvent.getParameters().refreshButtonPressed) {
                // Search field's 'refresh' button has been pressed.
                // This is visible if you select any master list item.
                // In this case no new search is triggered, we only
                // refresh the list binding.
                this.onRefresh();
            } else {
                var aTableSearchState = [];
                var sQuery = oEvent.getParameter("query");

                if (sQuery && sQuery.length > 0) {
                    aTableSearchState = [new Filter("summary", FilterOperator.Contains, sQuery)];
                }
                this._applySearch(aTableSearchState);
            }

        },
        /**
         * Internal helper method to apply both filter and search state together on the list binding
         * @param {sap.ui.model.Filter[]} aTableSearchState An array of filters for the search
         * @private
         */
        _applySearch: function (aTableSearchState) {
            var oTable = this._table,
                oViewModel = this.getModel();
            oTable.getBinding().filter(aTableSearchState);
            // changes the noDataText of the list in case there are no filter results
            // if (aTableSearchState.length !== 0) {
            // 	oViewModel.setProperty("/tableNoDataText", this.getResourceBundle().getText("worklistNoDataWithSearchText"));
            // }
        }

    });

});
