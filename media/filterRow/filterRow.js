/****************************************************
 * Filter row class.
 * 
 * Author: Surinder singh http://www.sencha.com/forum/member.php?75710-Surinder-singh, surinder83singh@gmail.com
 * Demo Page : http://www.developerextensions.com/index.php?option=com_extensiondemo&view=extensiondemo&layout=ext&extension=Ext-FilterRow_1.2&Itemid=482
 * @class Ext.ux.grid.FilterRow
 * Notes: Removed a columns resizable bug tested/told by gang.alecs@gmail.com
 ************************************************/
Ext.namespace('Ext.ux.grid');
Ext.ux.grid.FilterRow = function(config) {
    Ext.apply(this, config);
    this.addEvents(
        "change"
    );
    Ext.ux.grid.FilterRow.superclass.constructor.call(this);
};

Ext.extend(Ext.ux.grid.FilterRow, Ext.util.Observable, {	
	init: function(grid) {
		this.grid = grid;
		this.grid.addClass('filter-row');
		var view = grid.getView();
		var headerTpl = new Ext.Template(
			'<table border="0" cellspacing="0" cellpadding="0" style="{tstyle}">',
				'<thead><tr class="x-grid3-hd-row  ">{cells}</tr></thead>',
			"</table>"
		);
		
        Ext.applyIf(view, { templates: {} });
		view.templates.header = headerTpl;
		view.templates.hcell = new Ext.Template(
			'<td class="x-grid3-hd x-grid3-cell x-grid3-td-{id} {css}" style="{style}">',
				'<div {tooltip} {attr} class="x-grid3-hd-inner x-grid3-hd-{id}" unselectable="on" style="{istyle}">',
					this.grid.enableHdMenu ? '<a class="x-grid3-hd-btn" href="#"></a>' : '',
					'{value}',
					'<div class="x-small-editor filterInput" id="'+grid.id+'-filter-{id}"></div>',
					'<img class="x-grid3-sort-icon" src="', Ext.BLANK_IMAGE_URL, '" />',
				'</div>',
			'</td>'
       	);

        grid.on('resize', this.syncFields, this);
        grid.on('columnresize', this.syncFields, this);
        grid.on('render', this.renderFields, this);
		grid.on('render', this.renderFilterMenu, this);
		// private
		var FilterRow = this;
		view.updateHeaders = function(){
			this.innerHd.firstChild.innerHTML = this.renderHeaders();
			this.innerHd.firstChild.style.width = this.getOffsetWidth();
			this.innerHd.firstChild.firstChild.style.width = this.getTotalWidth();
			FilterRow.renderFields();
		};
        Ext.apply(grid, {
            enableColumnHide_: false,
            enableColumnMove: true
        });
		this.on('change', function(filterRow){
			grid.store.baseParams ={};
			for(var i in filterRow.data){
				grid.store.baseParams['filter['+i+']'] = filterRow.data[i];
			}
			grid.store.reload();
		}, grid);
    },
	filterOptionClick:function(filterMenu){		
		filterMenu.filterInput.filterOption = filterMenu.value;
		if( filterMenu.value=='NoFilter' ){
			filterMenu.filterInput.setValue('');
		}
		this.onChange();
	},
	beforeFilterMenuShow:function(){
		var grid = this.grid;
		var view = grid.getView();
		
		var cm = view.cm,  colCount = cm.getColumnCount();
		
        this.filterMenu.removeAll();
		var filterOptions 	= cm.config[view.hdCtxIndex].filterOptions;
		var filterInput 	= cm.config[view.hdCtxIndex].filterInput;
		
		this.filterMenu.add(new Ext.menu.CheckItem({
			itemId:"filteroption-clear",
			text: 'No Filter',
			value: 'NoFilter',
			cls: "filteroption-nofilter",
			filterInput:filterInput,
			checked:(filterInput.filterOption=='NoFilter')
		}));
				
		if(filterOptions && Ext.isArray(filterOptions)){			
			for(var i = 0; i < filterOptions.length; i++){				
				this.filterMenu.add(new Ext.menu.CheckItem({
                    itemId:"filteroption-"+filterOptions[i].value,
					text: filterOptions[i].text,
					value: filterOptions[i].value,
					cls: "filteroption-"+filterOptions[i].cls,
					filterInput:filterInput,
					checked:(filterInput.filterOption==filterOptions[i].value)
                }));
			}
		}
	},
	setFilterMenu:function(){
		var grid = this.grid;
		var view = grid.getView();
		var filterInput = view.cm.config[view.hdCtxIndex].filterInput;
		if(filterInput){
			view.hmenu.items.get("Filter").setDisabled( false );
		}else{
			view.hmenu.items.get("Filter").setDisabled( true );
		}
	},
	
	renderFilterMenu:function(){
		var grid = this.grid;
		var view = grid.getView();
		this.filterMenu = new Ext.menu.Menu({id:grid.id + "-filter-menu"});
		this.filterMenu.on({
			scope: this,
			beforeshow: this.beforeFilterMenuShow,
			itemclick: this.filterOptionClick
		});
		
		view.hmenu.on({
			scope: this,
			beforeshow: this.setFilterMenu
		});
		
		view.hmenu.add('-', {
			itemId:"Filter",
			hideOnClick: false,
			text:'Filter',
			menu: this.filterMenu,
			iconCls: 'x-filter-icon'
		});
	},
	
    renderFields: function() {
		//alert('renderFields')
        var grid = this.grid;
		var filterRow = this;
        var cm = grid.getColumnModel();
        var cols = cm.config;
        var gridId = grid.id;
        Ext.each(cols, function(col) {
            if (!col.hidden) {
                var filterDivId = gridId + "-filter-" + col.id;
                var editor 		= col.filterInput;
				var clearFilter = col.clearFilter;
                if (editor) {
					if(Ext.isIE){
						col.filterInput = editor = editor.cloneConfig({value:editor.getValue()});
					}
                    if (editor.getXType() == 'combo') {
                        editor.on('select', this.resetNoFilterOption, this, editor);
                    } else {
                        editor.on('change', this.resetNoFilterOption, this, editor);
                    }
					new Ext.Panel({border:false, layout:'fit', items:editor, renderTo:filterDivId});
                }else if(clearFilter) {
					/*var clearFilter = new Ext.form.DisplayField({						 
							  text:'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', 									  
							  scope:filterRow,
							  tooltip:'Clear Filters',
							  tooltipType:'qtip',
							  value:'xxxxx',
							  handler: function(){
								this.clearAllFilters();
								this.grid.getStore().baseParams = {};
								this.grid.getStore().reload();
							  }
						 });*/
					Ext.get(filterDivId).addClass('ClearFilter');
					Ext.EventManager.addListener( filterDivId, 'click', function(){																				
						this.clearAllFilters();
						this.grid.getStore().baseParams = {};
						this.grid.getStore().reload();									
					}, filterRow );
					/*new Ext.Panel({
					  border:false, 
					  layout:'fit',
					  cls:'ClearFilter',
					  items_:clearFilter,
					  html:'xxxx',
					  renderTo:filterDivId
					});*/
				}
            }
        }, this);
    },
    
     clearAllFilters: function() {
        var grid 	= this.grid;
        var cm 		= grid.getColumnModel();
        var cols 	= cm.config;       
        var data 	= {};
		var dataIndex = '';
        Ext.each(cols, function(col) {
			//alert(col.header);
            if (!col.hidden) {
                var editor = col.filterInput;
                if (editor) {	
                	editor.setValue('');
					dataIndex = editor.dataIndex?editor.dataIndex:col.dataIndex;
                    data[dataIndex] 				= editor.getValue();
					data[dataIndex+'_filterOption'] = editor.filterOption;
                }
            }
        });
        return data;
    },

    getData: function() {
        var grid 	= this.grid;
        var cm 		= grid.getColumnModel();
        var cols 	= cm.config;       
        var data 	= {};
		var value	= '';
		var dataIndex = '';
        Ext.each(cols, function(col) {
			//alert(col.header+'::'+col.hidden)
            if (!col.hidden) {
                var editor = col.filterInput;				
                if (editor) {
					value = editor.getValue();
					if(editor.getXType()=='datefield' && value.format){
						value = value.format(editor.format);
					}
					dataIndex = editor.dataIndex?editor.dataIndex:col.dataIndex;
                    data[dataIndex] 				= value;
					data[dataIndex+'_filterOption'] = editor.filterOption;
                }
            }
        });
        return data;
    },
	resetNoFilterOption: function(editor){
		if(editor.filterOption=='NoFilter'){//if filter value have been changed , but "NoFilter" menu is still selected then reset it 
			editor.filterOption = '';
		}
        this.onChange();
    },
    onChange: function(){	
        this.fireEvent("change", { filter: this, data: this.getData() });
    },

    clearFilters: function(){
        this.fireEvent("change", { filter: this, data: {} });
    },

    syncFields: function(){
		//return;
        var grid 	= this.grid;
        var cm 		= grid.getColumnModel();
        var cols 	= cm.config;
        Ext.each(cols, function(col){
            if (!col.hidden) {              
                var editor = col.filterInput; 
                if (editor) {
                    editor.setSize(col.width - 18);
                }else if(col.clearFilter && col.clearFilter.setSize){
					col.clearFilter.setSize(col.width - 10);
				}
            }
        });
    }
});
