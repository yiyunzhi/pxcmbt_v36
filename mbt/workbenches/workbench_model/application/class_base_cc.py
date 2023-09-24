# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_base_cc.py
# ------------------------------------------------------------------------------
#
# File          : class_base_cc.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx
from mbt.application.base import MBTContentContainer
from mbt.application.workbench_base import MBTBaseWorkbenchViewManager
from mbt.application.project import ProjectTreeNode


class CommandAppendProjectNode(wx.Command):
    def __init__(self, manager: MBTBaseWorkbenchViewManager, parent_node_uid: str, node_meta: dict, can_undo=True, name='AppendModelWorkbenchProjectNode'):
        wx.Command.__init__(self, can_undo, name)
        self.manager = manager
        self.parentNodeUid = parent_node_uid
        self.nodeMeta = node_meta
        self.nodeUid = None

    @property
    def project(self):
        return self.manager.workbench.project

    @property
    def parentNode(self):
        return self.project.projectTreeModel.find_node_by_uid(self.parentNodeUid)

    def Undo(self):
        _node = self.project.projectTreeModel.find_node_by_uid(self.nodeUid)
        self.project.contentManager.post_delete_project_node(_node)
        self.project.contentManager.manager.view.refresh_tree()
        return True

    def Do(self):
        _node = self.project.contentManager.post_add_child_node_of(self.parentNode, self.nodeMeta['role'], self.nodeMeta)
        self.nodeUid = _node.uuid
        self.project.contentManager.manager.emit_event(self.project.contentManager.manager.T_EVT_NODE_ADDED, uid=_node.uuid)
        self.project.contentManager.manager.view.refresh_tree()
        self.project.contentManager.manager.view.select_node(_node)
        return True


class CommandRemoveProjectNode(wx.Command):
    def __init__(self, manager: MBTBaseWorkbenchViewManager, node: ProjectTreeNode, can_undo=True, name='RemoveModelWorkbenchProjectNode'):
        wx.Command.__init__(self, can_undo, name)
        self.manager = manager
        self.nodeMeta = node.meta
        self.parentNodeUid = node.parent.uuid
        self.node = node
        self.nodeUid = node.uuid

    @property
    def project(self):
        return self.manager.workbench.project

    @property
    def parentNode(self):
        return self.project.projectTreeModel.find_node_by_uid(self.parentNodeUid)

    def Undo(self):
        _node = self.project.contentManager.post_add_child_node_of(self.parentNode, self.nodeMeta['role'], self.nodeMeta)
        _node.update(**self.nodeMeta)
        _node.uuid = self.nodeMeta['uuid']
        self.project.contentManager.manager.view.refresh_tree()
        self.project.contentManager.manager.view.select_node(_node)
        self.node = _node
        return True

    def Do(self):
        self.project.contentManager.post_delete_project_node(self.node)
        self.project.contentManager.manager.view.refresh_tree()
        self.project.contentManager.manager.emit_event(self.project.contentManager.manager.T_EVT_NODE_DELETED, uid=self.nodeUid)
        return True


class CommandModifyProjectNodeProperty(wx.Command):
    def __init__(self, manager: MBTBaseWorkbenchViewManager,
                 node: ProjectTreeNode,
                 modifier_key: str, new_value: any, old_value: any,
                 can_undo=True, name='RemoveModelWorkbenchProjectNode'):
        wx.Command.__init__(self, can_undo, name)
        self.manager = manager
        self.node = node
        self.nodeUid = node.uuid
        self.modifierKey = modifier_key
        self.oldValue = old_value
        self.newValue = new_value

    @property
    def project(self):
        return self.manager.workbench.project

    def Undo(self):
        self.node.modify_property(self.modifierKey, **self.oldValue)
        self.project.contentManager.manager.view.refresh_tree()
        self.project.contentManager.manager.emit_event(self.project.contentManager.manager.T_EVT_NODE_PROPERTY_CHANGED, uid=self.nodeUid, key=self.modifierKey)
        return True

    def Do(self):
        self.node.modify_property(self.modifierKey, **self.newValue)
        self.project.contentManager.manager.view.refresh_tree()
        self.project.contentManager.manager.emit_event(self.project.contentManager.manager.T_EVT_NODE_PROPERTY_CHANGED, uid=self.nodeUid, key=self.modifierKey)
        return True


class ModelWorkbenchBaseContentContainer(MBTContentContainer):
    def __init__(self, **kwargs):
        MBTContentContainer.__init__(self, **kwargs)

    def transform_data(self, transformer: any):
        pass
