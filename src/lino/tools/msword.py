#
# msword.py -- Python module for handling MS Word Documents
#
# Copyright (c) 2002, Silverback Software, LLC
#
# Brian St. Pierre, <brian @ silverback-software.com>
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose, without fee, and without a written agreement
# is hereby granted, provided that the above copyright notice and this
# paragraph and the following two paragraphs appear in all copies.
#
# IN NO EVENT SHALL THE AUTHOR BE LIABLE TO ANY PARTY FOR DIRECT,
# INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST
# PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION,
# EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE.  THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS"
# BASIS, AND THE AUTHOR HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#
# Change History
#  1 - 12/30/02 - Written
#
# Requirements
#  - win32 extensions for Python
#  - to extract content from files: MS Word
#  - to access document title: FPropSet
#    (http://www.panix.com/~dfoster/prog/office/fpropset/FPropSet.html)
#
# TODO
#  - conversion between different formats
#  - if no fpropset, fall back to Word
#

"""
This allows handling of MS Word documents.

Since we rely on automating Word for most of this, Word must be
installed on the machine in order to work properly.

This also uses FilePropertySet (FPropSet) to quickly get to file
summary information -- doesn't require waiting for Word to launch.
"""


import os

class MsWordDocument:
    def __init__(self, path=None, from_buffer=None):
        """
        This creates an MsWordDocument, but Word is not launched unless
        'content' is requested. Note that, if Word is launched, it is
        not shut down.

        path - Path to a Word document. Note that if the document does
        not have an extension, Word will "helpfully" add a .doc to the
        end. To open an extension-less document, you must add a dot to
        the end of the path. E.g. "foo" --> "foo."

        from_buffer - An in-memory buffer containing a Word
        file. E.g. the results of doing "buf = open('foo', 'rb').read()".

        Exactly one of path or from_buffer must be provided. If
        from_buffer is used, a temporary file will be created.

        Public attributes of MsWordDocument:

        title -- The title as set in document properties.
        content -- The contents of the file, as text (Unicode).
        """
        self._path = path
        if path == None and from_buffer == None:
            raise "Must provide either path or from_buffer."
        if path == None:
            # FIXME: tmpnam is a security hole. Better way??
            self._path = os.tmpnam()
            open(self._path, 'wb').write(from_buffer)
        self._title = None
        self._content = None
        return

    def _set_title(self):
        try:
            import win32com.client
        except ImportError:
            return
        # FIXME: catch 'missing FPropSet', fall back to Word.
        fps = win32com.client.Dispatch('FilePropertySet.FilePropertySet')
        fps.Pathname = self._path
        self._title = str(fps.BuiltInFileProperties().Item("Title"))
        return

    def _set_content(self):
        try:
            import win32com.client
        except ImportError:
            return
        app = win32com.client.Dispatch('Word.Application')
        doc = app.Documents.Add(self._path)
        self._content = doc.Content.Text
        doc.Close(0)
        #app.Quit()
        return

    def __getattr__(self, attr):
        if attr == 'title':
            if self._title == None:
                self._set_title()
            return self._title
        elif attr == 'content':
            if self._content == None:
                self._set_content()
            return self._content
        return self.__dict__[attr]

    def view(self):
        "Opens the file in Word (nonblocking)."
        try:
            import win32com.client
        except ImportError:
            return
        app = win32com.client.Dispatch('Word.Application')
        doc = app.Documents.Add(self._path)
        app.Visible = 1
        return

if __name__ == '__main__':
    # Yes, this test is rather fragile.
    import os
    doc = MsWordDocument(os.getcwd() + '\\test.doc')
    assert(doc.title == 'Test Document')
    assert(len(doc.content) == 296)
