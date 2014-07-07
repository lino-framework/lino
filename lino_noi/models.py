from email.parser import Parser

from lino import dd
from lino.modlib.smtpd.signals import mail_received


@dd.receiver(mail_received)
def process_message(sender=None, peer=None, mailfrom=None,
                    rcpttos=None, data=None, **kwargsg):
    print 'Receiving message from:', peer
    print 'Message addressed from:', mailfrom
    print 'Message addressed to  :', rcpttos
    print 'Message length        :', len(data)
    msg = Parser().parsestr(data)
    print 'To: %s' % msg['to']
    print 'From: %s' % msg['from']
    print 'Subject: %s' % msg['subject']
    return None



