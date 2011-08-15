# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
This module 
provides the models and functionality to collect emails 
and integrate them into the database.

This module 
also turns Lino into a potential mail client, 
but we don't expect to become a concurrent to 
the existing mail clients.
Our focus for this module is on *collecting* and/or *importing* 
emails that *have been sent*, and to integrate them into our data. 

For example in the Detail view of a Person
you can see a history of all emails sent to and 
received from this Person;
and not only on your own account but on all your colleagues.

"""