# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_workbench.py
# ------------------------------------------------------------------------------
#
# File          : class_workbench.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, copy
from framework.application.base import BasicProfile
from mbt.application.project import (EnumProjectItemRole,
                                     ProjectTreeNode,
                                     Project,
                                     ProjectNodeEditorTypeFactoryItem,
                                     EnumProjectItemFlag,
                                     ProjectNodeProfile)
from mbt.application.workbench_base import MBTProjectOrientedWorkbench, EnumMBTWorkbenchFlag
from mbt.gui.project import UtilProjectNodeEdit
from .application.define import WB_TEST_UID
from .class_workbench_view_manager import MBTTestWorkbenchViewManager
from .gui import TestEnvEditorManager, TestExeEditorManager, TestCaseResultEditorManager, TestCaseSettingEditorManager


class TestWorkbenchException(Exception): pass


class TestWorkbench(MBTProjectOrientedWorkbench):
    NODE_CFG = os.path.join(os.path.dirname(__file__), 'application', 'wb_test_project_nodes.yaml')

    def __init__(self, base_role: str):
        MBTProjectOrientedWorkbench.__init__(self,
                                             optional=False,
                                             icon='local.gauge',
                                             uid=WB_TEST_UID,
                                             flags=EnumMBTWorkbenchFlag.DEFAULT,
                                             base_role=base_role,
                                             construction_cfg_file=self.NODE_CFG,
                                             profile=BasicProfile(name='TestWorkbench', description='workbench for testing.')
                                             )
        _test_stereotype_uri = ProjectTreeNode.get_node_stereotype_uri(self.uid, ProjectTreeNode.NODE_ST_NATIVE, to_string=True)

        self.editorFactory.register_with('TestcaseSettingEditor',
                                         TestCaseSettingEditorManager,
                                         wb_uid=self.uid,
                                         role=EnumProjectItemRole.TESTCASE_SETTING.value,
                                         stereotype_uri=_test_stereotype_uri,
                                         item_class=ProjectNodeEditorTypeFactoryItem)
        self.editorFactory.register_with('TestcaseResultEditor',
                                         TestCaseResultEditorManager,
                                         wb_uid=self.uid,
                                         role=EnumProjectItemRole.TESTCASE_RESULT.value,
                                         stereotype_uri=_test_stereotype_uri,
                                         item_class=ProjectNodeEditorTypeFactoryItem)
        self.editorFactory.register_with('TestEnvEditor', TestEnvEditorManager,
                                         wb_uid=self.uid,
                                         role=EnumProjectItemRole.TEST_ENV.value,
                                         stereotype_uri=_test_stereotype_uri,
                                         item_class=ProjectNodeEditorTypeFactoryItem)
        self.editorFactory.register_with('TestExecutorEditor',
                                         TestExeEditorManager,
                                         wb_uid=self.uid,
                                         role=EnumProjectItemRole.TEST_RUN.value,
                                         stereotype_uri=_test_stereotype_uri,
                                         item_class=ProjectNodeEditorTypeFactoryItem)

    def setup(self, project: Project):
        _ret = super().setup(project)
        if _ret:
            _root_undo_stack = self.project.contentManager.manager.root.undoStack
            self.viewManager = MBTTestWorkbenchViewManager(uid=self.uid, workbench=self, undo_stack=_root_undo_stack)
            self.viewManager.parent = self.project.contentManager.manager
            self.viewManager.setup()
        return _ret

    def get_role_name(self, role: str) -> str:
        return EnumProjectItemRole(role).name

    def add_project_node(self, parent: ProjectTreeNode, child_role: str, **kwargs) -> str:
        if self.viewManager is None:
            raise TestWorkbenchException('viewManager was not initialized.')
        if not self.is_my_descendant(parent.uuid) or not self.is_my_descendant(child_role, 'role'):
            raise TestWorkbenchException('not a valid node parameter for adding.')
        _role_name = self.get_role_name(child_role).capitalize()
        _meta = kwargs.get('meta')
        _copy = True
        if not _meta:
            _copy = False
            _describable = self.project.contentManager.check_flag_of_role_config(child_role, EnumProjectItemFlag.DESCRIBABLE)
            _ret, _meta = self.viewManager.prepare_add_node(parent, child_role, _describable, _role_name, **kwargs)
            if _ret == -1:
                raise TestWorkbenchException('preparing for adding is failed.')
        # todo: fix if copy the name could duplicated.
        _ret, _res = self.viewManager.add_project_node(parent, _meta, _role_name, copy_=_copy)
        if not _ret:
            raise TestWorkbenchException(_res)
        return _res

    def remove_project_node(self, uid: str, **kwargs):
        if self.viewManager is None:
            raise TestWorkbenchException('viewManager was not initialized.')
        if not self.is_my_descendant(uid):
            raise TestWorkbenchException('not a valid node parameter for deleting.')
        _node = self.project.projectTreeModel.find_node_by_uid(uid)
        _ret, _res = self.viewManager.remove_project_node(_node)
        if not _ret:
            raise TestWorkbenchException(_res)

    def modify_project_node_property(self, uid: str, modifier_key: str):
        if self.viewManager is None:
            raise TestWorkbenchException('viewManager was not initialized.')
        _node = self.find_descendants_node_by_uid(uid)
        _ret, _res = self.viewManager.modify_node_property(_node, modifier_key)
        if not _ret:
            raise TestWorkbenchException(_res)

    def open_project_node(self, uid, **kwargs):
        if self.viewManager is None:
            raise TestWorkbenchException('viewManager was not initialized.')
        if not self.is_my_descendant(uid):
            raise TestWorkbenchException('not a valid node parameter for editing in this workbench.')
        _hash = kwargs.get('hash')
        _editor_mgr = None
        if self.has_flag(EnumMBTWorkbenchFlag.HAS_EDITOR):
            _node = self.find_descendants_node_by_uid(uid)
            _editor_mgr = self.editorFactory.create_instance(_hash, parent=self.viewManager, uid=uid, view_title=_node.get_path_string())
        return _editor_mgr

