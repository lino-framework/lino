;;; cygwin32-mount.el --- Teach EMACS about cygwin32 styles and mount points.

;; Emacs Lisp Archive Entry
;; Filename: cygwin32-mount.el
;; Version: 1.0 - 2001-01-07
;; Author: Klaus Berndl <berndl@sdm.de>
;; Maintenance: Klaus Berndl <berndl@sdm.de>
;; Original author: Michael Cook <mcook@cognex.com>
;; Keywords: files, mount, cygwin
;;
;; Additional info:
;; Copyright (C) 1997 Michael Cook <mcook@cognex.com>.
;;               2001 Klaus Berndl <berndl@sdm.de>
;; Additional code by: Keisuke Mori <ksk@ntts.com>
;;                     Drew Moseley (drewmoseley@mindspring.com)
;;                     James Ganong (jeg@bigseal.ucsc.edu)
;;                     Jeff Juliano <juliano@cs.unc.edu>
;;                     Klaus Berndl <berndl@sdm.de>
;;                     
;; This file is *NOT* (yet?) part of GNU Emacs.
;;
;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 2, or (at your option)
;; any later version.
;;
;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.
;;
;; You should have received a copy of the GNU General Public License
;; along with GNU Emacs; see the file COPYING.  If not, write to the
;; Free Software Foundation, Inc., 59 Temple Place - Suite 330,
;; Boston, MA 02111-1307, USA.

;;; Commentary

;; This package does all necessary so you can use cygwin-style filenames like
;; "//D/any/path/to/file" or "/cygdrive/d/any/path/to/file" in exactly the
;; same manner as the normal Windows-style filenames like
;; "D:\any\path\to\file" or "D:/any/path/to/file".
;; Furthermore this package enables using all your cygwin-mounts in
;; file-operations. For example you can call all file-operations (e.g.
;; find-file) for a file named "/usr/bin/anyfile" if you have mounted the
;; related Windows-path to /usr/bin.
;; The package also makes sure that ange-ftp will work correct if you are
;; using cygwin32-mount.el.

;;; Installation:

;; Put in your .emacs or site-start.el file the following lines:
;;   (require 'cygwin32-mount)
;;   (cygwin32-mount-activate)

;;; Customization and using

;; + All customization is done in the customize-group `cygwin32-mount'.
;; + Activating: cygwin32-mount-activate
;; + Deactivating: cygwin32-mount-deactivate

;; ----------------------------------------------------------------------

;;; History:

;; Original version by Michael Cook <mcook@cognex.com>.
;; + modified Jun 18 1998 by Keisuke Mori <ksk@ntts.com> to make it work with
;;   ange-ftp and enable mapping a drive letter
;; + modified Oct 25 1999 by Drew Moseley (drewmoseley@mindspring.com) to
;;   support /cygdrive style drive maps and for better coexistence with
;;   ange-ftp.
;; + modified Feb 7 2000 by James Ganong (jeg@bigseal.ucsc.edu) to work when
;;   / is mounted in a subdirectory instead of top level of a drive, and to
;;   check longest directory names first, to a / mount does not shadow.
;; + modified Mar 23 2000 by Jeff Juliano <juliano@cs.unc.edu> to make a
;;   user-callable function that performs the mapping. I use this in my
;;   .emacs file to find my non-version-specific site-lisp directory since
;;   NTemacs doesn't have one in its search path.
;; + modified July 2000 by Jeff Juliano <juliano@cs.unc.edu>: ps-print to
;;   //machine/printer-name was broken. cygwin-mount would intercept and try
;;   to convert the name to a local path, even though one doesn't exist.
;;   Also, don't do mount table lookup as early as used to. warning: this
;;   isn't extensively tested, and may not be correct.
;; + modified January 2001 by Klaus Berndl (berndl@sdm.de):
;;   - Added customization
;;   - Added activating and deactivating functions (emacs-packages should not
;;     activating itself only by loading!). Deactivating removes any new
;;     filehandlers and restore the original ange-ftp function.
;;   - Added test, if mount-program exists in PATH and if system-type is
;;     windows-nt.
;;   - Corrects a bug in the longest mount point substitution (network devices
;;     like //Host/Path are now never substituted because a mount point / then
;;     would always be incorrectly substituted. Now all file-operations work
;;     correct with network devices.
;;   - corrects a bug in the /cygdrive/-style regexp.
;;   - Makes the first "real" emacs-package cygwin32-mount.el
;;   All my changes are only removing bugs and adding stuff, so this code
;;   becomes a correct emacs-package. All substantiell working code and ideas
;;   come from the other authors.

(require 'cl)

(defgroup cygwin32-mount nil
  "Proper handling of cygwin mounts and filenames."
  :prefix "cygwin32-"
  :group 'files)

;; Added by Klaus
(defun cygwin32-mount-which (filename search-paths &optional extensions)
  "Search FILENAME in SEARCH-PATHS with EXTENSIONS. SEARCH-PATHS must be a
list of pathes in string-format and EXTENSIONS a list of extensions like
\".exe\" \(note the dot!). If EXTENSIONS is nil then the extensions of the
environment variable PATHEXT are used if it exists otherwise only \"exe\" is
used as extension. Returns a list of full filenames founded in SEARCH-PATHS
with EXTENSIONS or nil if FILENAME is not found."
  (let* (;; list of extensions for FILENAME
         (exts (cond ((consp extensions)
                      extensions)
                     (t
                      (if (getenv "PATHEXT")
                          (split-string (getenv "PATHEXT") ";")
                        '(".exe")))))
         ;; list of filename concatenated with all extensions
         (progs (mapcar #'(lambda( suffix )
                            (concat filename suffix ))
                        exts))
         ;; list of lists which contains the result of the executable
         ;; testing.
         (found-path-list
          (mapcar
           #'(lambda( path )
               (mapcar
                ;; test if a file is executable
                #'(lambda( progname )
                    (let ((filename (expand-file-name progname path)))
                      (when (file-executable-p filename)
                        filename)))
                progs))
           search-paths)))
    ;; delete all the nils in the list. If FILENAME was not found then nil is
    ;; returned.
    (delete-duplicates (delete nil (apply 'append found-path-list))
                       :test 'string=)))

(defun cygwin32-mount-build-table ()
  "Determine the cygwin mount points. The returned list has the format of
`cygwin32-mount-build-table'. This function uses the cygwin mount-program to
get all mount points."
  (if (and (eq system-type 'windows-nt)
           (cygwin32-mount-which "mount" exec-path))
      (let ((buf (get-buffer-create " *mount*"))
            (case-fold-search t)
            mounts)
        (save-excursion
          (set-buffer buf)
          (erase-buffer)
          (call-process "mount" nil t)
          ;; first pass tags each line with the length of the directory
          (goto-char (point-min))
          (while (search-forward-regexp
                  "^\\([a-z]:[^ \t\n]*\\) +\\([^ \t\n]+\\)" nil t)
            (let ((device (buffer-substring (match-beginning 1)
                                            (match-end 1)))
                  (direct (file-name-as-directory (buffer-substring
                                                   (match-beginning 2)
                                                   (match-end
                                                    2)))))
              (end-of-line) (insert ( format "\t%d" (length direct )))

              ))

          ;; now sort the lines numerically
          (sort-numeric-fields -1 (point-min) (point-max))

          ;; 2nd pass builds the mount list
          (goto-char (point-min))
          (while (search-forward-regexp
                  "^\\([a-z]:[^ \t\n]*\\) +\\([^ \t\n]+\\)" nil t)
            (let ((device (buffer-substring (match-beginning 1)
                                            (match-end 1)))
                  (direct (file-name-as-directory(buffer-substring
                                                  (match-beginning 2)
                                                  (match-end
                                                   2)))))

              (setq mounts (cons (cons device direct)
                                 mounts))))

          )

        (kill-buffer buf)
        mounts)
    nil))

(defcustom cygwin32-mount-table (cygwin32-mount-build-table)
  "*Alist of cygwin32 mount points or nil if there are no mount points.
An element of the alist has the form
\(<mounted windows-device> . <cygwin-directory>), e.g.
\(\"D:\\\\programs\\\\cygwin\\bin\" . \"/usr/bin/\") or
\(\"D:/programs/cygwin\" . \"/\").
This variable is initialized with all the mount-points the
cygwin-mount-program returns, so normally you are not needed to modify this
variable. But feel free..."
  :group 'cygwin32-mount
  :type '(repeat (cons :tag "Insert a mount point"
                       (directory :tag "Mounted device")
                       (string :tag "Cygwin directory"))))



(defun cygwin32-mount-name-hook-function (operation &rest args)
  (let ((fn (get operation 'cygwin32-mount-name)))
    (if fn (apply fn operation args)
      (cygwin32-mount-run-real-handler operation args))))

(defun cygwin32-mount-map-drive-hook-function (operation &rest args)
  (let ((fn (get operation 'cygwin32-mount-map-drive)))
    (if fn (apply fn operation args)
      (cygwin32-mount-run-real-handler operation args))))

(defun cygwin32-mount-run-real-handler (operation args)
  (let ((inhibit-file-name-handlers
         (cons 'cygwin32-mount-name-hook-function
               (cons 'cygwin32-mount-map-drive-hook-function
                     (and (eq inhibit-file-name-operation operation)
                          inhibit-file-name-handlers))))
        (inhibit-file-name-operation operation))
    (apply operation args)))


(defun cygwin32-mount-name-expand (operation name &rest args)
  (cygwin32-mount-run-real-handler
   operation
   (cons (cygwin32-mount-substitute-longest-mount-name name) args)))

(defun cygwin32-mount-substitute-longest-mount-name (name)
  "If NAME uses a mount directory, substitute the mount device and return the
resulting string. Otherwise, return NAME."
  (if (string-match "^//.+" name)
      ;; Added by Klaus: if name beginns with "//" then it can never contain a
      ;; cygwin mount point! Therefore we must not check for contained mount
      ;; points because if / is mounted then this will always match and we get
      ;; an incorrect substitution for network devices like //Host/path
      name
    (let ((mounts cygwin32-mount-table)
          (len (length (file-name-as-directory name)))
          match)
      (while mounts
        (let ((mount (file-name-as-directory (cdar mounts))))
          (and (>= len (length mount))
               (string= mount
                        (file-name-as-directory
                         (substring (file-name-as-directory name)
                                    0 (length mount))))
               (or (null match)
                   (> (length (cdar mounts)) (length (cdr match))))
               (setq match (car mounts))))
        (setq mounts (cdr mounts)))
      (if match
          (concat (file-name-as-directory (car match))
                  (substring name (length (file-name-as-directory (cdr
                                                                   match)))))
        name))))

(defun cygwin32-mount-map-drive (operation name &rest args)
  "Maps cygwin-style names to the windows-style \"[A-Za-z]:/\" and calls
OPERATION with the mapped filename. NAME must have the format looks like
\"^//[A-Za-z]/\" or \"/cygdrive/[A-Za-z]/\" here."
  (cygwin32-mount-run-real-handler
   operation
   (if (string-equal (substring name 0 2) "//")
       (cons (concat (substring name 2 3) ":" (substring name 3 nil))
             args)
     (cons (concat (substring name 10 11) ":" (substring name 11 nil))
           args))))

;;; ange-ftp
(require 'ange-ftp)
;;; save the original function definition of ange-ftp-run-real-handler
(defconst cygwin32-original-ange-ftp-handler
  (symbol-function 'ange-ftp-run-real-handler))

;;; This version of ange-ftp-run-real-handler also inhibits the
;;; cygwin file name expansion when we are doing ange-ftp expansion.
;;;
;;; This is a real hack.  If the real definition of this function
;;; changes, we have to modify this function
(defun cygwin32-ange-ftp-run-real-handler (operation args)
  (let ((inhibit-file-name-handlers
         (cons 'ange-ftp-hook-function
               (cons 'ange-ftp-completion-hook-function
                     (cons 'cygwin32-mount-name-hook-function
                           (cons 'cygwin32-mount-map-drive-hook-function
                                 (and (eq inhibit-file-name-operation
                                          operation)
                                      inhibit-file-name-handlers))))))
        (inhibit-file-name-operation operation))
    (apply operation args)))

;; Added by Klaus
(defconst cygwin32-cygwin-style1-regexp "^/[^:@]*$\\|^/|/[^/:]+\\(\\'\\|/\\)")
(defconst cygwin32-cygwin-style2-regexp "^//[A-Za-z]/")
;; Support cygdrive style drive maps (note the / at the end)
(defconst cygwin32-cygwin-style3-regexp "^/cygdrive/[A-Za-z]/")

;; Added by Klaus
(defun cygwin32-mount-activate ()
  "Activates the cygwin-mount- and cygwin-style-handling"
  (interactive)
  (if (not (eq system-type 'windows-nt))
      (message "cygwin32-mount is only available for NTEmacs!")
  ;; add the cygwin-filehandlers
    (or (assoc cygwin32-cygwin-style1-regexp file-name-handler-alist)
        (setq file-name-handler-alist
              (cons `(,cygwin32-cygwin-style1-regexp
                      . cygwin32-mount-name-hook-function)
                    file-name-handler-alist)))

    (or (assoc cygwin32-cygwin-style2-regexp file-name-handler-alist)
        (setq file-name-handler-alist
              (cons `(,cygwin32-cygwin-style2-regexp
                      . cygwin32-mount-map-drive-hook-function)
                    file-name-handler-alist)))
  
    (or (assoc cygwin32-cygwin-style3-regexp file-name-handler-alist)
        (setq file-name-handler-alist
              (cons `(,cygwin32-cygwin-style3-regexp
                      . cygwin32-mount-map-drive-hook-function)
                    file-name-handler-alist)))

    ;; add cygwin-properties
    (put 'substitute-in-file-name 'cygwin32-mount-name
         'cygwin32-mount-name-expand)
    (put 'expand-file-name 'cygwin32-mount-name 'cygwin32-mount-name-expand)
    (put 'substitute-in-file-name
         'cygwin32-mount-map-drive 'cygwin32-mount-map-drive)
    (put 'expand-file-name 'cygwin32-mount-map-drive
         'cygwin32-mount-map-drive)
  
    ;; rebind ange-ftp-run-real-handler to our version
    (fset 'ange-ftp-run-real-handler 'cygwin32-ange-ftp-run-real-handler)))

;; Added by Klaus
(defun cygwin32-mount-deactivate ()
  "Deactivates the cygwin-mount- and cygwin-style-handling"
  (interactive)
  (if (not (eq system-type 'windows-nt))
      (message "cygwin32-mount is only available for NTEmacs!")
    ;; remove the cygwin-filehandlers
    (setq file-name-handler-alist
          (delete (assoc cygwin32-cygwin-style1-regexp file-name-handler-alist)
                  file-name-handler-alist))
    (setq file-name-handler-alist
          (delete (assoc cygwin32-cygwin-style2-regexp file-name-handler-alist)
                  file-name-handler-alist))
    (setq file-name-handler-alist
          (delete (assoc cygwin32-cygwin-style3-regexp file-name-handler-alist)
                  file-name-handler-alist))
    
    ;; remove the cygwin properties
    (put 'substitute-in-file-name 'cygwin32-mount-name nil)
    (put 'expand-file-name 'cygwin32-mount-name nil)
    (put 'substitute-in-file-name 'cygwin32-mount-map-drive nil)
    (put 'expand-file-name 'cygwin32-mount-map-drive nil)
    
    ;; rebind ange-ftp-run-real-handler to itÅ¥s original definition.
    (fset 'ange-ftp-run-real-handler cygwin32-original-ange-ftp-handler)))
  
(provide 'cygwin32-mount)
