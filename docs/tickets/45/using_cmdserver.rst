A "command server" on each client
=================================

On a Windows machine, if we manually type in a DOS box::

  start http://lino/media/webdav/userdocs/test.rtf
  
then we get the expected result.

So one workaround might be to have a small "cmdserver" 
daemon that clients need to install and run on their machine,
at least if they want the feature of editing .rtf files.

This would be a minimal HTTP server which would react to a GET `http://localhost:8910/userdocs/test.rtf` by executing the 
corresponding file.    
Here is a functional but neither secure nor user-friendly 
proof-of-concept implementation of such a daemon:

.. literalinclude:: cmdserver.py
   
        
We could make the `cmdserver` method more user-friendly and secure, 
but it still remains a very strange workaround. 

But is there really no easier solution?
For many system administrators it is not a solution at all since 
installing such a command server on each client causes additional 
complexity as well as security risks.



