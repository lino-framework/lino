Learning Vim
=============

- The Vim help screen starts with::

                            VIM - main help file
                                                                           k
          Move around:  Use the cursor keys, or "h" to go left,	       h   l
                        "j" to go down, "k" to go up, "l" to go right.	 j
    Close this window:  Use ":q<Enter>".
       Get out of Vim:  Use ":qa!<Enter>" (careful, all changes are lost!).

    Jump to a subject:  Position the cursor on a tag (e.g. |bars|) and hit CTRL-].
       With the mouse:  ":set mouse=a" to enable the mouse (in xterm or GUI).
                        Double-click the left mouse button on a tag, e.g. |bars|.
            Jump back:  Type CTRL-T or CTRL-O (repeat to go further back).


  This first contact with the famous but unusual text editor might be 
  improved by adding a hint for users of non-US keyboards.
  For example when using an Estonian keyboard, 
  it should say :kbd`CTRL-ä` instead of :kbd`CTRL-]`.


- I don't really believe the following statement of the Vim tutorial::

      NOTE: The cursor keys should also work.  But using hjkl you will be able to
      move around much faster, once you get used to it.  Really!

