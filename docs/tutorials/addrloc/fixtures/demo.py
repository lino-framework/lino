from lino.utils.instantiator import Instantiator


def objects():
    b = Instantiator('addrloc.Company',
                     'name country zip_code city:name street street_no')
    yield b("First", "BE", "4700", "Eupen", "Favrunpark", 13)
    yield b("Second", "EE", "10115", "Tallinn", "Tartu mnt", 71)
