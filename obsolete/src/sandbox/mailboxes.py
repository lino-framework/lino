import os, mailbox, email


"""

Note: the standard mailbox module won't support Eudora mailboxes
because they contain some information in toc files.

http://eudora2unix.sourceforge.net/

"""

eudoraDir = r"t:\data\luc\eudora"

def getAttrOrNone(msg,name):
   if msg.has_key(name):
      return msg[name]
   return None

if __name__ == "__main__":
   
   for fn in os.listdir(eudoraDir):
      (root,ext) = os.path.splitext(fn)
      if ext == '.mbx':
         pfn = os.path.join(eudoraDir,fn)
         print "\nfound mailbox %s\n" % pfn
         f = file(pfn)
         mb = mailbox.PortableUnixMailbox(f,email.Message)
         count = 0
         while True:
            msg = mb.next()
            if msg is None:
               break
            print getAttrOrNone(msg,'date'),\
                  getAttrOrNone(msg,'from'),\
                  getAttrOrNone(msg,'to'),\
                  getAttrOrNone(msg,'subject')
            count += 1
         print "\n%s contains %d messages\n" % (fn,count)


