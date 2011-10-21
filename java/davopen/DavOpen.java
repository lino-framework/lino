/* thanks to 
http://www.realapplets.com/tutorial/ActionExample.html
http://java.sun.com/developer/technicalArticles/J2SE/Desktop/javase6/desktop_api/
http://de.selfhtml.org/javascript/objekte/applets.htm
http://www.java-forums.org/new-java/48589-whats-wrong-applet.html
http://stackoverflow.com/questions/4145942/problem-with-java-awt-desktop
http://www-personal.umich.edu/~lsiden/tutorials/signed-applet/signed-applet.html
http://download.oracle.com/javase/7/docs/technotes/tools/solaris/keytool.html
http://download.oracle.com/javase/7/docs/technotes/tools/solaris/jarsigner.html
http://www.ehow.com/how_6048581_access-windows-registry-java.html#ixzz1bEiAng8m

First compilation:

  javac DavOpen.java
  jar cvf DavOpen.jar DavOpen.class
  
  keytool -genkey
  keytool -selfcert
  keytool -list
  
  jarsigner DavOpen.jar mykey
  
Other compilations:

  javac DavOpen.java
  jar cvf DavOpen.jar DavOpen.class
  jarsigner DavOpen.jar mykey
  
  
TODO:

- get a trusted CA to avoid the "UNKNOWN" publisher warning
  http://stackoverflow.com/questions/5387793/help-to-set-publisher-for-japplet  
  
  
*/
package davopen;

import java.io.*;

//~ needed for open_using_ice_registry():
//~ import com.ice.jni.registry.Registry;
//~ import com.ice.jni.registry.RegistryException;
//~ import com.ice.jni.registry.RegistryKey;
//~ import com.ice.jni.registry.RegistryValue;


//~ needed for open_using_desktop
//~ import java.awt.Desktop;

//~ needed for open_using_prefs()
import java.util.prefs.Preferences;

//~ import java.awt.*;
import java.applet.Applet;
//~ import java.io.File;
//~ import java.io.IOException;
import java.security.Permission;
import java.io.FilePermission;


public class DavOpen extends Applet { 

  public void init() {
      //~ System.out.println("20111018 DavOpen.init()"); 
      System.setSecurityManager(new SecurityManager()
      {
        @Override
        public void checkPermission(Permission permission) {
           //~ System.out.println("20111018 checkPermission()"); 
           //~ if (permission instanceof AWTPermission) {
               //~ if (permission.getName().equals("showWindowWithoutWarningBanner")) {
                   //~ return;
               //~ }
           //~ }

           if (permission instanceof RuntimePermission) {
               //~ System.out.println(permission.getActions()); 
               return;
               //~ if (permission.getActions().equalsIgnoreCase("preferences")) {
                  //~ return;
               //~ }
           }
           if (permission instanceof FilePermission) {
               if (permission.getActions().equalsIgnoreCase("execute")) {
                  return;
               }
           }
           //~ System.out.println(permission); 
           java.security.AccessController.checkPermission(permission);
        }
      });
  }
  
  //~ public void open_using_desktop(String fileName) {
      //~ /*
      //~ Doesn't work, saying "file not found" because the fileName 
      //~ is actually an URL.
      //~ http://download.oracle.com/javase/6/docs/api/java/awt/Desktop.html
      //~ */
        //~ Desktop.getDesktop().open(new File(fileName));        
  //~ }
  
  /*
  Doesn't work, saying "file not found" because the fileName 
  is actually an URL.
  */
  /*
  public void open_using_ice_registry(String fileName) {
    
      System.out.println("20111018 open()"); 
      System.out.println(fileName); 
    
      System.out.println("okokok"); 
      Registry reg = new Registry();
      //~ RegistryKey topKey = Registry.HKEY_CURRENT_USER;
      //~ RegistryKey rk = topKey.openSubKey("Software\\Sparx Systems\\EA400\\EA");
      //~ String path = rk.getStringValue("Install Path");
      RegistryKey regkey = Registry.HKEY_CURRENT_USER;
      System.out.println("ok2");
      System.out.println(regkey);
      RegistryKey key = Registry.openSubkey(regkey,".doc",RegistryKey.ACCESS_READ);
      //~ RegistryKey regkey = Registry.HKEY_LOCAL_MACHINE;
      //~ RegistryKey key = Registry.openSubkey(regkey,"SOFTWARE\\SMS\\DHC",RegistryKey.ACCESS_READ);  
      //~ System.out.println(key.getFullName());
      System.out.println(key);
      System.out.println("ok2"); 
        
    
  }
  */
  
  /*
  //~ inspired by http://www.kodejava.org/examples/236.html
  //~ idea was to read from registry using java prefs.
  //~ but java prefs can read only below a key
  //~ HKCU\Software\JavaSoft\Prefs\myApp
  public void open_using_prefs(String fileName) {
      System.out.println("20111020 open(" + fileName + ")"); 
    
      Preferences userPrefs = Preferences.userRoot();
      System.out.println(userPrefs.get(".doc","not found"));
      
      //~ String OFFICEPATH = "C:\\Program Files\\Microsoft Office\\OFFICE11\\WINWORD.EXE";
      //~ String[] cmd = { OFFICEPATH, fileName };
      //~ Process p = Runtime.getRuntime().exec(cmd);
      //~ p.waitFor();
      //~ System.out.println(p.exitValue());
      
  }
  
  */
  
  public void open_using_regedit(String fileName) {
      //~ inspired by http://www.kodejava.org/examples/236.html
      System.out.println("20111020 open(" + fileName + ")"); 
    
      Preferences userPrefs = Preferences.userRoot();
      System.out.println(userPrefs.get(".doc","not found"));
      
      //~ String OFFICEPATH = "C:\\Program Files\\Microsoft Office\\OFFICE11\\WINWORD.EXE";
      //~ String[] cmd = { OFFICEPATH, fileName };
      //~ Process p = Runtime.getRuntime().exec(cmd);
      //~ p.waitFor();
      //~ System.out.println(p.exitValue());
      
  }
  
  import java.io.File; 
  
  private File find_executable(String paramString1, String paramString2, File paramFile)
  {
    String os_name = System.getProperty("os.name");
    paramString1 = paramString1;
    paramString2 = paramString2;
    File[] roots = File.listRoots();  //~ Object localObject 
    ArrayList localArrayList = new ArrayList();
    if (b.a())
      localArrayList.add(new File(System.getenv("SystemDrive") + "\\"));
    for (int j = 0; j < roots.length; j++)
    {
      if (localArrayList.contains(roots[j]))
        continue;
      localArrayList.add(roots[j]);
    }
    k localk = new k(this, paramString1);
    e locale = new e(this, paramString2);
    if (b.a())
      roots = new String[] { "Program Files", "Program Files (x86)" };
    else if (b.b())
      roots = new String[] { "/Applications/" };
    else
      roots = new String[] { "/usr/lib/" };
    if (paramFile == null)
      for (paramFile = 0; paramFile < localArrayList.size(); paramFile++)
      {
        h.a("root: " + localArrayList.get(paramFile));
        if ((((File)localArrayList.get(paramFile)).toString().equalsIgnoreCase("a:\\")) || (((File)localArrayList.get(paramFile)).toString().equalsIgnoreCase("b:\\")))
          continue;
        for (int m = 0; m < roots.length; m++)
        {
          File localFile = new File(localArrayList.get(paramFile) + roots[m]);
          h.a("search " + paramString1 + " in  " + localFile);
          File[] arrayOfFile;
          int n = (arrayOfFile = paramString2 = b.a(localFile, locale, 0)).length;
          for (int k = 0; k < n; k++)
            if ((paramString2 = a(paramString2 = arrayOfFile[k], localk)) != null)
              return paramString2;
        }
      }
    else if ((paramFile = a(paramFile, localk)) != null)
      return paramFile;
    return (File)null;
  }  
  
  public void open(String fileName) {
      try {
        //~ open_using_ice_registry(fileName)
        //~ open_using_desktop(fileName)
        //~ open_using_prefs(fileName);
        open_using_regedit(fileName);
      } catch (Exception err) {
        err.printStackTrace();
      }
  }
  
}



