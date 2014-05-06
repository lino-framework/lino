from lino import dd
from django.db import models


class Author(dd.Model):
    first_name = models.CharField("First name", max_length=50)
    last_name = models.CharField("Last name", max_length=50)
    country = models.CharField("Country", max_length=50)
    
    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)


class Authors(dd.Table):
    model = Author
    column_names = 'first_name last_name country'


class Book(dd.Model):
    author = models.ForeignKey(Author)
    title = models.CharField("Title", max_length=200)
    published = models.IntegerField("Published")
    price = models.DecimalField("Price", decimal_places=2, max_digits=10)


class Books(dd.Table):
    model = Book
    column_names = 'author title published *'


class BooksByAuthor(Books):
    master_key = 'author'
    column_names = 'published title'
    order_by = ['published']
