# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_prop_container.py
# ------------------------------------------------------------------------------
#
# File          : class_prop_container.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import anytree
from framework.gui.base import (PropertyDefPageManager, CategoryPropertyDef,
                                BasePropContainer,
                                StringPropertyDef,
                                FlagsPropertyDef,
                                BoolPropertyDef, IntPropertyDef)
from .define import EnumProjectItemRole, EnumProjectItemFlag
from .class_project import ProjectTreeNode


class _ObjectPlaceHolder:
    pass


class ProjectNodePropContainer(BasePropContainer):
    def __init__(self):
        BasePropContainer.__init__(self)
        # for reuse with self.set_node() purpose
        _obj = _ObjectPlaceHolder()
        self._pageDefault = PropertyDefPageManager(name='default')
        _cat_profile = self._pageDefault.register_with(CategoryPropertyDef, object=_obj,
                                                       label='Profile')
        self._pageDefault.register_with(StringPropertyDef, object=_obj,
                                        label='label', getter='label', readonly=True, parent=_cat_profile)
        self._pageDefault.register_with(StringPropertyDef, object=_obj,
                                        label='description', getter='description', readonly=True, parent=_cat_profile)
        _cat_data = self._pageDefault.register_with(CategoryPropertyDef, object=_obj,
                                                    label='Attributes')
        self._pageDefault.register_with(StringPropertyDef, object=_obj,
                                        label='uuid', getter='uuid', readonly=True, parent=_cat_data)
        self._pageDefault.register_with(StringPropertyDef, object=_obj,
                                        label='role', getter=lambda x: EnumProjectItemRole(x.role), readonly=True, parent=_cat_data)
        self._pageDefault.register_with(StringPropertyDef, object=_obj,
                                        label='path', getter='get_path_string', readonly=True, parent=_cat_data)
        self._pageDefault.register_with(FlagsPropertyDef, object=_obj,
                                        labels=[x.name for x in EnumProjectItemFlag],
                                        values=[x.value for x in EnumProjectItemFlag],
                                        label='flag', getter='flag', readonly=True, parent=_cat_data)
        self._pageDefault.register_with(StringPropertyDef, object=_obj,
                                        label='workbench', getter='workbenchUid', readonly=True, parent=_cat_data)
        self._pageDefault.register_with(StringPropertyDef, object=_obj,
                                        label='stereotype', getter='stereotype', readonly=True, parent=_cat_data)
        self._pageDefault.register_with(StringPropertyDef, object=_obj,
                                        label='stereotypeUri', getter='stereotypeUri', readonly=True, parent=_cat_data)

        # self._pageDefault.register_with(IntPropertyDef, object=_obj,
        #                                  label='Test', getter='_test',setter='_test', parent=_cat_data)
        self.add_page(self._pageDefault)

    def set_node(self, node: ProjectTreeNode):
        _l = anytree.findall(self._pageDefault.root, lambda x: isinstance(x.object, (ProjectTreeNode, _ObjectPlaceHolder)))
        for x in _l:
            x.set_object(node)
