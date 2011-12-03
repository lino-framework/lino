## Copyright 2009-2011 Luc Saffre
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
This defines Lino's permission system.
It is written by a naive and simple-minded person 
and has not yet been used in complex situations.
Possible that it will be replaced in the future.
"""

from django.conf import settings

class Condition:
    pass
    
class never(Condition):
    @staticmethod
    def passes(user): return False
      
class always(Condition):        
    @staticmethod
    def passes(user): return True
      
        
if settings.LINO.user_model is None:
  
    is_staff = always
    is_expert = always
    is_authenticated = always
    #~ is_anonymous = never
    def has_flag(name):
        return always
    
else:    
  
    class is_staff(Condition):
        @staticmethod
        def passes(user):
            return user.is_staff or user.is_superuser
            
    class is_expert(Condition):
        @staticmethod
        def passes(user):
            return user.is_expert or user.is_superuser
            
    class is_authenticated(Condition):
        @staticmethod
        def passes(user):
            return user is not None
            #~ return user.is_authenticated()
            
    def has_flag(name):
        """
        Use this to specify permissions for custom user attributes.
        
        For example if your application 
        uses :func:`reports.inject_field` to add a 
        custom field `is_foo` to your user model,
        it can say ::
        
          can_add = perms.has_flag('is_foo')
          
        
        """
        class inner(Condition):
            @staticmethod
            def passes(user):
                return getattr(user,name,Fale)
        return inner
        
            
    #~ class is_anonymous(Condition):
        #~ @staticmethod
        #~ def passes(user):
            #~ return user is None
            #~ return not user.is_authenticated()

        
#~ from django.conf import settings

#~ if settings.BYPASS_PERMS:
    #~ is_authenticated = always
    #~ is_staff = always
