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
from .application.define import WB_REQ_REPO_UID
from .class_workbench_view_manager import MBTReqRepoWorkbenchViewManager
from .gui import TestReqRepoEditorManager


class ReqRepoWorkbench(MBTProjectOrientedWorkbench):
    NODE_CFG = os.path.join(os.path.dirname(__file__), 'application', 'wb_reqrepo_project_nodes.yaml')

    def __init__(self, base_role: str):
        MBTProjectOrientedWorkbench.__init__(self,
                                             optional=False,
                                             icon='pi.receipt',
                                             uid=WB_REQ_REPO_UID,
                                             flags=EnumMBTWorkbenchFlag.OPTIONAL | EnumMBTWorkbenchFlag.DEFAULT,
                                             base_role=base_role,
                                             construction_cfg_file=self.NODE_CFG,
                                             profile=BasicProfile(name='ReqRepoWorkbench', description='workbench for requirements managing.')
                                             )
        self.viewManager = MBTReqRepoWorkbenchViewManager(uid=self.uid, workbench=self)
        _req_stereotype_uri = ProjectTreeNode.get_node_stereotype_uri(self.uid, ProjectTreeNode.NODE_ST_NATIVE, to_string=True)
        self.editorFactory.register_with('ReqRepoEditor',
                                         TestReqRepoEditorManager,
                                         wb_uid=self.uid,
                                         role=EnumProjectItemRole.REQ_REPO.value,
                                         stereotype_uri=_req_stereotype_uri,
                                         item_class=ProjectNodeEditorTypeFactoryItem)

    def get_role_name(self, role: str) -> str:
        return EnumProjectItemRole(role).name
