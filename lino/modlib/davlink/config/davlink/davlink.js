/*
 Copyright 2009-2014 Luc Saffre
 License: BSD (see file COPYING for details)
*/

Lino.davlink_open = function(webdavURL) {
  /* Calls lino.applets.davlink.DavLink.open()
  */
  //~ console.log('Going to call document.applets.DavLink.open(',webdavURL,')');
  var rv = document.applets.DavLink.open(webdavURL);
  if (rv) window.alert(rv);
}

Lino.davlink_reset = function() {
  var rv = document.applets.DavLink.generate_default_prefs();
  if (rv) window.alert(rv);
}

