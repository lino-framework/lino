# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""

See also :blogref:`20160620`.


In your :xfile:`conf.py` file, add this line::

    from lino.sphinxcontrib.help_text_builder import setup
    
Run sphinx-build using::

    $ sphinx-build -b lino . tmp

Copy the result to the right place, e.g.::

    $ cp tmp/help_texts.py ../lino_voga/lib/voga/


Example of a field description::

    <desc desctype="attribute" domain="py" noindex="False" objtype="attribute">
      <desc_signature class="Plan" first="False" fullname="Plan.journal" 
            ids="lino_cosi.lib.invoicing.models.Plan.journal" 
            module="lino_cosi.lib.invoicing.models" 
            names="lino_cosi.lib.invoicing.models.Plan.journal">
        <desc_name>journal</desc_name>
      </desc_signature>
      <desc_content>
        <paragraph>
          The journal where to create invoices.  When this field is
          empty, you can fill the plan with suggestions but cannot
          execute the plan.
        </paragraph>
      </desc_content>
    </desc>

Example of a class description::

    <desc desctype="class" domain="py" noindex="False" objtype="class">
      <desc_signature class="" first="False" fullname="Plan" ids="lino_cosi.lib.invoicing.models.Plan" module="lino_cosi.lib.invoicing.models" names="lino_cosi.lib.invoicing.models.Plan">
        <desc_annotation>class </desc_annotation>
        <desc_addname>lino_cosi.lib.invoicing.models.</desc_addname>
        <desc_name>Plan</desc_name>
        <desc_parameterlist>
            <desc_parameter>*args</desc_parameter>
            <desc_parameter>**kwargs</desc_parameter>
        </desc_parameterlist>
      </desc_signature>
      <desc_content>
        <paragraph>Bases: <reference internal="False" reftitle="(in Lino v1.7)" refuri="http://www.lino-framework.org/api/lino.modlib.users.mixins.html#lino.modlib.users.mixins.UserAuthored"><literal classes="xref py py-class">lino.modlib.users.mixins.UserAuthored</literal></reference>
        </paragraph>
        <paragraph>An <strong>invoicing plan</strong> is a rather temporary database object which represents the plan of a given user to have Lino generate a series of invoices.
        </paragraph>
        <index entries="[('single', u'user (lino_cosi.lib.invoicing.models.Plan attribute)', u'lino_cosi.lib.invoicing.models.Plan.user', '', None)]"/>
        <desc desctype="attribute" domain="py" noindex="False" objtype="attribute"><desc_signature class="Plan" first="False" fullname="Plan.user" ids="lino_cosi.lib.invoicing.models.Plan.user" module="lino_cosi.lib.invoicing.models" names="lino_cosi.lib.invoicing.models.Plan.user"><desc_name>user</desc_name></desc_signature><desc_content/></desc><index entries="[('single', u'journal (lino_cosi.lib.invoicing.models.Plan attribute)', u'lino_cosi.lib.invoicing.models.Plan.journal', '', None)]"/><desc desctype="attribute" domain="py" noindex="False" objtype="attribute"><desc_signature class="Plan" first="False" fullname="Plan.journal" ids="lino_cosi.lib.invoicing.models.Plan.journal" module="lino_cosi.lib.invoicing.models" names="lino_cosi.lib.invoicing.models.Plan.journal"><desc_name>journal</desc_name></desc_signature><desc_content><paragraph>The journal where to create invoices.  When this field is
    empty, you can fill the plan with suggestions but cannot
    execute the plan.</paragraph></desc_content></desc><index entries="[('single', u'max_date (lino_cosi.lib.invoicing.models.Plan attribute)', u'lino_cosi.lib.invoicing.models.Plan.max_date', '', None)]"/><desc desctype="attribute" domain="py" noindex="False" objtype="attribute"><desc_signature class="Plan" first="False" fullname="Plan.max_date" ids="lino_cosi.lib.invoicing.models.Plan.max_date" module="lino_cosi.lib.invoicing.models" names="lino_cosi.lib.invoicing.models.Plan.max_date"><desc_name>max_date</desc_name></desc_signature><desc_content/></desc><index entries="[('single', u'today (lino_cosi.lib.invoicing.models.Plan attribute)', u'lino_cosi.lib.invoicing.models.Plan.today', '', None)]"/><desc desctype="attribute" domain="py" noindex="False" objtype="attribute"><desc_signature class="Plan" first="False" fullname="Plan.today" ids="lino_cosi.lib.invoicing.models.Plan.today" module="lino_cosi.lib.invoicing.models" names="lino_cosi.lib.invoicing.models.Plan.today"><desc_name>today</desc_name></desc_signature><desc_content/></desc><index entries="[('single', u'partner (lino_cosi.lib.invoicing.models.Plan attribute)', u'lino_cosi.lib.invoicing.models.Plan.partner', '', None)]"/><desc desctype="attribute" domain="py" noindex="False" objtype="attribute"><desc_signature class="Plan" first="False" fullname=
    ...


"""

from __future__ import print_function
from __future__ import unicode_literals

import os

from docutils import nodes
from docutils import core
from sphinx import addnodes
from sphinx.builders import Builder
# from pprint import pprint

# from importlib import import_module


def node2html(node):
    parts = core.publish_from_doctree(node, writer_name="html")
    return parts['body']


class HelpTextBuidler(Builder):
    name = 'lino'

    def __init__(self, *args, **kwargs):
        super(HelpTextBuidler, self).__init__(*args, **kwargs)
        self.texts = dict()
        # self.models = dict()
        # self.node_classes = set()

    def write_doc(self, docname, doctree):
        # if docname != 'api/lino_cosi.lib.invoicing.models':
        #     return
        # print(doctree)
        # return
        # for node in doctree.traverse():
        #     self.node_classes.add(node.__class__)
        for node in doctree.traverse(addnodes.desc):
            if node['domain'] == 'py':
                if node['objtype'] == 'class':
                    self.load_class(node)
                elif node['objtype'] == 'attribute':
                    self.load_attribute(node.parent, node)
        # for node in doctree.traverse(nodes.field):
        #     self.fields.add(node.__class__)

    def load_class(self, node):
        self.store_content(self.texts, node)

    def load_attribute(self, parent, node):
        self.store_content(self.texts, node)

    def store_content(self, d, node):
        sig = []
        content = []
        for c in node.children:
            if isinstance(c, addnodes.desc_content):
                for cc in c.children:
                    if isinstance(cc, nodes.paragraph):
                        p = cc.astext()
                        if not p.startswith("Bases:"):
                            if len(content) == 0:
                                content.append(p)
            elif isinstance(c, addnodes.desc_signature):
                sig.append(c)
        # if len(sig) != 1:
        #     raise Exception("sig is {}!".format(sig))
        sig = sig[0]
        # sig = list(node.traverse(addnodes.desc_signature))[0]
        # content = [
        #     p.astext() for p in node.traverse(addnodes.desc_content)]
        # content = [p for p in content if not p.startswith("Bases:")]
        if not content:
            return
        content = '\n'.join(content)
        for fn in sig['names']:
            d[fn] = content

    def get_outdated_docs(self):
        for docname in self.env.found_docs:
            yield docname

    def prepare_writing(self, docnames):
        pass

    def get_target_uri(self, docname, typ=None):
        return 'help_texts.py'

    def finish(self):
        fn = os.path.join(self.outdir, 'help_texts.py')
        print("Write output to {}".format(fn))
        fd = file(fn, "w")

        def writeln(s):
            s = s.encode('utf-8')
            fd.write(s)
            fd.write("\n")

        writeln("# -*- coding: UTF-8 -*-")
        writeln("# generated by help_text_builder")
        writeln("from __future__ import unicode_literals")
        writeln("from lino.api import _")
        writeln("help_texts = {")
        for k, v in self.texts.items():
            writeln('''  '{}' : _("""{}"""),'''.format(k, v))
        writeln("}")
        fd.close()


def setup(app):
    app.add_builder(HelpTextBuidler)
