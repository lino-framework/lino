;/////////////////////////////////////////////////////////////////////
;        tex-site.el - Teilkopie von AucTeXs tex.el (9.10g)
;             (Aenderungen sind durch <--- markiert.)
;                         Dr. Justus Noll   c't 22/99
;/////////////////////////////////////////////////////////////////////

;=====================================================================
; Verzeichnisse und Autoloads (erst bei Bedarf zu ladende Funktionen)
;=====================================================================

; Hinweis, dass Funktion noch nicht geladen ist 

(defvar no-doc
  "Diese Funktion ist Teil von AucTeX, wurde aber noch nicht geladen.
   Nach dem Laden steht die volle Dokumentation zur Verfuegung."
  "Dokumentation fuer autoload-Funktionen.")

; Verzeichnis von AucTeX
    
 (defvar TeX-lisp-directory "s:/emacs/site-lisp/auctex/" ; <---
  "Verzeichnis der AucTeX-Dateien. Muá mit
   Schr„gstrich / enden!!!")

; Verzeichnis von TeX

(defcustom TeX-macro-global '("s:/miktex/") ;<---
  "Verzeichnis, in dem sich die TeX-Macros befinden. Muss mit
   Schrägstrich / enden!!!"
  :group 'TeX-file
  :type '(repeat (directory :format "%v")))

; Autoloads

(or (assoc TeX-lisp-directory 
       (mapcar 'list load-path))               ; noch kein `member' 
    (assoc (substring TeX-lisp-directory 0 -1) ; ohne fuehrenden Slash.
	   (mapcar 'list load-path))
    (setq load-path (cons TeX-lisp-directory load-path)))

(autoload 'tex-mode "tex" no-doc t)

(autoload 'plain-tex-mode "tex" no-doc t)

(autoload 'latex-mode "latex" no-doc t)

;=====================================================================
; LaTeX-Version
;=====================================================================

; LaTeX-Version beim Start ist LaTeX2e.

(defcustom LaTeX-version "2e"
  "LaTeX version beim Start. Zur Zeit sind \"2\" und \"2e\" moeglich."
  :group 'LaTeX
  :type '(radio (const :format "%v\n%h"
		       :doc "\
 Programm `latex' ist LaTeX-Version 2."
		       "2")
		(const :format "%v\n%h"
		       :doc "\
 Programm `latex' ist LaTeX-Version 2e.
 !!!Nicht waehlen, wenn man statt latex.exe latex2e.exe aufrufen muss!!!"
		       "2e")
		(string :tag "Other")))
		
;=====================================================================
; Menue-Befehle zur Ausfuehrung externer Programme.
;=====================================================================

(defcustom TeX-command-list
  (list (list "TeX interaktiv" "tex %t" 'TeX-run-interactive nil t)
	(list "LaTeX interaktiv" "%l %t" 'TeX-run-interactive nil t)
	(if (or window-system (getenv "DISPLAY"))
	    (list "Yap" "%v " 'TeX-run-silent nil t); ohne RET: t nil
	  (list "View" "dvi2tty -q -w 132 %s " 'TeX-run-command t nil))
	(list "BibTeX" "bibtex %s" 'TeX-run-BibTeX nil nil)
	(list "Index" "makeindex %s" 'TeX-run-command nil t)
)
  "Menu-Befehle, die von der Shell ausgefuehrt werden: Aufruf
   von TeX, dem Viewer YAP, BibTeX und MakeIndex."
  :group 'TeX-command
  :type '(repeat (group (string :tag "Name")
			(string :tag "Command")
			(choice :tag "How"
				:value TeX-run-command
				(function-item TeX-run-command)
				(function-item TeX-run-format)
				(function-item TeX-run-TeX)
				(function-item TeX-run-LaTeX)
				(function-item TeX-run-BibTeX)
				(function-item TeX-run-compile)
				(function-item TeX-run-shell)
				(function-item TeX-run-discard)
				(function-item TeX-run-background)
				(function-item TeX-run-silent)
				(function-item TeX-run-dviout)
				(function :tag "Other"))<
			(boolean :tag "Prompt")
			(sexp :format "End\n"))))
		       

; Spezielle Optionen verschiedener LaTeX-Stile (LaTeX2e kombiniert 
; sie alle). Funktioniert nur, wenn TeX-Parsing eingeschaltet ist. 
; LaTeX soll mit Source-Specials kompilieren (<---), die ermoeglichen, 
; dass der Viewer spaeter an eine mit dem Editor korrespondierende 
; Stelle in der .dvi-Datei gesetzt werdec:/My/CT/tex-word/n kann). 

(defcustom LaTeX-command-style
  (if (string-equal LaTeX-version "2")
       '(("^latex2e$" "latex2e")
	("^foils$" "foiltex")
	("^ams" "amslatex")
	("^slides$" "slitex")
	("^plfonts\\|plhb$" "platex")
	("." "latex"))
      '(("." "latex --src-specials"))) ;<---
  "Liste der Stiloptionen und LaTeX-Befehle.
   Wenn das erste Element, ein regulaerer Ausdruck, der Name 
   eines Syle-Files ist, wird in einem Befehl der TeX-Befehls-Liste
   jedes Vorkommen von %l mit dem zweiten Element ersetzt. Der 
   erste passende Ausdruck wird gewaehlt, falls es keinen gibt,
   wird %l durch den Leer-String ersetzt."
  :group 'TeX-command
  :type '(repeat (group :value ("" "")
			regexp (string :tag "Style"))))

; Um den MikTeX-Viewer YAP an eine bestimmte Textstelle zu
; setzen, muá die Zeilennummer der TeX-Datei (%n) vor ihren
; Namen (%b) mit .dvi-Erweiterung (%d) gesetzt werden (<---). 
; Damit wird dann mittels der Option -s das entsprechende 
; Source-Spezial aufgerufen. Option -1 bedeutet, daá immer 
; nur eine Instanz von YAP ge”ffnet ist.  

(defcustom TeX-view-style '(("^a5$" "yap %d -paper a5")
			    ("^landscape$" "yap %d -paper a4r -s 4")
			    ("^epsf$" "ghostview %f")
                	    ("." "yap -1 -s%n%b %d"));<---
  "Liste der Viewer-Optionen.
   Wenn das erste Element, ein regulaerer Ausdruck, der Name 
   eines Syle-Files ist, wird in einem Befehl der TeX-Befehls-Liste
   jedes Vorkommen von %v mit dem zweiten Element ersetzt. Der 
   erste passende Ausdruck wird gewaehlt, falls es keinen gibt,
   wird %v durch den Leer-String ersetzt."
  :group 'TeX-command
  :type '(repeat (group regexp (string :tag "Command"))))

; Liste der String-Expansionen fuer Befehle der TeX-Befehls-Liste.
; Normalerweise braucht sie nicht geaendert werden. Will man aber
; aus Emacs heraus YAP aufrufen und an eine bestimmte Textstelle
; setzen, wird der Name der aktuellen Datei benoetigt, nicht
; nur des TeX-Master-Files. Daher wird die Liste durch %b
; erweitert (<---).

(defcustom TeX-expand-list 
  (list (list "%p" 'TeX-printer-query);%p muss erster Eintrag sein
	(list "%q" (function (lambda ()
		     (TeX-printer-query TeX-queue-command 2))))
	(list "%v" 'TeX-style-check TeX-view-style)
	(list "%l" 'TeX-style-check LaTeX-command-style)
	(list "%s" 'file nil t)
	(list "%t" 'file 't t)
	(list "%n" 'TeX-current-line)
	(list "%d" 'file "dvi" t)
	(list "%f" 'file "ps" t)
        (list "%b" (function (lambda () ;<---
        (file-name-nondirectory buffer-file-name)))))
  "Liste der String-Expansionen fuer TeX-Befehle. Das erste
   Element ist der zu erweiternde String. Das zweite Element
   ist der Name einer Funktion, die den expandierten String
   zurueckgibt, wenn sie mit den restlichen Elementen als
   Argumente aufgerufen wird. Der Wert file wird zum
   aktuellen Dateinamen mit optionaler Extension erweitert."
  :group 'TeX-command
  :type '(repeat (group (string :tag "Key")
			(sexp :tag "Expander")
			(repeat :inline t
				:tag "Arguments"
				(sexp :format "%v")))))

;=====================================================================
; Tastenbelegungen
;=====================================================================

; Shortcuts für LaTeX und Yap

(defun do-LaTeX ()
 "LaTeX ausfuehren."
 (interactive)
 (TeX-command "LaTeX interaktiv" 'TeX-master-file))

(defun do-DVIview ()
 "Mit Yap aktuelles dvi.-File betrachten."
 (interactive)
 (TeX-command "Yap" 'TeX-master-file))

(global-set-key [(control f5)] 'do-LaTeX)  
(global-set-key [(control f6)] 'do-DVIview)

 
; Ctrl-TAB fr TeX-Erg„nzungsfunktion

(global-set-key [C-tab] 'TeX-complete-symbol)

;=====================================================================
; TeX-Start-Modus wird erzwungen 
;=====================================================================

(defcustom TeX-force-default-mode t ;<----
 "Wenn TeX-force-default-mode den Wert nil hat, versucht Emacs den
  Modus aus dem Inhalt der Datei zu erschliessen."
  :group 'AUC-TeX
  :type 'boolean)

;=====================================================================
; tex-site.el wird verfuegbar gemacht.
;=====================================================================

(provide 'tex-site)

(provide 'hilit-LaTeX)

;/////////////////////////////////////////////////////////////////////
;                      Ende von tex-site.el
;/////////////////////////////////////////////////////////////////////
