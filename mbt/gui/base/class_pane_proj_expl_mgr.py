# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       :
# Sourcefile(s) : class_pane_proj_expl_mgr.py
# ------------------------------------------------------------------------------
#
# File          : class_pane_proj_expl_mgr.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import copy, wx
import logging
import traceback

import wx.adv
import json
import os.path
import wx.lib.newevent as wxevt
from framework.application.define import _
from framework.application.utils_helper import (util_set_custom_data_to_clipboard,
                                                util_get_custom_data_from_clipboard,
                                                util_get_uuid_string, util_is_dir_exist,
                                                util_generate_uri)
from framework.gui.base.class_feedback_dialogs import FeedbackDialogs
from framework.gui.utils import gui_util_get_simple_text_header
from framework.gui.widgets import ZWizardPage
from framework.application.base import TreeModel
from mbt.application.project import (ProjectTreeNode,
                                     EnumProjectItemFlag,
                                     DF_PROJECT_NODE_FMT,
                                     EnumProjectItemRole,
                                     ProjectNodeProfile, EnumNodeSorter,
                                     SORTER_MAP,
                                     ProjectNodePropContainer,
                                     ProjectContentProvider, Project
                                     )
from mbt.application.workbench_base import MBTProjectOrientedWorkbench
from mbt.application.utils import WxMenuBuilder
from mbt.application.define import EnumAppSignal, DF_PY_OBJ_FMT, EVT_APP_TOP_MENU
from mbt.application.define_path import PROJECT_PATH
from mbt.application.base import MBTViewManager, MBTContentContainer
from mbt.gui.widgets import ProfileEditPanel, ChoiceEditPanel
from .class_pane_proj_expl_view import ProjectExplorerView, TreeView
from .define import EnumProjectExplorerContextMenuIDs
from .class_pane_proj_expl_cc import ProjectExplorerContentContainer, CommandAppendNode, CommandRemoveNode


class _TstCmd(wx.Command):
    def __init__(self):
        wx.Command.__init__(self, True, 'Test')

    def Do(self):
        print('---->_TstCmd do()')
        return True

    def Undo(self):
        return True


class ProjectExplorerManager(MBTViewManager):
    T_EVT_NODE_SELECTED, EVT_NODE_SELECTED = wxevt.NewCommandEvent()
    T_EVT_PROJECT_CREATED, EVT_PROJECT_CREATED = wxevt.NewCommandEvent()
    T_EVT_PROJECT_OPENED, EVT_PROJECT_OPENED = wxevt.NewCommandEvent()
    T_EVT_PROJECT_SAVED, EVT_PROJECT_SAVED = wxevt.NewCommandEvent()
    T_EVT_PROJECT_CLOSED, EVT_PROJECT_CLOSED = wxevt.NewCommandEvent()
    T_EVT_NODE_ADDED, EVT_NODE_ADDED = wxevt.NewCommandEvent()
    T_EVT_NODE_EDIT_REQUIRED, EVT_NODE_EDIT_REQUIRED = wxevt.NewCommandEvent()
    T_EVT_NODE_DELETED, EVT_NODE_DELETED = wxevt.NewCommandEvent()
    T_EVT_NODE_HIGHLIGHT_EDITOR, EVT_NODE_HIGHLIGHT_EDITOR = wxevt.NewCommandEvent()
    T_EVT_NODE_PROPERTY_CHANGED, EVT_NODE_PROPERTY_CHANGED = wxevt.NewCommandEvent()

    # todo: EVT_NODE_PROPERTY_CHANGED not finished
    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)
        self.menuBuilder = None
        self._propContainer = ProjectNodePropContainer()
        self._contentProvider = None
        # bind event

    @property
    def view(self) -> ProjectExplorerView:
        return self._view

    @property
    def iconSize(self) -> wx.Size:
        return wx.Size(16, 16)

    def get_prop_container(self):
        return self._propContainer

    def create_view(self, **kwargs) -> ProjectExplorerView:
        if self._view is not None:
            return self._view
        _app = wx.App.GetInstance()
        _cc = ProjectExplorerContentContainer()
        # collection all icons which used in projectExplorer
        _image_names = set()
        for k, v in self.root.get_workbenches().items():
            if v.projectNodeConstructor is None:
                continue
            [_image_names.add(x) for x in v.projectNodeConstructor.get_required_icon_names()]
        [_image_names.add(x) for x in Project.nodeConstructor.get_required_icon_names()]
        _image_names = list(_image_names)
        # add solution icon into image list
        _mbt_slt_mgr = _app.mbtSolutionManager
        for k, v in _mbt_slt_mgr.solutions.items():
            _image_names.append(v.iconInfo[1])
        self.post_content_container(_cc)
        _view = ProjectExplorerView(**kwargs, manager=self, image_names=_image_names)
        self.post_view(_view)
        # _view.PushEventHandler(self) could be useful if emit event to other object
        self.menuBuilder = WxMenuBuilder(self, self.view.treeView)
        self.menuBuilder.sigCommandSendTriggered.connect(self.on_menu_builder_message_send_required, self.menuBuilder)
        self.view.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_proj_item_context_menu)
        self.view.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_proj_item_select_changed)
        self.view.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_proj_item_activate)
        self.view.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.on_proj_item_get_tooltip)
        self.view.Bind(EVT_APP_TOP_MENU, self.on_top_menu)
        self.view.treeView.Bind(wx.EVT_MENU, self.on_context_menu)
        self.view.Bind(wx.EVT_TOOL, self.on_tool)
        # self.view.Bind(wx.EVT_CLOSE, self.on_close)
        # self.undoStack.Submit(_TstCmd())
        return self._view

    def register_to_content_resolver(self):
        """
        method make this contentcontainer as ProjectContentProvider registered into global content resolver.
        Returns: None
        """

        _app = wx.App.GetInstance()
        self._contentProvider = ProjectContentProvider(self.contentContainer)
        _app.baseContentResolver.register(self._contentProvider, override=True)

    def unregister_from_content_resolver(self):
        """
        method unregister previous registered provider from global content resolver.
        Returns: None
        """
        _app = wx.App.GetInstance()
        _app.baseContentResolver.unregister(ProjectContentProvider.AUTHORITY)
        self._contentProvider = None

    def set_project_tree(self, model: TreeModel, expand_all=True):
        self.view.treeView.set_model(model)
        if model is not None:
            self.view.enable_tools(True)
        if expand_all:
            self.view.treeView.ExpandAll()
        self.view.SetFocus()
        wx.CallAfter(self.view.select_node, model.root)

    def expand_node(self, node, recursive=True):
        self._view.treeView.expand_node(node, recursive)

    def collapse_node(self, node, recursive=True):
        self._view.treeView.collapse_node(node, recursive)

    def get_node_sop(self, node: ProjectTreeNode):
        """
        method to get the supported operation by given node.
        Args:
            node: ProjectTreeNode

        Returns: dict

        """
        return {wx.ID_COPY: node.has_flag(EnumProjectItemFlag.CAN_COPY),
                wx.ID_CUT: False,
                wx.ID_PASTE: node.has_flag(EnumProjectItemFlag.CAN_PASTE) and wx.TheClipboard.IsSupported(
                    DF_PROJECT_NODE_FMT),
                wx.ID_DELETE: node.has_flag(EnumProjectItemFlag.REMOVABLE),
                EnumProjectExplorerContextMenuIDs.REPROFILE: not node.has_flag(EnumProjectItemFlag.LABEL_READONLY),
                EnumProjectExplorerContextMenuIDs.OPEN: node.has_flag(EnumProjectItemFlag.CAN_EDIT_CONTENT),
                }

    def close_project(self):
        if self._contentContainer.project is None:
            return
        # todo: check if changed if not then return, otherwise pop yes or no msgbox prompt user option. finally close the project.
        self.unregister_from_content_resolver()
        self.emit_event(self.T_EVT_PROJECT_CLOSED,
                        project_name=self._contentContainer.project.name,
                        project_path=self._contentContainer.project.projectPath)

    def open_project(self, evt: wx.CommandEvent):
        _path = evt.GetClientData()
        if _path is None:
            _path = FeedbackDialogs.show_file_open_dialog(PROJECT_PATH, wildcard='Project file (*.proj)|*.proj')
            if _path is None:
                return
            _path = os.path.dirname(_path)
        if not os.path.exists(_path):
            FeedbackDialogs.show_msg_dialog(_('Error'), _('Projects path <%s> is not exist.') % _path)
            return
        if self._contentContainer.project is not None:
            _name = self._contentContainer.project.name
            # same name not need to be closed.
            if _name == os.path.basename(_path):
                FeedbackDialogs.show_msg_dialog(_('Info'), _('Projects %s is already opened.') % _name)
                return
        self.close_project()
        # assume the project name same as the dir name
        if self._contentContainer.open_project(_path):
            self.set_project_tree(self._contentContainer.project.projectTreeModel)
            # loading content
            _nodes_need_prepare_content = self._contentContainer.project.nodesHasContent
            with FeedbackDialogs.show_progress_dialog(_('Loading'), '', len(_nodes_need_prepare_content), self.root.view) as pd:
                _failed_list = []
                self._contentContainer.project.clear_work_file_dirs()
                for idx, x in enumerate(_nodes_need_prepare_content):
                    pd.Update(idx, 'load node %s' % x.label)
                    _ret = self._contentContainer.prepare_node_content(x)
                    if not _ret:
                        _failed_list.append(x.label)
                # todo: load mainPerspective
                # if _app.project.mainPerspective is not None:
                #     self._auiMgr.LoadPerspective(_app.project.mainPerspective)
                pd.Destroy()
            self.register_to_content_resolver()
            self.emit_event(self.T_EVT_PROJECT_OPENED, project=self._contentContainer.project)
            if _failed_list:
                FeedbackDialogs.show_msg_dialog(_('Warning'), 'follow node content load failed.%s' % ('\n'.join(_failed_list)))
        else:
            FeedbackDialogs.show_msg_dialog(_('Error'), 'can not open the project.\n%s' % self._contentContainer.pop_error())

    def create_project(self):
        self.close_project()
        # get optional workbenches
        _wb_choices = self.root.get_workbench_choices(filter_=lambda k: isinstance(k[1], MBTProjectOrientedWorkbench))
        # show dialog for gathering the form to creating project
        _ret, _proj_name, _project_path = self.view.show_create_new_project_dialog(_wb_choices)
        if not _ret:
            return
        _workbenches = [x.uid for x in _wb_choices if x.selected]

        if not _proj_name.strip():
            FeedbackDialogs.show_msg_dialog(_('Failed'), _('Project name is empty.'), icon=wx.ICON_ERROR)
            return
        _project_full_path = os.path.join(_project_path, _proj_name)
        _exist = util_is_dir_exist(_project_full_path)
        if _exist:
            FeedbackDialogs.show_msg_dialog(_('Failed'), _('Project path <%s> is not empty') % _project_full_path, icon=wx.ICON_ERROR)
            return
        if not _workbenches:
            FeedbackDialogs.show_msg_dialog(_('Failed'), _('Empty workbenches is not allowed.'), icon=wx.ICON_ERROR)
            return

        with FeedbackDialogs.show_progress_dialog(_('Create Project'), '', parent=self.root.view) as pd:
            pd.Update(5, _('start creating project'))
            _ret = self._contentContainer.create_new_project(_proj_name, _project_path, _workbenches)
            pd.Update(100, _('workbenches and project initialized'))
            if not _ret:
                FeedbackDialogs.show_msg_dialog(_('Error'), 'Can not create the project %s, at %s.\nError:%s' % (
                    _proj_name, _project_path, self._contentContainer.pop_error()))
                self._contentContainer.delete_project_dir(_proj_name, _project_path)
                return
        self.set_project_tree(self._contentContainer.project.projectTreeModel)
        self.expand_node(self._contentContainer.projectRoot, False)
        self.register_to_content_resolver()
        self.emit_event(self.T_EVT_PROJECT_CREATED, project=self._contentContainer.project)

    def _create_new_file(self):
        FeedbackDialogs.show_msg_dialog('Fail', 'todo: create supported node type file....')

    def save_project(self):
        if self._contentContainer.project is None:
            return
        with FeedbackDialogs.show_progress_dialog(_('Processing...'), _('Save Project'), parent=self.root.view) as pd:
            # todo: collection all unsaved nodes, then update it?
            pd.Update(90, 'Compose project data')
            self._contentContainer.project.do_save_project_data()
            self._contentContainer.project.do_save_project_content()
            pd.Destroy()

    def add_node(self, role: str):
        try:
            _cc: ProjectExplorerContentContainer = self._contentContainer
            _parent = _cc.find_parent_node_by_child_role(role)
            _wb: MBTProjectOrientedWorkbench = _cc.get_current_workbench(_parent.workbenchUid)
            if _wb is not None:
                _role_name = _wb.get_role_name(role).capitalize()
                _wb.add_project_node(_parent, role)
            else:
                FeedbackDialogs.show_msg_dialog(_('todo'), _('for no workbench node should also add node possible'))
                # self.view.refresh_tree()
                # self.emit_event(self.T_EVT_NODE_ADDED, uid=_uid)
        except Exception as e:
            FeedbackDialogs.show_msg_dialog(_('Error'), _('Can not add node. since:%s') % e,
                                            icon=wx.ICON_ERROR)
            self.print_traceback()

    def copy_node(self, node: ProjectTreeNode):
        try:
            _d = json.dumps(node.meta)
            _ret = util_set_custom_data_to_clipboard(wx.TheClipboard, DF_PROJECT_NODE_FMT, _d.encode('utf-8'))
        except Exception as e:
            _ret = False
            if not _ret:
                FeedbackDialogs.show_msg_dialog(_('Error'), _('Can not copy the node into clipboard.') + '\n%s' % e)
                return

    def cut_node(self, node: ProjectTreeNode):
        # not supported
        pass

    def paste_on_node(self, node: ProjectTreeNode):
        try:
            _b = util_get_custom_data_from_clipboard(wx.TheClipboard, DF_PROJECT_NODE_FMT)
            if _b is None:
                FeedbackDialogs.show_msg_dialog(_('Error'), _('Can not find the required format data from clipboard.'))
                return
            if isinstance(_b, memoryview):
                _b = _b.tobytes()
            _meta = json.loads(_b)
            _meta['uuid'] = util_get_uuid_string()
            _meta['profile']['name'] += 'Copy'
            _role = _meta.get('role')
            if node.is_children_role(_role):
                _parent = node
            else:
                _parent = self._contentContainer.find_parent_node_by_child_role(_role)
            if _parent is None:
                FeedbackDialogs.show_msg_dialog(_('Error'),
                                                _('Can not find the parent for the pasting node role %s.') % _role)
                return
            _wb: MBTProjectOrientedWorkbench = self._contentContainer.get_current_workbench(_parent.workbenchUid)
            if _wb is not None:
                _wb.add_project_node(_parent, _role, meta=_meta)
            else:
                _cmd = CommandAppendNode(self, _parent.uuid, _meta, name='PasteNode')
                _ret = self.undoStack.Submit(_cmd)
                assert _ret, 'command not be executed successfully.'
        except Exception as e:
            FeedbackDialogs.show_msg_dialog('Error', _('can not paste node.\n%s') % e,
                                            icon=wx.ICON_ERROR)
            self.log.error('can not execute paste node, since:\n%s' % e)
            if self.log.getEffectiveLevel() == logging.DEBUG:
                traceback.print_exc()

    def delete_node(self, node: ProjectTreeNode):
        try:
            _ret = FeedbackDialogs.show_yes_no_dialog(_('Delete'), _('Are you sure to delete?'))
            if _ret:
                _n_uid = node.uuid
                _wb: MBTProjectOrientedWorkbench = self._contentContainer.get_current_workbench(node.workbenchUid)
                if _wb is not None:
                    _wb.remove_project_node(_n_uid)
                else:
                    _cmd = CommandRemoveNode(self, node, name='DeleteNode')
                    _ret = self.undoStack.Submit(_cmd)
                    assert _ret, 'command not be executed successfully.'
                    self.view.refresh_tree()
                    self.emit_event(self.T_EVT_NODE_DELETED, uid=_n_uid)
        except Exception as e:
            FeedbackDialogs.show_msg_dialog('Error', _('can not delete node.\n%s') % e, icon=wx.ICON_ERROR)
            self.log.error('can not execute delete node, since:\n%s' % e)
            self.print_traceback()

    def open_node(self, node: ProjectTreeNode):
        if node.has_flag(EnumProjectItemFlag.CAN_EDIT_CONTENT):
            self.emit_event(self.T_EVT_NODE_EDIT_REQUIRED, node=node)

    def reprofile_node(self, node: ProjectTreeNode):
        try:
            _wb: MBTProjectOrientedWorkbench = self._contentContainer.get_current_workbench(node.workbenchUid)
            if _wb is not None:
                _wb.modify_project_node_property(node.uuid, ProjectTreeNode.MODIFIER_KEY_PROFILE)
        except Exception as e:
            FeedbackDialogs.show_msg_dialog('Error', _('Reprofile failed.\n%s') % e, icon=wx.ICON_ERROR)
            self.log.error('can not execute reprofile node, since:\n%s' % e)
            self.print_traceback()

    def do_sop(self, sop_id, **kwargs):
        """
        execute supported operation (copy,cut,paste currently)
        Args:
            sop_id:
            **kwargs:

        Returns:

        """
        _item = self._view.treeView.GetSelection()
        if not _item.IsOk():
            return
        _node = self._view.treeView.item_to_node(_item)
        if sop_id == wx.ID_COPY:
            self.copy_node(_node)
        elif sop_id == wx.ID_CUT:
            self.cut_node(_node)
        elif sop_id == wx.ID_PASTE:
            self.paste_on_node(_node)

    def focus_on_node_with_uid(self, uid):
        if self._contentContainer.project is None:
            return
        _node = self._contentContainer.find_node_by_uid(uid)
        if _node is None:
            return
        self.view.select_node(_node, True, evt_propagation=False, focus=False)

    # --------------------------------------------------------------
    # event handling
    # --------------------------------------------------------------
    def on_top_menu(self, evt: wx.MenuEvent):
        self.on_context_menu(evt)

    def on_context_menu(self, evt: wx.MenuEvent):
        _id = evt.GetId()
        _item = self._view.treeView.GetSelection()
        if not _item.IsOk():
            return
        _node = self._view.treeView.item_to_node(_item)
        if _id == wx.ID_COPY:
            self.copy_node(_node)
        elif _id == wx.ID_CUT:
            self.cut_node(_node)
        elif _id == wx.ID_PASTE:
            self.paste_on_node(_node)
        elif _id == wx.ID_DELETE:
            self.delete_node(_node)
        elif _id == EnumProjectExplorerContextMenuIDs.OPEN:
            self.open_node(_node)
        elif _id == EnumProjectExplorerContextMenuIDs.REPROFILE:
            self.reprofile_node(_node)

    def on_menu_builder_message_send_required(self, *args, **kwargs):
        _message = kwargs.get('message')
        _event = kwargs.get('event')
        if _message is None:
            return
        _topic, _action = _message.split('.')
        if _topic == 'projectAddNode':
            _role = kwargs.get('role')
            _pr, _cr = _role.split('_')
            self.add_node(_cr)
        elif _topic == 'project':
            pass
            print('---->project topic action:', _action)

    def on_proj_item_context_menu(self, evt: wx.TreeEvent):
        _item = evt.GetItem()
        _view = self.view.treeView
        _view.SelectItem(_item)
        _node: ProjectTreeNode = _view.item_to_node(_item)
        _cm_cfg: list = copy.deepcopy(Project.baseContextMenuCfg)
        _node_cm_cfg = copy.deepcopy(self._contentContainer.get_project_node_cm_config(_node.role))
        if _node_cm_cfg:
            # add a separator
            _cm_cfg.append({'kind': -1, 'children': []})
        _cm_cfg.extend(_node_cm_cfg)
        if not _cm_cfg:
            return
        _ctx = {'wx': wx, 'this': _node}
        _edit_op = self.get_node_sop(_node)
        _disable_map = [k for k, v in _edit_op.items() if not v]
        _menu = self.menuBuilder.get_menu(_cm_cfg, _ctx, _disable_map)
        _view.PopupMenu(_menu)
        _menu.Destroy()

    def on_proj_item_select_changed(self, evt: wx.TreeEvent):
        _item = evt.GetItem()
        _view: TreeView = self.view.treeView
        _node: ProjectTreeNode = _view.item_to_node(_item)
        _link_editor_cond = _node.has_flag(EnumProjectItemFlag.CAN_EDIT_CONTENT) and self.root.is_node_editor_exist(_node)
        self.view.enable_tools(_link_editor_cond, self.view.tbIdLinkEditor)
        if _node.children:
            if all([x.has_flag(EnumProjectItemFlag.ORDERABLE) for x in _node.children]):
                self.view.enable_tools(True, self.view.tbIdSort)
                _sort_c, _flag = SORTER_MAP.get(_node.sorter)
                self.view.update_sort_tool_icon(_flag)
            else:
                self.view.enable_tools(False, self.view.tbIdSort)
        else:
            self.view.enable_tools(False, self.view.tbIdSort)
        self._propContainer.set_node(_node)
        EnumAppSignal.sigProjectNodeSelectChanged.send(self, node=_node)
        EnumAppSignal.sigSupportedOperationChanged.send(self, op=self.get_node_sop(_node))
        _evt = self.T_EVT_NODE_SELECTED(self.view.GetId(), node=_node)
        wx.PostEvent(self.view, _evt)
        evt.Skip()

    def on_proj_item_activate(self, evt: wx.TreeEvent):
        _item = evt.GetItem()
        _view: TreeView = self.view.treeView
        _node: ProjectTreeNode = _view.item_to_node(_item)
        # let root open node content editor. if has children collapse or expand it.
        if _node.children:
            _view.Toggle(_item)
            return
        if _node.has_flag(EnumProjectItemFlag.CAN_EDIT_CONTENT):
            self.emit_event(self.T_EVT_NODE_EDIT_REQUIRED, node=_node)

    def on_proj_item_get_tooltip(self, evt: wx.TreeEvent):
        _item = evt.GetItem()
        _node = self.view.treeView.item_to_node(_item)
        if _node.description is not None:
            evt.SetToolTip(_node.description)

    def on_tool(self, evt: wx.CommandEvent):
        _id = evt.GetId()
        self.view.SetFocus()
        if _id == self.view.tbIdExpandAll:
            self.view.treeView.ExpandAll()
        elif _id == self.view.tbIdCollapseAll:
            self.view.treeView.CollapseAll()
        elif _id == self.view.tbIdLinkEditor:
            self.emit_event(self.T_EVT_NODE_HIGHLIGHT_EDITOR, node=self.view.get_current_selected())
        elif _id == self.view.tbIdSort:
            if self._contentContainer.project is None: return
            # all its children could be sortable, currently sort the item only base on the label
            _node = self.view.get_current_selected()
            if _node.sorter == EnumNodeSorter.SORTER_LABEL_ASC:
                _node.update(sorter=EnumNodeSorter.SORTER_LABEL_DSC.value)
            elif _node.sorter == EnumNodeSorter.SORTER_LABEL_DSC:
                _node.update(sorter=EnumNodeSorter.SORTER_LABEL_ASC.value)
            _flag = self._contentContainer.project.projectTreeModel.sort(_node)
            self.view.refresh_tree()
            self.view.update_sort_tool_icon(_flag)
