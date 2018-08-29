# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from builtins import range
from builtins import object

from django.db import models

from lino.api import dd, _


class ComputeResults(dd.Action):
    label = _("Compute results")
    icon_name = 'lightning'
    readonly = False

    def run_from_ui(self, ar, **kw):
        for obj in ar.selected_rows:
            obj.compute_summary_values()
        ar.success(refresh=True)


# class UpdateSummary(dd.Action):
#     icon_name = 'bell'
#     label = _("Update summary")
#     sort_index = 90

#     def run_from_ui(self, ar):
#         # print(20150327, ar.selected_rows)
#         for obj in ar.selected_rows:
#             obj.update_
#         ar.set_response(refresh_all=True)


class UpdateSummariesByMaster(dd.Action):
    icon_name = 'lightning'

    def __init__(self, master_model, summary_models):
        self.master_model = master_model
        self.summary_models = summary_models
        super(UpdateSummariesByMaster, self).__init__()

    def run_from_ui(self, ar, fix=None):
        for master in ar.selected_rows:
            assert isinstance(master, self.master_model)
            for sm in self.summary_models:
                sm.update_for_master(master)
        ar.set_response(refresh=True)


class SimpleSummary(dd.Model):
    
    class Meta(object):
        abstract = True
        
    allow_cascaded_delete = 'master'
    compute_results = ComputeResults()
    
    @classmethod
    def get_summary_master_model(cls):
        return cls._meta.get_field('master').remote_field.model

    @classmethod
    def get_summary_masters(cls):
        return cls.get_summary_master_model().objects.all()
        
    def get_summary_collectors(self):
        raise NotImplementedError()

    def reset_summary_data(self):
        pass

    def get_summary_querysets(self):
        return []

    @classmethod
    def get_for_master(cls, master, **flt):
        qs = cls.objects.filter(master=master, **flt)
        count = qs.count()
        if count > 1:
            # Theoretically this should never happen. There cannot be
            # more than one object for a given master and period.
            qs.delete()
            count = 0
        if count == 0:
            return cls(master=master, **flt)
        return qs[0]
        
    @classmethod
    def update_for_master(cls, master):
        obj = cls.get_for_master(master)
        obj.compute_summary_values()
                
    def compute_summary_values(self):
        self.reset_summary_data()
        for collector, qs in self.get_summary_collectors():
            for obj in qs:
                collector(obj)
        self.full_clean()
        self.save()
        

# SUMMARY_PERIODS = ['yearly', 'monthly', 'timeless']
SUMMARY_PERIODS = ['yearly', 'monthly']

        
class Summary(SimpleSummary):
    class Meta(object):
        abstract = True

    # summary_period = 'yearly'
    summary_period = 'monthly'

    year = models.IntegerField(_("Year"), null=True, blank=True)
    month = models.IntegerField(_("Month"), null=True, blank=True)


    # def __init__(self, *args, **kwargs):
    #     self.reset_summary_data()
    #     super(Summary, self). __init__(*args, **kwargs)

    @classmethod
    def on_analyze(cls, site):
        if cls.summary_period not in SUMMARY_PERIODS:
            raise Exception(
                "Invalid summary_period {!r} for {}".format(
                    cls.summary_period, cls))
    

    @classmethod
    def get_summary_periods(cls):
        config = dd.plugins.summaries
        if cls.summary_period == 'timeless':
            yield None, None
            return
        for year in range(config.start_year, config.end_year+1):
            if cls.summary_period == 'yearly':
                yield year, None
            elif cls.summary_period == 'monthly':
                for month in range(1, 13):
                    yield year, month

    @classmethod
    def get_for_period(cls, master, year, month):
        return cls.get_for_master(master, year=year, month=month)

    @classmethod
    def update_for_master(cls, master):
        for year, month in cls.get_summary_periods():
            obj = cls.get_for_period(master, year, month)
            obj.compute_summary_values()
                
    def add_date_filter(self, qs, fldname, **kwargs):
        if self.year is not None:
            kwargs[fldname+'__year'] = self.year
        if self.month is not None:
            kwargs[fldname+'__month'] = self.month
        return qs.filter(**kwargs)

    # @classmethod
    # def get_widget_options(cls, name, **options):
    #     if name in ('year', 'month'):
    #         options.update(hide_sum=True)
    #     return super(Summary, cls).get_widget_options(name, **options)


Summary.set_widget_options('year', hide_sum=True)
Summary.set_widget_options('month', hide_sum=True)
