from django.utils.translation import ugettext_lazy as _

from lino import dd, mixins


class Expression(mixins.BabelNamed):

    class Meta:
        verbose_name = _('Expression')
        verbose_name_plural = _('Expressions')


class Expressions(dd.Table):
    model = Expression
    #~ column_names = 'name'


