"""
start the user's mail client with a ready-to-send message.

USAGE : openmail FILE

where FILE describes the contents of the message using a simplified
pseudo RFC822 format.  Supported message header fields are "to" and
"subject", and the "body".  "to" is mandatory, the other fields are
optional.

See also :pageref:`/docs/openmail`.

"""

import sys,os

from lino.timtools.mail import readmail, openmail


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print __doc__
		sys.exit(-1)

	msg = readmail(sys.argv[1])

	openmail(msg)

