/*

See http://lino.saffre-rumma.net/davlink  

http://download.oracle.com/javase/6/docs/api/java/util/ArrayList.html

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
      
        if (name == null) {
            return;
        }
        for (String ext : extensions) {
            DocType t = add_doctype(ext); 
            add_launcher(t,name);
        }
    }
    
    
    public void init() {
        System.out.println("Initializing");
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
    }
    
    public void generate_default_prefs() {
        //~ System.out.println("generate_default_prefs()");
      
      
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
        
        //~ System.out.println(bindirs);
      
        File[] roots = File.listRoots();  //~ Object localObject 
        //~ System.out.println(roots);
      
        for (int j = 0; j < roots.length; j++) {
            if (! drives.contains(roots[j]))
                drives.add(roots[j]);
        }
        
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
        if (path == null) 
            throw new RuntimeException("No launcher defined for " + fileName);
        return path;
        
    }
    
   public void open(String fileName) {
        String path = getLauncherFor(fileName);
        String[] cmd = { path, fileName };
        System.out.println(path + " " + fileName);
        try {
            Process p = Runtime.getRuntime().exec(cmd);
            //~ p.waitFor();
            //~ System.out.println(p.exitValue());
        } catch (Exception err) {
            err.printStackTrace();
        //~ } catch (IOException err) {
            //~ err.printStackTrace();
        //~ } catch (InterruptedException err) {
            //~ err.printStackTrace();
        }
          
    }
    
    //~ public static void main(String args[]) {
       //~ theOneAndOnly.open(args[0]);
    //~ }
}