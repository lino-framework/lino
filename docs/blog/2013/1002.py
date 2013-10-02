"""
Custom-specific script to import pupils into :ref:`faggio`
from an .xls file. To be invoked using something like::

  python manage.py run /path/lino/blog/2013/1002.py Input_file.xls
  


"""

import sys

import logging
logger = logging.getLogger('lino')

from dateutil.parser import parse as parse_date

from lino.utils import iif
from lino.utils import IncompleteDate
from xlrd import open_workbook, xldate_as_tuple

from lino.modlib.contacts.utils import street2kw

from lino.runtime import courses, countries
from lino import dd
from djangosite.dbutils import is_valid_email


def string2date(s):
    return parse_date(s,fuzzy=True)

class MyBook():

    column_headers = """
    Nr.
    Titel
    Name
    Vorname
    Strasse
    PLZ
    Ort
    -
    Handy
    GEBURTSTAG
    BEZ.
    Datum
    -
    COK-MG
    E-Mail
    """.split()
    column_headers = [iif(x=='-','',x) for x in column_headers]


    def date_converter(self,v):
        if not v: return None
        if isinstance(v,basestring):
            v = string2date(v)
            return IncompleteDate.from_date(v)
            #~ return v
        t = xldate_as_tuple(v,self.book.datemode)
        assert len(t) == 6
        t = t[:3]
        #~ print t
        return IncompleteDate(*t)

    def row2instance(self,nr,title,last_name,first_name,street,zip_code,city_name,phone,gsm,birth_date,bez,datum,mg,mgnr,email):
        kw = dict(last_name=last_name,first_name=first_name)
        if nr:
            kw.update(id=nr)
        kw.update(phone=phone)
        kw.update(gsm=gsm)
        kw.update(zip_code=zip_code)
        if email:
            if isinstance(email,basestring) and is_valid_email(email):
                kw.update(email=email)
            else:
                logger.warning("Ignored invalid email address %r",email)
        #~ kw.update(street=street)
        
        #~ kw.update(pupil_type=mg)
        
        kw.update(street2kw(street))
        
        if title == "Herr":
            kw.update(gender=dd.Genders.male)
        elif title == "Frau":
            kw.update(gender=dd.Genders.female)
        elif title:
            kw.update(title=title)
        if city_name:
            #~ countries.City.objects.get(name)
            kw.update(city=countries.City.lookup_or_create('name',city_name,country=self.country))
        #~ print birth_date
        kw.update(birth_date=self.date_converter(birth_date))
        return courses.Pupil(**kw)
        

    def __init__(self,filename):
        #~ filename = '/home/luc/Downloads/Eiche 2013.xls'

        self.country = countries.Country.objects.get(isocode="BE")
        self.book = open_workbook(filename)
        s = self.book.sheet_by_index(0)
        #~ print 'Sheet:',s.name
        found = False
        ncols = len(self.column_headers)
        for row in range(s.nrows):
            values = [s.cell(row,col).value for col in range(ncols)]
            if found:
                obj = self.row2instance(*values)
                obj.full_clean()
                obj.save()
                logger.info("%s has been saved",obj)
            elif values == self.column_headers:
                found = True
            elif row < 5:
                print "Ignored line %s" % values
       
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "must specify input filename as argument.", sys.argv
        sys.exit(-1)
    MyBook(sys.argv[1])

