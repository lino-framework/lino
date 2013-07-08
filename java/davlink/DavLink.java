/*
* See http://lino-framework.org/davlink/index.html
* 
* Copyright 2013 Luc Saffre
* This file is part of the Lino project.
* Lino is free software; you can redistribute it and/or modify 
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation; either version 3 of the License, or
* (at your option) any later version.
* Lino is distributed in the hope that it will be useful, 
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
* GNU General Public License for more details.
* You should have received a copy of the GNU General Public License
* along with Lino; if not, see <http://www.gnu.org/licenses/>.
*
*/

package davlink;

import java.io.File; 
import java.io.IOException; 
import java.util.Hashtable; 
import java.util.ArrayList; 
import java.util.List; 
import java.applet.Applet;
//~ import java.security.AccessControlException;
import java.io.FilenameFilter;
import java.io.FileFilter;

import java.security.Permission;
import java.io.FilePermission;


import java.util.prefs.Preferences;
//~ import javax.swing.JOptionPane;


//~ enum OS { LINUX, WINDOWS }

//~ class Program {
    //~ String unix_name;
    //~ String mac_name;
    //~ String windows_name;
    //~ String[] extensions;
    //~ Program(String wn,String un,String mn,String... exts) {
        //~ unix_name = un;
        //~ mac_name = mn;
        //~ windows_name = wn;
        //~ extensions = exts;
    //~ }
//~ }

class Launcher {
    /**
    */
    //~ ArrayList<String> extensions;
    String name;
    //~ File path;
    String path;
    Launcher(String n) {
        name = n;
        //~ launchers = new ArrayList<String>();
    }
}
class DocType {
    String extension;
    ArrayList<Launcher> launchers = new ArrayList<Launcher>();
  
    DocType(String ext) {
        extension = ext;
        //~ launchers = new ArrayList<Launcher>();
    }
    
    Launcher getPreferredLauncher() {
        return launchers.get(0);
    }
}



class Searcher {
    DavLink app;
    //~ FileFilter filter;
    Searcher(DavLink a) {
        app = a;
    }
    public final void traverse( final File f ) throws IOException {
        if (f.isDirectory()) {
          System.out.println("Searching " + f.getAbsolutePath());
          //~ onDirectory(f);
          for (String name : f.list()) {
             traverse(new File(f,name));
          }
        } else {
          onFile(f);
        }   
    }

    //~ void onDirectory( final File d )  throws IOException {
        //~ final String[] names = d.list();
        //~ for (String name : names) {
           //~ traverse(new File(d,name));
        //~ }
    //~ }
    
    void onFile( final File file ) {
        for (Object o : app.launchers.values()) {
            Launcher la = (Launcher)o;
            if (la.path == null){
                if (file.getName().equalsIgnoreCase(la.name)) {
                    la.path = file.getAbsolutePath();
                    System.out.println("  Found " + file);
                }
            }
        }
    }
    

}



public class DavLink extends Applet {
      
    static Preferences prefs =  Preferences.systemRoot().node("/lino/davlink");
  
    Hashtable<String,DocType> docTypes = new Hashtable<String,DocType>();
    Hashtable<String,Launcher> launchers = new Hashtable<String,Launcher>();
  
    //~ static DavLink theOneAndOnly = new DavLink();
    //~ DavLink() { init(); }
    //~ final static IsDirFilter IS_DIR = new IsDirFilter();
  
    //~ static private List<File> getFileListingNoSort(File top) 
    //~ throws FileNotFoundException 
    //~ {
      //~ List<File> result = new ArrayList<File>();
      //~ File[] filesAndDirs = top.listFiles();
      //~ List<File> filesDirs = Arrays.asList(filesAndDirs);
      //~ for(File file : filesDirs) {
        //~ result.add(file); //always add, even if directory
        //~ if ( ! file.isFile() ) {
          //~ //must be a directory
          //~ //recursive call!
          //~ List<File> deeperList = getFileListingNoSort(file);
          //~ result.addAll(deeperList);
        //~ }
      //~ }
      //~ return result;
    //~ }
  
  
    //~ private File[] get_subdirs(File top) {
        //~ File[] ret = {};
        //~ File[] subdirs = top.list(IS_DIR);
        //~ if (subdirs != null) {
            //~ for (int i = 0; i < subdirs.length; j++) {
                //~ get_subdirs(subdirs[i]);
            //~ }
        
        //~ if (! d.isDirectory()) return null;
      
    //~ }
    
    DocType add_doctype(String ext) {
        DocType t;
        if (docTypes.containsKey(ext)) 
            t = (DocType)docTypes.get(ext);
        else {
            t = new DocType(ext);
            docTypes.put(ext,t);
        }
        return t;
    }
    
    Launcher add_launcher(DocType t,String fileName) {
        Launcher l;
        if (launchers.containsKey(fileName)) 
            l = (Launcher)launchers.get(fileName);
        else {
            l = new Launcher(fileName);
            launchers.put(fileName,l);
        }
        t.launchers.add(l);
        return l;
    }
    
    //~ void add_launchers(OS os, DocType t, String... names) {
        //~ String os_name = System.getProperty("os.name");
        //~ if (os == OS.WINDOWS && ! os_name.startsWith("Windows")) return;
        //~ if (os == OS.LINUX && ! os_name.startsWith("Linux")) return;
        //~ for (String name : names) add_launcher(t,name);
      
    //~ }
    
    void add_program(
        String windowsName, 
        String linuxName,
        String macName,
        String... extensions) 
    {
        /** 
        os and arch value collection:
        http://lopica.sourceforge.net/os.html
        */
        String os_name = System.getProperty("os.name");
        String name = null;
        if (os_name.startsWith("Windows")) name = windowsName;
        else if (os_name.startsWith("Linux")) name = linuxName;
        else if (os_name.startsWith("Mac")) name = macName;
        else
            throw new RuntimeException("Unknown os.name " + os_name);
      
        if (name == null) {
            //~ System.err.println("20130708 name is null");
            return;
        }
        for (String ext : extensions) {
            DocType t = add_doctype(ext); 
            add_launcher(t,name);
        }
    }
    
    
    public void unused_init() {
        System.err.println("Gonna disable the security manager...");
        System.setSecurityManager(null);
        System.err.println("Security manager has been disabled ");
    }
    
    public void init() {
        System.err.println("Gonna set the security manager...");
        //~ System.out.println("toto");
        
        System.setSecurityManager(new SecurityManager()
        {
          @Override
          public void checkPermission(Permission permission) {
             if (permission instanceof RuntimePermission) {
                 return;
                 //~ if (permission.getActions().equalsIgnoreCase("preferences")) {
                    //~ return;
                 //~ }
                 //~ if (permission.getActions().equalsIgnoreCase("getenv.SystemDrive")) {
                    //~ return;
                 //~ }
             }
             if (permission instanceof FilePermission) {
                 return;
                 //~ if (permission.getActions().equalsIgnoreCase("execute")) {
                    //~ return;
                 //~ }
             }
             java.security.AccessController.checkPermission(permission);
          }
        });
        System.err.println("Initialized");
    }
    
    public void generate_default_prefs() {
        //~ System.err.println("20130708 generate_default_prefs()");
      
        add_program("winword.exe", null,          null,   "rtf","doc");
        add_program("swriter.exe", "libreoffice", null,   "rtf","doc","odt");
        add_program("excel.exe"  , null,          null,   "xls","csv");
        add_program("scalc.exe"  , "libreoffice", null,   "xls","ods","csv");

        List<File> drives = new ArrayList<File>();
        String[] bindirs;
      
        String os_name = System.getProperty("os.name");
      
        if (os_name.startsWith("Windows")) {
          bindirs = new String[] { "Program Files", "Program Files (x86)" };
          //~ crack:
          String s = System.getenv("SystemDrive") + "\\";
          File fd = new File(s);
          drives.add(fd);
          //~ drives.add(new File(System.getenv("SystemDrive") + "\\"));
          //~ System.out.println("generate_default_prefs() 10");
        } else {
          bindirs = new String[] { "/usr/bin/" };
        } 
        
        //~ System.err.println("20130708 bindirs.length is " + bindirs.length);
        if (bindirs.length == 0) {
            throw new RuntimeException("No binary dirs! Seems that your OS is not supported!");        
        }
      
        File[] roots = File.listRoots();  //~ Object localObject 
        //~ System.err.println("20130708 roots.length is " + roots.length);
      
        for (int j = 0; j < roots.length; j++) {
            if (! drives.contains(roots[j]))
                drives.add(roots[j]);
        }
        
        //~ System.err.println("20130708 drives.size() is " + drives.size());
        
        try {
            Searcher search = new Searcher(this);
            //~ LauncherFilter filter = new LauncherFilter(this);
            for (int i = 0; i < drives.size(); i++) {
              File drive = drives.get(i);
              //~ File drive = (File) drives.get(i);
              for (String name : bindirs) {
                  search.traverse(new File(drive,name));
              }
            }
            
            for (Object o : docTypes.values()) {
                DocType t = (DocType)o;
                for (Launcher la : t.launchers) {
                    if (la.path != null) {
                        prefs.put(t.extension,la.path);
                        System.out.println("prefs.put(" + 
                          t.extension + "," + la.path + ")");
                        break;
                    }
                }
            }
            prefs.put("","Generated");
            
         } catch (IOException err) {
           err.printStackTrace();
         }
    }
    
    
    String getLauncherFor(String fileName) {
        int pos = fileName.lastIndexOf('.');
        if (pos == -1) 
            throw new RuntimeException("No extension specified in " + fileName);
        String ext = fileName.substring(pos+1);
        
        if (prefs.get("",null) == null) 
            generate_default_prefs();
        String path = prefs.get(ext,null);
        if (path == null) {
            throw new RuntimeException("No launcher defined for extension '" + ext + "'");
        }
        return path;
        
    }
    
   public String open(String fileName) {
       /*
        * Launches the application associated with the specified fileName.
        * returns null upon success, otherwise the exception object.
        * 
        * */
        try {
            String path = getLauncherFor(fileName);
            String[] cmd = { path, fileName };
            //~ System.out.println(path + " " + fileName);
            Process p = Runtime.getRuntime().exec(cmd);
            return null;
            //~ p.waitFor();
            //~ System.out.println(p.exitValue());
        } catch (Exception e) {
            //~ JOptionPane.showMessageDialog(null, 
                //~ e, 
                //~ "Error",
                 //~ JOptionPane.ERROR_MESSAGE);        
            //~ e.printStackTrace();
        //~ } catch (IOException err) {
            //~ e.printStackTrace();
        //~ } catch (InterruptedException err) {
            //~ e.printStackTrace();
            return e.toString();
        }
    }
    
    public static void main(String args[]) {
        DavLink a = new DavLink();
        a.init();
        //~ try {
            for (String arg : args) {
                //~ Exception e = a.open(arg);
                //~ if (e != null)
                    //~ e.printStackTrace();
                String msg = a.open(arg);
                if (msg != null)
                    System.err.println(msg);
            }
        //~ } catch (IOException err) {
            //~ err.printStackTrace();
        //~ }
    }
}
