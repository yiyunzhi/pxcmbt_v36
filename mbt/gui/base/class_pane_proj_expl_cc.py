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
import os, shutil, anytree
import wx
from framework.application.define import _
from framework.application.io import AppYamlFileIO
from framework.application.urlobject import URLObject
from framework.application.utils_helper import util_is_dir_exist
from mbt.application.mbt_solution_manager import MBTSolutionsManager
from mbt.application.project import (ProjectTreeNode,
                                     NODE_CONSTRUCTOR_CFG,
                                     TreeNodeConstructorImporter,
                                     Project,
                                     ProjectTreeModel,
                                     EnumProjectItemRole, EnumProjectItemFlag)
from mbt.gui.base import MBTContentContainer, MBTViewManager


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
        self.manager.emit_event(self.manager._T_NODE_ADDED, uid=_node.uuid)
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
        self.manager.emit_event(self.manager._T_NODE_DELETED, uid=_uid)
        self.manager.view.refresh_tree()
        # self.manager.view.select_node(_node)
        return True


class ProjectExplorerContentContainer(MBTContentContainer):
    def __init__(self, **kwargs):
        MBTContentContainer.__init__(self, **kwargs)
        self.project = None
        self.projectCNImporter = TreeNodeConstructorImporter(ProjectTreeNode,
                                                             NODE_CONSTRUCTOR_CFG)

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

    def check_flag_of_role_config(self, role: EnumProjectItemRole, flag: EnumProjectItemFlag):
        """
        Args:
            role: EnumProjectItemRole
            flag: EnumProjectItemFlag

        Returns:

        """
        _elements = self.projectCNImporter.get_elements()
        _cfg = _elements.get(role)
        assert _cfg is not None
        return flag in _cfg['flag']

    def create_new_project(self, project_name: str, project_path: str) -> bool:
        if util_is_dir_exist(os.path.join(project_path, project_name)):
            self.push_error('project %s already exist in path %s.' % (project_name, project_path))
            return False
        _construct_k = 'new_project'
        self.project = Project(project_name)
        self.project.set_workspace_path(project_path)
        _model = self.project.projectTreeModel
        _root = self.projectCNImporter.construct(_construct_k)
        # call hooks of new_project_<child_role>@<parent_role>
        _constructors = self.projectCNImporter.get_constructors()
        for k, v in _constructors.items():
            if '@' in k:
                _, _r, _hpt_role = k.split('@')
                if _ == _construct_k:
                    _parent = anytree.find(_root, lambda x: x.role == _hpt_role)
                    if _parent:
                        _node = self.projectCNImporter.construct(k)
                        _node.parent = _parent
        # reparent the nodes
        _root.parent = _model.root
        _root.label = self.project.name
        self.project.projectTreeRoot = _root
        if not self.project.do_create_project_file():
            self.push_error('can not create project file')
            return False
        self.project.do_save_project_node()
        return True

    def delete_project(self, name, path):
        _pp = os.path.join(path, name)
        if util_is_dir_exist(_pp):
            shutil.rmtree(_pp, ignore_errors=True)
        if self.project and name == self.project.name:
            self.project = None

    def set_default_node_content(self, node=None):
        if node is None:
            node = self.project.projectTreeRoot
        _descendants = node.descendants
        for x in _descendants:
            self.set_default_node_content(x)

    def open_project(self, path):
        _proj_path, _proj_name = os.path.split(path)
        if self.project is not None and _proj_name == self.project.name:
            self.push_error(_('Project %s already opened') % _proj_name)
            return False
        self.project = Project(_proj_name)
        self.project.set_workspace_path(_proj_path)
        _ret = self.project.do_load_project(self.projectCNImporter.to_dict())
        for x in anytree.iterators.LevelOrderIter(self.project.projectTreeRoot):
            if x.role == EnumProjectItemRole.BEHAVIOUR.value:
                self.update_solution_type_uri_node(x)
            # todo: check if typeUri file has explict path, then load content
        # try:
        #     # load the blocks content into it's node, currently on blocks node considered
        #     _block_nodes = self.get_project_nodes_by_role(EnumProjectItemRole.ENGINE_IMPL_ITEMS.value)
        #     for x in _block_nodes:
        #         for n in x.descendants:
        #             _content_io = self.read_content_of_project_node(n)
        #             if _content_io is not None:
        #                 _body = _content_io.body
        #                 n.set_content(_body if not isinstance(_body, AppFileIOBody) else None)
        # except Exception as e:
        #     pass
        return _ret

    def get_project_node_config(self, role):
        _elements = self.projectCNImporter.get_elements()
        _element = _elements.get(role)
        return _element

    def get_project_node_cm_config(self, role):
        _elements = self.projectCNImporter.get_elements()
        _element = _elements.get(role)
        if _element is not None:
            return _element['contextMenu']
        else:
            return []

    def find_parent_node_by_child_role(self, child_role: EnumProjectItemRole) -> ProjectTreeNode:
        if self.project is None:
            return
        return anytree.find(self.project.projectTreeModel.root, lambda x: x.is_children_role(child_role))

    def find_node_by_uid(self, uid):
        return self.projectModel.find_node_by_uid(uid)

    def get_solution_manager(self) -> MBTSolutionsManager:
        _app = wx.App.GetInstance()
        return _app.mbtSolutionManager

    def update_solution_type_uri_node(self, node: ProjectTreeNode):
        _type_uri = URLObject(node.typeUri)
        _qd = _type_uri.query_dict
        if _type_uri.path == 'solution':
            _slt_uid = _qd.get('uid')
            _slt_mgr = self.get_solution_manager()
            _slt = _slt_mgr.get_solution_by_uuid(_slt_uid)
            node.icon = _slt.iconInfo[1]

    def post_add_child_node_of(self, parent_node, child_role, meta: dict, ignore_attr: list = None, use_constructor=True):
        _attrs = copy.deepcopy(meta)
        if ignore_attr is not None:
            [_attrs.pop(x) for x in ignore_attr]
        if use_constructor:
            _constructed_node: ProjectTreeNode = self.projectCNImporter.construct('new_child_node_of_%s_%s' % (parent_node.role, child_role))
            if _constructed_node is None:
                return None
            _constructed_node.update(**_attrs)
            _uid = _attrs.get('uuid')
            if _uid is not None:
                _constructed_node.uuid = _uid
            _constructed_node.parent = parent_node
        else:
            _constructed_node = self.projectModel.append_node(parent_node, **_attrs)
        # determine the icon name base on the typeUri
        self.update_solution_type_uri_node(_constructed_node)
        # _constructed_node.parent = parent_node
        for x in anytree.iterators.PostOrderIter(_constructed_node):
            _io_cls = None if x.fileExtend is None else AppYamlFileIO
            self.project.create_project_node_file(x, _io_cls)
        self.project.do_save_project_node()
        return _constructed_node

    def post_delete_project_node(self, node):
        self.project.remove_project_node_file(node)
        self.projectModel.remove_node(node)
        self.project.do_save_project_node()
        return True

    @staticmethod
    def read_file_in_raw(path, flag='r', encoding='utf-8'):
        with open(path, flag, encoding=encoding) as f:
            _ret = f.read()
        return _ret

    def load_default_perspective(self) -> str:
        return self.read_file_in_raw(APP_DEFAULT_PERSPECTIVE_PATH)

    @staticmethod
    def open_path_in_explorer(path):
        subprocess.Popen('explorer /n,/e,/select,"%s"' % path)

    def transform_data(self, transformer: any):
        pass
