# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_prefs_manager.py
# ------------------------------------------------------------------------------
#
# File          : class_prefs_manager.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, anytree, weakref
from framework.application.base import TreeModelAnyTreeNode, TreeModel, singleton, Serializable


class PreferenceTreeNode(TreeModelAnyTreeNode):
    def __init__(self, **kwargs):
        TreeModelAnyTreeNode.__init__(self, **kwargs)
        self.uuid = kwargs.get('uuid')
        self.viewCls: 'BasePreferencePage' = kwargs.get('viewCls')
        self.content = kwargs.get('content')
        self.viewRef = None
        if self.viewCls is not None and 'icon' not in kwargs:
            self.icon = self.viewCls.get_icon_id()


class PreferenceTreeModel(TreeModel):
    def __init__(self):
        TreeModel.__init__(self, node_class=PreferenceTreeNode)


class PreferenceMgr:
    def __init__(self):
        self.model = PreferenceTreeModel()
        self.viewRef = None
        self.currentPage = None

    @property
    def root(self):
        return self.model.root

    @property
    def imageNameList(self):
        _icons = set()
        for x in anytree.iterators.LevelOrderIter(self.model.root):
            if x.viewCls is None:
                _icon_id=x.icon
            else:
                if x.icon is not None:
                    _icon_id=x.icon
                else:
                    _icon_id = x.viewCls.get_icon_id()
            if _icon_id is not None:
                _icons.add(_icon_id)
        return list(_icons)

    def set_view(self, view: wx.Window):
        self.viewRef = weakref.ref(view)

    def register(self, **kwargs):
        _parent = kwargs.get('parent')
        if _parent is None:
            _parent = self.root
        kwargs.update({'parent': _parent})
        return self.model.append_node(**kwargs)

    def unregister(self, uid: str):
        _find = self.get_preference_node(uid)
        if _find is not None:
            self.model.remove_node(_find)

    def get_preference_node(self, uid: str):
        return anytree.find(self.root, lambda x: x.uuid == uid)

    def create_view(self, uid: str, parent: wx.Window):
        _find = self.get_preference_node(uid)
        if _find is not None:
            if self.currentPage is not None:
                self.currentPage.Show(False)
            if _find.viewRef is not None:
                _find.viewRef.Show(True)
            else:
                if _find.viewCls is None:
                    return
                _win: 'BasePreferencePage' = _find.viewCls(parent)
                _win.set_content(_find.content)
                parent.Bind(_win.EVT_PREFERENCE_CHANGED, self.on_preference_changed)
                _find.viewRef = _win
            self.currentPage = _find.viewRef

    def on_preference_changed(self, evt: wx.CommandEvent):
        raise NotImplementedError
