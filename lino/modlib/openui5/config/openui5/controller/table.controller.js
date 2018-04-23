sap.ui.define([
   "lino/controller/baseController",
	"sap/ui/model/json/JSONModel",
	"sap/ui/unified/Menu",
	"sap/ui/unified/MenuItem",
	"sap/m/MessageToast",
	"sap/ui/core/format/DateFormat"
], function(baseController, JSONModel, Menu, MenuItem, MessageToast, DateFormat) {
	"use strict";

	return baseController.extend("lino.controller.table", {

        getParentView: function(){
            var v = this.getView()
            while (v && v.getParent) {
                v = v.getParent();
                if (v instanceof sap.ui.core.mvc.View){
//                    console.log(v.getMetadata()); //you have found the view
                    return v
                    break;
                    }
                }
            },

		onInit : function () {
			var oView = this.getView();
			var oMainTable = this.getView().byId("MAIN_TABLE");
            this._table = oView.byId("MAIN_TABLE")
			this.page_no = 0;
            this.page_limit = this.visibleRowCount;
            this.pv = []; // unused,
            this._PK = oMainTable.data("PK");
            this._actor_id = oMainTable.data("actor_id");
            this._content_type = oMainTable.data("content_type"); // null or int
            this._is_slave = oMainTable.data("is_slave"); // null or int
            this._table.setBusy(true);
            if (this.count == undefined) this.count = 0;
			// set explored app's demo model on this sample
			oView.setModel(new JSONModel({
//				showVisibilityMenuEntry: false,
				showFreezeMenuEntry: false,
				enableCellFilter: false
			}), "ui");
		},

        onAfterRendering : function(oEvent){
            console.log("loading data");
    		var oJSONModel = this.initSampleDataModel();
			this.getView().setModel(oJSONModel);
        },

        beforeExit: function(){console.log("beforeExit")},

		initSampleDataModel : function() {
		    var me = this
			this._table.setBusy(true);
			var oModel = new JSONModel();
            var data = {limit:15, fmt:'json', mt:this._content_type }
			var oDateFormat = DateFormat.getDateInstance({source: {pattern: "timestamp"}, pattern: "dd/MM/yyyy"});
            if (this._is_slave){
                data.mk = this.getParentView().getController()._PK
            }

			jQuery.ajax(this.getView().byId("MAIN_TABLE").data("url"), {
				dataType: "json",
				data:data,
				success: function (oData) {
					oModel.setData(oData);
				    me._table.setBusy(false)
				},
				error: function () {
					jQuery.sap.log.error("failed to load json");
				}
			});
			console.log(this.count++)

			return oModel;
		},

		getNavport: function(){
		    var vp = sap.ui.getCore().byId("__component0---MAIN_VIEW").byId('viewport');
            return vp
		},


		onRowNavPress : function(oEvent) {
		    // todo refactor into open_window method of app controller
		    var oRow = oEvent.getParameter("row");
            var oBindingContext = oRow.getBindingContext();
			var oItem = oEvent.getParameter("item");
			var sPk = this.getView().getModel().getProperty(this._PK, oBindingContext);
			console.log("Opening detail for: " +  this._actor_id  + "/" + sPk);

            var msg = "'" + oEvent.getParameter("item").getText() + this._actor_id +":" + "detail" + "' pressed";
			MessageToast.show(msg);

			this.routeTo("detail", this._actor_id,{"sPK":sPk});

        },


		onColumnSelect : function (oEvent) {
			var oCurrentColumn = oEvent.getParameter("column");
			var oImageColumn = this.getView().byId("image");
			if (oCurrentColumn === oImageColumn) {
				MessageToast.show("Column header " + oCurrentColumn.getLabel().getText() + " pressed.");
			}
		},

		onColumnMenuOpen: function (oEvent) {
			var oCurrentColumn = oEvent.getSource();
			var oImageColumn = this.getView().byId("image");
			if (oCurrentColumn != oImageColumn) {
				return;
			}

			//Just skip opening the column Menu on column "Image"
			oEvent.preventDefault();
		},

		onProductIdCellContextMenu : function (oEvent) {
			if (sap.ui.Device.support.touch) {
				return; //Do not use context menus on touch devices
			}

			if (oEvent.getParameter("columnId") != this.getView().createId("productId")) {
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
				select: function() {
					MessageToast.show("Context action triggered on Column 'Product ID' on id '" + oRowContext.getProperty("ProductId") + "'.");
				}
			}));

			//Open the menu on the cell
			var oCellDomRef = oEvent.getParameter("cellDomRef");
			var eDock = sap.ui.core.Popup.Dock;
			this._oIdContextMenu.open(false, oCellDomRef, eDock.BeginTop, eDock.BeginBottom, oCellDomRef, "none none");
		},

		onQuantityCustomItemSelect : function(oEvent) {
			MessageToast.show("Some custom action triggered on column 'Quantity'.");
		},

		onQuantitySort : function(oEvent) {
			var bAdd = oEvent.getParameter("ctrlKey") === true;
			var oColumn = this.getView().byId("quantity");
			var sOrder = oColumn.getSortOrder() == "Ascending" ? "Descending" : "Ascending";

			this.getView().byId("table").sort(oColumn, sOrder, bAdd);
		},

		showInfo : function(oEvent) {
			try {
				jQuery.sap.require("sap.ui.table.sample.TableExampleUtils");
				sap.ui.table.sample.TableExampleUtils.showInfo(jQuery.sap.getModulePath("sap.ui.table.sample.Menus", "/info.json"), oEvent.getSource());
			} catch (e) {
				// nothing
			}
		}

	});

});
