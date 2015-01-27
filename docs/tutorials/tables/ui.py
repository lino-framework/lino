from lino.api import dd


class Authors(dd.Table):
    model = 'Author'
    column_names = 'first_name last_name country'


class Books(dd.Table):
    model = 'Book'
    column_names = 'author title published *'
    hide_sums = True


class RecentBooks(Books):
    column_names = 'published title author'
    order_by = ['published']


class BooksByAuthor(Books):
    master_key = 'author'
    column_names = 'published title'
    order_by = ['published']
