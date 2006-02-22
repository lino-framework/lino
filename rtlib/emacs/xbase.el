;;; xbase.el --- A mode for editing Xbase programs.
;; Copyright (C) 2002 Mike Romberg <romberg@fsl.noaa.gov> and
;;                    Dave Pearson <davep@davep.org>
;; $Id: xbase.el,v 1.38 2002/07/15 23:18:00 davep Exp $

;; xbase.el is free software distributed under the terms of the GNU General
;; Public Licence, version 2. For details see the file COPYING.

;;; Commentary:
;;
;; xbase.el provides a mode for editing Xbase source code. xbase.el mostly
;; supports programs written for CA-Clipper and Clipper compatible compilers
;; (for example, harbour <URL:http://www.harbour-project.org/>) although,
;; where possible, support for other Xbase dialects will be added.
;;
;; You can always find the latest version of xbase.el at:
;;
;; <URL:http://cvs.sourceforge.net/cgi-bin/viewcvs.cgi/xbasemode/xbasemode/xbase.el?rev=HEAD>

;;; THANKS:
;;

;;; BUGS:
;;
;; o The indentation code is easily confused by multi-statement lines. For
;;   example, this code:
;;
;;      For n := 1 To 10; Next
;;
;;   will look like an unclosed For...Next loop.
;;
;; o No support for the [] string delimiters.

;;; TODO:
;;
;; o Fix all bugs.
;;
;; o Fully document.
;;
;; o Add OO oriented indentation support.
;;
;; o Provide function for `forward-sexp-function'.
;;
;; o Pre-processor indentation is a bit of a kludge. Actually, I'm starting
;;   to wonder if the indentation "engine" could do with a total overhaul.

;;; INSTALLATION:
;;
;; o Drop xbase.el somewhere into your `load-path'. Try your site-lisp
;;   directory for example. You might also want to consider byte compiling
;;   the file to produce xbase.elc (see `byte-compile-file' in your emacs
;;   documentation).
;;
;; o Add an autoload to ~/.emacs, for example:
;;
;;   (autoload 'xbase-mode "xbase" "Xbase mode" t)
;;
;; o Add the following to ~/.emacs to ensure that xbase-mode is used when
;;   you edit Xbase code:
;;
;;   (setq auto-mode-alist (cons (cons "\\.\\(prg\\|ch\\)$" 'xbase-mode) auto-mode-alist))

;;; Code:

;; Things we need:
(eval-when-compile
  (require 'cl))
(require 'font-lock)

;; Attempt to handle older/other emacs.
(eval-and-compile
  ;; If customize isn't available just use defvar instead.
  (unless (fboundp 'defgroup)
    (defmacro defgroup  (&rest rest) nil)
    (defmacro defcustom (symbol init docstring &rest rest)
      `(defvar ,symbol ,init ,docstring))))

;; General customize options.

(defgroup xbase nil
  "Mode for editing Xbase source."
  :group 'languages
  :prefix "xbase-")

(defcustom xbase-mode-indent 2
  "*Default indentation per nesting level"
  :type 'integer
  :group 'xbase)

(defcustom xbase-indent-rules
;;   Rule Name            RegExp                          Opening Rule         Closing Rule       Offset   Subsequent Offset  Is Statement?
  '((xbase-if             "^[\t ]*if"                     nil                  xbase-endif        nil      nil                t)
    (xbase-else           "^[\t ]*else\\(if\\)?"          xbase-if             xbase-endif        nil      nil                t)
    (xbase-endif          "^[\t ]*end[\t ]*if"            xbase-if             nil                nil      nil                t)
    (xbase-hash-if        "^[\t ]*#if"                    nil                  xbase-hash-endif   0        nil                nil)
    (xbase-hash-else      "^[\t ]*#else\\(if\\)?"         xbase-hash-if        xbase-hash-endif   0        nil                nil)
    (xbase-hash-endif     "^[\t ]*#end[\t ]*if"           xbase-hash-if        nil                0        nil                nil)
    (xbase-do-case        "^[\t ]*do[\t ]+case"           nil                  xbase-end-case     nil      nil                t)
    (xbase-case           "^[\t ]*\\(case\\|otherwise\\)" xbase-do-case        xbase-end-case     +        nil                t)
    (xbase-end-case       "^[\t ]*endcase"                xbase-do-case        nil                nil      nil                t)
    (xbase-for            "^[\t ]*for"                    nil                  xbase-next         nil      nil                t)
    (xbase-next           "^[\t ]*next"                   xbase-for            nil                nil      nil                t)
    (xbase-do-while       "^[\t ]*\\(do[\t ]*\\)?while"   nil                  xbase-enddo        nil      nil                t)
    (xbase-enddo          "^[\t ]*enddo"                  xbase-do-while       nil                nil      nil                t)
    (xbase-begin-sequence "^[\t ]*begin[\t ]+sequence"    nil                  xbase-end-sequence nil      nil                t)
    (xbase-break          "^[\t ]*break"                  xbase-begin-sequence xbase-end-sequence +        -                  t)
    (xbase-recover        "^[\t ]*recover"                xbase-begin-sequence xbase-end-sequence nil      nil                t)
    (xbase-end-sequence   "^[\t ]*end[\t ]+sequence"      xbase-begin-sequence nil                nil      nil                t)
    (xbase-text           "^[\t ]*text"                   nil                  xbase-endtext      nil      0                  t)
    (xbase-endtext        "^[\t ]*endtext"                xbase-text           nil                nil      nil                t)
    (xbase-local          "^[\t ]*local"                  xbase-defun          xbase-defun        nil      nil                t)
    (xbase-defun          "^[\t ]*\\(static\\|init\\|exit\\)?[\t ]*\\(procedure\\|function\\)[\t ]+\\(\\w+\\)[\t ]*(?" xbase-defun xbase-defun nil nil t))
  "*Rules for indenting Xbase code."
  :type '(repeat (list    :tag "Indentation rule"
                  (symbol :tag "Rule name")
                  (regexp :tag "Regular expression for matching code")
                  (symbol :tag "Name of opening rule")
                  (symbol :tag "Name of closing rule")
                  (choice :tag "Extra offset for this statement"
                   (const :tag "Add one extra level of indentation" +)
                   (const :tag "Remove one level of indentation" -)
                   (const :tag "Remove all indentation" 0)
                   (const :tag "Use the calculated indentation level" nil))
                  (choice :tag "Extra offset for subsequent lines of code"
                   (const :tag "Add one extra level of indentation" +)
                   (const :tag "Remove one level of indentation" -)
                   (const :tag "Remove all indentation" 0)
                   (const :tag "Use the calculated indentation level" nil))))
  :group 'xbase)

;; Indentation rules functions:

(defsubst xbase-rule (rule)
  (if (symbolp rule)
      (assoc rule xbase-indent-rules)
    rule))

(defsubst xbase-rule-name (rule)
  (nth 0 (xbase-rule rule)))

(defsubst xbase-rule-regexp (rule)
  (nth 1 (xbase-rule rule)))

(defsubst xbase-rule-opening-rule (rule)
  (nth 2 (xbase-rule rule)))

(defsubst xbase-rule-closing-rule (rule)
  (nth 3 (xbase-rule rule)))

(defsubst xbase-rule-offset (rule)
  (nth 4 (xbase-rule rule)))

(defsetf xbase-rule-offset (rule) (store)
  `(setf (nth 4 (xbase-rule ,rule)) ,store))

(defsubst xbase-rule-subsequent-offset (rule)
  (nth 5 (xbase-rule rule)))

(defsetf xbase-rule-subsequent-offset (rule) (store)
  `(setf (nth 5 (xbase-rule ,rule)) ,store))

(defsubst xbase-rule-statement-p (rule)
  (nth 6 (xbase-rule rule)))

(defsetf xbase-rule-statement-p (rule) (store)
  `(setf (nth 6 (xbase-rule ,rule)) ,store))

(defsubst xbase-rule-opening-p (rule)
  (let ((rule (xbase-rule rule)))
    (and (not (xbase-rule-opening-rule rule))
         (xbase-rule-closing-rule rule))))

(defsubst xbase-rule-closing-p (rule)
  (let ((rule (xbase-rule rule)))
    (and (xbase-rule-opening-rule rule)
         (not (xbase-rule-closing-rule rule)))))

(defsubst xbase-rule-interim-p (rule)
  (let ((rule (xbase-rule rule)))
    (and (xbase-rule-opening-rule rule)
         (xbase-rule-closing-rule rule))))

(defsubst xbase-rule-opening-regexp (rule)
  (let ((rule (xbase-rule rule)))
    (if (xbase-rule-opening-p rule)
        (xbase-rule-regexp rule)
      (xbase-rule-regexp (xbase-rule (xbase-rule-opening-rule rule))))))

(defsubst xbase-rule-closing-regexp (rule)
  (let ((rule (xbase-rule rule)))
    (if (xbase-rule-closing-p rule)
        (xbase-rule-regexp rule)
      (xbase-rule-regexp (xbase-rule (xbase-rule-closing-rule rule))))))

(defun xbase-set-offset (rule-name offset)
  (let ((rule (xbase-rule rule-name)))
    (if rule
        (setf (xbase-rule-offset rule) offset)
      (error "%s is not a valid indent rule" rule-name))))

(defun xbase-set-subsequent-offset (rule-name offset)
  (let ((rule (xbase-rule rule-name)))
    (if rule
        (setf (xbase-rule-subsequent-offset rule) offset)
      (error "%s is not a valid indent rule" rule-name))))

(defun xbase-add-rule (name regexp opening-rule closing-rule is-statement &optional offset subsequent-offset)
  "Add a new rule to xbase-mode's identation rules.

NAME is a symbol that is the name of the rule.
REGEXP is a regular expression for checking a line matches the rule.
OPENING-RULE is the name of a rule that is the opening for this line type.
CLOSING-RULE is the name of a rule that is the closing for this line type.
If IS-STATEMENT is non-nil then the rule will be be for a statement.
OFFSET is an optional offset value for indenting a line matching this rule.
SUBSEQUENT-OFFSET is an optional offset value for indenting subsequent lines.

Example:

If you write your Xbase code so that you only have one RETURN statement in a
function or procedure and you want the RETURN statement to be indented to
the 0th column you could use this function to add such a rule:

  (xbase-add-rule 'xbase-return \"^[\\t ]*return\" 'xbase-defun nil t 0)

Calling this function updates `xbase-indent-rules'."
  (unless (xbase-rule name)
    (nconc xbase-indent-rules (list (list name regexp opening-rule closing-rule offset subsequent-offset is-statement)))))

;; Functions for calculating indentation.

(defun xbase-calculate-indent-with-offset (indent offset)
  "Calculate the indentation level given INDENT and OFFSET.

INDENT is the intended indentation level.
If OFFSET is nil then INDENT is returned.
If OFFSET is a number then that value will be returned, minus
`xbase-mode-indent'.
If OFFSET is `+' or `-' INDENT will be either increased or decreased by
`xbase-mode-indent'."
  (cond ((null offset)                  ; No offset.
         indent)
        ((numberp offset)               ; Specific column.
         (- offset xbase-mode-indent))
        ((fboundp offset)               ; + and - are used as functions.
         (+ indent (funcall offset xbase-mode-indent)))
        (t
         (error "'%s' is not a valid offset" offset))))

(defun xbase-continuation-line-p ()
  "Is the current line of code a continuation of the previous line?"
  (save-excursion
    (beginning-of-line)
    (unless (bobp)
      (forward-line -1)
      (looking-at "^.*;[\t ]*$"))))

(defun xbase-beginning-of-line ()
  "Goto the start of the current line of code."
  (beginning-of-line)
  (while (and (not (bobp)) (xbase-continuation-line-p))
    (forward-line -1)))

(defun xbase-previous-line ()
  "Goto the start of the previous line of code."
  (xbase-beginning-of-line)
  (unless (bobp)
    (forward-line -1)
    (xbase-beginning-of-line)))

(defun xbase-find-matching-statement (rule)
  "Find the opening statement for a block statement of RULE type."
  (let ((level            1)
        (case-fold-search t)            ; Xbase is case insensitive.
        (open-re          (xbase-rule-opening-regexp rule))
        (close-re         (xbase-rule-closing-regexp rule)))
    (beginning-of-line)
    (while (not (or (bobp) (zerop level)))
      (xbase-previous-line)
      (cond ((looking-at close-re)
             (incf level))
            ((looking-at open-re)
             (decf level))))))

(defun xbase-current-line-match ()
  "Does the current line match anything in `xbase-indent-rules'?"
  (save-excursion
    (xbase-beginning-of-line)
    (let ((case-fold-search t))         ; Xbase is case insensitive.
      (loop for rule in xbase-indent-rules
            when (looking-at (xbase-rule-regexp rule))
            return rule))))

(defun xbase-find-statement-backward ()
  "Find a statement, looking at the current line and then working backwards."
  (loop for match = (xbase-current-line-match)
        until (or (bobp) (and match (xbase-rule-statement-p match)))
        do (xbase-previous-line)
        finally return match))

(defun xbase-find-some-statement-backward (test)
  "Find a statement which satisfies TEST.

This function looks at the current line and then works backwards."
  (loop for match = (xbase-find-statement-backward)
        while (and (not (bobp)) match (not (funcall test match)))
        do (progn
             (when (xbase-rule-closing-p match)
               (xbase-find-matching-statement match))
             (xbase-previous-line))
        finally return match))

(defun xbase-find-opening-statement-backward ()
  "Find a block opening statement.

This function looks at the current line and then works backwards."
  (xbase-find-some-statement-backward #'(lambda (rule) (xbase-rule-opening-p rule))))

(defun xbase-find-opening/interim-statement-backward ()
  "Find a block opening or interim statement.

This function looks at the current line and then works backwards."
  (xbase-find-some-statement-backward #'(lambda (rule) (not (xbase-rule-closing-p rule)))))

(defun xbase-some-statement-indentation (statement-type)
  "Get the indentation level of previous statement of STATEMENT-TYPE.

This function works backwards from the previous line."
  (save-excursion
    (let ((match (unless (bobp)
                   (xbase-previous-line)
                   (funcall statement-type))))
      (cond (match
             (message "Matched to %s" (xbase-rule-name match))
             (xbase-calculate-indent-with-offset (current-indentation) (xbase-rule-subsequent-offset match)))
            (t
             (message "No matches found")
             (- xbase-mode-indent))))))

(defun xbase-previous-opening-statement-indentation ()
  "Get the indentation level of previous opening statement.

This function works backwards from the previous line."
  (xbase-some-statement-indentation #'xbase-find-opening-statement-backward))

(defun xbase-previous-opening/interim-statement-indentation ()
  "Get the indentation level of previous opening or interim statement.

This function works backwards from the previous line."
  (xbase-some-statement-indentation #'xbase-find-opening/interim-statement-backward))

(defun xbase-matching-statement-indentation (rule)
  "Return the indentation level of the opening RULE type statement."
  (save-excursion
    (xbase-find-matching-statement rule)
    (message "Matched to %s" (xbase-rule-name (xbase-current-line-match)))
    (current-indentation)))

(defun xbase-indent-level ()
  "Return the indentation level to be used for the current line of code."
  (save-excursion
    (let ((match (xbase-current-line-match)))
      (if match
          ;; We're on a statement.
          (cond ((numberp (xbase-rule-offset match))
                 ;; Specific column.
                 (message "Fixed at %d" (xbase-rule-offset match))
                 (xbase-rule-offset match))
                ((xbase-rule-opening-p match)
                 ;; It's a block opening, indent it relative to the previous
                 ;; block opening statement.
                 (+ (xbase-previous-opening/interim-statement-indentation) xbase-mode-indent))
                ((xbase-rule-closing-p match)
                 ;; It's a closing statement, indent it to the same indentation
                 ;; level as its opening statement.
                 (xbase-matching-statement-indentation match))
                (t
                 ;; It's an "interim" statement.
                 (xbase-calculate-indent-with-offset (xbase-previous-opening-statement-indentation) (xbase-rule-offset (xbase-current-line-match)))))
        ;; We're on a "normal" line of code, indent it to the previous
        ;; opening/interim statement.
        (+ (xbase-previous-opening/interim-statement-indentation) xbase-mode-indent)))))

(defun xbase-indent-line (&optional whole-exp)
  "Indent current line of Xbase code.

Note: WHOLE-EXP is currently ignored."
  (interactive "p")
  (let ((pos (- (point-max) (point))))
    (back-to-indentation)
    (let ((indent-level (xbase-indent-level)))
      (when (/= (current-column) indent-level)
        (beginning-of-line)
        (delete-horizontal-space)
        (indent-to indent-level)))
    (let ((target-pos (- (point-max) pos)))
      (when (> target-pos (point))
        (setf (point) target-pos)))))

;; Useful commands for use in xbase-mode.

(defun xbase-describe-line ()
  "Describe the current line."
  (interactive)
  (let ((match (xbase-current-line-match)))
    (if match
        (message "This line matches the %s rule" (xbase-rule-name match))
      (message "This is an ordinary line of code"))))

;; xbase-mode customize options.

(defcustom xbase-mode-hook nil
  "*List of hooks to execute on entry to `xbase-mode'."
  :type  'hook
  :group 'xbase
  )

;; xbase-mode keyboard map.

(defvar xbase-mode-map
  (let ((map (make-sparse-keymap)))
    (define-key map [(control c) (control l)] #'xbase-describe-line)
    map)
  "Keymap used in `xbase-mode'.")

;; xbase-mode non-customizable variables.

(defvar xbase-mode-syntax-table
  (let ((st (make-syntax-table)))
    (modify-syntax-entry ?_  "w"      st)
    (modify-syntax-entry ?#  "w"      st) ; So that PP stuff font locks correctly. TODO: Is this the right thing to do?
    (modify-syntax-entry ?\' "\""     st) ; "'" is a string delimiter.
    (modify-syntax-entry ?/  ". 124b" st) ; Enable "//" and "/**/" comments.
    (modify-syntax-entry ?*  ". 23"   st) ; Ditto.
    (modify-syntax-entry ?&  ". 12b"  st) ; Enable "&&" comments.
    (modify-syntax-entry ?\n "> b"    st) ; New line ends "//" and "&&" comments.
    st)
  "`xbase-mode' syntax table.")

;; xbase-mode font lock customize options.

(defcustom xbase-font-lock-statements
  '("announce"
    "begin" "sequence" "break" "recover" "using" "end" "sequence"
    "declare"
    "default"
    "do"
    "case" "otherwise" "endcase"
    "while" "exit" "loop" "enddo"
    "procedure"
    "field" "in" "local" "memvar" "return"
    "external"
    "for" "to" "step" "next"
    "static" "function" "local"
    "create" "class" "inherit" "from" "method" "access" "assign" "endclass"
    "if" "else" "elseif" "endif"
    "init"
    "parameters"
    "private"
    "public"
    "request")
  "*Xbase statements for font locking."
  :type  '(repeat string)
  :group 'xbase)

(defcustom xbase-font-lock-directives
  '("command" "xcommand" "translate" "xtranslate"
    "define"
    "error"
    "ifdef" "ifndef" "else" "endif"
    "include"
    "stdout"
    "undef")
  "*Xbase directives for font locking."
  :type  '(repeat string)
  :group 'xbase)

(defcustom xbase-font-lock-logic
  '("and" "or" "not")
  "*Xbase logic operators for font locking."
  :type  '(repeat string)
  :group 'xbase)

(defcustom xbase-font-lock-commands
  '("text" "endtext")                   ; TODO: Lots more to add.
  "*Xbase commands for font locking."
  :type  '(repeat string)
  :group 'xbase)

(defcustom xbase-keyword-face 'font-lock-keyword-face
  "*Face to use for Xbase keywords."
  :type  'face
  :group 'xbase)

(defcustom xbase-directive-face 'font-lock-builtin-face
  "*Face to use for Xbase pre-processor directives."
  :type  'face
  :group 'xbase)

(defcustom xbase-command-face 'font-lock-keyword-face
  "*Face to use for Xbase commands."
  :type  'face
  :group 'xbase)

(defcustom xbase-function-name-face 'font-lock-function-name-face
  "*Face to use for function names."
  :type  'face
  :group 'xbase)

(defcustom xbase-variable-name-face 'font-lock-variable-name-face
  "*Face to use for variable names."
  :type  'face
  :group 'xbase)

(defcustom xbase-constant-face 'font-lock-constant-face
  "*Face to use for constants."
  :type  'face
  :group 'xbase)

(defcustom xbase-logic-face 'font-lock-builtin-face
  "*Face to use for logic operators"
  :type  'face
  :group 'xbase)

;; xbase-mode code.

(defun xbase-end-of-defun ()
  "Place `point' on what looks like the end of the current defun.

This function is used by `xbase-mode' as the value for
`end-of-defun-function'. This makes \\[end-of-defun] work in Xbase buffers."
  (flet ((defunp ()
           (eq (xbase-rule-name (xbase-current-line-match)) 'xbase-defun)))
    (when (defunp)                      ; If we're on the start of a function.
      (forward-line 1))                 ; skip forward a line.
    ;; Look for the start of another function or the end of the buffer.
    (while (not (or (eobp) (defunp)))
      (forward-line 1))
    ;; If we're on a defun, back up one line.
    (when (defunp)
      (forward-line -1))))

(print "ok")

;;;###autoload
(defun xbase-mode ()
  "Major mode for editing Xbase source files.

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


;;; xbase.el ends here


