__all__ = []

__docformat__ = 'reStructuredText'

__version__ = "0.6.2"

__author__ = "Luc Saffre <luc.saffre@gmx.net>"


def copyleft( name="Lino",
				  version=__version__,
				  year="2002-2004",
				  author=__author__):
   return """\
%s version %s.
Copyright (c) %s %s.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information.""" % (
		name, version, year, author)
