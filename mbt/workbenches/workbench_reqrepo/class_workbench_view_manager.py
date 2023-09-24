# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_workbench_view_manager.py
# ------------------------------------------------------------------------------
#
# File          : class_workbench_view_manager.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, copy
from mbt.application.workbench_base import MBTBaseWorkbenchViewManager
from mbt.application.project import ProjectTreeNode, ProjectNodeProfile, EnumProjectItemRole
from mbt.gui.project import UtilProjectNodeEdit
from .application.class_base_cc import CommandRemoveProjectNode, CommandModifyProjectNodeProperty, CommandAppendProjectNode
from .gui.class_view import ReqRepoWorkbenchMainView


class MBTReqRepoWorkbenchViewManager(MBTBaseWorkbenchViewManager):
    def __init__(self, **kwargs):
        MBTBaseWorkbenchViewManager.__init__(self, **kwargs)

    def create_view(self, **kwargs) -> ReqRepoWorkbenchMainView:
        pass

    def setup(self, *args, **kwargs):
        pass

    def teardown(self, *args, **kwargs):
        pass

    def prepare_add_node(self, parent: ProjectTreeNode, child_role: str, describable: bool, role_name: str, **kwargs):
        _auto_name = ProjectTreeNode.auto_generate_name(parent, role_name)
        _init_param = {'profile':
                           {'name': _auto_name,
                            'description': 'description of %s' % role_name
                            },
                       'role': child_role
                       }
        if describable:
            _wz_options = dict()
            _wz_options['title'] = 'New%sNode' % role_name
            _wz_options['profile_content'] = _init_param['profile']
            _solution_choice = False
            _ret, _res = UtilProjectNodeEdit.wizard_for_new_or_edit_node(**_wz_options)
            _res['role'] = child_role
            return _ret, _res
        else:
            _res = copy.deepcopy(_init_param)
            _res.update({'profile': ProjectNodeProfile(**_init_param['profile'])})
            return True, _res

    def add_project_node(self, parent_node: ProjectTreeNode, meta: dict, role_name: str, copy_=False):
        if copy_:
            _name = 'ModelWorkbenchCopy%sNode' % role_name
        else:
            _name = 'ModelWorkbenchAddNew%sNode' % role_name
        _cmd = CommandAppendProjectNode(self, parent_node.uuid, meta, name=_name)
        _ret = self.undoStack.Submit(_cmd)
        if _ret:
            return _ret, _cmd.nodeUid
        else:
            return _ret, 'undostack command could not executed successfully.'

    def remove_project_node(self, node: ProjectTreeNode):
        _cmd = CommandRemoveProjectNode(self, node, name='ModelWorkbenchRemove%sNode' % node.label)
        _ret = self.undoStack.Submit(_cmd)
        if _ret:
            return _ret, _cmd.node
        else:
            return _ret, 'undostack command could not executed successfully.'

    def modify_node_property(self, node: ProjectTreeNode, modifier_key: str):
        if modifier_key == ProjectTreeNode.MODIFIER_KEY_PROFILE:
            _wz_options = dict()
            _wz_options['title'] = 'Reprofile %s' % node.label
            _wz_options['profile_content'] = {'name': node.profile.get('name'), 'description': node.profile.get('description')}
            _ret, _res = UtilProjectNodeEdit.wizard_for_new_or_edit_node(**_wz_options)
            if _ret:
                _cmd = CommandModifyProjectNodeProperty(self, node,
                                                        name='ModelWorkbenchModify%sNode' % node.label,
                                                        new_value=_res['profile'], old_value=_wz_options['profile_content'], modifier_key=modifier_key)
                _ret = self.undoStack.Submit(_cmd)
                if _ret:
                    return _ret, _cmd.node
                else:
                    return _ret, 'undostack command could not executed successfully.'
        else:
            return False, 'unsupported modifier key %s' % modifier_key

    # --------------------------------------------------------------
    # event handling
    # --------------------------------------------------------------

    def on_menu(self, evt: wx.CommandEvent):
        pass
