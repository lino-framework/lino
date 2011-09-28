/*

  Copyright 2011 Luc Saffre
  This file is part of the Lino project.
  Lino is free software; you can redistribute it and/or modify 
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.
  Lino is distributed in the hope that it will be useful, 
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
  GNU General Public License for more details.
  You should have received a copy of the GNU General Public License
  along with Lino; if not, see <http://www.gnu.org/licenses/>.

  Accessing the Windows Registry Using XPCOM:
  https://developer.mozilla.org/en/Accessing_the_Windows_Registry_Using_XPCOM
  
*/


function get_associated_app(extension) {
  var candidates = new Array();
  // try and find launcher on Windows
  var classInst = Components.classes["@mozilla.org/windows-registry-key;1"]
  if (classInst) {
    var wrk = classInst.createInstance(Components.interfaces.nsIWindowsRegKey);
    if (wrk) {
      wrk.open(wrk.ROOT_KEY_CLASSES_ROOT, "." + extension, wrk.ACCESS_READ);
      var n = wrk.readStringValue("");
      wrk.close();
      wrk.open(wrk.ROOT_KEY_CLASSES_ROOT, n + "\\shell\\Open\\command", wrk.ACCESS_READ);
      var cmd = wrk.readStringValue("");
      wrk.close();
      console.log(cmd);
      //~ cmd now may contain for example:
      //~ "C:\Program Files\Microsoft Office\OFFICE11\WINWORD.EXE" /n /dde
      //~ "C:\Program Files\Microsoft Office\OFFICE11\WINWORD.EXE" /n /dde
      if (cmd.charAt(0) == '"') {
          cmd = cmd.substr(1);
          cmd = cmd.substr(0,cmd.indexOf('"'));
      }
      candidates.push(cmd);
    }
  }
  if (navigator.platform.indexOf("Mac") != -1) {
      candidates.push("/Applications/NeoOffice.app");
  } else if (navigator.platform.indexOf("Linux") != -1) {
      candidates.push("/usr/bin/ooffice");
  }
  for (i = 0; i < candidates.length; i++) {
      var file = Components.classes["@mozilla.org/file/local;1"]  
                          .createInstance(Components.interfaces.nsILocalFile);  
      console.log(candidates[i]);
      try {
        file.initWithPath(candidates[i]);
        return file;
      } catch (e) {
        //~ catch and ignore any exception, e.g.
        //~ [Exception... "Component returned failure code: 0x80520001 (NS_ERROR_FILE_UNRECOGNIZED_PATH) 
        //~ [nsILocalFile.initWithPath]"  nsresult: "0x80520001 (NS_ERROR_FILE_UNRECOGNIZED_PATH)"  ]
      }
  }
}

function startfile(filename) {
  if (navigator.userAgent.indexOf('Firefox') != -1) {
    //~ console.log("It's a Firefox");
    netscape.security.PrivilegeManager.enablePrivilege('UniversalXPConnect');
    var ext = filename.substr(filename.lastIndexOf(".") + 1);
    var file = get_associated_app(ext);
    if (file) {
        var process = Components.classes["@mozilla.org/process/util;1"]  
                                .createInstance(Components.interfaces.nsIProcess);  
        process.init(file);
        var args = [ filename ];
        //~ args.push('/n');
        process.run(false, args, args.length); 
        // If first param is true, calling thread will be blocked until  
        // called process terminates.  
    //~ } else {
        //~ console.log("Sorry, startfile() could not find application to start ."+ext+" files.");
    }
  //~ } else if (navigator.userAgent.indexOf('MSIE') != -1) {
    //~ WshShell = new ActiveXObject("WScript.Shell");
    //~ WshShell.Run(cmd + ' "' + filename + '"'); // ,1,true);
    //~ todo: search the registry using MSIE
  //~ } else {
    //~ console.log("Sorry, startfile() not yet implemented for " + navigator.userAgent);
  }
  //~ console.log(filename.substr(0,4))
  if (filename.substr(0,4) == 'http') window.open(filename);
}
