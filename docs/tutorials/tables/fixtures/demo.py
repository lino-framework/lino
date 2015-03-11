from lino.api.shell import *
from lino.utils.instantiator import Instantiator


def objects():
    author = Instantiator(
        'tables.Author', 'first_name last_name country').build
    adams = author("Douglas", "Adams", "UK")
    yield adams
    camus = author("Albert", "Camus", "FR")
    yield camus
    huttner = author("Hannes", "Huttner", "DE")
    yield huttner

    book = Instantiator('tables.Book', 'title author published price').build
    yield book("Last chance to see...", adams, 1990, '9.90')
    yield book("The Hitchhiker's Guide to the Galaxy", adams, 1978, '19.90')
    yield book("Das Blaue vom Himmel", huttner, 1975, '14.90')
    yield book("L'etranger", camus, 1957, '6.90')

