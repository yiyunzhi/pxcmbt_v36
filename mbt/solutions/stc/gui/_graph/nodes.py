# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : nodes.py
# ------------------------------------------------------------------------------
#
# File          : nodes.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from core.gui.qtproperty_grid import (Property,
                                      PropertyCategory,
                                      StringProperty,
                                      BoolProperty,
                                      BitFlagProperty, PropertyModel)
from mbt.gui.node_graph import (NodeObject,
                                BackdropNode,
                                GroupNode,
                                EnumNodeConnectionPolicy)
from .factory import SOLUTION_STC_CLS_FACTORY


class _MixinConnectionAccept:
    def accept_incoming_connection(self):
        raise NotImplementedError()

    def accept_outgoing_connection(self):
        raise NotImplementedError()


class _MixinPropertyDefs:
    def build_property_defs(self: NodeObject):
        self.propertyManager.propertyModel = PropertyModel()
        _cate_data = PropertyCategory(name='cateData', label='data')
        _cate_appearance = PropertyCategory(name='cateAppearance', label='appearance')
        _cate_layout = PropertyCategory(name='cateLayout', label='layout')
        _uid_prop = StringProperty(name='data.uid', label='uid', host=self, getter='uid', readonly=True, parent=_cate_data)
        _typ_prop = StringProperty(name='data.type', label='type', host=self, getter='type_', readonly=True, parent=_cate_data)
        _disabled_prop = BoolProperty(name='data.disabled', label='disabled', host=self, getter='disabled', readonly=True, parent=_cate_data)
        _selected_prop = BoolProperty(name='data.selected', label='selected', host=self, getter=self.view.isSelected, readonly=True, parent=_cate_data)
        _visible_prop = BoolProperty(name='data.visible', label='visible', host=self, getter='visible', readonly=True, parent=_cate_data)
        _connect_policy_prop = BoolProperty(name='data.connectPolicy', label='connectPolicy', host=self, getter='connectPolicy', readonly=True,
                                            parent=_cate_data)

        _label_prop = StringProperty(name='data.label', label='label', host=self, getter='label', readonly=True, parent=_cate_appearance)
        _color_prop = StringProperty(name='data.color', label='color', host=self, getter='color', readonly=True, parent=_cate_appearance)
        _border_color_prop = StringProperty(name='data.borderColor', label='borderColor', host=self, getter='borderColor', readonly=True,
                                            parent=_cate_appearance)
        _sel_border_color_prop = StringProperty(name='data.selectedBorderColor', label='selectedBorderColor', host=self, getter='selectedBorderColor',
                                                readonly=True, parent=_cate_appearance)
        _text_color_prop = StringProperty(name='data.textColor', label='textColor', host=self, getter='textColor', readonly=True, parent=_cate_appearance)
        # _icon_prop = StringProperty(name='data.icon', label='icon', host=self, getter='icon', readonly=True, parent=_cate_appearance)
        _w_prop = StringProperty(name='data.width', label='width', host=self, getter='width', readonly=True, parent=_cate_appearance)
        _h_prop = StringProperty(name='data.height', label='height', host=self, getter='height', readonly=True, parent=_cate_appearance)

        _layout_dir_prop = StringProperty(name='data.layoutDir', label='layoutDir', host=self, getter='layoutDirection', readonly=True, parent=_cate_appearance)
        self.propertyManager.append_property(_cate_data)
        self.propertyManager.append_property(_cate_appearance)
        self.propertyManager.append_property(_cate_layout)


class InitialStateNode(NodeObject, _MixinConnectionAccept, _MixinPropertyDefs):
    serializeTag = '!InitialStateNode'
    __namespace__ = 'SysML'
    __alias__ = 'initialState'
    viewFactory = SOLUTION_STC_CLS_FACTORY

    def __init__(self, **kwargs):
        NodeObject.__init__(self, **kwargs, view_type='SysMLView:initialStateView')
        self._color = kwargs.get('color', '#000000')
        self._width = kwargs.get('width', 24.0)
        self._height = kwargs.get('height', 24.0)
        self._minWidth = kwargs.get('min_width', 24.0)
        self._minHeight = kwargs.get('min_height', 24.0)
        self._connectPolicy = EnumNodeConnectionPolicy.ANYWHERE
        self.build_property_defs()

    def accept_incoming_connection(self):
        return []

    def accept_outgoing_connection(self):
        return ['SysML.SimpleStateNode']


class FinalStateNode(NodeObject, _MixinConnectionAccept, _MixinPropertyDefs):
    serializeTag = '!FinalStateNode'
    __namespace__ = 'SysML'
    __alias__ = 'finalState'
    viewFactory = SOLUTION_STC_CLS_FACTORY

    def __init__(self, **kwargs):
        NodeObject.__init__(self, **kwargs, view_type='SysMLView:finalStateView')
        self._color = kwargs.get('color', '#000000')
        self._borderColor = kwargs.get('border_color', '#000000')
        self._width = kwargs.get('width', 24.0)
        self._height = kwargs.get('height', 24.0)
        self._minWidth = kwargs.get('min_width', 24.0)
        self._minHeight = kwargs.get('min_height', 24.0)
        self._connectPolicy = EnumNodeConnectionPolicy.ANYWHERE
        self.build_property_defs()

    def accept_incoming_connection(self):
        return ['SysML.SimpleStateNode']

    def accept_outgoing_connection(self):
        return []


class SimpleStateNode(NodeObject, _MixinConnectionAccept, _MixinPropertyDefs):
    serializeTag = '!SimpleStateNode'
    __namespace__ = 'SysML'
    __alias__ = 'state'
    viewFactory = SOLUTION_STC_CLS_FACTORY

    def __init__(self, **kwargs):
        NodeObject.__init__(self, **kwargs, view_type='SysMLView:stateView', label='New State')
        self._color = kwargs.get('color', '#ffeccc')
        self._borderColor = kwargs.get('color', '#0d1217')
        self._textColor = kwargs.get('text_color', '#0d1217')
        self._connectPolicy = EnumNodeConnectionPolicy.ANYWHERE
        self.build_property_defs()

    def accept_incoming_connection(self):
        return ['SysML.SimpleStateNode', 'SysML.InitialStateNode']

    def accept_outgoing_connection(self):
        return ['SysML.SimpleStateNode', 'SysML.FinalStateNode']


class CompositeStateNode(BackdropNode, _MixinConnectionAccept):
    serializeTag = '!CompositeStateNode'
    __namespace__ = 'SysML'
    __alias__ = 'compositeState'
    viewFactory = SOLUTION_STC_CLS_FACTORY

    def __init__(self, **kwargs):
        BackdropNode.__init__(self, **kwargs, view_type='SysMLView:compositeStateView')
        self._color = kwargs.get('color', '#ffeccc')
        self._borderColor = kwargs.get('color', '#0d1217')
        self._textColor = kwargs.get('text_color', '#0d1217')
        self._connectPolicy = EnumNodeConnectionPolicy.ANYWHERE

    def accept_incoming_connection(self):
        return ['SysML.SimpleStateNode', 'SysML.InitialStateNode', 'SysML.CompositeStateNode']

    def accept_outgoing_connection(self):
        return ['SysML.SimpleStateNode', 'SysML.FinalStateNode', 'SysML.CompositeStateNode']


class SubStateNode(GroupNode, _MixinConnectionAccept):
    serializeTag = '!SubStateNode'
    __namespace__ = 'SysML'
    __alias__ = 'subState'
    viewFactory = SOLUTION_STC_CLS_FACTORY

    def __init__(self, **kwargs):
        GroupNode.__init__(self, **kwargs, view_type='SysMLView:subStateView')
        self._color = kwargs.get('color', '#ffeccc')
        self._borderColor = kwargs.get('color', '#0d1217')
        self._textColor = kwargs.get('text_color', '#0d1217')
        self._connectPolicy = EnumNodeConnectionPolicy.ANYWHERE

    def accept_incoming_connection(self):
        return ['SysML.SimpleStateNode', 'SysML.InitialStateNode']

    def accept_outgoing_connection(self):
        return ['SysML.SimpleStateNode', 'SysML.FinalStateNode']


SOLUTION_STC_CLS_FACTORY.register(InitialStateNode)
SOLUTION_STC_CLS_FACTORY.register(FinalStateNode)
SOLUTION_STC_CLS_FACTORY.register(SimpleStateNode)
# SOLUTION_STC_CLS_FACTORY.register(CompositeStateNode)
# SOLUTION_STC_CLS_FACTORY.register(SubStateNode)
