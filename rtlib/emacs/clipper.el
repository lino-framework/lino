(defun clipper-mode ()
  "Major mode for editing Clipper source files.

Special commands:

\\{xbase-mode-map}"
  (interactive)
  (kill-all-local-variables)
  (use-local-map xbase-mode-map)
  (make-local-variable 'indent-line-function)
  (make-local-variable 'font-lock-defaults)
  (make-local-variable 'defun-prompt-regexp)
  (make-local-variable 'end-of-defun-function)
  (setq major-mode            'xbase-mode
        mode-name             "Xbase"
        indent-line-function  #'xbase-indent-line
        defun-prompt-regexp   (xbase-rule-regexp 'xbase-defun)
        end-of-defun-function #'xbase-end-of-defun
        font-lock-defaults    (list
                               (list

                                ;; The first few entries deal with lists that
                                ;; the user can configure.

                                ;; User configurable list of statements.
                                (list (regexp-opt xbase-font-lock-statements 'words) 1 xbase-keyword-face)

                                ;; User configurable list of pre-processor directives.
                                (list (concat "\\<#" (regexp-opt xbase-font-lock-directives t) "\\>") 1 xbase-directive-face)

                                ;; User configurable list of commands.
                                (list (regexp-opt xbase-font-lock-commands 'words) 1 xbase-command-face)

                                ;; User configurable list of logic operators
                                (list (concat "\\." (regexp-opt xbase-font-lock-logic 'words) "\\.") 1 xbase-logic-face)

                                ;; Now for some "hard wired" rules.

                                ;; "defun" function names.
                                (list "\\<\\(function\\|procedure\\|method\\|access\\|assign\\|class\\|inherit\\|from\\)\\>\\s-\\<\\(\\w*\\)\\>" 2 xbase-function-name-face)

                                ;; #define/ifdef/ifndef "constant" name.
                                (list "#[ \t]*\\(define\\|ifn?def\\)[ \t]+\\(\\sw+\\)" 2 xbase-variable-name-face)

                                ;; Common constants.
                                (list "\\(\\.\\(f\\|\\t\\)\\.\\|\\<\\(nil\\|self\\|super\\)\\>\\)" 0 xbase-constant-face)

                               )
                               nil t))
  (set-syntax-table xbase-mode-syntax-table)
  (run-hooks 'xbase-mode-hook))

