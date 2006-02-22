;-*-emacs-lisp-*-
;;/etc/emacs/site-start.d/50local.el
;
;; overides by dirk
;;luc hat auch drin geändert.

;(require 'iso-syntax)
(setq default-major-mode 'text-mode)
(add-hook 'text-mode-hook 'turn-on-auto-fill)
(setq-default indent-tabs-mode nil)
(setq search-highlight t)
(resize-minibuffer-mode 1)
(setq resize-minibuffer-mode t)
; don't like next-line (cursor down to add newlines)
(setq next-line-add-newlines nil) 
;; Start with new default.
;(setq mode-line-format default-mode-line-format)
(setq column-number-mode t)

;;; make the compiler scroll its output:
(setq compilation-scroll-output t)

;; space is the new sense of luxury:
;(menu-bar-mode nil)
;(scroll-bar-mode -1)

;;; possibly anoying/interesting behaviour:
;;;
;;;(setq next-line-add-newlines nil)
;;;(setq track-eol t)
;;;(setq-default indent-tabs-mode nil)

;;; if set to t then the newline will be silently added!
(setq require-final-newline t) ;;luc
;;luc(setq require-final-newline 1) 

;; override anything that comes from etags.
(require 'etags)

(defun lisp-style-of-dirk ()
  (put 'do 'lisp-indent-function 'defun)
  (put 'with-open-file 'lisp-indent-function 'defun)
  (put 'with-input-from-string 'lisp-indent-function 'defun)
  (put 'cond 'lisp-indent-function 0)
  (put 'multiple-value-bind 'lisp-indent-function 1)
  (put 'case 'lisp-indent-function 'defun))

(require 'compile)
(global-set-key "\C-m" 'newline-and-indent)
(global-set-key [f10] 'previous-error)
(global-set-key [f11] 'next-error)
(global-set-key [f9] 'compile)

(setq completion-ignored-extensions
      (append
       (list ".ps" )
       (if (boundp 'completion-ignored-extensions)
           completion-ignored-extensions)))

(defun dirk-compilation-hook ()
  (modify-syntax-entry ?\< "(>")
  (modify-syntax-entry ?\> ")<")
  (show-paren-mode t))

(add-hook 'compilation-mode-hook 'dirk-compilation-hook)

;; stroustrup down to two indentations.
(c-add-style "dirk" '((c-basic-offset . 2)
                      (c-comment-only-line-offset . 0)
                      (c-offsets-alist . ((statement-block-intro . +)
                                          (substatement-open . 0)
                                          (label . 0)
                                          (statement-cont . +)
                                          (innamespace . -) ;; no indent in namespaces
                                          ))))
             
(defun dirk-cc-mode-hook ()
  (c-set-style "dirk")
  ;; FIXME: doesn't do its job :-(
  ;; c-baseclass-key comes gets in the way I guess...
;;  (setq c-access-key "\\<\\(public\\|protected\\|private\\|public slots\\|protected slots\\|private slots\\\\)\\>[ \t]*:")
  ;; I do not want to indent for namespaces. makes a mess of
  ;; colorisation heuristics for function declarations
  (c-set-offset 'innamespace '-)
  )

;; removed by ls: (add-hook 'c++-mode-hook 'dirk-cc-mode-hook)

(setq auto-mode-alist
      (append
       '(("\\.h\\'" . c++-mode))
       auto-mode-alist))

;; for linux kernel sources.
(define-derived-mode linux-c-mode
  c-mode "Linux"
  "Major mode for Linux"
  (c-set-style "linux")
  (font-lock-mode t))


;;; I want to see redland here... --- dirk
;(add-hook 'c++-mode-hook (lambda () (progn (make-local-variable 'compile-command)
;					   (setq compile-command
;						 "make-project -j 4 smrMain"))))
;;; my super-hyper-fast parser....
;(setq compilation-error-regexp-alist
;      '(("^\\([a-zA-Z]?:?[^:( \t\n]+\\)[:( \t]+\\([0-9]+\\)[:) \t]" 1 2)))
;(require 'compile)
;(defun compile-me ()
;  "compile the current buffer, by calling the command make-module"
;  (interactive)
;  (if (or (not (buffer-modified-p))
;	  (not (y-or-n-p (format "Buffer %s is modified, save it? " (buffer-name))))
;	  (save-buffer)
;	  t)
;      (compile-internal (format "make-module %s" buffer-file-name)
;			"No More Errors")))
;(define-key global-map [(shift f9)] 'compile-me)


(cond ((eq window-system 'x)
       (require 'font-lock)
;       (font-lock-make-faces)   ; important, otherwise the following won't work
       (set-face-underline-p 'underline nil)
       (set-face-foreground font-lock-comment-face "#6920ac")
       (set-face-foreground font-lock-keyword-face "#6920ac")
       (set-face-foreground font-lock-function-name-face "red3")
       (set-face-foreground font-lock-string-face "green4")
       (setq font-lock-maximum-decoration nil)
       (global-font-lock-mode t)
       (setq c-basic-offset 2)))

;; makes reading the jargon file much more fun!
;; the middle mouse button tries to follow an 'informal' jargon reference.
(defun my-Info-try-follow-nearest-node ()
  "Follow a node reference near point.  Return non-nil if
successful. Jargon friendly."
  (let (node)
    (cond
     ((setq node (Info-get-token (point) "\\*note[ \n]"
				 "\\*note[ \n]\\([^:]*\\):"))
      (Info-follow-reference node))
     ((setq node (Info-get-token (point) "\\* " "\\* \\([^:]*\\)::"))
      (Info-goto-node node))
     ((setq node (Info-get-token (point) "\\{" "\\{\\([^,\\{\\}\n\t]*\\)\\}"))
      (Info-goto-node node))
     ((setq node (Info-get-token (point) "\\* " "\\* \\([^:]*\\):"))
      (Info-menu node))
     ((setq node (Info-get-token (point) "Up: " "Up: \\([^,\n\t]*\\)"))
      (Info-goto-node node))
     ((setq node (Info-get-token (point) "Next: " "Next: \\([^,\n\t]*\\)"))
      (Info-goto-node node))
     ((setq node (Info-get-token (point) "File: " "File: \\([^,\n\t]*\\)"))
      (Info-goto-node "Top"))
     ((setq node (Info-get-token (point) "Prev: " "Prev: \\([^,\n\t]*\\)"))
      (Info-goto-node node)))
    node))
(add-hook 'Info-mode-hook
	  (function (lambda ()
		      (defun Info-try-follow-nearest-node ()
			(my-Info-try-follow-nearest-node)))))


(require 'ps-print)
(setq ps-lpr-command "lpr")
(setq ps-paper-type 'a4)

(define-key global-map [(meta tab)]          'dabbrev-expand)
(define-key global-map [(control tab)]          'dabbrev-expand)



(defun revert-all-buffers ()
  "revert all buffers. Confirmation will be asked if the buffer is in
a modified state."
  (interactive)
  (save-excursion
    (setq blist (buffer-list))
    (while blist
      (set-buffer (car blist))
      (if (and (buffer-file-name)
               (file-readable-p (buffer-file-name))
	       (or (not (buffer-modified-p))
		   (y-or-n-p
		    (format "Buffer %s is modified, really revert it? "
			    (buffer-name)))))
	  (revert-buffer t t))
      (setq blist (cdr blist)))))

(put 'erase-buffer 'disabled nil)
;;; set the place to look for the TAGS table
;(setq tags-table-list (list (getenv "SRCROOT")))

;;; now I can drop frames
(setq truncate-partial-width-windows nil)

