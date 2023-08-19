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
import os
from framework.application.base import BasicProfile
from mbt.application.project import EnumProjectItemRole, ProjectTreeNode, ProjectNodeEditorTypeFactoryItem
from mbt.application.workbench_base import MBTProjectOrientedWorkbench, EnumMBTWorkbenchFlag
from .application.define import WB_TEST_UID
from .class_workbench_view_manager import MBTTestWorkbenchViewManager
from .gui import TestEnvEditorManager, TestExeEditorManager, TestCaseResultEditorManager, TestCaseSettingEditorManager


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
        self.viewManager = MBTTestWorkbenchViewManager(uid=self.uid, workbench=self)
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

    def get_role_name(self, role: str) -> str:
        return EnumProjectItemRole(role).name
