"""
start the user's mail client with a ready-to-send message.

USAGE : openmail FILE

where FILE describes the contents of the message using a simplified
pseudo RFC822 format.  Supported message header fields are "to" and
"subject", and the "body".  "to" is mandatory, the other fields are
optional.

See also :pageref:`/docs/openmail`.

"""

import sys

from lino.timtools.mail import readmail, openmail

def main(argv):
	if len(argv) != 1:
		print __doc__
		sys.exit(-1)

	msg = readmail(argv[0])

	openmail(msg)

if __name__ == '__main__':
    main(sys.argv[1:])
    

