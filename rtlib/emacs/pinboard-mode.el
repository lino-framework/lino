;; Code letters for interactive:
;; S -- Any symbol.
;; v -- Variable name: symbol that is user-variable-p.
;; In addition, if the string begins with `*'
;;  then an error is signaled if the buffer is read-only.
;;  This happens before reading any arguments.

(defun pinboard-insert-ref-title (title)
  "insert a [ref ] using the title of the page.

Asks for a title. The user can use TAB to expand while he types.
"
  (interactive "MTitle: ")
  (insert "ref ")
  (insert title)
  (insert "")
  )

(global-set-key [c-f1] 'pinboard-insert-ref-title)



(defun pinboard-test ()
  "just for internal testing"
  (interactive)
  (insert "window-system: ")
  (cond
   ((eq window-system 'pc)  (insert "pc"))
   ((eq window-system 'w32) (insert "w32"))
   ((eq window-system 'x)   (insert "x"))
   ((eq window-system nil)  (insert "nil"))
   (insert "error")
   )
  )

(defun pinboard-mode ()
  "Major mode for editing pinboard files."
  (interactive)
  )

(provide 'pinboard-mode)


;; window-system: w32
