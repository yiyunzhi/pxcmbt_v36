# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_prop_container.py
# ------------------------------------------------------------------------------
#
# File          : stc_prop_container.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import enum, anytree
from framework.application.utils_helper import util_get_object_props
from framework.gui.base import (PropertyDefPageManager,
                                PropertyDef,
                                BoolPropertyDef,
                                ArrayStringPropertyDef,
                                FloatPropertyDef,
                                CategoryPropertyDef,
                                StringPropertyDef,
                                FlagsPropertyDef,
                                BasePropContainer,
                                XYPropertyDef,
                                PropContainerException)
from framework.gui.wxgraph import WxShapeBase, __VERSION__, EnumGraphViewStyleFlag, EnumShapeStyleFlags
from .diagram.class_diagram_graph_view import STCGraphView
from .class_preference import STCPreference


class DiagramViewPropContainer(BasePropContainer):
    def __init__(self, view: STCGraphView):
        BasePropContainer.__init__(self)
        self.view = view
        self._pageDefault = PropertyDefPageManager(name='default')
        _cat_profile = self._pageDefault.register_with(CategoryPropertyDef, object=self.view,
                                                       label='Profile')
        self._pageDefault.register_with(StringPropertyDef, object=StringPropertyDef.CONSTANT,
                                        label='version', getter=__VERSION__, readonly=True, parent=_cat_profile)
        _cat_data = self._pageDefault.register_with(CategoryPropertyDef, object=self.view,
                                                    label='Attributes')
        _em = util_get_object_props(EnumGraphViewStyleFlag)
        _em = enum.Enum('EnumGraphViewStyleFlag', _em)
        self._pageDefault.register_with(FlagsPropertyDef, object=self.view.setting,
                                        labels=[x.name for x in _em],
                                        values=[x.value for x in _em],
                                        label='style', getter='style', readonly=True, parent=_cat_data)
        self._pageDefault.register_with(BoolPropertyDef, object=self.view,
                                        auto_init=True,
                                        label='hasScene', getter=lambda x: x.scene is not None, readonly=True, parent=_cat_data)
        self._pageDefault.register_with(FloatPropertyDef, object=self.view,
                                        auto_init=True,
                                        label='maxScale', getter=lambda x: x.setting.maxScale, readonly=True, parent=_cat_data)
        self._pageDefault.register_with(FloatPropertyDef, object=self.view,
                                        auto_init=True,
                                        label='minScale', getter=lambda x: x.setting.minScale, readonly=True, parent=_cat_data)
        self._pageDefault.register_with(BoolPropertyDef, object=self.view,
                                        auto_init=True,
                                        label='antialiasing', getter=lambda x: x.setting.enableGC, readonly=True, parent=_cat_data)
        self.add_page(self._pageDefault)


class _ElementPlaceHolder:
    pass


class DiagramElementPropContainer(BasePropContainer):
    def __init__(self, element: WxShapeBase = _ElementPlaceHolder()):
        BasePropContainer.__init__(self)
        self.element = element
        self._pageDefault = PropertyDefPageManager(name='default')
        _cat_profile = self._pageDefault.register_with(CategoryPropertyDef, object=self.element,
                                                       label='Profile')
        self._pageDefault.register_with(StringPropertyDef, object=self.element,
                                        label='uid', getter='uid', readonly=True, parent=_cat_profile)
        self._pageDefault.register_with(StringPropertyDef, object=self.element,
                                        label='identity', getter='identity', readonly=True, parent=_cat_profile)
        _cat_data = self._pageDefault.register_with(CategoryPropertyDef, object=self.element,
                                                    label='Attributes')
        self._pageDefault.register_with(XYPropertyDef, object=self.element,
                                        label='position', getter='absolutePosition', readonly=True, parent=_cat_data)
        self._pageDefault.register_with(XYPropertyDef, object=self.element,
                                        label='size', getter=lambda x: x.stylesheet.size, readonly=True, parent=_cat_data)
        self._pageDefault.register_with(ArrayStringPropertyDef, object=self.element,
                                        label='style', getter=self.format_element_style, readonly=True, parent=_cat_data)
        self._pageDefault.register_with(ArrayStringPropertyDef, object=self.element,
                                        label='allowedChildren', getter=self.format_accepted_children, readonly=True, parent=_cat_data)
        self._pageDefault.register_with(ArrayStringPropertyDef, object=self.element,
                                        label='allowedSrcElement', getter=self.format_accepted_src, readonly=True, parent=_cat_data)
        self._pageDefault.register_with(ArrayStringPropertyDef, object=self.element,
                                        label='allowedDstElement', getter=self.format_accepted_dst, readonly=True, parent=_cat_data)
        self._pageSpec = PropertyDefPageManager(name='specified')
        self.add_page(self._pageDefault)
        # todo: element has specified property
        self.add_page(self._pageSpec)

    def set_element(self, element: WxShapeBase):
        _l = anytree.findall(self._pageDefault.root, lambda x: isinstance(x.object, (WxShapeBase, _ElementPlaceHolder)))
        for x in _l:
            x.set_object(element)

    def format_element_style(self, element: WxShapeBase):
        _ret = list()
        _em = util_get_object_props(EnumShapeStyleFlags)
        _em = enum.Enum('EnumShapeStyleFlags', _em)
        for x in _em:
            if element.has_style(x.value):
                _str = '%s|%s' % (x.name, 'Y')
            else:
                _str = '%s|%s' % (x.name, 'N')
            _ret.append(_str)
        return _ret

    def format_accepted_children(self, element: WxShapeBase):
        _ret = list()
        for x in element.ddAcceptedChildren:
            _ret.append(x)
        if not _ret:
            _ret.append('NONE')
        return _ret

    def format_accepted_connection(self, element: WxShapeBase):
        _ret = list()
        for x in element.acceptedConnections:
            _ret.append(x)
        if not _ret:
            _ret.append('NONE')
        return _ret

    def format_accepted_src(self, element: WxShapeBase):
        _ret = list()
        for x in element.acceptedSrcNeighbours:
            _ret.append(x)
        if not _ret:
            _ret.append('NONE')
        return _ret

    def format_accepted_dst(self, element: WxShapeBase):
        _ret = list()
        for x in element.acceptedDstNeighbours:
            _ret.append(x)
        if not _ret:
            _ret.append('None')
        return _ret


class PreferenceViewPropContainer(BasePropContainer):
    def __init__(self, preference: STCPreference):
        BasePropContainer.__init__(self)
        self.preference = preference
        self._pageUi = PropertyDefPageManager(name='ui')
        _cat_bg = self._pageUi.register_with(CategoryPropertyDef, object=self.preference,
                                             label='Background')
        self._pageUi.register_with(BoolPropertyDef, object=self.preference,
                                   label='showGrid', getter='isGridVisible', setter='isGridVisible', parent=_cat_bg)
        self._pageUi.register_with(BoolPropertyDef, object=self.preference,
                                   label='showGradient', getter='isGradientVisible', setter='isGradientVisible', parent=_cat_bg)

        self._pageSpec = PropertyDefPageManager(name='specified')
        self.add_page(self._pageUi)
        self.add_page(self._pageSpec)
        self.update()

    def set_preference(self, preference):
        _l = anytree.findall(self._pageUi.root, lambda x: isinstance(x.object, (WxShapeBase, _ElementPlaceHolder)))
        for x in _l:
            x.set_object(preference)
