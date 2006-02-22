(require 'gnuserv)
(gnuserv-start)

;;By default, gnuserv will load files into new frames. If you would
;;rather have gnuserv load files into an existing frame, then evaluate
;;the following in the chosen frame:

(setq gnuserv-frame (selected-frame))

;;Placing the above in your startup file, for example, will have
;;gnuserv load files into the original Emacs frame. Note: one drawback
;;of this approach is that if the frame associated with gnuserv is
;;ever closed, gnuserv won't have a frame in which to place buffers

