;; support-w32.el
;; Author : Luc Saffre <luc.saffre@gmx.net>


;; ask for confirmation before really leaving Emacs
;; found on
;; http://www.be.gnu.org/software/emacs/windows/faq3.html#unpack :
;;(setq kill-emacs-query-functions
;;      (cons (lambda () (yes-or-no-p "Really kill Emacs? "))
;;            kill-emacs-query-functions))



;;As of Emacs 20.4.1 there is native support for maximizing, and
;;minimizing the Emacs window from Lisp, the following functions will
;;do the job for you:
(defun w32-restore-frame ()
    "Restore a minimized frame"
     (interactive)
     (w32-send-sys-command 61728))

(defun w32-maximize-frame ()
    "Maximize the current frame"
     (interactive)
     (w32-send-sys-command 61488))


;;(defun maximize-frame (frame)
;;  (w32-send-sys-command ?\xf030))

(add-hook 'window-setup-hook 'w32-maximize-frame)





;;(w32-maximize-frame)
;; does not work as expected... appearently the maximize gets scrabled
;; again when the font sizes change... but why do they change only
;; after here...?


