# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_wx_menu_builder.py
# ------------------------------------------------------------------------------
#
# File          : class_wx_menu_builder.py
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
import blinker


class WxMenuBuilder:
    sigCommandSendTriggered = blinker.signal('sigCommandSendTriggered')

    def __init__(self, evt_handler: wx.EvtHandler, evt_object: wx.EvtHandler = None):
        assert isinstance(evt_handler, wx.EvtHandler)
        self.evtHandler = evt_handler
        self.evtObject = evt_object
        if self.evtObject is None:
            self.evtObject = self.evtHandler
        self.iconSize = wx.Size(16, 16)

    def _make_menu(self, menu: wx.Menu, cfg_dict: dict, context, disable_map):
        _kind=cfg_dict['kind']
        if _kind==wx.ITEM_SEPARATOR:
            menu.AppendSeparator()
        else:
            _icon = cfg_dict.pop('icon')
            _id = cfg_dict.pop('wxId') if 'wxId' in cfg_dict else None
            _children = cfg_dict.pop('children')
            _handler = cfg_dict.pop('handler') if 'handler' in cfg_dict else None
            if _children:
                _sub_menu = wx.Menu()
                menu.AppendSubMenu(_sub_menu, cfg_dict.get('text'))
                for x in _children:
                    self._make_menu(_sub_menu, x, context, disable_map)
            else:
                if _id is None:
                    _id = wx.NewIdRef()
                else:
                    if isinstance(_id, str) and _id.startswith('&'):
                        _id = eval(_id[1::], globals(), context)
                _this = context.get('this')
                _item = menu.Append(_id, cfg_dict.get('text'), cfg_dict.get('helpString'))
                if _handler is not None and _handler:
                    _handler_name = _handler.get('name')
                    _handler_kwargs = _handler.get('kwargs')
                    if _handler_name.startswith('>'):
                        _msg = _handler_name[1::]
                        self.evtObject.Bind(wx.EVT_MENU,
                                             lambda evt: self.sigCommandSendTriggered.send(self, event=evt, message=_msg, object=_this, **_handler_kwargs),
                                             _item)
                    else:
                        assert hasattr(self.evtHandler, _handler_name), 'no handler %s found in class %s' % (_handler_name, self.evtHandler.__class__.__name__)
                        self.evtHandler.Bind(wx.EVT_MENU,
                                             lambda evt: getattr(self.evtHandler, _handler_name)(evt, _this, **_handler_kwargs),
                                             _item)
                if _id in disable_map:
                    _item.Enable(False)
                if _icon is not None:
                    _item.SetBitmap(wx.ArtProvider.GetBitmap(_icon, wx.ART_MENU, self.iconSize))

    def get_menu(self, cfg_collection: list, context: dict, disable_map: list):
        _menu = wx.Menu()
        for x in cfg_collection:
            _kind = x['kind']
            if _kind == wx.ITEM_SEPARATOR:
                _menu.AppendSeparator()
            else:
                self._make_menu(_menu, x, context, disable_map)
        return _menu
