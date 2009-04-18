=========
TIM Tools
=========

The TIM Tools are an easy-to-install binary distribution of some
selected command-line tools from the Lino Scripts collection.

This selection is targeted to my customers who work with 
`TIM <http://tim.saffre-rumma.ee>`_. 

:doc:`changes/index`

TIM users use mainly the following TIM Tools:

- prn2pdf.py and prnprint.py to print classical text-mode reports on printers without text support.

- sync.py makes backups and mirror copies. sync.py is a simple directory synchronizer. It is almost like `xcopy /s/d` on Windows, except that it also deletes the files on the destination that no longer exist on the source. 

- sendmail.py — reads an e-mail from a text file in standard RFC 2822 format and sends it to the recipients specified in a separate file. 

Some less often tools are:

- diag.py displays some system settings and prints out a text containing non-ASCII characters. Non-ASCII characters are handled depending on the context and your computer settings and thus might fail to display correctly.
    
- sysinfo.py creates a file sysinfo.html with a selection of technical information about your computer. 


Some other TIM Tools are now rather obsolete:

- pds2pdf.py lets TIM print business documents as PDF files

- openurl.py invokes the user's Web browser to visit a Web site of a business partner. 

- openmail.py opens the user's default mail client with a ready-to-send but not-yet-sent mail message. 

TIM Tools are available as a zip of executables for windows. 
Get it from the Download page.
On UNIX you just install the Lino and maybe write a main lino script.

