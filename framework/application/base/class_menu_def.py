# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_menu_def.py
# ------------------------------------------------------------------------------
#
# File          : class_menu_def.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx
import anytree


class MenuDef(anytree.NodeMixin):
    def __init__(self, **kwargs):
        self.iconSize = kwargs.get('iconSize', wx.Size(16, 16))
        self.icon = kwargs.get('icon', wx.ART_NORMAL_FILE)
        self.label = kwargs.get('label', 'UnnamedMenu')
        self.id = kwargs.get('id', wx.NewIdRef())
        self.userData = kwargs.get('userData')
        self.shortcut = kwargs.get('shortcut')
        self.kind = kwargs.get('kind', wx.ITEM_NORMAL)
        self.helpString = kwargs.get('helpString', self.label)
        self.parent = kwargs.get('parent')
        _children = kwargs.get('children')
        if _children:
            self.children = _children

    def find_by_attr(self, val, attr: str = 'id') -> any:
        return anytree.find_by_attr(self, val, attr)

    @staticmethod
    def build_menu(def_node: 'MenuDef', exclusive=[]):
        _menu = wx.Menu()
        for x in def_node.children:
            if x.id in exclusive:
                continue
            _submenu = None
            if x.children:
                _submenu = x.build_menu(x, exclusive)
            if x.shortcut is not None:
                _label = x.label + x.shortcut
            else:
                _label = x.label
            _item = wx.MenuItem(_menu, x.id, _label, x.helpString, x.kind, _submenu)
            if x.icon is not None:
                if isinstance(x.icon, (str, bytes)):
                    _item.SetBitmap(wx.ArtProvider.GetBitmap(x.icon, size=x.iconSize))
                elif isinstance(x.icon, wx.Bitmap):
                    _item.SetBitmap(x.icon)
            _menu.Append(_item)
        return _menu
