# -*- coding: utf-8 -*-
import copy
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_pane_proj_expl_cc.py
# ------------------------------------------------------------------------------
#
# File          : class_pane_proj_expl_cc.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, typing, shutil, anytree
import wx
from framework.application.base import Serializable
from framework.application.define import _
from framework.application.io import AppYamlFileIO, AppFileIO
from framework.application.urlobject import URLObject
from framework.application.utils_helper import util_is_dir_exist
from mbt.application.workbench_base import MBTProjectOrientedWorkbench
from mbt.application.mbt_solution_manager import MBTSolutionsManager
from mbt.application.project import (ProjectTreeNode,
                                     Project,
                                     ProjectTreeModel,
                                     EnumProjectItemRole, EnumProjectItemFlag,
                                     ProjectContentProvider, ContentContract,
                                     ProjectContentQueryContract, ProjectContentUpdateContract,
                                     ProjectContentInsertContract, ProjectContentDeleteContract, WorkFileNode,
                                     ProjectContentNodeQueryContract, MBTProjectNodeConstructorImporter)
from mbt.application.base import MBTContentContainer, MBTViewManager


class CommandAppendNode(wx.Command):
    def __init__(self, manager: MBTViewManager, parent_node_uid: str, node_meta: dict, can_undo=True, name='AppendNode'):
        wx.Command.__init__(self, can_undo, name)
        self.manager = manager
        self.parentNodeUid = parent_node_uid
        self.nodeMeta = node_meta

    @property
    def managerCC(self) -> 'ProjectExplorerContentContainer':
        return self.manager.contentContainer

    @property
    def parentNode(self):
        return self.managerCC.projectModel.find_node_by_uid(self.parentNodeUid)

    def Undo(self):
        _node = self.managerCC.projectModel.find_node_by_uid(self.nodeMeta['uuid'])
        self.managerCC.post_delete_project_node(_node)
        self.manager.view.refresh_tree()
        return True

    def Do(self):
        _node = self.managerCC.post_add_child_node_of(self.parentNode, self.nodeMeta['role'], self.nodeMeta)
        self.manager.emit_event(self.manager.T_EVT_NODE_ADDED, uid=_node.uuid)
        self.manager.view.refresh_tree()
        self.manager.view.select_node(_node)
        return True


class CommandRemoveNode(wx.Command):
    def __init__(self, manager: MBTViewManager, node: ProjectTreeNode, can_undo=True, name='RemoveNode'):
        wx.Command.__init__(self, can_undo, name)
        self.manager = manager
        self.nodeMeta = node.meta
        self.parentNodeUid = node.parent.uuid
        self.node = node

    @property
    def managerCC(self) -> 'ProjectExplorerContentContainer':
        return self.manager.contentContainer

    @property
    def parentNode(self):
        return self.managerCC.projectModel.find_node_by_uid(self.parentNodeUid)

    def Undo(self):
        _node = self.managerCC.post_add_child_node_of(self.parentNode, self.nodeMeta['role'], self.nodeMeta)
        _node.update(**self.nodeMeta)
        _node.uuid = self.nodeMeta['uuid']
        self.manager.view.refresh_tree()
        self.manager.view.select_node(_node)
        self.node = _node
        return True

    def Do(self):
        _uid = self.node.uuid
        _node = self.managerCC.post_delete_project_node(self.node)
        self.manager.emit_event(self.manager.T_EVT_NODE_DELETED, uid=_uid)
        self.manager.view.refresh_tree()
        # self.manager.view.select_node(_node)
        return True


class ProjectExplorerContentContainer(MBTContentContainer):
    def __init__(self, **kwargs):
        MBTContentContainer.__init__(self, **kwargs)
        self.project = None
        self.currentWorkbenches = []
        self.reset_to_default()
        self._filterProjOrtWb = lambda k: isinstance(k[1], MBTProjectOrientedWorkbench)

    @property
    def projectModel(self) -> ProjectTreeModel:
        return self.project.projectTreeModel

    @property
    def projectRoot(self) -> ProjectTreeNode:
        return self.project.projectTreeRoot

    @property
    def projectName(self) -> str:
        return self.project.name

    @property
    def projectPath(self) -> list:
        return self.project.projectPath

    def set(self, contract: ContentContract):
        if self.project is None:
            return

        if isinstance(contract, ProjectContentInsertContract):
            _find: ProjectTreeNode = self.find_node_by_uid(contract.uid)
            if _find:
                return self.project.append_work_file_for_node(_find,
                                                              name=contract.name,
                                                              extension=contract.extension,
                                                              path=contract.path,
                                                              data=contract.data)
        elif isinstance(contract, ProjectContentUpdateContract):
            _find: ProjectTreeNode = self.find_node_by_uid(contract.uid)
            if _find:
                _uri = contract.get_work_file_node_uri()
                return self.project.save_data_into_node_work_file(_find, _uri, contract.data)
        elif isinstance(contract, ProjectContentDeleteContract):
            _find: ProjectTreeNode = self.find_node_by_uid(contract.uid)
            if _find:
                _uri = contract.get_work_file_node_uri()
                return self.project.remove_node_work_file(_find, _uri)
        else:
            Warning('unsupported contract:%s' % contract)
        return False

    def get(self, contract: ContentContract):
        if self.project is None:
            return
        if isinstance(contract, ProjectContentQueryContract):
            _find: ProjectTreeNode = self.find_node_by_uid(contract.uid)
            if _find:
                return self.project.read_data_from_node_work_file(_find, uri=contract.get_work_file_node_uri())
        elif isinstance(contract, ProjectContentNodeQueryContract):
            return contract.action(self.project.projectTreeModel.root)
        else:
            Warning('unsupported contract:%s' % contract)
            return

    def reset_to_default(self):
        self._content = dict()
        for x in self.currentWorkbenches:
            if isinstance(x, MBTProjectOrientedWorkbench):
                x.teardown()
        self.currentWorkbenches.clear()

    def check_flag_of_role_config(self, role: EnumProjectItemRole, flag: EnumProjectItemFlag):
        """
        Args:
            role: EnumProjectItemRole
            flag: EnumProjectItemFlag

        Returns:

        """
        _element = self.get_project_node_config(role)
        assert _element is not None
        return flag in _element['flag']

    def create_new_project(self, project_name: str, project_path: str, workbench_uids) -> bool:
        self.reset_to_default()
        if util_is_dir_exist(os.path.join(project_path, project_name)):
            self.push_error('project %s already exist in path %s.' % (project_name, project_path))
            return False
        _construct_k = MBTProjectNodeConstructorImporter.CONSTRUCTION_KEY_NEW_PROJECT
        self.project = Project(project_name)
        self.project.contentManager = self
        self.project.set_base_path(project_path)
        _model = self.project.projectTreeModel
        _wbs = self.manager.root.get_workbenches(filter_=self._filterProjOrtWb)
        _wbs = [v for k, v in _wbs.items() if k in workbench_uids]
        _root = Project.nodeConstructor.construct(_construct_k)
        for x in _wbs:
            if x.projectNodeConstructor is None:
                continue
            _ret, _res = x.do_project_node_construction(_construct_k)
            if not _ret:
                self.reset_to_default()
                self.push_error(_res)
                return False
            else:
                _res.stereotype = ProjectTreeNode.NODE_ST_WORKBENCH_ROOT
                _res.parent = _root
            self.currentWorkbenches.append(x)
        # reparent the nodes
        _root.parent = _model.root
        _root.label = self.project.name
        self.project.projectTreeRoot = _root
        if not self.project.do_create_project_node_files():
            self.push_error('can not create project file')
            return False
        self.project.do_save_project_data()
        self.project.do_save_project_content()
        [x.setup(self.project) for x in self.currentWorkbenches]
        return True

    def delete_project_dir(self, name: str, path: str):
        _pp = os.path.join(path, name)
        if util_is_dir_exist(_pp):
            shutil.rmtree(_pp, ignore_errors=True)
        if self.project and name == self.project.name:
            self.project = None

    def open_project(self, path):
        _proj_path, _proj_name = os.path.split(path)
        if self.project is not None and _proj_name == self.project.name:
            self.push_error(_('Project %s already opened') % _proj_name)
            return False
        self.reset_to_default()
        self.clear_error_stack()
        self.project = Project(_proj_name)
        self.project.contentManager = self
        self.project.set_base_path(_proj_path)
        _wbs = self.manager.root.get_workbenches(filter_=self._filterProjOrtWb)
        _node_cfgs = copy.deepcopy(Project.nodeConstructor.get_elements())
        for k, v in _wbs.items():
            if v.projectNodeConstructor is None:
                continue
            _elm = v.projectNodeConstructor.get_elements()
            _node_cfgs.update(_elm)
        _ret = self.project.do_load_project_data(_node_cfgs)
        for x in anytree.iterators.LevelOrderIter(self.project.projectTreeRoot):
            if x.isWorkbenchRoot:
                _wb = _wbs[x.uuid]
                _wb.setup(self.project)
                self.currentWorkbenches.append(_wbs[x.uuid])
            if x.role == EnumProjectItemRole.BEHAVIOUR.value:
                # todo: did no type uri
                self.update_solution_type_uri_node(x)
        # content load please use contentProvider from contentSolver with authority "project".
        return _ret

    def prepare_node_content(self, node: ProjectTreeNode) -> bool:
        if self.project is None:
            return False
        _exist = self.find_node_by_uid(node.uuid)
        if _exist is None:
            return False
        # the order must be like below.
        # first: create work file resolver
        # second: decompose the file in workspace
        # third: restore the work file from meta file.
        # then: decompose the file in workspace again, since the meta file also in node data,
        # the second decompose is purpose for refresh and unzip all the necessary files.
        self.project.create_node_work_file_resolver(node)
        self.project.decompose_work_files_in_workspace(node)
        self.project.restore_work_file_resolver(node)
        self.project.decompose_work_files_in_workspace(node)
        return True

    def get_project_node_config(self, role) -> dict:
        if role == EnumProjectItemRole.ROOT.value:
            _elements = Project.nodeConstructor.get_elements()
            return _elements.get(EnumProjectItemRole.ROOT.value)
        for wb in self.currentWorkbenches:
            _elements = wb.projectNodeConstructor.get_elements()
            _element = _elements.get(role)
            if _element is not None:
                return _element

    def get_project_node_cm_config(self, role):
        _element = self.get_project_node_config(role)
        if _element is not None:
            return _element['contextMenu']
        else:
            return []

    def get_current_workbench(self, wb_uid: str) -> typing.Union[None, MBTProjectOrientedWorkbench]:
        _filtered = filter(lambda x: x.uid == wb_uid, self.currentWorkbenches)
        if _filtered:
            _filtered = list(_filtered)
            assert len(_filtered) == 1
            return _filtered[0]
        return

    def find_parent_node_by_child_role(self, child_role: EnumProjectItemRole) -> typing.Union[ProjectTreeNode, None]:
        if self.project is None:
            return
        return anytree.find(self.project.projectTreeModel.root, lambda x: x.is_children_role(child_role))

    def find_node_by_uid(self, uid):
        return self.projectModel.find_node_by_uid(uid)

    def get_solution_manager(self) -> MBTSolutionsManager:
        _app = wx.App.GetInstance()
        return _app.mbtSolutionManager

    def update_solution_type_uri_node(self, node: ProjectTreeNode):
        _type_uri = URLObject(node.stereotypeUri)
        _qd = _type_uri.query_dict
        if _type_uri.path == 'solution':
            _slt_uid = _qd.get('uid')
            _slt_mgr = self.get_solution_manager()
            _slt = _slt_mgr.get_solution_by_uuid(_slt_uid)
            node.icon = _slt.iconInfo[1]

    def post_add_child_node_of(self, parent_node: ProjectTreeNode, child_role, meta: dict, ignore_attr: list = None, use_constructor=True):
        _attrs = copy.deepcopy(meta)
        if ignore_attr is not None:
            [_attrs.pop(x) for x in ignore_attr]
        if use_constructor:
            _wb_uid = parent_node.workbenchUid
            _wb = list(filter(lambda x: x.uid == _wb_uid, self.currentWorkbenches))
            _ck = MBTProjectNodeConstructorImporter.CONSTRUCTION_KEY_NEW_CHILD_NODE_OF
            if _wb:
                _ret,_constructed_node = _wb[0].do_project_node_construction('%s_%s_%s' % (_ck, parent_node.role, child_role))
            else:
                _constructed_node: ProjectTreeNode = Project.nodeConstructor.construct('%s_%s_%s' % (_ck, parent_node.role, child_role))

            if _constructed_node is None:
                return None
            _constructed_node.update(**_attrs)
            _uid = _attrs.get('uuid')
            if _uid is not None:
                _constructed_node.uuid = _uid
            _constructed_node.parent = parent_node
            self.projectModel.sort(parent_node)
        else:
            _constructed_node = self.projectModel.append_node(parent_node, **_attrs)
        for x in anytree.iterators.PostOrderIter(_constructed_node):
            self.project.create_project_node_file(x)
        self.project.do_save_project_data()
        return _constructed_node

    def post_delete_project_node(self, node):
        self.project.remove_project_node_file(node)
        self.projectModel.remove_node(node)
        self.project.do_save_project_data()
        return True

    def load_default_perspective(self) -> str:
        return AppFileIO.read_file_in_raw(APP_DEFAULT_PERSPECTIVE_PATH)

    @staticmethod
    def open_path_in_explorer(path):
        subprocess.Popen('explorer /n,/e,/select,"%s"' % path)

    def transform_data(self, transformer: any):
        pass
