;; my-set-key.el
;; Author : Luc Saffre <luc.saffre@gmx.net>
;;
;; Note:
;; this is the only startup file which is also used by em.bat

;; Makes things a little bit more consistent:
(fset 'yes-or-no-p 'y-or-n-p)


;; visualize couples of parentheses:
;; not supported in XEmacs: (show-paren-mode)


;; not supported in XEmacs:
(global-set-key [C-home] 'beginning-of-buffer)
(global-set-key [C-end] 'end-of-buffer)
;; (global-set-key "\C-m" 'newline-and-indent)
;; (print 'Hello)

;; (global-set-key "\C-x\C-\\" 'next-line)

(global-set-key [f6] 'other-window)
(global-set-key [f7] (lambda ()
			 (interactive)
			 (switch-to-buffer (other-buffer))))
(global-set-key [f8] 'call-last-kbd-macro)

(setq scroll-step 1)
;; When you scroll down with the cursor,
;; emacs will move down the buffer one 
;; line at a time, instead of in larger amounts.

(global-set-key [backspace] 'backward-delete-char-untabify)
;;(global-set-key [delete] 'delete-char)
(global-set-key [home] 'beginning-of-line)
(global-set-key [end] 'end-of-line)
;; (global-set-key [return] 'newline)


(global-set-key "\M-g" 'goto-line)
;; (global-set-key [C-tab] 'dabbrev-expand)
(global-set-key [(control tab)] 'dabbrev-expand)

(define-key minibuffer-local-map [(control tab)] 'dabbrev-expand)

(global-set-key [(control backspace)] 'backward-kill-word)

;;(define-key global-map [(meta t)] 'tags-search)
;;(define-key global-map [(meta n)] 'tags-loop-continue)
;;(define-key global-map [(control t)] 'find-tag)
;;(define-key global-map [(control n)] 'tags-loop-continue)

;; editing in search buffer...
(define-key isearch-mode-map [backspace] 'isearch-delete-char)
(define-key isearch-mode-map [delete] 'isearch-delete-char)
(define-key isearch-mode-map "\C-h" 'isearch-delete-char)

(setq dabbrev-case-fold-search nil)



(global-set-key [(control backspace)] 'backward-kill-word)

; Funktionstasten für Datei-Management

(global-set-key [f2] 'save-buffer)
(global-set-key [f3] 'find-file)

(defun load-emacs-file ()
 "find-file ~/emacs/init.el"
 (interactive)
 (find-file "~/emacs/init.el"))
(global-set-key [C-f3] 'load-emacs-file)

;(global-set-key [f4] 'speedbar)

(global-set-key [M-f4] 'save-buffers-kill-emacs)
(global-set-key [f5] 'goto-line)
;(global-set-key "\C-j" 'goto-line)


;; (setq dos-keypad-mode t)

(setq read-quoted-char-radix 10)
;; dann kann ich nämlich "C-q 2 2 3 RET" tippen,
;; um ein ß zu kriegen. 

(global-set-key [M-kp-0] 'quoted-insert)
;; oder noch leichter zu lernen :
;; Alt-0 (aber dann loslassen) und dann "223"

;;(setq grep-command "grep -noe xx *.java")


(defun scharfes-s ()
  "scharfes s"
  (interactive)
  (insert "ß")
  )

(global-set-key "\M-s" 'scharfes-s)

(global-set-key [(shift insert)] 'yank)


(global-set-key [(control delete)] 'kill-word)

;; accept 8-bit input:
(set-input-mode  (car (current-input-mode))
		 (nth 1 (current-input-mode))
		 0)


(defun tagebuch-insert-datum ()
  "insert current date and time at point"
  (interactive)
  (beginning-of-line)
  (insert "\\datum{")
  (insert (current-time-string))
  (insert "}\n")
  )

(global-set-key [\C-d] 'tagebuch-insert-datum)

;(setq auto-mode-alist
;      (append
;       '(("\\.xsd\\'" . sgml-mode))
;       auto-mode-alist ))




(global-set-key [(control f2)] 'server-edit)
(global-set-key [(control f4)] 'kill-buffer)





