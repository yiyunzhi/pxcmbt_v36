# -*- coding: utf-8 -*-
import copy
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
from mbt.application.project import (ProjectTreeNode, Project, EnumProjectItemRole,
                                     EnumProjectItemFlag, ProjectNodeProfile,
                                     ProjectNodeEditorTypeFactoryItem)
from mbt.application.workbench_base import MBTProjectOrientedWorkbench, EnumMBTWorkbenchFlag
from mbt.gui.project import UtilProjectNodeEdit
from .gui import ModelPrototypeSketchEditorManager
from .application.model_content_provider import ModelContentInsertContract, ModelContentDeleteContract, ModelContentUpdateContract, ModelContentQueryContract
from .application.define import WB_MODEL_UID
from .class_workbench_view_manager import MBTModelWorkbenchViewManager


class ModelWorkbenchException(Exception): pass


class ModelWorkbench(MBTProjectOrientedWorkbench):
    # todo: preference about to this workbench could also inject into main preference page.
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
        _model_stereotype_uri = ProjectTreeNode.get_node_stereotype_uri(self.uid, ProjectTreeNode.NODE_ST_NATIVE, to_string=True)
        self.editorFactory.register_with('ModelPrototypeSketchEditor',
                                         ModelPrototypeSketchEditorManager,
                                         wb_uid=self.uid,
                                         role=EnumProjectItemRole.PROTOTYPE_SKETCH.value,
                                         stereotype_uri=_model_stereotype_uri,
                                         item_class=ProjectNodeEditorTypeFactoryItem)

    def _do_find_this_child_by_uid(self, uid):
        return Project.find(self.rootNode, lambda x: x.uuid == uid.uid)

    def setup(self, project: Project):
        _ret = super().setup(project)
        if _ret:
            _root_undo_stack = self.project.contentManager.manager.root.undoStack
            self.viewManager = MBTModelWorkbenchViewManager(uid=self.uid, workbench=self, undo_stack=_root_undo_stack)
            self.viewManager.parent = self.project.contentManager.manager
            self.viewManager.setup()
        return _ret

    def get_role_name(self, role: str) -> str:
        return EnumProjectItemRole(role).name

    def add_project_node(self, parent: ProjectTreeNode, child_role: str, **kwargs) -> str:
        if self.viewManager is None:
            raise ModelWorkbenchException('viewManager was not initialized.')
        if not self.is_my_descendant(parent.uuid) or not self.is_my_descendant(child_role, 'role'):
            raise ModelWorkbenchException('not a valid node parameter for adding.')
        _role_name = self.get_role_name(child_role).capitalize()
        _meta = kwargs.get('meta')
        _copy = True
        if not _meta:
            _copy = False
            _describable = self.project.contentManager.check_flag_of_role_config(child_role, EnumProjectItemFlag.DESCRIBABLE)
            _ret, _meta = self.viewManager.prepare_add_node(parent, child_role, _describable, _role_name, **kwargs)
            if _ret == -1:
                raise ModelWorkbenchException('preparing for adding is failed.')
        # todo: fix if copy the name could duplicated.
        _ret, _res = self.viewManager.add_project_node(parent, _meta, _role_name, copy_=_copy)
        if not _ret:
            raise ModelWorkbenchException(_res)
        return _res

    def remove_project_node(self, uid: str, **kwargs):
        if self.viewManager is None:
            raise ModelWorkbenchException('viewManager was not initialized.')
        if not self.is_my_descendant(uid):
            raise ModelWorkbenchException('not a valid node parameter for deleting.')
        _node = self.project.projectTreeModel.find_node_by_uid(uid)
        _ret, _res = self.viewManager.remove_project_node(_node)
        if not _ret:
            raise ModelWorkbenchException(_res)

    def modify_project_node_property(self, uid: str, modifier_key: str):
        if self.viewManager is None:
            raise ModelWorkbenchException('viewManager was not initialized.')
        _node = self.find_descendants_node_by_uid(uid)
        _ret, _res = self.viewManager.modify_node_property(_node, modifier_key)
        if not _ret:
            raise ModelWorkbenchException(_res)

    def open_project_node(self, uid, **kwargs):
        if self.viewManager is None:
            raise ModelWorkbenchException('viewManager was not initialized.')
        if not self.is_my_descendant(uid):
            raise ModelWorkbenchException('not a valid node parameter for editing in this workbench.')
        _hash = kwargs.get('hash')
        _editor_mgr = None
        if self.has_flag(EnumMBTWorkbenchFlag.HAS_EDITOR):
            _node = self.find_descendants_node_by_uid(uid)
            _editor_mgr = self.editorFactory.create_instance(_hash, parent=self.viewManager, uid=uid, view_title=_node.get_path_string())
        return _editor_mgr

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
