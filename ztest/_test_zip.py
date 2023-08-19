# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_zip.py
# ------------------------------------------------------------------------------
#
# File          : _test_zip.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, anytree, shutil
from framework.application.io import ZipFileIO, AppFileIO, AppYamlFileIO

_node_uid = 'a2cd6e77'

_this_path = os.path.dirname(__file__)

IO_CLS_FACTORY = {'.obj': AppYamlFileIO}


class ProjectContentFileNode(anytree.NodeMixin):
    separator = os.sep

    def __init__(self, **kwargs):
        self.label = kwargs.get('label', '')
        self.extension = kwargs.get('extension', '')
        self.ioCls = kwargs.get('io_cls', IO_CLS_FACTORY.get(self.extension))
        self.parent = kwargs.get('parent')
        _children = kwargs.get('children')
        if _children:
            self.children = _children

    @property
    def filePath(self):
        return self.separator.join([x.label for x in self.path]) + self.extension

    def init(self):
        if self.is_leaf:
            _dir = os.path.dirname(self.filePath)
            _file_name = os.path.basename(self.filePath)
            _io = self.ioCls(file_path=_dir, filename=_file_name, extension=self.extension)
            _io.write('')
        else:
            os.makedirs(self.filePath,exist_ok=True)

    def read(self, **kwargs):
        if not os.path.exists(self.filePath):
            return
        if self.is_leaf:
            _dir = os.path.dirname(self.filePath)
            _file_name = os.path.basename(self.filePath)
            _io = self.ioCls(file_path=_dir, filename=_file_name, extension=self.extension)
            return _io.read(**kwargs)

    def write(self, data, **kwargs):
        if self.is_leaf:
            _dir = os.path.dirname(self.filePath)
            _file_name = os.path.basename(self.filePath)
            _io = self.ioCls(file_path=_dir, filename=_file_name, extension=self.extension)
            return _io.write(data, **kwargs)

    def remove(self):
        if self.children:
            if os.path.exists(self.filePath):
                shutil.rmtree(self.filePath)
        else:
            if os.path.exists(self.filePath):
                os.unlink(self.filePath)


class ProjectNodeContentFileResolver:
    """
    used to compose multi files into one file.
    """
    VERSION = '1.0.0'
    EXTENSION = '.ioz'

    def __init__(self, composed_path, workspace_path):
        self.composedPath = composed_path
        self.workspacePath = workspace_path
        self._root = ProjectContentFileNode(label=self.workspacePath)
        # meta, content default exist.
        _dir = ProjectContentFileNode(parent=self._root, label='test_dir1')
        _dir2 = ProjectContentFileNode(parent=self._root, label='test_dir2')
        _kk = ProjectContentFileNode(parent=self._root, label='kk', extension='.obj')
        _meta = ProjectContentFileNode(parent=_dir, label='meta', extension='.obj')
        _rsc = ProjectContentFileNode(parent=_dir, label='resource', extension='.obj')
        _main = ProjectContentFileNode(parent=_dir2, label='main', extension='.obj')

    def init_composed_file(self):
        if not os.path.isfile(self.composedPath):
            self.composedPath += self.EXTENSION
        _dir = os.path.dirname(self.composedPath)
        _filename = os.path.basename(self.composedPath)
        _io = ZipFileIO(file_path=_dir, filename=_filename)
        _io.write([])

    def init_workspace(self):
        self._root.init()
        for x in self._root.descendants:
            x.init()

    def clear_workspace(self, remove_folder=False):
        if os.path.exists(self.workspacePath):
            shutil.rmtree(self.workspacePath)
        if not remove_folder:
            os.mkdir(self.workspacePath)

    def remove_file_from_workspace(self, file_node: ProjectContentFileNode):
        if file_node.root is self._root:
            file_node.remove()

    def read(self, content_path) -> AppFileIO:
        _c_node = anytree.find(self._root, lambda x: x.filePath == content_path)
        if _c_node is not None:
            pass

    def write(self, content_path, data):
        pass

    def decompose(self):
        # node.ioz->workspace etc.
        _path = os.path.dirname(self.composedPath)
        _name = os.path.basename(self.composedPath)
        _io = ZipFileIO(file_path=self.composedPath, filename=_name)
        _files_to_decompose = [x.filePath for x in self._root.leaves]
        _io.read(extract_to=self.workspacePath, extract_files=_files_to_decompose)

    def compose(self):
        # workspace->node.ioz etc.
        _path = os.path.dirname(self.composedPath)
        _name = os.path.basename(self.composedPath)
        _io = ZipFileIO(file_path=self.composedPath, filename=_name)
        _files_to_compose = [x.filePath for x in self._root.leaves]
        map(lambda x: os.path.join(self.workspacePath, x), _files_to_compose)
        _io.write(_files_to_compose)


#
# io = ZipFileIO(file_path=_this_path, filename='test_zip')
# io.write(['test.png', 'test_dir/a1.txt', 'test_dir/a2.jpg'])
# io.read(extract_to=os.path.join(_this_path, 'test_rcv_dir'), extract_files=['test_dir/a1.txt'])
_resolver = ProjectNodeContentFileResolver(os.path.join(_this_path, _node_uid), os.path.join(_this_path, _node_uid))
_resolver.init_composed_file()
_resolver.init_workspace()
_resolver.compose()
