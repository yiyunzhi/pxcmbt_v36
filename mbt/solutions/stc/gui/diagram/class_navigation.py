# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_navigation.py
# ------------------------------------------------------------------------------
#
# File          : class_navigation.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.define import _
from framework.application.urlobject import URLObject
from .define import *
from ..class_image_resources import get_xpm_resources_icon

GRAPHVIEW_CTX_MENU_DEF = MenuDef()
_n = MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, label=_('Create'),icon=wx.ART_NEW)
MenuDef(parent=_n, label=_('InitialState'), id=EnumSTCMenuId.CREATE_INITIAL_STATE, icon=get_xpm_resources_icon(identity=IDENTITY_INITIAL_STATE),
        userData=URLObject.quick_create(STC_DIAGRAM_URL_SCHEME,
                                        STC_DIAGRAM_URL_CREATE_ELEM_NETLOC,
                                        queries={
                                            'identity': IDENTITY_INITIAL_STATE}))
MenuDef(parent=_n, label=_('SimpleState'), id=EnumSTCMenuId.CREATE_SIMPLE_STATE, icon=get_xpm_resources_icon(identity=IDENTITY_SIMPLE_STATE),
        userData=URLObject.quick_create(STC_DIAGRAM_URL_SCHEME,
                                        STC_DIAGRAM_URL_CREATE_ELEM_NETLOC,
                                        queries={'identity': IDENTITY_SIMPLE_STATE}))
MenuDef(parent=_n, label=_('FinalState'), id=EnumSTCMenuId.CREATE_FINAL_STATE, icon=get_xpm_resources_icon(identity=IDENTITY_FINAL_STATE),
        userData=URLObject.quick_create(STC_DIAGRAM_URL_SCHEME,
                                        STC_DIAGRAM_URL_CREATE_ELEM_NETLOC,
                                        queries={'identity': IDENTITY_FINAL_STATE}))
MenuDef(parent=_n, kind=wx.ITEM_SEPARATOR)
MenuDef(parent=_n, label=_('Note'), id=EnumSTCMenuId.CREATE_NOTE, icon=get_xpm_resources_icon(identity=IDENTITY_NOTE),
        userData=URLObject.quick_create(STC_DIAGRAM_URL_SCHEME,
                                        STC_DIAGRAM_URL_CREATE_ELEM_NETLOC,
                                        queries={'identity': IDENTITY_NOTE}))
# MenuDef(parent=_n, kind=wx.ITEM_SEPARATOR)
# MenuDef(parent=_n, label=_('Transition'), id=EnumSTCMenuId.CREATE_TRANSITION)
# MenuDef(parent=_n, label=_('NoteAssociation'), id=EnumSTCMenuId.CREATE_NOTE_CONN)
MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, kind=wx.ITEM_SEPARATOR)
MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, label=_('Undo'), id=wx.ID_UNDO, icon=wx.ART_UNDO,shortcut='\tCTRL+Z')
MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, label=_('Redo'), id=wx.ID_REDO, icon=wx.ART_REDO)
MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, label=_('Paste'), id=wx.ID_PASTE, icon=wx.ART_PASTE)
MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, kind=wx.ITEM_SEPARATOR)
_vn=MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, label=_('Validate'),icon=wx.ART_TIP)
MenuDef(parent=_vn, label=_('Compliance'), id=EnumSTCMenuId.VALIDATE_DIAGRAM_COMPLIANCE)
MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, kind=wx.ITEM_SEPARATOR)
MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, label=_('ZoomFit'), id=EnumSTCMenuId.ZOOM_FIT,icon=wx.ART_FULL_SCREEN)
MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, label=_('Zoom100%'), id=EnumSTCMenuId.ZOOM_100P, icon=get_xpm_resources_icon(name='zoom_100'),)
MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, kind=wx.ITEM_SEPARATOR)
_en=MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, label=_('Export'),icon='pi.export')
MenuDef(parent=_en, label=_('Image'), id=EnumSTCMenuId.EXPORT_TO_IMAGE,icon='pi.image')
# todo: add export to scxml
MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, label=_('Print'), id=EnumSTCMenuId.PRINT,icon=wx.ART_PRINT)
MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, kind=wx.ITEM_SEPARATOR)
MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, label=_('RemoveAll'), id=EnumSTCMenuId.REMOVE_ALL,icon=wx.ART_DELETE)
MenuDef(parent=GRAPHVIEW_CTX_MENU_DEF, label=_('EditProperty'), id=EnumSTCMenuId.EDIT_PROP,icon=wx.ART_EDIT)


ELEMENT_CTX_MENU_DEF = MenuDef()
_n = MenuDef(parent=ELEMENT_CTX_MENU_DEF, label=_('Create'),icon=wx.ART_NEW)
MenuDef(parent=_n, label=_('Transition'), id=EnumSTCMenuId.CREATE_TRANSITION,icon=get_xpm_resources_icon(identity=IDENTITY_TRANSITION),
        userData=URLObject.quick_create(STC_DIAGRAM_URL_SCHEME,
                                        STC_DIAGRAM_URL_CREATE_ELEM_NETLOC,
                                        queries={
                                            'identity': IDENTITY_TRANSITION}))
MenuDef(parent=_n, label=_('NoteAssociation'), id=EnumSTCMenuId.CREATE_NOTE_CONN,icon=get_xpm_resources_icon(identity=IDENTITY_NOTE_CONN),
        userData=URLObject.quick_create(STC_DIAGRAM_URL_SCHEME,
                                        STC_DIAGRAM_URL_CREATE_ELEM_NETLOC,
                                        queries={
                                            'identity': IDENTITY_NOTE_CONN}))
MenuDef(parent=ELEMENT_CTX_MENU_DEF, label=_('Copy'), id=wx.ID_COPY, icon=wx.ART_COPY)
MenuDef(parent=ELEMENT_CTX_MENU_DEF, label=_('Cut'), id=wx.ID_CUT, icon=wx.ART_CUT)
MenuDef(parent=ELEMENT_CTX_MENU_DEF, kind=wx.ITEM_SEPARATOR)
MenuDef(parent=ELEMENT_CTX_MENU_DEF, label=_('Remove'), id=wx.ID_REMOVE,icon=wx.ART_DELETE)
MenuDef(parent=ELEMENT_CTX_MENU_DEF, label=_('EditProperty'), id=EnumSTCMenuId.EDIT_ELEMENT_PROP,icon=wx.ART_EDIT)