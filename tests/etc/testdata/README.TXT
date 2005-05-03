
 ฺฤฤฤฤฤฤฟฤฟฺฤฤยฤฤฟ
 ภฤฟ  ฺฤู ณณ     ณ
   ภฤฤู ภฤูภฤมฤมฤู when Time Is Money

Installation instructions :

- Copy the distribution files to a directory of your choice
  (usually c:\tim). This will be the "program path"

- (if necessary) rename unzip.ex_ to unzip.exe

- unzip *.zip

- Check the following MANUALLY :
  - TIM requires minimum 85 file handles
  - Add the programm path (usually c:\tim) to your PATH environment

  If you don't know how to do it, see instructions below:
    Windows NT/2000
    - Arbeitsplatz/Eigenschaften/Erweitert/Umgebungsvariablen
      modify the "Path" : add ";C:\TIM" at the end
      create PC

    Windows 9x
    - edit c:\autoexec.bat :
      modify the "PATH" : add ";C:\TIM" at the end
      (or add a line PATH C:\TIM)
    - edit c:\config.sys and put a line
        files=85
      (or more)
    - Reboot the PC

    Win3.1 :
    - emm386 noemm novcpi in config.sys

  IF YOU GET A "DOS ERROR 4" MESSAGE THEN YOU DID NOT SUCCEED THIS STEP.

- cd to c:\tim and run INSTALL.BAT once.

  This will extract the zip files and run TIM a first time.
  You will see this dialog:
    ษอออออออออออออออออออ Datenbank reorganisieren อออออออออออออออออออออป
    บ   INDEX   : Indexdateien (*.NTX) neu erstellen                   บ
    บ   REBUILD : Datenbank kompaktieren                               บ
    บ X CHECK   : Dateistrukturen prfen und evtl. konvertieren.       บ
    บ            X Konvertierungen besttigen                          บ
    บ                                                                  บ
    บ Folgende Dateien nicht reorganisieren :                          บ
    บ Ausschlieแlich folgende Dateien reorganisieren :                 บ
    บ   gemeinsame Dateien ignorieren                                  บ
    ศออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออผ
  Confirm this Dialog by pressing F10.

- Start TIM using the file tim.bat in your program path.
  Create a Shortcut to this file.

Network installation :

- create a directory c:\tim\home
- SET PC on each computer
- create a directory %PC% under c:\tim\home for each PC
- in each PC's working directory there must be a sub-directory "rpt"



