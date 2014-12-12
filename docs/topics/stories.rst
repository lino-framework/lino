=======
Stories
=======

One part of Lino is a system for programming complex printable reports.

One part of that system are "stories".

A story is a sequence of "chunks" of a bigger document. These chunks
can be either an HTML element or a :class:`rt.TableRequest` instance.

TODO: write more documentation.

Example::

    class Foo(dd.Model):
        ...

    class FooDetail(dd.FormLayout)

        preview_tab = dd.Panel("""
        second_box
        summary_box
        """, label=_("Preview"))

    class Foos(dd.Table):

        @dd.virtualfield(dd.HtmlBox(_("Summary")))
        def summary_box(self, ar):
            return E.div(*ar.story2html(self.summary_story(ar)))

        @dd.virtualfield(dd.HtmlBox(_("Second")))
        def second_box(self, ar):
            return E.div(*ar.story2html(self.second_story(ar)))
    
        def summary_story(self, ar):

            def render(t):
                sar = ar.spawn(t, master_instance=self)
                if sar.get_total_count():
                    yield E.h2(unicode(sar.get_title()))
                    yield sar

            yield render(ResultByBudget)
            yield render(DebtsByBudget)
            yield render(BailiffDebtsByBudget)
            yield render(DistByBudget)

