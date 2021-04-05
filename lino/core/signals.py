# Copyright 2013-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""This defines Lino's standard system signals.

See :doc:`/dev/signals`.

"""

from django.dispatch import Signal, receiver

pre_startup = Signal()
post_startup = Signal()
testcase_setup = Signal()
pre_analyze = Signal()  # ['models_list'])
post_analyze = Signal()  # ['models_list'])
auto_create = Signal()  # ["field", "value"])
pre_merge = Signal()  # ['request'])
pre_remove_child = Signal()  # ['request', 'child'])
pre_add_child = Signal()  # ['request'])
on_ui_created = Signal()  # ['request'])
on_ui_updated = Signal()  # ['request', 'watcher'])
pre_ui_save = Signal()  # ['instance', 'ar'])
pre_ui_delete = Signal()  # ['request'])
pre_ui_build = Signal()
post_ui_build = Signal()
# database_connected = Signal()
