;/////////////////////////////////////////////////////////////////////
; Konfigurations-Datei _emacs für Emacs 20.4 unter MS-Windows
;                     Dr. Justus Noll      c't 22/99
;/////////////////////////////////////////////////////////////////////


(setq gs-dir "t:\\texmf\gstools\\gsview\\")

;=====================================================================
; Display und Font-Menü 
;=====================================================================

; disabled for Version 21.1.1 (standard-display-european 1 1); ... 1 1, sonst kein Mule-Menü!
;(print 'Hello)



(setq w32-use-w32-font-dialog t) ; Windows-Font-Menü, Unix: nil

;=====================================================================
; Rahmengröße und Farben
;=====================================================================

(setq default-frame-alist 
 '(
   (top . 4) (left . 20)
   (width . 80) (height . 34)
   (cursor-color . "red")
   (background-color . "light grey")
   (vertical-scroll-bars . right)
   (font
    .
    "-*-Lucida Console-normal-r-*-*-11-82-96-96-c-*-*-iso8859-1") 
   )
 )

; Textfarben

(set-face-foreground 'region "white")
(set-face-background 'region "black")

;=====================================================================
; Klingel und Uhr
;=====================================================================

; Klingelzeichen abstellen

(setq visible-bell t)

; Uhr im 24-Stunden-Format anzeigen

;(setq display-time-24hr-format t)
;(display-time)


;=====================================================================
; Drucker
;=====================================================================

(setq printer-name "LPT2:") ; nur falls Drucker nicht LPT1

;=====================================================================
; Umbruch, Löschen, ^M-Filter, Syntax-Farben (Font Lock), TEMP
;=====================================================================

; Automatischer Zeilenumbruch nach 78 Zeichen
;(setq fill-column 78)
;(add-hook 'text-mode-hook 'turn-on-auto-fill) 

; Aufruf ohne Argument löscht ganze Zeile
; (setq kill-whole-line t)

; Beim Suchen immer genaue Schreibweise finden
; (setq-default case-fold-search nil)

;; Overview of Font Lock Mode : c-h f font-lock-mode RET
(global-font-lock-mode t) 
(setq font-lock-maximum-decoration t)

; Temporäres Windows-Verzeichnis setzen

(setenv "TEMP" "c:/temp")
(setenv "TMP" "c:/temp")

;=====================================================================
; Neue Funktionen
;=====================================================================

; Funktionen zum Einrücken, Löschen, Doppeln

(defun indent-three-spaces ()
  "3 Leerzeichen einruecken."
  (interactive)
  (beginning-of-line)
  (insert "   ")
  (next-line 1))

(defun kill-current-line ()
  "Aktuelle Zeile loeschen."
  (interactive)
  (beginning-of-line)
  (kill-line))


(defun double-current-line ()
  "Aktuelle Zeile verdoppeln."
  (interactive)
  (beginning-of-line)
  (kill-line)
  (yank)
  (yank)
  (previous-line 1))

(defun load-tex-site-file ()
  "tex-site.el laden."
  (interactive)
  (find-file "t:/programme/emacs/site-lisp/tex-site.el")) 
(global-set-key [S-f3] 'load-tex-site-file)

(defun next-buffer ()
  "Schaltet zwischen den beiden letzten Fenstern hin und her."
  (interactive)
  (switch-to-buffer-other-window nil)
  (delete-other-windows))
(global-set-key [S-f4] 'next-buffer)



; (defun kill-current-or-next-word ()
;   "Aktuelles oder naechstes Wort loeschen."
;   (interactive)
;   (forward-word 1)
;   (backward-kill-word 1))
;    ;(delete-char 1))

; Drucken

(defun win-shell-befehl (prg)
 "Programm ausfuehren unter Windows."
  (shell-command 
   (concat prg buffer-file-name))) 

(defun ps-name ()
 "Name für PS-Datei."
 (concat (file-name-nondirectory buffer-file-name) ".ps"))

(defun np-drucken () 
 "Druck Puffer mit Windows Notepad."
 (interactive)
 (win-shell-befehl "notepad/p "))

(defun wp-drucken () 
 "Druck Puffer mit Windows Notepad."
 (interactive) 
 (win-shell-befehl "wordpad ")) ; /p Sofortdruck

(defun gs-drucken () 
 "Druck mit GhostSkript."
 (interactive)
  (ps-print-buffer (ps-name))
   (shell-command (concat gs-dir "gsview32 " (ps-name))))

; Region vom Mark bis zum Cursor wird markiert

;(transient-mark-mode t)  

; in tex-site.el: [C-Tab] TeX-Completion

; AFTER


(scroll-bar-mode -1)
; Toggle display of vertical scroll bars on all frames.
; This command applies to all frames that exist and frames to be
; created in the future.
; With a numeric argument, if the argument is negative,
; turn off scroll bars; otherwise, turn on scroll bars.



(set-default-font
"-*-Lucida Console-normal-r-*-*-11-82-96-96-c-*-*-iso8859-1") 

