# -*- coding: utf-8 -*-
import time

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_cc.py
# ------------------------------------------------------------------------------
#
# File          : stc_cc.py
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
from framework.application.content_resolver import ContentContract
from mbt.application.base import MBTViewManager, MBTContentContainer, ChangeDetectableContentElement, MBTContentException
from mbt.workbenches.workbench_model import (ModelContentQueryContract, ModelContentProvider,
                                             ModelContentInsertContract, ModelContentUpdateContract, ModelContentDeleteContract)
from mbt.workbenches.workbench_model.application.define import WB_NODE_IPOD_RESOLVER_NAME, WB_NODE_VISUAL_RESOLVER_NAME,WB_NODE_WHITEBOX_RESOLVER_NAME
from .application.class_ipode_impl import StcIPODE
from .application.class_visual import STCVisual
from .application.class_white_box import STCWhitebox
"""
graph->.bvi(userData of element store the impl(textPreview,uuid))
ipod->.ipod (statechart,action impl)

.ipode
    - iod
    - evt
    - funcs
    - impl
    - stc
simulation needs:
    .bvi for visualisation
    .ipode  for stateMachine simulation

"""


class IODContentConstractor:
    pass


class STCEditorContentContainer(MBTContentContainer):
    CONTENT_RESOLVER_NAMES = []

    def __init__(self, **kwargs):
        MBTContentContainer.__init__(self, **kwargs)
        self.compositeContent = dict()
        self.compositeContent.update({WB_NODE_IPOD_RESOLVER_NAME: ChangeDetectableContentElement(name=WB_NODE_IPOD_RESOLVER_NAME, data=StcIPODE()),
                                      WB_NODE_VISUAL_RESOLVER_NAME: ChangeDetectableContentElement(name=WB_NODE_VISUAL_RESOLVER_NAME, data=STCVisual()),
                                      WB_NODE_WHITEBOX_RESOLVER_NAME: ChangeDetectableContentElement(name=WB_NODE_WHITEBOX_RESOLVER_NAME, data=STCWhitebox()),
                                      })
        # todo: !!!!!!!!!!lineShape could not be serialized.!!!!!!!!!!!!!!!!!

    def transform_data(self, *args):
        return {}

    def prepare(self):
        assert self.manager is not None, MBTContentException('must be called from it owned manager.')
        _app = self.manager.appInstance
        _resolver_uri = ModelContentProvider.build_uri(authority=ModelContentProvider.AUTHORITY)
        for k, x in self.compositeContent.items():
            _c = ModelContentQueryContract(uri=_resolver_uri,
                                           uid=self.manager.uid,
                                           name=x.name,
                                           path=x.path,
                                           data=None,
                                           extension=x.extension)
            _io = _app.baseContentResolver.query(_c)
            if _io is None or _io.data is None:
                _ic = ModelContentInsertContract(uri=_resolver_uri,
                                                 uid=self.manager.uid,
                                                 name=x.name,
                                                 path=x.path,
                                                 data=x.data,
                                                 extension=x.extension)
                _ret = _app.baseContentResolver.insert(_ic)
                assert _ret
                x.ready = True
            else:
                x.data = _io.data
                x.ready = True
            x.mark_state()

    def get(self, cursor: typing.Union[ContentContract, str]):
        if self.manager is None:
            return
        if isinstance(cursor, ModelContentQueryContract):
            _resolver_name = cursor.name
        elif isinstance(cursor, str):
            _resolver_name = cursor
        else:
            raise MBTContentException('unknown resolver name')
        return self.compositeContent.get(_resolver_name)

    def set(self, *args, **kwargs):
        # normally only for external calling. this editor
        # assigned content from external is not allowed. use ContentResolver instead.
        Warning('not used method called.')

    def has_changed(self):
        """
        by top manager cyclic called.
        Returns: bool

        """
        return any([c.inspect_change() for k, c in self.compositeContent.items()])

    def change_apply(self, which: str = None):
        _app = self.manager.appInstance
        _ret = True
        _resolver_uri = ModelContentProvider.build_uri(authority=ModelContentProvider.AUTHORITY)
        if which is None:
            for x, v in self.compositeContent.items():
                _c = ModelContentUpdateContract(uri=_resolver_uri,
                                                uid=self.manager.uid,
                                                name=v.name,
                                                path=v.path,
                                                data=v.data,
                                                extension=v.extension)
                _r = _app.baseContentResolver.update(_c)
                if _r: v.mark_state()
                _ret &= _r
        else:
            if which not in self.compositeContent:
                return False
            _el = self.compositeContent.get(which)
            _c = ModelContentUpdateContract(uri=_resolver_uri,
                                            uid=self.manager.uid,
                                            name=_el.name,
                                            path=_el.path,
                                            data=_el.data,
                                            extension=_el.extension)
            _ret &= _app.baseContentResolver.update(_c)
            if _ret: _el.mark_state()
        return _ret
