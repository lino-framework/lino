def objects():
    from lino.modlib.countries.fixtures.few_countries import objects
    yield objects()
    from lino.modlib.countries.fixtures.few_cities import objects
    yield objects()
