from lino.api import dd

DATA = [
    ["Belgium", "Eupen", 17000],
    ["Belgium", "Liege", 400000],
    ["Belgium", "Raeren", 5000],
    ["Estonia", "Tallinn", 400000],
    ["Estonia", "Vigala", 1500],
]


class CitiesAndInhabitants(dd.VirtualTable):

    column_names = "country city population"

    @classmethod
    def get_data_rows(cls, ar):
        return DATA

    @dd.displayfield("Country")
    def country(cls, row, ar):
        return row[0]

    @dd.displayfield("City")
    def city(cls, row, ar):
        return row[1]

    @dd.displayfield("Population")
    def population(cls, row, ar):
        return row[2]


