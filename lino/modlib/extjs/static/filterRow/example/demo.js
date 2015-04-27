Ext.onReady(function(){	
	var sampleGridColumns= [{
		header: 'Id',
		width:90,
		dataIndex: 'id',
		clearFilter:true//used to show clear filter icon in this column
	},{
		header: 'Title', 
		dataIndex: 'title',
		sortable: true,
		width:150,
		filterInput: new Ext.form.TextField(),
		filterOptions:[{value:'startwith', text:'Start With'},{value:'endwith', text:'End With'},{value:'contain', text:'Contain'},{value:'doesnotcontain', text:'Does Not Contain'}]
	},{
		header: 'Alias', 
		dataIndex: 'alias',
		sortable: true,
		width:230,
		filterInput: new Ext.form.TextField(),
		filterOptions:[{value:'startwith', text:'Start With'},{value:'endwith', text:'End With'},{value:'contain', text:'Contain'},{value:'doesnotcontain', text:'Does Not Contain'}]
	},{
		header: 'Created',
		width:130,
		dataIndex: 'created_date',
		filterInput: new Ext.form.DateField({format:'Y-m-d',  dataIndex:'created' /* you can pass different dataIndex for filtering into all filter inputs */}),
		filterOptions:[{value:'before', text:'Before'},{value:'after', text:'After'},{value:'contain', text:'Is'}]
	},{
		header: 'Published', 
		dataIndex: 'state',
		sortable: true,
		renderer:function(v){if(v==1){return 'Published'}else{return '<span style="color:red">UnPublished</span>'}},
		filterInput	:  new Ext.form.ComboBox({				
			displayField	: 'name',
			valueField		: 'state',
			triggerAction	: 'all',		
			typeAhead		: false,				
			mode			: 'local',
			listWidth		: 160,
			hideTrigger		: false,
			emptyText		: 'Select',
			store			:[['1','Published'],['0','UnPublished']]
		}),
		filterOptions:[{value:'equal', text:'Is'},{value:'notequal', text:'Not'}]
	}];
	
	var sampleGridReader = new Ext.data.JsonReader({
			totalProperty: 'total',
			successProperty: 'success',
			idProperty: 'id',
			root: 'data'
		},[
			{name: 'id'},
			{name: 'title'},
			{name: 'created'},
			{name: 'state'},
			{name: 'alias'},
			{name: 'created_date'}			
	]);
	
	var filterRow = new Ext.ux.grid.FilterRow();
	
	// Typical Store collecting the Proxy, Reader and Writer together.
	var sampleGridStore = new Ext.data.Store({
		reader		: sampleGridReader,
		autoLoad	: true,	
		url			: scriptUrl+'ux/filterRow/example/index.php'
	});
	
	// create the Grid
	var grid = new Ext.grid.GridPanel({
		store: sampleGridStore,
		renderTo:'filterRowGridExample',
		columns: sampleGridColumns,
		plugins: [filterRow],
		stripeRows: true,
		height: 350,
		title: 'Grid with Filters'
	});

});