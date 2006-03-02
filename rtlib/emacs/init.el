;;; Add things at the end, unconditionally
;;;(setq load-path (nconc load-path '("t:/data/luc/home/.xemacs" "bar")))

;;; (message (concat "Running on " (system-type)))
;;; (concat "Running on " system-type)
;;; (if (equal system-type 'gnu/linux) "yes" "no")
; (cond
;  ((eq system-type 'gnu/linux)
;   (message "Running on GNU/Linux")
;   (nconc load-path '(expand-file-name "~/emacs")))
;  (t 
;   (nconc load-path '("t:\\data\\luc\\home\\emacs")))
;  )


;;; Add things at the beginning of the load-path, do not add
;;; duplicate directories:
;;; (pushnew "t:/data/luc/home/.xemacs" load-path :test 'equal)

(defun activate-cp850 () "activates codepage 850"
  (interactive)
  ; (codepage-setup '850)
  (prefer-coding-system 'raw-text)
  ; (prefer-coding-system 'cp850)
  ;(prefer-coding-system 'no-conversion)
  ;(set-keyboard-coding-system 'cp850)
  ;(set-keyboard-coding-system 'raw-text)
  ; Display chars in range L to H literally:
  (standard-display-8bit 128 255)
  )


(cond
 ((eq window-system 'x)
  (load-library "my-suse-support.el")
  (server-start)
  )
 ((eq window-system 'w32)
  (load-library "justus-noll.el")
  (load-library "tex-site.el")
  (load-library "support-w32.el")
  (load-library "support-gnuserv.el")
  ; only on w32 because I use DOS-Emacs only for TIM files
  ;(standard-display-european 1 1)
  (standard-display-8bit 128 255)
  )
 ((eq window-system nil)
  (activate-cp850)
  )
 )

(load-library "c-x_c-r.el")

; diese Zeile ja eigentlich nur auf win32... aber wie testen?
(if (eq system-type 'windows-nt)
    (load-library "support-cygwin-bash.el"))

(defun my-split ()
  "splits frame if size allows it"
  (interactive)
  (message
   (number-to-string (frame-parameter (selected-frame) 'width)))

  (cond
   ((> (frame-parameter (selected-frame) 'width) 120)
    (split-window-horizontally)
    )
   )
  )

(add-hook 'window-setup-hook 'my-split)




(autoload 'sgml-mode "psgml" "Major mode to edit SGML files." t)
(autoload 'xml-mode "psgml" "Major mode to edit XML files." t)

(autoload 'xbase-mode "xbase" "Xbase mode" t)
(setq auto-mode-alist
      (cons
       (cons "\\.\\(prg\\|ch\\)$" 'xbase-mode)
       auto-mode-alist))

; (add-hook 'xbase-mode-hook 'activate-cp850)
; (add-hook 'xbase-mode-hook (setq indent-tabs-mode nil))

; (set-variable 'indent-tabs-mode nil)
 

(load-library "python-mode.el")
(setq auto-mode-alist
      (append
       '(("\\.py\\'" . python-mode))
       auto-mode-alist ))
(setq auto-mode-alist
      (append
       '(("\\.pds\\'" . python-mode))
       auto-mode-alist ))
;(add-hook 'python-mode-hook (setq indent-tabs-mode t))
;(add-hook 'python-mode-hook (setq py-smart-indentation nil))


(setq auto-mode-alist
      (append
       '(("\\.php\\'" . c++-mode))
       auto-mode-alist ))

(load-library "pinboard-mode.el")
(setq auto-mode-alist
      (append
       '(("\\.pin\\'" . pinboard-mode))
       auto-mode-alist ))

(load-library "50local.el")
(load-library "my-set-key.el")


(setq european-calendar-style t)
;; (display-time)

(setq frame-title-format "%b (%f)")


;(cond ((fboundp 'global-font-lock-mode)
;       ;; Turn on font-lock in all modes that support it
;       (global-font-lock-mode t)
;       ;; Maximum colors
;       (setq font-lock-maximum-decoration t)))


; (set-message-beep 'ok)


; (message "Hello")



; (load-library "support-jde.el")
; (custom-set-variables
;  '(jde-help-docsets (quote (("javadoc" "k:/collect/doc/java/jdk1.3/docs/api" nil))))
;  '(jde-run-application-class "jan.JanDemo")
;  '(jde-db-source-directories (quote ("t:\\data\\luc\\jan\\src" "t:\\soft\\jdk1.3\\tmp\\src")))
;  '(jde-make-program "ant ")
;  '(jde-jdk-doc-url "file://k:/collect/doc/java/jdk1.3/docs/index.html")
;  '(jde-db-debugger (quote ("JDEbug" "" . "Executable")))
;  '(jde-run-working-directory "t:\\data\\luc\\jan")
;  '(jde-enable-abbrev-mode t)
;  '(jde-make-working-directory "")
;  '(jde-make-args "-emacs -find"))
; (custom-set-faces)


;(defun runtests () (interactive)
;  (compile "python t:/data/luc/release/lino/make.py unittest doctest"))

;(global-set-key [(ctrl t)] 'runtests)




; (require 'emacs-wiki)



; (load-library "lilypond-mode.el")
; (setq auto-mode-alist
;       (cons '("\\.ly$" . LilyPond-mode) auto-mode-alist))
; (add-hook 'LilyPond-mode-hook (lambda () (turn-on-font-lock)))


