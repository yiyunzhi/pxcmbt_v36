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
import typing
from framework.application.define import _
from framework.application.content_resolver import ContentContract
from framework.application.base import BaseSelectionItem, GenericTypeFactory
from framework.application.workbench import BaseWorkbench
from mbt.application.base import MBTViewManager
from mbt.application.project import MBTProjectNodeConstructorImporter, ProjectTreeNode, Project


class EnumMBTWorkbenchFlag:
    PROJECT_NODE_CONSTRUCTION = 1 << 0
    HAS_EDITOR = 1 << 1
    OPTIONAL = 1 << 4
    DEFAULT = HAS_EDITOR


class MBTBaseWorkbenchViewManager(MBTViewManager):
    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)
        self.workbench=kwargs.get('workbench')

    def setup(self, *args, **kwargs):
        raise NotImplementedError

    def teardown(self, *args, **kwargs):
        raise NotImplementedError


class MBTBaseWorkbench(BaseWorkbench):
    def __init__(self, **kwargs):
        BaseWorkbench.__init__(self, **kwargs)
        assert self.uid is not None
        if self.has_flag(EnumMBTWorkbenchFlag.HAS_EDITOR):
            self.editorFactory = kwargs.get('editor_factory', GenericTypeFactory())
        else:
            self.editorFactory = None
        self.viewManager = MBTBaseWorkbenchViewManager(uid=self.uid,workbench=self)

    def setup(self, **kwargs):
        _parent = kwargs.get('view_manager_parent')
        if _parent is not None:
            self.viewManager.parent = _parent
        self.viewManager.setup()

    def teardown(self):
        if self.viewManager is not None:
            self.viewManager.teardown()
            self.viewManager.parent = None


class MBTProjectOrientedWorkbench(MBTBaseWorkbench):
    """
    project oriented workbench will show the node in projectExplorer.
    """

    def __init__(self, **kwargs):
        MBTBaseWorkbench.__init__(self, **kwargs)
        self.baseRole = kwargs.get('base_role')
        self.add_flag(EnumMBTWorkbenchFlag.PROJECT_NODE_CONSTRUCTION)
        self.projectNodeConstructor = MBTProjectNodeConstructorImporter(kwargs.get('construction_cfg_file'))
        # todo: maybe check projectNodeConstructor first.
        self.rootNode: ProjectTreeNode = None
        self.project: Project = None

    def setup(self, project: Project):
        self.project = project
        _node = project.projectTreeModel.find_node_by_uid(self.uid)
        if _node.role != self.baseRole:
            return False, _('unsupported node uid or baseRole.')
        self.rootNode = _node
        if self.viewManager is not None:
            if self.viewManager.parent != self.project.contentManager.manager:
                self.viewManager.parent = self.project.contentManager.manager
                self.viewManager.setup()
        return True, ''

    def teardown(self):
        self.project = None
        self.rootNode = None
        if self.viewManager is not None:
            self.viewManager.teardown()
            self.viewManager.parent = None

    def do_project_node_construction(self, construct_key: str) -> (bool, typing.Union[ProjectTreeNode, str]):
        """
        for CONSTRUCTION_KEY_NEW_PROJECT must this return this locale root back, since the project could have
        multi workbenches. after the check in project, then this locale root will be assigned by inject_project.

        but for add child node just done in this workbench. the supervisors start this process and emit the corresponding event.
        Args:
            construct_key: str

        Returns: bool, TreeModelAnyTreeNode. base on the given type in projectNodeConstructor.
                the root of this workbench will be created for adding in projectTree.

        """
        if self.projectNodeConstructor is None or not self.has_flag(EnumMBTWorkbenchFlag.PROJECT_NODE_CONSTRUCTION):
            return False, _('no constructor assigned.')
        if construct_key == MBTProjectNodeConstructorImporter.CONSTRUCTION_KEY_NEW_PROJECT:

            _data = self.projectNodeConstructor.data
            # n is the workbench root node
            _n = self.projectNodeConstructor.construct(construct_key)
            if _data.get('isWorkbench'):
                if 'uuid' not in _data:
                    return False, _('invalid constructor data structure. uuid key is required if configuration for workbench.')
                if _n.role != self.projectNodeConstructor.get_base_role():
                    return False, _('invalid constructor data structure. the root role must identical with the configuration.')
                _n.uuid = _data.get('uuid')
            return True, _n
        elif construct_key.startswith(MBTProjectNodeConstructorImporter.CONSTRUCTION_KEY_NEW_CHILD_NODE_OF):
            # todo: implement this branches
            pass

    def is_my_descendant(self, val: any, by_: str = 'uuid') -> bool:
        if not hasattr(self.rootNode, by_):
            return False
        if by_=='role':
            return self.baseRole in val
        _descendant_attrs = [getattr(x, by_) for x in self.rootNode.descendants]
        return val in _descendant_attrs

    def auto_generate_name_in(self, parent: ProjectTreeNode) -> str:
        pass

    def is_node_name_exist(self, parent: ProjectTreeNode):
        pass

    def get_role_name(self, role) -> str:
        raise NotImplementedError

    def prepare_add_node(self, parent_uid: str, child_role: str, **kwargs):
        raise NotImplementedError

    def prepare_remove_node(self, uid: str, **kwargs):
        raise NotImplementedError

    def prepare_edit_node(self, uid: str, **kwargs):
        raise NotImplementedError

    def prepare_sort(self, uid: str, sort_type, **kwargs):
        raise NotImplementedError

    def do_content_insert(self, contract: ContentContract):
        raise NotImplementedError

    def do_content_update(self, contract: ContentContract):
        raise NotImplementedError

    def do_content_delete(self, contract: ContentContract):
        raise NotImplementedError

    def do_content_query(self, contract: ContentContract):
        raise NotImplementedError


class WorkbenchChoiceItem(BaseSelectionItem):
    def __init__(self, wb: MBTBaseWorkbench):
        BaseSelectionItem.__init__(self)
        self.uid = wb.uid
        self.name = wb.name
        self.icon = wb.icon
        self.description = wb.description
