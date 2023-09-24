# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_project_node.py
# ------------------------------------------------------------------------------
#
# File          : class_project_node.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.base import TreeModelAnyTreeNode, NodeContent
from framework.application.urlobject import URLObject
from framework.application.utils_helper import util_get_uuid_string, util_generate_uri
# from mbt.application.base import WorkbenchRegistry
from .define import (EnumProjectItemFlag,
                     EnumProjectItemRole)


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
    NODE_STEREOTYPE_URI_SCHEME = 'stereotype'
    NODE_ST_UNRESOLVED = 'node/unresolved'
    NODE_ST_NATIVE = 'node/native'
    NODE_ST_WORKBENCH_ROOT = 'node/workbenchRoot'
    NODE_ST_SOLUTION = 'node/solution'
    NODE_ST_ADDON = 'node/addon'
    NODE_ST_LINK = 'node/link'
    VALID_NODE_ST = [NODE_ST_NATIVE, NODE_ST_SOLUTION, NODE_ST_ADDON, NODE_ST_LINK, NODE_ST_WORKBENCH_ROOT]
    MODIFIER_KEY_PROFILE = 'profile'

    # todo: maybe more ST like custom,,,?
    # what application expect, the workbenches are always shown in projectExplorer.
    # that means the node must hava some relation or binding to the workbench.
    def __init__(self, **kwargs):
        TreeModelAnyTreeNode.__init__(self, **kwargs)
        _flag = kwargs.get('flag', EnumProjectItemFlag.FLAG_DEFAULT)
        self.uuid = kwargs.get('uuid', util_get_uuid_string())
        self.role = kwargs.get('role')
        self.sorter = kwargs.get('sorter', 0)
        self.flag = 0
        self._realize_flag(_flag)
        self.icon = kwargs.get('icon', self.icon)
        self.stereotypeQuery = kwargs.get('stereotypeQuery', dict())
        self.stereotype = kwargs.get('stereotype', self.NODE_ST_NATIVE)
        assert self.stereotype in self.VALID_NODE_ST, ValueError('unsupported stereotype %s' % self.stereotype)
        self.contextMenu = kwargs.get('contextMenu')
        self.profile = None
        self._test = 0
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
                'sorter': self.sorter,
                'stereotype': self.stereotype,
                'stereotypeQuery': self.stereotypeQuery,
                'contextMenu': self.contextMenu,
                'profile': self.profile.serializer}

    @property
    def stereotypeUri(self) -> URLObject:
        # stereotypeUri uri indicated which contenttype is, not relative for content loading
        # just only for storing the additional info and determine how to show and edit the content.
        # stereotypeUri define the role, workbench and more information in one uri string.
        # path could be node,link, queries could be solution,addon
        # uri: stereotype://unresolved is as the default URI assigned.
        # uri: stereotype://wb_uid/node/native
        # uri: stereotype://wb_uid/node/native?a=12&b=13
        # uri: stereotype://wb_uid/node/solution?name=stc?uid=7232de9a23
        # uri: stereotype://wb_uid/node/addon?
        # uri: stereotype://wb_uid/node/link?path=dw\wd\a.obj (if path not explict<like a link> then use default get_file_path()???)
        try:
            _wb_uid = self.workbenchUid
        except:
            _wb_uid = self.NODE_ST_UNRESOLVED
        if _wb_uid is None:
            _wb_uid = self.NODE_ST_UNRESOLVED
        _uri = self.get_node_stereotype_uri(_wb_uid, self.stereotype, to_string=False, **self.stereotypeQuery)
        return _uri

    @property
    def workbenchUid(self):
        _wr = self.workbenchRoot
        if _wr is not None:
            return _wr.uuid
        else:
            return None

    @property
    def workbenchRoot(self) -> 'ProjectTreeNode':
        if self.is_root or self.role == EnumProjectItemRole.ROOT.value:
            return None
        if self.isWorkbenchRoot:
            return self
        else:
            for x in self.ancestors:
                if x.isWorkbenchRoot:
                    return x
        Warning('node %s not in any workbench' % self.get_path_string())
        return None

    @property
    def isWorkbenchRoot(self):
        return self.stereotype == self.NODE_ST_WORKBENCH_ROOT

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

    @staticmethod
    def get_node_stereotype_uri(workbench_uid, node_st: str, to_string: bool = True, **queries):
        if node_st not in ProjectTreeNode.VALID_NODE_ST:
            raise ValueError('unsupported node stereotype %s.' % node_st)
        _uri = util_generate_uri(ProjectTreeNode.NODE_STEREOTYPE_URI_SCHEME, workbench_uid, node_st, to_string=to_string, **queries)
        return _uri

    def update(self, **kwargs):
        if 'flag' in kwargs:
            self.flag = 0
            self._realize_flag(kwargs.get('flag'))
        if 'icon' in kwargs:
            self.icon = kwargs.get('icon')
        if 'sorter' in kwargs:
            self.sorter = kwargs.get('sorter')
        if 'stereotype' in kwargs:
            self.stereotype = kwargs.get('stereotype')
        if 'stereotypeQuery' in kwargs:
            self.stereotypeQuery = kwargs.get('stereotypeQuery')
        if 'contextMenu' in kwargs:
            self.contextMenu = kwargs.get('contextMenu')
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

    def modify_property(self, key: str, **kwargs):
        if key == self.MODIFIER_KEY_PROFILE:
            self.update_profile(**kwargs)

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

    @staticmethod
    def auto_generate_name(parent_node: 'ProjectTreeNode', base_name: str = None):
        if base_name is None:
            base_name = 'new%sNode' % EnumProjectItemRole(parent_node.role).name.capitalize()
        _idx = 0
        _name = base_name
        _siblings_name = [x.label for x in parent_node.children]
        while _name in _siblings_name:
            _idx += 1
            _name = base_name + '%s' % _idx
        return _name

    @staticmethod
    def is_node_name_exist(parent_node: 'ProjectTreeNode', name: str):
        _siblings_name = [x.label for x in parent_node.children]
        return name in _siblings_name
