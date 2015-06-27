from lino.api import rt
# from lino.api.doctest import post_json_dict

from lino.utils.test import DocTest  # automatically tests index.rst

# # the remaining passes but is useless. covered by index.rst
# from lino.utils.djangotest import TestCase


# def changes_to_rst(master):
#     A = rt.modules.changes.ChangesByMaster
#     return A.request(master).to_rst(
#         column_names='type object diff:30 object_type object_id')


# class TestCase(TestCase):

#     fixtures = ['std', 'demo']
#     maxDiff = None

#     def test00(self):

#         Person = rt.modules.contacts.Person

#         obj = Person.objects.get(pk=127)

#         s = changes_to_rst(obj)
#         # print s
#         self.assertEqual(s, '\nNo data to display\n')
        

