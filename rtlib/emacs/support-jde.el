
  (add-to-list 'load-path (expand-file-name "t:/soft/emacs/site-lisp/jde/lisp"))
  (add-to-list 'load-path (expand-file-name "t:/soft/emacs/site-lisp/semantic"))
  (add-to-list 'load-path (expand-file-name "t:/soft/emacs/site-lisp/speedbar"))
  (add-to-list 'load-path (expand-file-name "t:/soft/emacs/site-lisp/elib"))
  (add-to-list 'load-path (expand-file-name "t:/soft/emacs/site-lisp/eieio"))


;; If you want Emacs to defer loading the JDE until you open a 
;; Java file, edit the following line
;;(setq defer-loading-jde nil)
;; to read:
;;
(setq defer-loading-jde t)
;;

(if defer-loading-jde
    (progn
      (autoload 'jde-mode "jde" "JDE mode." t)
      (setq auto-mode-alist
	    (append
	     '(("\\.java\\'" . jde-mode))
	     auto-mode-alist)))
  (require 'jde))


;; Sets the basic indentation for Java source files
;; to two spaces.
(defun my-jde-mode-hook ()
  (setq c-basic-offset 2))

(add-hook 'jde-mode-hook 'my-jde-mode-hook)





;;Problem I can't get the JDE to use Internet Explorer to display the
;;JDK doc or the JDE User's Guide.

;;Solution The JDE uses Emacs browse-url interface to web
;;browsers. browse-url supports Netscape by default. To use Internet
;;Explorer:
;; 1. Add the following code to your .emacs file

(if (eq system-type 'windows-nt)
  (defadvice browse-url-generic (around show-window act)
    "*Sets `start-process-show-window' on."
    (let ((w32-start-process-show-window t))
      ad-do-it)))
  

;;This code causes Emacs to show the window of the browser launched by
;;the function browse-url-generic.








;;From: Richard den Adel 
;;Subject: Small extension to jde-run to run JUnit tests 
;;Date: Tue, 20 Feb 2001 23:01:26 -0800 

;;Hi all,

;;I have written some lisp functions that allow me to run the JUnit
;;test that corresponds with the current buffer.  If your current
;;buffer is :com/acriter/util/GUIAccess.java, the jde-run-test-class
;;will run the class com.acriter.util.TestGUIAccess and
;;jde-run-package-test-class will run the class com.acriter.util.Test
;;(we use this syntax to run all tests in a current package, it is an
;;automatically generated TestSuite of JUnit.)

;;I don't know if it is of any use to anyone but me, but anyway

;;It is my first tryout in lisp, so please be gentle to me ;-)


(defun jde-run-test-class()
  "Runs the corresponding test class that belongs to the current buffer"
  (interactive)
  (jde-run-internal (jde-run-get-test-class)))


(defun jde-run-get-test-class()
  "Gets the test class for the current buffer"
  (let ((test-class (jde-run-get-main-class)))
    (if (string-match ".*Test.*" (jde-run-get-main-class))
        (setq test-class (jde-run-get-main-class))
      (setq test-class
            (concat (jde-db-get-package)
                    "Test"
                    (file-name-sans-extension
                     (file-name-nondirectory (buffer-file-name))))))
    test-class))

(defun jde-run-package-test-class()
  "Runs the corresponding test class that belongs to the package of the current
buffer"
  (interactive)
  (jde-run-internal (jde-run-get-package-test-class)))

(defun jde-run-get-package-test-class()
  "Gets the package test class for the current buffer"
  (let ((package-test-class (concat (jde-db-get-package) "Test")))
    package-test-class))
                       













;; Include the following only if you want to run
;; bash as your shell.

;; Setup Emacs to run bash as its primary shell.
(setq shell-file-name "bash")
(setq shell-command-switch "-c")
(setq explicit-shell-file-name shell-file-name)
(setenv "SHELL" shell-file-name)
(setq explicit-sh-args '("-login" "-i"))
(if (boundp 'w32-quote-process-args)
  (setq w32-quote-process-args ?\")) ;; Include only for MS Windows.
