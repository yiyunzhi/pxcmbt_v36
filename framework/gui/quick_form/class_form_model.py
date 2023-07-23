# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_form_model.py
# ------------------------------------------------------------------------------
#
# File          : class_form_model.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.base import TreeModel, TreeModelAnyTreeNode


class FormTreeNode(TreeModelAnyTreeNode):
    def __init__(self, **kwargs):
        TreeModelAnyTreeNode.__init__(self, **kwargs)
        self.fieldDef = kwargs.get('field_def')

    def __repr__(self):
        return '{}.'.format(self.label)


class FormModel(TreeModel):
    def __init__(self):
        TreeModel.__init__(self, FormTreeNode)
