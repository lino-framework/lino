import getopt, sys
import uno

from unohelper import Base, systemPathToFileUrl, absolutize
from os import getcwd
from os.path import splitext
from com.sun.star.beans import PropertyValue
from com.sun.star.uno import Exception as UnoException
from com.sun.star.io import IOException, XOutputStream

class OutputStream( Base, XOutputStream ):
    def __init__( self ):
        self.closed = 0
    def closeOutput(self):
        self.closed = 1
    def writeBytes( self, seq ):
        sys.stdout.write( seq.value )
    def flush( self ):
        pass

def main():
    retVal = 0
    doc = None
    stdout = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:",
            ["help", "connection-string=" , "html", "pdf", "stdout" ])
        
    except getopt.GetoptError,e:
        sys.stderr.write( str(e) + "\n" )
        usage()
        return 1

        url = "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"
        filterName = "Text (Encoded)"
        extension  = "txt"
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
                sys.exit()
            if o in ("-c", "--connection-string" ):
                url = "uno:" + a + ";urp;StarOffice.ComponentContext"
            if o == "--html":
                filterName = "HTML (StarWriter)"
                extension  = "html"
            if o == "--pdf":
                filterName = "writer_pdf_Export"
                extension  = "pdf"
            if o == "--stdout":
                stdout = True
                
        if not len(args):
            usage()
            sys.exit()
              
        ctxLocal = uno.getComponentContext()
        smgrLocal = ctxLocal.ServiceManager

        resolver = smgrLocal.createInstanceWithContext(
                 "com.sun.star.bridge.UnoUrlResolver", ctxLocal )
        ctx = resolver.resolve( url )
        smgr = ctx.ServiceManager

        desktop = smgr.createInstanceWithContext(
            "com.sun.star.frame.Desktop", ctx )

        cwd = systemPathToFileUrl( getcwd() )
        outProps = (
            PropertyValue( "FilterName" , 0, filterName , 0 ),
            PropertyValue( "Overwrite" , 0, True , 0 ),
            PropertyValue( "OutputStream", 0, OutputStream(), 0)
            )
        
        inProps = PropertyValue( "Hidden" , 0 , True, 0 ),
        for path in args:
            try:
                fileUrl = absolutize( cwd, systemPathToFileUrl(path) )
                doc = desktop.loadComponentFromURL( fileUrl ,
                                                    "_blank", 0,
                                                    inProps )

                if not doc:
                    raise UnoException(
                        "Couldn't open stream for unknown reason",
                        None )

                if not stdout:
                    (dest, ext) = splitext(path)
                    dest = dest + "." + extension
                    destUrl = absolutize( cwd, systemPathToFileUrl(dest) )
                    sys.stderr.write(destUrl + "\n")
                    doc.storeToURL(destUrl, outProps)
                else:
                    doc.storeToURL("private:stream",outProps)
            except IOException, e:
                sys.stderr.write(
                    "Error during conversion: " + e.Message + "\n" )
                retVal = 1
            except UnoException, e:
                sys.stderr.write( "Error ("+repr(e.__class__)
                                  +") during conversion:"
                                  + e.Message + "\n" )
                retVal = 1
            if doc:
                doc.dispose()

    except UnoException, e:
        sys.stderr.write( "Error ("+repr(e.__class__)+") :"
                          + e.Message + "\n" )
        return 1
    return retVal
    
def usage():
    sys.stderr.write( "usage: ooextract.py --help | --stdout\n"+
                  "       [-c <connection-string> | --connection-string=<connection-string>\n"+
          "       [--html|--pdf]\n"+
          "       [--stdout]\n"+
                  "       file1 file2 ...\n"+
                  "\n" +
                  "Extracts plain text from documents and prints it to a file (unless --stdout is specified).\n" +
                  "Requires an OpenOffice.org instance to be running. The script and the\n"+
                  "running OpenOffice.org instance must be able to access the file with\n"+
                  "by the same system path. [ To have a listening OpenOffice.org instance, just run:\n"+
          "openoffice \"-accept=socket,host=localhost,port=2002;urp;\" \n"
                  "\n"+
          "--stdout \n" +
          "         Redirect output to stdout. Avoids writing to a file directly\n" + 
                  "-c <connection-string> | --connection-string=<connection-string>\n" +
                  "        The connection-string part of a uno url to where the\n" +
                  "        the script should connect to in order to do the conversion.\n" +
                  "        The strings defaults to socket,host=localhost,port=2002\n"
                  "--html \n"
                  "        Instead of the text filter, the writer html filter is used\n"
                  "--pdf \n"
                  "        Instead of the text filter, the pdf filter is used\n"
                  )

sys.exit(main())
