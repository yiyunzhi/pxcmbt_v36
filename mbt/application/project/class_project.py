import logging, traceback
import os, pathlib, anytree
import shutil
import typing
from dataclasses import dataclass
from anytree.exporter import DictExporter
from anytree.importer import DictImporter
from framework.application.base import Serializable, TreeModel, BaseSelectionItem
from framework.application.io.class_yaml_file_io import AppYamlFileIO, AppFileIO
from mbt.application.define_path import PROJECT_PATH
from mbt.application.log.class_logger import get_logger
from .class_project_node import ProjectTreeNode
from .define import (EnumProjectItemFlag,
                     PROJECT_FILE_EXTEND, SORTER_MAP)
from .class_file_resolver import ProjectWorkFileResolverFactory, WorkFileNode
from .class_node_constructor import MBTProjectNodeConstructorImporter

_log = get_logger('application.project')

BASE_NODE_CONSTRUCTOR_CFG = os.path.join(os.path.dirname(__file__), 'project_root_nodes.yaml')


class ProjectNodeChoiceItem(BaseSelectionItem):
    def __init__(self, node: ProjectTreeNode):
        BaseSelectionItem.__init__(self)
        self.uid = node.uuid
        self.name = node.label
        self.icon = node.icon
        self.description = node.get_path_string()


class ProjectTreeModel(TreeModel):
    def __init__(self):
        TreeModel.__init__(self, ProjectTreeNode)
        self.name = 'ProjectTreeModel'

    def remove_node(self, node):
        node.parent = None

    def append_node(self, parent, **kwargs):
        _node = super().append_node(parent, **kwargs)
        self.sort(_node.parent)

    def find_node_by_uid(self, uid: str) -> ProjectTreeNode:
        return anytree.find(self.root, lambda x: x.uuid == uid)

    def sort(self, node: ProjectTreeNode):
        _sort_c, _flag = SORTER_MAP.get(node.sorter)
        _sortable = all(x.has_flag(EnumProjectItemFlag.ORDERABLE) for x in node.children)
        if _sortable and node.sorter is not None:
            self.sort_children_with(node, _sort_c, True if _flag == 'dsc' else False)
        return _flag


@dataclass
class ProjectMeta(Serializable):
    serializeTag = '!ProjectMeta'
    fileResolverVersion: str = '1.0.0'
    DBfileExt: str = '.ioz'

    @property
    def serializer(self):
        return {
            'fileResolverVersion': self.fileResolverVersion,
            'DBfileExt': self.DBfileExt,
        }


_BASE_CONTEXT_MENU_IO = AppYamlFileIO(file_path=os.path.dirname(__file__), filename='base_context_menu.yaml')
_BASE_CONTEXT_MENU_IO.read()

class Project:
    nodeConstructor = MBTProjectNodeConstructorImporter(BASE_NODE_CONSTRUCTOR_CFG)
    baseContextMenuCfg = _BASE_CONTEXT_MENU_IO.data

    def __init__(self, name, file_resolver_ver='1.0.0'):
        self.name = name
        self.meta = ProjectMeta()
        self.contentManager=None
        if file_resolver_ver is not None:
            self.meta.fileResolverVersion = file_resolver_ver
        self.basePath = None
        self.projectPath = None
        self.workspacePath = None
        self.dbspacePath = None
        self.projectEntryFilePath = None
        self.set_base_path(PROJECT_PATH, False)
        self.metaTemplateFile = os.path.join(os.path.dirname(__file__), 'meta.yaml')

        self.projectTreeModel = ProjectTreeModel()
        self.projectTreeRoot = None
        self.workFileResolvers = dict()

        self._noSavableRole = []

        self.mainPerspective = None

    @property
    def entryFilename(self):
        return self.name + PROJECT_FILE_EXTEND

    def get_node_composed_file_path(self, node: ProjectTreeNode):
        return os.path.join(self.dbspacePath, node.workbenchUid, node.uuid + self.meta.DBfileExt)

    def get_node_decomposed_file_path(self, node: ProjectTreeNode):
        return os.path.join(self.workspacePath, node.uuid)

    def set_base_path(self, path, persistent=True):
        self.basePath = path
        self.projectPath = os.path.join(path, self.name)
        self.projectEntryFilePath = os.path.join(self.projectPath, self.entryFilename)
        self.workspacePath = os.path.join(self.projectPath, '.tmp')
        self.dbspacePath = os.path.join(self.projectPath, 'data')
        if persistent:
            if not os.path.exists(self.workspacePath):
                os.makedirs(self.workspacePath, exist_ok=True)
            if not os.path.exists(self.dbspacePath):
                os.makedirs(self.dbspacePath, exist_ok=True)

    def do_create_project_node_files(self):
        assert self.projectTreeRoot is not None
        _ret = True
        for x in self.projectTreeRoot.descendants:
            _ret &= self.create_project_node_file(x)
        return _ret

    def do_save_project_data(self):
        _file_io = AppYamlFileIO(file_path=self.projectPath, filename=self.entryFilename)
        # export exclusive the attribute contextMenu
        _exporter = DictExporter(attriter=lambda attr: [(k, v) for k, v in attr if k in ['uuid', 'role', 'profile',
                                                                                         'stereotype', 'stereotypeQuery', 'sorter']],
                                 childiter=lambda children: [child for child in children if
                                                             child.role not in self._noSavableRole])
        _d = {'meta': self.meta,
              'project': _exporter.export(self.projectTreeRoot),
              'perspective': self.mainPerspective}
        _file_io.write(_d)
        return True

    def do_load_project_data(self, node_cfg: dict = None):
        _file_io = AppYamlFileIO(file_path=self.projectPath, filename=self.entryFilename)
        _file_io.read()
        _body = _file_io.data
        _project_d = _body.get('project')
        _perspective = _body.get('perspective')
        self.meta = _body.get('meta')
        if not _project_d:
            return False
        self.projectTreeModel = ProjectTreeModel()
        _imp_root = DictImporter(ProjectTreeNode).import_(_project_d)
        if node_cfg is not None:
            for x in anytree.LevelOrderIter(_imp_root):
                _cfg = node_cfg.get(x.role)
                x.update(**_cfg)
                if x.has_flag(EnumProjectItemFlag.DESCRIBABLE.value):
                    x.label = x.profile.get('name')
                if x.is_root:
                    x.label = self.name
        self.projectTreeRoot = _imp_root
        self.projectTreeRoot.parent = self.projectTreeModel.root
        self.mainPerspective = _perspective
        return True

    def save_perspective(self, main_perspective_str: str):
        if main_perspective_str is not None:
            self.mainPerspective = main_perspective_str
            self.do_save_project_data()

    def create_node_work_file_resolver(self, node: ProjectTreeNode, override=False):
        if node is not None:
            if self.is_node_has_content(node) and node.root is self.projectTreeModel.root:
                if node.uuid in self.workFileResolvers and not override:
                    return
                _fs_cls = ProjectWorkFileResolverFactory.get(self.meta.fileResolverVersion)
                self.workFileResolvers.update({node.uuid: _fs_cls(self.get_node_composed_file_path(node), self.workspacePath, node.uuid)})

    def composed_work_files_in_dbspace(self, node: ProjectTreeNode, files: list = None):
        _fs = self.workFileResolvers.get(node.uuid)
        if _fs is not None:
            if files is None:
                files = []
            _fs.compose(files)

    def decompose_work_files_in_workspace(self, node: ProjectTreeNode):
        _fs = self.workFileResolvers.get(node.uuid)
        if _fs is not None:
            _fs.decompose()

    def restore_work_file_resolver(self, node: ProjectTreeNode):
        _fs = self.workFileResolvers.get(node.uuid)
        if _fs is not None:
            _fs.restore_from_meta()

    def append_work_file_for_node(self, node: ProjectTreeNode, name, extension=WorkFileNode.DEFAULT_EXTENSION, path=None, data=None) -> WorkFileNode:
        _fs = self.workFileResolvers.get(node.uuid)
        assert _fs is not None, KeyError('node %s has not workFileResolver' % node.get_path_string())
        _n = _fs.append_node(name=name, extension=extension, dir_path=path)
        if _n is not None:
            _n.write(data)
        _fs.save_to_meta()
        return _n

    def save_data_into_node_work_file(self, node: ProjectTreeNode, uri: str, data: object):
        _fs = self.workFileResolvers.get(node.uuid)
        assert _fs is not None, KeyError('node %s has not workFileResolver' % node.get_path_string())
        return _fs.write(uri, data)

    def remove_node_work_file(self, node: ProjectTreeNode, uri: str):
        _fs = self.workFileResolvers.get(node.uuid)
        assert _fs is not None, KeyError('node %s has not workFileResolver' % node.get_path_string())
        _ret = _fs.remove(uri)
        _fs.save_to_meta()
        return _ret

    def clear_work_file_dirs(self):
        for filename in os.listdir(self.workspacePath):
            _file_path = os.path.join(self.workspacePath, filename)
            try:
                if os.path.isfile(_file_path) or os.path.islink(_file_path):
                    os.unlink(_file_path)
                elif os.path.isdir(_file_path):
                    shutil.rmtree(_file_path)
            except Exception as e:
                _log.error('Failed to delete %s. Reason: %s' % (_file_path, e))

    def append_work_file_for_node_with_path(self, node: ProjectTreeNode, path: str, extension=WorkFileNode.DEFAULT_EXTENSION, data=None) -> WorkFileNode:
        _fs = self.workFileResolvers.get(node.uuid)
        assert _fs is not None, KeyError('node %s has not workFileResolver' % node.get_path_string())
        _path_strs = path.split(_fs.root.separator)
        _name = _path_strs.pop(-1)
        return self.append_work_file_for_node(node, _name, extension, _path_strs, data)

    def create_project_node_file(self, node: ProjectTreeNode):
        try:
            if node is not None:
                if node.has_flag(EnumProjectItemFlag.SAVABLE) and node.has_flag(
                        EnumProjectItemFlag.CAN_EDIT_CONTENT) and node.root is self.projectTreeModel.root:
                    if self.workFileResolvers.get(node.uuid) is None:
                        self.create_node_work_file_resolver(node)
                    self.composed_work_files_in_dbspace(node)
                    self.decompose_work_files_in_workspace(node)
            return True
        except Exception as e:
            _log.error('can not create file for node %s. since:%s' % (node.get_path_string(), str(e)))
            if _log.getEffectiveLevel() == logging.DEBUG:
                traceback.print_exc()
            return False

    def remove_project_node_file(self, node: ProjectTreeNode):
        if node is not None:
            if node.has_flag(EnumProjectItemFlag.REMOVABLE) and self.is_node_has_content(node):
                _file_path = self.get_node_composed_file_path(node)
                _d_file_path = self.get_node_decomposed_file_path(node)
                if os.path.exists(_file_path):
                    pathlib.Path(_file_path).unlink()
                if os.path.exists(_d_file_path):
                    shutil.rmtree(_d_file_path)
                if node.uuid in self.workFileResolvers:
                    self.workFileResolvers.pop(node.uuid)

    def read_data_from_node_work_file(self, node: ProjectTreeNode, uri: str) -> typing.Union[AppFileIO, None]:
        assert node.root is self.projectTreeModel.root, ValueError('node not exist.')
        if self.is_node_has_content(node):
            _fs = self.workFileResolvers.get(node.uuid)
            if _fs is not None:
                return _fs.read(uri)

    def do_save_project_node_content(self, node: ProjectTreeNode):
        if self.is_node_has_content(node):
            _fs = self.workFileResolvers.get(node.uuid)
            if _fs is not None:
                _fs.compose()

    def do_save_project_content(self):
        for k, v in self.workFileResolvers.items():
            v.compose()

    def is_node_has_content(self, node: ProjectTreeNode) -> bool:
        return node.has_flag(EnumProjectItemFlag.CAN_EDIT_CONTENT)

    @property
    def nodesHasContent(self):
        return anytree.findall(self.projectTreeRoot, lambda x: self.is_node_has_content(x))

    @staticmethod
    def find(node, filter_=None, stop=None, maxlevel=None):
        return anytree.find(node, filter_, stop, maxlevel)

    @staticmethod
    def find_all(node, filter_=None, stop=None, maxlevel=None, mincount=None, maxcount=None):
        return anytree.findall(node, filter_, stop, maxlevel, mincount, maxcount)

    @staticmethod
    def find_by_attr(node, value, name="name", maxlevel=None):
        return anytree.find_by_attr(node, value, name, maxlevel)

    @staticmethod
    def findall_by_attr(node, value, name="name", maxlevel=None, mincount=None, maxcount=None):
        return anytree.findall_by_attr(node, value, name, maxlevel, mincount, maxcount)
