# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.


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

