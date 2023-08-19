# -*- coding: utf-8 -*-
import enum
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : editor_test_case_setting_cc.py
# ------------------------------------------------------------------------------
#
# File          : editor_test_case_setting_cc.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from dataclasses import dataclass
import wx, platform
from framework.application.define import _
from framework.gui.base import (PropertyDefPageManager, CategoryPropertyDef,
                                BasePropContainer,
                                StringPropertyDef,
                                FlagsPropertyDef,
                                BoolPropertyDef, FloatPropertyDef, SingleChoicePropertyDef)
from framework.application.base import Serializable, ChangeDetectable
from framework.application.utils_helper import util_get_computer_name
from mbt.application.define import EnumTEProtocol
from mbt.application.project import ProjectContentContractor, ProjectContentProvider
from mbt.application.base import MBTContentContainer


class TestCaseSettingContentException(Exception): pass


class SettingGeneralContent(Serializable, ChangeDetectable):
    serializeTag = '!TCSettingGeneral'

    def __init__(self, **kwargs):
        ChangeDetectable.__init__(self)
        self.author = kwargs.get('author', util_get_computer_name())
        self.version = kwargs.get('version', '1.0')
        self.platform = kwargs.get('platform', platform.platform())
        self.testFor = kwargs.get('test_for', '')
        self.description = kwargs.get('description', 'description...')
        self.discarded = kwargs.get('discarded', False)
        self.testEnvProtocol = kwargs.get('te_protocol', EnumTEProtocol.PROTOCOL_URPC.value)
        self.testEnvComToS = kwargs.get('te_com_to', 5.0)
        self.testEnvStepExeToS = kwargs.get('te_step_exe_to', 5.0)

    @property
    def serializer(self):
        return {
            'author': self.author,
            'version': self.version,
            'platform': self.platform,
            'test_for': self.testFor,
            'description': self.description,
            'discarded': self.discarded,
            'te_protocol': self.testEnvProtocol,
            'te_com_to': self.testEnvComToS,
            'te_step_exe_to': self.testEnvStepExeToS,
        }

    def _te_protocol_setter(self, idx: int):
        self.testEnvProtocol = [x.value for x in EnumTEProtocol][idx]

    def build_prop_container(self):
        _prop_container = BasePropContainer()
        _page_default = PropertyDefPageManager(name='default')
        _cat_public = _page_default.register_with(CategoryPropertyDef, object=self,
                                                  label='Public')
        _page_default.register_with(StringPropertyDef, object=self, auto_init=True,
                                    label='Author', getter='author', setter='author', parent=_cat_public,
                                    description='give the author name in text.')
        _page_default.register_with(StringPropertyDef, object=self, auto_init=True,
                                    label='Version', getter='version', setter='version', parent=_cat_public,
                                    description='give the version in text.')
        _page_default.register_with(StringPropertyDef, object=self, auto_init=True,
                                    label='Platform', getter='platform', setter='platform', readonly=True, parent=_cat_public,
                                    description='readonly field.\nThis value is automatically initialed by internal function..')
        _page_default.register_with(StringPropertyDef, object=self, auto_init=True,
                                    label='TestFor', getter='testFor', setter='testFor', parent=_cat_public,
                                    description='give the test purpose in text.')
        _page_default.register_with(BoolPropertyDef, object=self, auto_init=True,
                                    label='Discarded', getter='discarded', setter='discarded', parent=_cat_public,
                                    description='give the if this testcase discarded.')
        _cat_execute = _page_default.register_with(CategoryPropertyDef, object=self,
                                                   label='Execute')
        _page_default.register_with(SingleChoicePropertyDef, object=self, auto_init=True,
                                    label='TEProtocol',
                                    labels=[x.value for x in EnumTEProtocol],
                                    getter='testEnvProtocol',
                                    setter=self._te_protocol_setter,
                                    parent=_cat_execute,
                                    description='which communication protocol used.\nurpc is used as the default.')
        _page_default.register_with(FloatPropertyDef, object=self, auto_init=True,
                                    min=0.0, max=60.0,
                                    label='TEComTimeout', getter='testEnvComToS', setter='testEnvComToS', parent=_cat_execute,
                                    description='timeout of communication of TestEnv in second.\nvalue range between 0-60')
        _page_default.register_with(FloatPropertyDef, object=self, auto_init=True,
                                    min=0.0, max=60.0,
                                    label='StepExeTimeout', getter='testEnvStepExeToS', setter='testEnvStepExeToS', parent=_cat_execute,
                                    description='timeout of execution of a test step in second.'
                                                '\nfor delay assigned test step this timeout is added.\nvalue range between 0-60')
        _prop_container.add_page(_page_default)
        return _prop_container


class SettingOutlineContent:
    pass


@dataclass
class _ContentElement:
    ready: bool = False
    path: str = ''
    name: str = ''
    extension: str = '.obj'
    data: ChangeDetectable = None

    def mark_state(self):
        if self.data is not None and self.ready:
            self.data.mark_change_state()
            self.inspect_change()

    def inspect_change(self):
        if self.data is None or not self.ready:
            return False
        return self.data.is_changed()


class TestCaseSettingContentContainer(MBTContentContainer):
    def __init__(self, **kwargs):
        MBTContentContainer.__init__(self, **kwargs)
        self.projectContentContractor = ProjectContentContractor()
        self.compositeContent = dict()
        self.compositeContent.update({'general': _ContentElement(name='general', data=SettingGeneralContent())})

    def prepare(self):
        # todo: check outline bind uid is exist.
        assert self.manager is not None, TestCaseSettingContentException('must be call from it owned manager.')
        _app = wx.App.GetInstance()
        for k, x in self.compositeContent.items():
            _c = self.projectContentContractor.build_query_contract(self.manager.uid, name=x.name, extension=x.extension)
            _io = _app.baseContentResolver.query(_c)
            if _io is None:
                _ic = self.projectContentContractor.build_insert_contract(self.manager.uid, x.name, path=x.path, extension=x.extension, data=x.data)
                _ret = _app.baseContentResolver.insert(_ic)
                assert _ret
                x.ready = True
            else:
                x.data = _io.data
                x.ready = True
            x.mark_state()

    def has(self, el_name: str):
        return el_name in self.compositeContent

    def query_project_node(self, filter_func: callable):
        _app = wx.App.GetInstance()
        _c = self.projectContentContractor.build_node_query_contract(filter_func)
        return _app.baseContentResolver.query(_c)

    def set(self, *args, **kwargs):
        # normally only for external calling. this editor
        # assigned content from external is not allowed. use ContentResolver instead.
        Warning('not used method called.')

    def get(self, el_name: str) -> _ContentElement:
        return self.compositeContent.get(el_name)

    def reset_to_default(self, which: str):
        """
        this method required, the content is already exist.
        Args:
            which:

        Returns:

        """
        if not self.has(which):
            return
        _app = wx.App.GetInstance()
        _el = self.compositeContent.get(which)
        if not _el.inspect_change():
            # if no changed no necessary to restore.
            return
        _el.ready = False
        _c = self.projectContentContractor.build_query_contract(self.manager.uid, name=_el.name, extension=_el.extension, path=_el.path)
        _io = _app.baseContentResolver.query(_c)
        if _io is None:
            raise TestCaseSettingContentException('can not restore the content, since the content is not exist.')
        _el.data = _io.data
        _el.ready = True
        _el.mark_state()

    def has_changed(self):
        """
        by top manager cyclic called.
        Returns: bool

        """
        return any([c.inspect_change() for k, c in self.compositeContent.items()])

    def change_apply(self, el_name: str = None):
        _app = wx.App.GetInstance()
        _ret = True
        if el_name is None:
            for x, v in self.compositeContent.items():
                _c = self.projectContentContractor.build_update_contract(self.manager.uid, v.name, v.path, data=v.data, extension=v.extension)
                _r = _app.baseContentResolver.update(_c)
                if _r: v.mark_state()
                _ret &= _r
        else:
            if el_name not in self.compositeContent:
                return False
            _el = self.compositeContent.get(el_name)
            _c = self.projectContentContractor.build_update_contract(self.manager.uid, _el.name, _el.path, data=_el.data, extension=_el.extension)
            _ret &= _app.baseContentResolver.update(_c)
            if _ret: _el.mark_state()
        return _ret

    def transform_data(self, transformer: any):
        pass
