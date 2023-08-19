# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_workbench_registry.py
# ------------------------------------------------------------------------------
#
# File          : class_workbench_registry.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import typing
from framework.application.base import singleton
from framework.application.utils_helper import util_is_string_valid_for_dir
from .class_workbench import MBTBaseWorkbench, MBTProjectOrientedWorkbench


class WorkbenchRegistryException(Exception): pass


@singleton
class WorkbenchRegistry:
    def __init__(self):
        self._workbenches = dict()

    @property
    def all(self):
        return self._workbenches

    def register_workbench(self, wb: typing.Union[MBTBaseWorkbench, MBTProjectOrientedWorkbench]):
        assert util_is_string_valid_for_dir(wb.uid), WorkbenchRegistryException('illegal uid %s applied.' % wb.uid)
        assert wb.uid not in self._workbenches, WorkbenchRegistryException('workbench with uid %s already exist.' % wb.uid)
        if isinstance(wb, MBTProjectOrientedWorkbench):
            assert wb.baseRole not in [v.baseRole for k, v in self._workbenches.items()] and wb.baseRole != '0', \
                WorkbenchRegistryException('workbench with baseRole %s already exist.' % wb.baseRole)
        self._workbenches.update({wb.uid: wb})

    def unregister_workbench(self, uid):
        if uid in self._workbenches:
            self._workbenches.pop(uid)

    def register_workbench_item_editor(self, wb_uid, editor_name, editor_cls, **kwargs):
        _wb: MBTBaseWorkbench = self.get(wb_uid)
        assert _wb is not None, WorkbenchRegistryException('workbench with uid %s not exist.' % wb_uid)
        _wb.editorFactory.register_with(editor_name, editor_cls, **kwargs)

    def unregister_workbench_item_editor(self, wb_uid, editor_uid):
        _wb: MBTBaseWorkbench = self.get(wb_uid)
        assert _wb is not None, WorkbenchRegistryException('workbench with uid %s not exist.' % wb_uid)
        _wb.editorFactory.unregister(editor_uid)

    def get(self, uid):
        return self._workbenches.get(uid)

    def get_by_type(self, type_):
        return {k: v for k, v in self._workbenches.items() if isinstance(v, type_)}
