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
import os, wx
from framework.application.base import BasicProfile
from framework.application.utils_helper import util_generate_uri
from mbt.application.project import (ProjectTreeNode, Project, EnumProjectItemRole, EnumProjectItemFlag, ProjectNodeProfile, ProjectNodeEditorTypeFactoryItem)
from mbt.application.workbench_base import MBTProjectOrientedWorkbench, EnumMBTWorkbenchFlag
from .gui import ModelPrototypeSketchEditorManager
from .application.model_content_provider import ModelContentInsertContract, ModelContentDeleteContract, ModelContentUpdateContract, ModelContentQueryContract
from .application.define import WB_MODEL_UID
from .class_workbench_view_manager import MBTModelWorkbenchViewManager


class ModelWorkbench(MBTProjectOrientedWorkbench):
    NODE_CFG = os.path.join(os.path.dirname(__file__), 'application', 'wb_model_project_nodes.yaml')

    def __init__(self, base_role: str):
        MBTProjectOrientedWorkbench.__init__(self,
                                             optional=False,
                                             icon='local.cube',
                                             uid=WB_MODEL_UID,
                                             base_role=base_role,
                                             flags=EnumMBTWorkbenchFlag.DEFAULT,
                                             construction_cfg_file=self.NODE_CFG,
                                             profile=BasicProfile(name='ModelWorkbench', description='workbench for modeling.')
                                             )
        self.viewManager = MBTModelWorkbenchViewManager(uid=self.uid, workbench=self)
        _model_stereotype_uri = ProjectTreeNode.get_node_stereotype_uri(self.uid, ProjectTreeNode.NODE_ST_NATIVE, to_string=True)
        self.editorFactory.register_with('ModelPrototypeSketchEditor',
                                         ModelPrototypeSketchEditorManager,
                                         wb_uid=self.uid,
                                         role=EnumProjectItemRole.PROTOTYPE_SKETCH.value,
                                         stereotype_uri=_model_stereotype_uri,
                                         item_class=ProjectNodeEditorTypeFactoryItem)

    def _do_find_this_child_by_uid(self, uid):
        return Project.find(self.rootNode, lambda x: x.uuid == uid.uid)

    def get_role_name(self, role: str) -> str:
        return EnumProjectItemRole(role).name

    def prepare_add_node(self, parent_uid: str, child_role: str, **kwargs) -> dict:
        if not self.is_my_descendant(parent_uid) or not self.is_my_descendant(child_role, 'role'):
            return {}
        _describable = self.project.contentManager.check_flag_of_role_config(child_role, EnumProjectItemFlag.DESCRIBABLE)
        _role_name = self.get_role_name(child_role).capitalize()
        return self.viewManager.prepare_add_node(child_role, _describable, _role_name)

    def do_content_insert(self, contract: ModelContentInsertContract):
        if self.project is None or contract.workbench != self.uid:
            return False
        _find: ProjectTreeNode = self._do_find_this_child_by_uid(contract.uid)
        if _find:
            return self.project.append_work_file_for_node(_find,
                                                          name=contract.name,
                                                          extension=contract.extension,
                                                          path=contract.path,
                                                          data=contract.data)

    def do_content_update(self, contract: ModelContentUpdateContract):
        if self.project is None or contract.workbench != self.uid:
            return False
        _find: ProjectTreeNode = self._do_find_this_child_by_uid(contract.uid)
        if _find:
            _uri = contract.get_work_file_node_uri()
            return self.project.save_data_into_node_work_file(_find, _uri, contract.data)

    def do_content_delete(self, contract: ModelContentDeleteContract):
        if self.project is None or contract.workbench != self.uid:
            return False
        _find: ProjectTreeNode = self._do_find_this_child_by_uid(contract.uid)
        if _find:
            _uri = contract.get_work_file_node_uri()
            return self.project.remove_node_work_file(_find, _uri)

    def do_content_query(self, contract: ModelContentQueryContract):
        if self.project is None or contract.workbench != self.uid:
            return
        _find: ProjectTreeNode = self._do_find_this_child_by_uid(contract.uid)
        if _find:
            return self.project.read_data_from_node_work_file(_find, uri=contract.get_work_file_node_uri())
