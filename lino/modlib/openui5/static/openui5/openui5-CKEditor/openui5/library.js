/*!
 * ${copyright}
 */

/**
 * Initialization Code and shared classes of library openui5.
 */
sap.ui.define([
	'jquery.sap.global',
	'sap/ui/core/library' // library dependency
	],  function(jQuery, library) {

		"use strict";

		/**
		 * Suite controls library.
		 *
		 * @namespace
		 * @name it.designfuture.qrcode
		 * @author Emanuele Ricci <stermi@gmail.com>
		 * @version ${version}
		 * @public
		 */

		// delegate further initialization of this library to the Core
		sap.ui.getCore().initLibrary({
			name : "openui5",
			noLibraryCSS: true,
			version: "1",
			dependencies : ["sap.ui.core", "sap.m"],
			types: [],
			interfaces: [],
			controls: [
				"openui5.CKEditor"
			],
			elements: []
		});

		return openui5;

}, /* bExport= */ false);