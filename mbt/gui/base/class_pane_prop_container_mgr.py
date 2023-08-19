# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_pane_prop_container_mgr.py
# ------------------------------------------------------------------------------
#
# File          : class_pane_prop_container_mgr.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import typing,wx
import wx.propgrid as wxpg
from framework.gui.base import BasePropContainer, PropertyDefPageManager, CategoryPropertyDef, PropertyDef
from mbt.application.base import MBTViewManager, MBTContentContainer
from .class_pane_prop_container_view import PropContainerView
from .class_pane_prop_container_cc import PropContainerViewContentContainer


class PropContainerManager(MBTViewManager):
    # todo: SOP(copy)
    # todo: currently the prop changed over attribute setter directly, no event triggered.
    #       in the corresponding setter should be use undoStack.
    # todo: add preference for PropGridManager likes [showPropertyDescription(boolean)]...
    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)

    @property
    def iconSize(self) -> wx.Size:
        return wx.Size(16, 16)

    def create_view(self, **kwargs):
        if self._view is not None:
            return self._view
        _cc = PropContainerViewContentContainer()
        self.post_content_container(_cc)
        # create view
        _view = PropContainerView(**kwargs, manager=self)
        _view.propsPG.Bind(wxpg.EVT_PG_CHANGED, self.on_prop_value_changed)
        self.post_view(_view)
        return self._view

    def _build(self, node, page: wxpg.PropertyGridPage):
        for x in node.children:
            _editor = x.get_editor_instance()
            if x.readonly:
                page.SetPropertyReadOnly(_editor)
            page.Append(_editor)
            if x.children:
                self._build(x, page)

    def on_prop_value_changed(self, evt: wxpg.PropertyGridEvent):
        self.log.debug('--->on_prop_value_changed:%s %s' % (evt.GetPropertyName(), evt.GetPropertyValue()))
        _content: BasePropContainer = self.contentContainer.get()
        _prop_defs: typing.List[PropertyDef] = _content.find_property_def(evt.GetPropertyName())
        # could be mult page???
        for pg_name, prop_def in _prop_defs:
            if prop_def.editorInstance is evt.GetProperty():
                _val = prop_def.get_editor_value()
                prop_def.set_value(_val)

    def set_content(self, content: BasePropContainer):
        super().set_content(content)
        self.view.clear_view()
        if content is not None:
            for pg_name, pg in content.pages.items():
                _page: wxpg.PropertyGridPage = self.view.propsPG.AddPage(pg_name)
                _root = pg.root
                self._build(_root, _page)
            self.view.propsPG.ShowHeader()
        self.view.propsPG.Update()
        self.view.Layout()
