## Copyright 2003-2007 Luc Saffre 

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

class StartupDelay(Exception):
    pass

class InvalidRequestError(Exception):
    "The requested action was refused"

class RefuseValue(Exception):
    "Invalid data submitted"

class RowLockFailed(Exception):
    "Failed to get a lock for a row"

class LockRequired(InvalidRequestError):
    "Tried to update a row that is not locked"

class DatabaseError(Exception):
    "dbd-specific exception was raised"

class DataVeto(Exception):
    "Invalid data submitted"

class NoSuchField(DataVeto,AttributeError):
    pass

class UserAborted(Exception):
    pass

class OperationFailed(Exception):
    pass

class UsageError(Exception):
    pass

#class ApplicationError(Exception):
#    pass
    

__all__ = [
    'StartupDelay',
    'InvalidRequestError',
    'RowLockFailed',
    'DataVeto',
    'DatabaseError',
    'UserAborted',
    'OperationFailed']
