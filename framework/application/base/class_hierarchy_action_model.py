# -*- coding: utf-8 -*-
import typing

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_app_mode_select_action.py
# ------------------------------------------------------------------------------
#
# File          : class_app_mode_select_action.py
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


class HierarchyActionModel(anytree.NodeMixin):
    def __init__(self, **kwargs):
        self.i18nNs = kwargs.get('i18nNs', 'app')
        self.uid = kwargs.get('uid', 0)
        self.oid = kwargs.get('oid', 0)
        self.label = kwargs.get('label')
        self.asContainer = kwargs.get('asContainer', False)
        self.tooltip = kwargs.get('tooltip', self.label)
        self.iconNs = kwargs.get('iconNs', 'fa')
        self.iconName = kwargs.get('iconName', 'mdi6.view-dashboard')
        self.state = kwargs.get('initCheckState', False)
        self.stateGrouEnabled = kwargs.get('stateGroupEnabled', [])
        self.checkable = kwargs.get('checkable', False)
        self.enabled = kwargs.get('enabled', True)
        self.shortcut = kwargs.get('shortcut', None)
        self.handle = kwargs.get('handle', None)
        self.actionGroup = kwargs.get('actionGroup', None)
        self.actionName = kwargs.get('actionName', None)
        self.parent = kwargs.get('parent')
        self.layoutModifiers = []
        _layoutModifiers = kwargs.get('layoutModifiers', [])
        for x in _layoutModifiers:
            self.layoutModifiers.append(x)

    def get_label(self):
        return '%s.%s' % (self.i18nNs, self.label)

    def get_icon_info(self):
        if self.iconNs is None or self.iconName is None:
            return None
        return self.iconNs, self.iconName

    def is_in_state_group_enabled(self, s_name: typing.Union[str, typing.Sequence]):
        if not self.stateGrouEnabled:
            return True
        if isinstance(s_name, str):
            s_name = [s_name]
        for x in self.stateGrouEnabled:
            if isinstance(x, str):
                if x in s_name:
                    return True
            elif isinstance(x, (list, tuple, set)):
                if all([ss in s_name for ss in x]):
                    return True
        return False
