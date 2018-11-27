# -*- coding: UTF-8 -*-
# Copyright 2014-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from django.dispatch import Signal

mail_received = Signal(['msg'])
"""Sent for every incoming mail.

sender:
  the Site instance


peer, mailfrom, rcpttos, data:

    are those passed to the standard Python
    `smtpd.SMTPServer.process_message` method:

    peer is the remote host’s address, mailfrom is the envelope
    originator, rcpttos are the envelope recipients and data is a
    string containing the contents of the e-mail (which should be in
    :rfc:`2822` format).


"""

