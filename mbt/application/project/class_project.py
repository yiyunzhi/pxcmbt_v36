import copy
import os, pathlib, anytree
from dataclasses import dataclass, field as data_field
from anytree.exporter import DictExporter
from anytree.importer import DictImporter
from framework.application.base import Serializable, TreeModelAnyTreeNode, TreeModel, NodeContent
from framework.application.utils_helper import util_remove_folder, util_get_uuid_string
from framework.application.io.class_yaml_file_io import AppYamlFileIO
from framework.application.define_path import ROOT
from mbt.application.define_path import PROJECT_PATH
from mbt.application.log.class_logger import get_logger
from .define import (EnumProjectItemFlag,
                     EnumProjectItemRole,
                     EnumProjectNodeFileAttr,
                     PROJECT_FILE_EXTEND)

_log = get_logger('application.project')

NODE_CONSTRUCTOR_CFG = os.path.join(os.path.dirname(__file__), 'project_tree_node.ctree')


class ProjectNodeProfile(NodeContent):
    serializeTag = '!Profile'

    def __init__(self, **kwargs):
        _attr = {'name': kwargs.get('name', ''), 'description': kwargs.get('description', 'no description')}
        _node = kwargs.get('node')
        NodeContent.__init__(self, _node, _attr)

    def set(self, k, v, force=True):
        if k not in ['name', 'description']:
            return
        super().set(k, v, force)


class ProjectTreeNode(TreeModelAnyTreeNode):
    def __init__(self, **kwargs):
        TreeModelAnyTreeNode.__init__(self, **kwargs)
        _flag = kwargs.get('flag', EnumProjectItemFlag.FLAG_DEFAULT)
        self.uuid = kwargs.get('uuid', util_get_uuid_string())
        self.role = kwargs.get('role')
        self.flag = 0
        self._realize_flag(_flag)
        self.icon = kwargs.get('icon', self.icon)
        self.typeUri = kwargs.get('type_uri', 'type://file')
        # typeUri define see below
        # uri: type://solution?name=stc?uid=7dwdwxsswfa232swd23
        # uri: type://addon?
        # uri: type://file?path=dw\wd\a.obj (if path not explict<like a link> then use default get_file_path())
        self.contextMenu = kwargs.get('contextMenu')
        self.fileAttr = kwargs.get('fileAttr', EnumProjectNodeFileAttr.FOLDER)
        self.fileExtend = kwargs.get('fileExtend')
        self.fileName = kwargs.get('fileName', self.label.lower())
        self.profile = None
        _profile = kwargs.get('profile', ProjectNodeProfile(node=self, name=self.label))
        self.set_profile(_profile)

    def __repr__(self):
        return 'ProjectTreeNode: {} uid:{}, role:{}.'.format(self.label, self.uuid, EnumProjectItemRole(self.role).name)

    @property
    def meta(self):
        return {'uuid': self.uuid,
                'role': self.role,
                'flag': self.flag,
                'icon': self.icon,
                'contextMenu': self.contextMenu,
                'fileAttr': self.fileAttr,
                'fileExtend': self.fileExtend,
                'fileName': self.fileName,
                'profile': self.profile.serializer}

    def _realize_flag(self, val):
        if isinstance(val, list):
            for x in val:
                self.add_flag(x)
        else:
            assert isinstance(val, int), 'invalid flag. %s' % val
            self.flag = val

    @property
    def description(self):
        return self.profile.get('description')

    def update(self, **kwargs):
        if 'flag' in kwargs:
            self.flag = 0
            self._realize_flag(kwargs.get('flag'))
        if 'icon' in kwargs:
            self.icon = kwargs.get('icon')
        if 'contextMenu' in kwargs:
            self.contextMenu = kwargs.get('contextMenu')
        if 'fileAttr' in kwargs:
            self.fileAttr = kwargs.get('fileAttr')
        if 'fileName' in kwargs:
            self.fileName = kwargs.get('fileName')
        if 'fileExtend' in kwargs:
            self.fileExtend = kwargs.get('fileExtend')
        if 'profile' in kwargs:
            _p = kwargs.get('profile')
            if isinstance(_p, ProjectNodeProfile):
                self.set_profile(_p)
            elif isinstance(_p, dict):
                self.update_profile(**_p)

    def set_profile(self, profile: ProjectNodeProfile):
        if profile is not None:
            assert isinstance(profile, ProjectNodeProfile), 'type ProjectNodeProfile is required, given <%s>' % type(
                profile)
            self.profile = profile
            self.profile.link_node(self)
            if self.has_flag(EnumProjectItemFlag.DESCRIBABLE.value):
                self.label = self.profile.get('name')
            else:
                self.profile.set('name', self.label)

    def update_profile(self, name: str, description: str):
        self.profile.set('description', description)
        if self.has_flag(EnumProjectItemFlag.DESCRIBABLE):
            self.profile.set('name', name)
            self.label = name

    def get_file_name(self):
        if self.fileAttr != EnumProjectNodeFileAttr.LINK:
            if self.fileName.startswith('.'):
                return getattr(self, self.fileName[1::])
            else:
                self.fileName = self.label.lower()
                return self.fileName
        else:
            return self.fileName

    def get_file_path(self):
        if self.fileAttr == EnumProjectNodeFileAttr.FOLDER:
            _parent_path = self.path
        else:
            _parent_path = self.path[0:-1]
        return os.path.join(*[x.get_file_name() for x in _parent_path])

    def get_file_info(self):
        _file_path = self.get_file_path()
        _file_base_name = None
        if self.fileAttr == EnumProjectNodeFileAttr.FOLDER:
            return _file_path, _file_base_name
        elif self.fileAttr == EnumProjectNodeFileAttr.FILE:
            _file_base_name = self.get_file_name() + self.fileExtend
            return _file_path, _file_base_name
        elif self.fileAttr == EnumProjectNodeFileAttr.LINK:
            _file_path = os.path.join(ROOT, self.fileName)
            return os.path.split(_file_path)
        else:
            return _file_path, _file_base_name

    def has_flag(self, flag):
        return (self.flag & flag) != 0

    def add_flag(self, flag):
        self.flag |= flag

    def reset_flag(self):
        self.flag = 0

    def is_children_role(self, role: str):
        if role.count('-') == 0:
            return False
        _p_r = '-'.join([x for x in role.split('-')[0:-1]])
        return _p_r == self.role


class ProjectTreeModel(TreeModel):
    def __init__(self):
        TreeModel.__init__(self, ProjectTreeNode)
        self.name = 'ProjectTreeModel'

    def remove_node(self, node):
        node.parent = None

    def find_node_by_uid(self, uid: str) -> ProjectTreeNode:
        return anytree.find(self.root, lambda x: x.uuid == uid)


@dataclass
class ProjectMeta(Serializable):
    serializeTag = '!ProjectMeta'
    requiredSolutions: list = data_field(default_factory=list)

    @property
    def serializer(self):
        return {
            'requiredSolutions': self.requiredSolutions
        }

    def add_solution_ref(self, uid):
        if uid not in self.requiredSolutions:
            self.requiredSolutions.append(uid)

    def remove_solution_ref(self, uid):
        if uid in self.requiredSolutions:
            self.requiredSolutions.remove(uid)


class Project:
    def __init__(self, name):
        self.name = name
        self.meta = ProjectMeta()
        self.workspacePath = PROJECT_PATH
        self.projectPath = os.path.join(PROJECT_PATH, name)
        self.projectEntryFilePath = os.path.join(self.projectPath, PROJECT_FILE_EXTEND)
        self.projectTreeModel = ProjectTreeModel()
        self.projectTreeRoot = None
        self._noSavableRole = []
        self.mainPerspective = None

    def set_workspace_path(self, path):
        self.workspacePath = path
        self.projectPath = os.path.join(path, self.name)
        self.projectEntryFilePath = os.path.join(self.projectPath, self.name + PROJECT_FILE_EXTEND)

    def is_solution_required(self, solution_id):
        return solution_id in self.meta.requiredSolutions

    def add_ipod_engine_ref(self, engine_id):
        self.meta.add_solution_ref(engine_id)

    def remove_ipod_engine_ref(self, engine_id):
        self.meta.remove_solution_ref(engine_id)

    def do_create_project_file(self):
        assert self.projectTreeRoot is not None
        _eps = anytree.findall(self.projectTreeRoot, lambda x: not x.children)
        _ret = True
        for node in _eps:
            _ret &= self.create_project_node_file(node)
        return _ret

    def do_save_project_node(self):
        _file_io = AppYamlFileIO(self.projectPath, self.name + PROJECT_FILE_EXTEND)
        # export exclusive the attribute contextMenu
        _exporter = DictExporter(attriter=lambda attr: [(k, v) for k, v in attr if k in ['uuid', 'role', 'profile']],
                                 childiter=lambda children: [child for child in children if
                                                             child.role not in self._noSavableRole])
        _d = {'meta': self.meta,
              'project': _exporter.export(self.projectTreeRoot),
              'perspective': self.mainPerspective}
        _file_io.write(_d)
        return True

    def do_load_project(self, node_cfg: dict = None):
        _file_io = AppYamlFileIO(self.projectPath, self.name + PROJECT_FILE_EXTEND)
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
            self.do_save_project_node()

    def create_project_node_file(self, node, f_io_cls=None):
        try:
            if node is not None:
                if node.has_flag(EnumProjectItemFlag.SAVABLE):
                    _file_path, _file_name = node.get_file_info()
                    _file_path = os.path.join(self.workspacePath, _file_path)
                    pathlib.Path(_file_path).mkdir(exist_ok=True, parents=True)
                    if _file_name:
                        if f_io_cls is None:
                            _file_path = os.path.join(_file_path, _file_name)
                            with open(_file_path, 'w') as f:
                                f.write('')
                        else:
                            _f_io = f_io_cls(_file_path, _file_name)
                            _f_io.write(None)
            return True
        except Exception as e:
            _log.error('can not create file for node %s.' % node.label)
            return False

    def remove_project_node_file(self, node):
        if node is not None:
            if node.has_flag(EnumProjectItemFlag.REMOVABLE):
                _file_path, _file_name = node.get_file_info()
                _file_path = os.path.join(self.workspacePath, _file_path)
                if _file_name:
                    _file_path = os.path.join(self.workspacePath, _file_path, _file_name)
                    pathlib.Path(_file_path).unlink()
                else:
                    util_remove_folder(_file_path)

    def do_save_project_node_content(self, node, io_cls=None, recursive=False):
        if node is None:
            node = self.projectTreeModel.root
        if node.has_flag(EnumProjectItemFlag.SAVABLE) and node.fileAttr == EnumProjectNodeFileAttr.FILE:
            _file_path, _file_name = node.get_file_info()
            _file_path = os.path.join(self.workspacePath, _file_path)
            if io_cls is None:
                _io = AppYamlFileIO(_file_path, _file_name)
            else:
                _io = io_cls(_file_path, _file_name)
            if not recursive:
                _io.write(node.content)
            del _io
        return True
