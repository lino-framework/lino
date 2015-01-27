from django.db import models
from lino.api import dd


class Foo(dd.Model):
  
    name = models.CharField(max_length=100, blank=True)
    remarks = models.TextField("Remarks", blank=True)
    input_mask_test = dd.CharField(
        "Question text",
        blank=True,
        max_length=200,
        help_text="""This field is here to play with the
        CharField parameters regex, mask_re and strip_chars_re.
        By default it accepts all letters except Z.
        """,
        #~ regex='/^[a-yA-Y]*$/')
        mask_re='/^[a-yA-Y]*$/')
        #~ strip_chars_re='/^[a-yA-Y]*$/')


class Foos(dd.Table):
    model = Foo

    column_names = 'name input_mask_test id remarks'

    detail_layout = """
    id name input_mask_test
    remarks
    """

    insert_layout = """
    name
    input_mask_test
    """


