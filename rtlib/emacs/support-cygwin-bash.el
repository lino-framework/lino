;; support-cygwin-bash.el
;; Author: Luc Saffre <luc.saffre@gmx.net>



(setq Info-default-directory-list '
      (
       "u:/cygwin/usr/info/"
       "/cygdrive/s/emacs/info/"
       ))

;;( Info-directory-list)




;WARNING:The latest version of bash sets and uses the environment
;variable PID. For some as yet unknown reason, if PID is set and Emacs
;passes it on to bash subshells, bash croaks (Emacs can inherit the
;PID variable if it's started from a bash shell). If you clear the PID
;variable in your startup file, you should be able to continue to use
;bash as your subshell: (12/18/97)

(setenv "PID" nil)



;; from http://www.be.gnu.org/software/emacs/windows/faq7.html#shell
;;Alternatively, if you do not want to mess with the SHELL or COMSPEC
;;variables, you can explicitly place the following in your startup
;;file: For the interactive shell
(setq explicit-shell-file-name "u:/cygwin/bin/bash.exe")
;; For subprocesses invoked via the shell (e.g., "shell -c command")
(setq shell-file-name "u:/cygwin/bin/bash.exe")




;; using Cygwin bash instead of command.com 
(defun my-shell-setup ()
  "For bash (cygwin 18) under Emacs 20"
  (setq comint-scroll-show-maximum-output 'this)
  (setq comint-completion-addsuffix t)
  ;; (setq comint-process-echoes t)
  ;; reported that this is no longer needed
  (setq comint-eol-on-send t)
  ;; (setq w32-quote-process-args \")
  (make-variable-buffer-local 'comint-completion-addsuffix))

;(add-hook shell-mode-hook 'my-shell-setup)
(setq shell-mode-hook 'my-shell-setup)

;(setq process-coding-system-alist (cons '("bash" . raw-text-unix)
;                                        process-coding-system-alist))


;; Justus Noll
;; Ausgabe von ^M in der Shell filtern
(add-hook 
 'comint-output-filter-functions 
 'shell-strip-ctrl-m nil t)


