# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_file_resolver.py
# ------------------------------------------------------------------------------
#
# File          : class_file_resolver.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, shutil, anytree, pathlib
from anytree import exporter, importer
from framework.application.urlobject import URLObject
from framework.application.io import ZipFileIO, AppFileIO, AppYamlFileIO

IO_CLS_FACTORY = {'.obj': AppYamlFileIO}


class WorkFileResolverException(Exception): pass


class WorkFileNode(anytree.NodeMixin):
    DEFAULT_EXTENSION = '.obj'
    SCHEME = 'node'
    PATH = 'WorkFileNode'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.extension = kwargs.get('extension', self.DEFAULT_EXTENSION)
        self.reversion = kwargs.get('reversion', 0)
        self.permission = kwargs.get('permission', 'RW')
        self.parent = kwargs.get('parent')
        self.dirPath = kwargs.get('dir_path', '')
        self.uri = self.get_uri(path=self.dirPath, name=self.name, ext=self.extension)
        # separator for file path is same as os.seq
        _children = kwargs.get('children')
        if _children:
            self.children = _children

    @property
    def canRead(self) -> bool:
        return 'R' in self.permission

    @property
    def canWrite(self) -> bool:
        return 'W' in self.permission

    @property
    def fileBasename(self):
        return self.name + self.extension

    @property
    def fileRelativePath(self):
        return os.path.relpath(self.fileAbsPath, self.root.dirPath)

    @property
    def dirRelativePath(self):
        return os.path.relpath(self.dirAbsPath, self.root.dirPath)

    @property
    def fileAbsPath(self):
        return os.path.join(self.dirAbsPath, self.fileBasename)

    @property
    def dirAbsPath(self):
        return os.path.join(self.root.dirPath, self.dirPath)

    @property
    def ioCls(self) -> type:
        return IO_CLS_FACTORY.get(self.extension)

    @staticmethod
    def get_uri(**kwargs):
        _uri = URLObject()
        _uri = _uri.with_scheme(WorkFileNode.SCHEME)
        _uri = _uri.with_path(WorkFileNode.PATH)
        _uri = _uri.set_query_params(**kwargs)
        return str(_uri)

    def init(self, *args, **kwargs):
        raise NotImplementedError

    def read(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, *args, **kwargs):
        raise NotImplementedError

    def remove(self, *args, **kwargs):
        raise NotImplementedError


class ProjectWorkFileNode100(WorkFileNode):
    separator = os.sep

    def __init__(self, **kwargs):
        WorkFileNode.__init__(self, **kwargs)

    def init(self):
        assert self.extension is not None, ValueError('extension is required if node is leaf.')
        _dir = self.dirAbsPath
        pathlib.Path(_dir).mkdir(exist_ok=True, parents=True)
        _file_name = self.fileAbsPath
        _io = self.ioCls(file_path=_dir, filename=_file_name, extension=self.extension)
        _io.write('')

    def read(self, **kwargs):
        if not os.path.exists(self.fileAbsPath):
            return
        if self.is_leaf:
            assert self.extension is not None, ValueError('extension is required if node is leaf.')
            _dir = os.path.dirname(self.fileAbsPath)
            _file_name = os.path.basename(self.fileAbsPath)
            _io = self.ioCls(file_path=_dir, filename=_file_name, extension=self.extension)
            _io.read(**kwargs)
            return _io
        return

    def write(self, data, **kwargs):
        self.reversion += 1
        if self.is_leaf:
            assert self.extension is not None, ValueError('extension is required if node is leaf.')
            _dir = os.path.dirname(self.fileAbsPath)
            _file_name = os.path.basename(self.fileAbsPath)
            pathlib.Path(_dir).mkdir(exist_ok=True, parents=True)
            _io = self.ioCls(file_path=_dir, filename=_file_name, extension=self.extension)
            return _io.write(data, **kwargs)
        return True

    def remove(self, remove_node=True):
        if os.path.exists(self.fileAbsPath):
            os.unlink(self.fileAbsPath)
        if remove_node:
            self.parent = None


class ProjectWorkFileResolver:
    def __init__(self):
        pass

    def append_node(self, *args, **kwargs):
        raise NotImplementedError

    def read(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, *args, **kwargs):
        raise NotImplementedError

    def compose(self, *args, **kwargs):
        raise NotImplementedError

    def decompose(self, *args, **kwargs):
        raise NotImplementedError


class ProjectWorkFileResolver100(ProjectWorkFileResolver):
    """
    used to compose multi files into one file.
    """
    VERSION = '1.0.0'

    # todo: path meta should not be exposed to client for writing. only read is allowed
    def __init__(self, composed_file: str, workspace_dir_path: str, work_dir_name: str):
        ProjectWorkFileResolver.__init__(self)
        self.composedFilePath = composed_file
        _this_dir = os.path.join(workspace_dir_path, work_dir_name)
        self._root = ProjectWorkFileNode100(name=work_dir_name, dir_path=_this_dir, extension='')
        self._metaNode = self.append_node(name='meta', extension='.obj')
        self.save_to_meta()

    @property
    def root(self):
        return self._root

    def _serialization_filter(self, attrs):
        _kv = list()
        for k, v in attrs:
            if k == 'dirPath' and v.strip() != '':
                _kv.append((k, os.path.relpath(self._root.dirPath, v)))
            elif k in ['uri']:
                continue
            else:
                _kv.append((k, v))
        return _kv

    def save_to_meta(self):
        _data = exporter.DictExporter(attriter=self._serialization_filter).export(self._root)
        self._metaNode.write(_data)

    def restore_from_meta(self):
        _io = self._metaNode.read()
        if _io is not None and _io.data is not None:
            _r = importer.DictImporter(ProjectWorkFileNode100).import_(_io.data)
            self._root.children = _r.children
            self._metaNode = self.get_node(self._metaNode.uri)

    def append_node(self, **kwargs):
        _node = ProjectWorkFileNode100(**kwargs)
        _exist = self.get_node(_node.uri)
        if _exist:
            _node.parent = None
            return _exist
        _node.parent = self._root
        _node.init()
        return _node

    def remove_node(self, uri: str, remove_file=False):
        _find: ProjectWorkFileNode100 = self.get_node(uri)
        if _find:
            _find.parent = None
            if remove_file:
                _find.remove()

    def get_node(self, uri: str):
        def _match(node):
            _req = URLObject(uri)
            _to_match = URLObject(node.uri)
            return _req.scheme == _to_match.scheme and _req.path == _to_match.path and _req.query_dict == _to_match.query_dict

        return anytree.find(self._root, _match)

    def read(self, uri: str, **kwargs) -> AppFileIO:
        _c_node = self.get_node(uri)
        if _c_node is not None:
            return _c_node.read(**kwargs)

    def write(self, uri: str, data, **kwargs):
        _c_node = self.get_node(uri)
        if _c_node is not None:
            return _c_node.write(data, **kwargs)
        return False

    def remove(self, uri: str, **kwargs):
        _c_node = self.get_node(uri)
        if _c_node is not None:
            _c_node.remove()

    def decompose(self):
        # node.ioz->workspace etc.
        assert os.path.isfile(self.composedFilePath)
        _path = os.path.dirname(self.composedFilePath)
        _name = os.path.basename(self.composedFilePath)
        _io = ZipFileIO(file_path=_path, filename=_name)
        _files_to_decompose = [x.fileRelativePath for x in self._root.leaves]
        _io.read(extract_to=self._root.dirPath, extract_files=_files_to_decompose)

    def compose(self, files: list = None):
        # workspace->node.ioz etc.
        _io = ZipFileIO(file_path=self._root.dirPath, filename=self.root.name)
        _files_to_compose = [x.fileAbsPath for x in self._root.leaves]
        _file_need_to_clear = list()
        if files is None:
            files = []
        # copy required files and dirs into this dir
        for f in files:
            if os.path.isdir(f):
                _f = shutil.copytree(f, self._root.dirPath)
                _file_need_to_clear.append(_f)
            elif os.path.isfile(f):
                _f = shutil.copy(f, self._root.dirPath)
                _file_need_to_clear.append(_f)
        # extend files and dir into list for packing
        _files_to_compose.extend(_file_need_to_clear)
        _pp = _io.write(_files_to_compose)
        # clear copied files and dirs.
        for f in _file_need_to_clear:
            if os.path.isdir(f):
                shutil.rmtree(f)
            elif os.path.isfile(f):
                os.unlink(f)
        # cut file into composedFilePath
        _path = os.path.dirname(self.composedFilePath)
        pathlib.Path(_path).mkdir(exist_ok=True, parents=True)
        shutil.move(_pp, self.composedFilePath)


ProjectWorkFileResolverFactory = {ProjectWorkFileResolver100.VERSION: ProjectWorkFileResolver100}
