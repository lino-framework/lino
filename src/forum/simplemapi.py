# http://www.kirbyfooty.com/simplemapi.py
# Author Ian Cook <ian@kirbyfooty.com>
import os
from ctypes import *

FLAGS = c_ulong
LHANDLE = c_ulong
LPLHANDLE = POINTER(LHANDLE)


# Return codes
SUCCESS_SUCCESS = 0
# Recipient class
MAPI_ORIG = 0
MAPI_TO = 1


NULL = c_void_p(None)


class MapiRecipDesc(Structure):
    _fields_ = [('ulReserved', c_ulong),
               ('ulRecipClass', c_ulong),
               ('lpszName', c_char_p),
               ('lpszAddress', c_char_p),
               ('ulEIDSize', c_ulong),
               ('lpEntryID', c_void_p),
              ]
lpMapiRecipDesc = POINTER(MapiRecipDesc)


class MapiFileDesc(Structure):
    _fields_ = [('ulReserved', c_ulong),
               ('flFlags', c_ulong),
               ('nPosition', c_ulong),
               ('lpszPathName', c_char_p),
               ('lpszFileName', c_char_p),
               ('lpFileType', c_void_p),
              ]
lpMapiFileDesc = POINTER(MapiFileDesc)


class MapiMessage(Structure):
    _fields_ = [('ulReserved', c_ulong),
               ('lpszSubject', c_char_p),
               ('lpszNoteText', c_char_p),
               ('lpszMessageType', c_char_p),
               ('lpszDateReceived', c_char_p),
               ('lpszConversationID', c_char_p),
               ('flFlags', FLAGS),
               ('lpOriginator', lpMapiRecipDesc), # ignored?
               ('nRecipCount', c_ulong),
               ('lpRecips', lpMapiRecipDesc),
               ('nFileCount', c_ulong),
               ('lpFiles', lpMapiFileDesc),
              ]
lpMapiMessage = POINTER(MapiMessage)


MAPI = windll.mapi32


MAPISendMail=MAPI.MAPISendMail
MAPISendMail.restype = c_ulong          # Error code
MAPISendMail.argtypes = (LHANDLE,       # lhSession
                        c_ulong,       # ulUIParam
                        lpMapiMessage, # lpMessage
                        FLAGS,         # lpFlags
                        c_ulong,       # ulReserved
                        )


def SendMail(recipient, subject, body, attachfiles):
    """Post an e-mail message using Simple MAPI


    recipient - string: address to send to (multiple address sperated with a semicolon)
    subject - string: subject header
    body - string: message text
    attach - string: files to attach (multiple attachments sperated with a semicolin)

    Example usage
    import simplemapi
    simplemapi.SendMail("to1address@server.com;to2address@server.com","My Subject","My message body","c:\attachment1.txt;c:\attchment2")
    
    
    """
    
    # get list of file attachments
    attach = []
    AttachWork = attachfiles.split(';')
    
    #verify the attachment file exists
    for file in AttachWork:
        if os.path.exists(file):
            attach.append(file)

    
    attach = map( os.path.abspath, attach )
    nFileCount = len(attach)
    
    if attach: 
        MapiFileDesc_A = MapiFileDesc * len(attach) 
        fda = MapiFileDesc_A() 
        for fd, fa in zip(fda, attach): 
            fd.ulReserved = 0 
            fd.flFlags = 0 
            fd.nPosition = -1 
            fd.lpszPathName = fa 
            fd.lpszFileName = None 
            fd.lpFileType = None 
        lpFiles = fda
    else:
       # No attachments
        lpFiles = cast(NULL, lpMapiFileDesc) # Make NULL

    # Get the number of recipients
    RecipWork = recipient.split(';')
    RecipCnt = len(RecipWork)

    # Formulate the recipients
    MapiRecipDesc_A = MapiRecipDesc * len(RecipWork) 
    rda = MapiRecipDesc_A() 
    for rd, ra in zip(rda, RecipWork): 
        rd.ulReserved = 0 
        rd.ulRecipClass = MAPI_TO
        rd.lpszName = None
        rd.lpszAddress = ra
        rd.ulEIDSize = 0
        rd.lpEntryID = None
    recip = rda

    # send the message   
    msg = MapiMessage(0, subject, body, None, None, None, 0,
                     cast(NULL, lpMapiRecipDesc), RecipCnt, recip,
                     nFileCount, lpFiles)    
   

    rc = MAPISendMail(0, 0, byref(msg), 0, 0)
    if rc != SUCCESS_SUCCESS:
        raise WindowsError, "MAPI error %i" % rc

