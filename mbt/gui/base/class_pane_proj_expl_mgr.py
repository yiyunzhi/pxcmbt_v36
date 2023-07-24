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
import wx.adv
import json
import os.path
import wx.lib.newevent as wxevt
from framework.application.define import _
from framework.application.io import AppYamlFileIO
from framework.application.utils_helper import (util_set_custom_data_to_clipboard,
                                                util_get_custom_data_from_clipboard,
                                                util_get_uuid_string)
from framework.gui.base.class_feedback_dialogs import FeedbackDialogs
from framework.gui.utils import gui_util_get_simple_text_header
from framework.application.base import TreeModel
from mbt.application.project import (ProjectTreeNode,
                                     EnumProjectItemFlag,
                                     DF_PROJECT_NODE_FMT,
                                     EnumProjectItemRole,
                                     ProjectNodeProfile)
from mbt.gui.base import MBTViewManager, MBTContentContainer
from mbt.gui.widgets import ZWizardPage, ProfileEditPanel, ChoiceEditPanel
from mbt.application.utils import WxMenuBuilder
from mbt.application.define import EnumAppSignal, DF_PY_OBJ_FMT
from mbt.application.define_path import PROJECT_PATH
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
    _T_NODE_SELECTED, EVT_NODE_SELECTED = wxevt.NewCommandEvent()
    _T_PROJECT_CREATED, EVT_PROJECT_CREATED = wxevt.NewCommandEvent()
    _T_PROJECT_OPENED, EVT_PROJECT_OPENED = wxevt.NewCommandEvent()
    _T_PROJECT_SAVED, EVT_PROJECT_SAVED = wxevt.NewCommandEvent()
    _T_NODE_ADDED, EVT_NODE_ADDED = wxevt.NewCommandEvent()
    _T_NODE_DELETED, EVT_NODE_DELETED = wxevt.NewCommandEvent()
    _T_NODE_PROPERTY_CHANGED, EVT_NODE_PROPERTY_CHANGED = wxevt.NewCommandEvent()

    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)
        self.menuBuilder = None
        # bind event

    @property
    def iconSize(self) -> wx.Size:
        return wx.Size(16, 16)

    def create_view(self, **kwargs):
        if self._view is not None:
            return self._view
        _cc = ProjectExplorerContentContainer()
        _image_names = _cc.projectCNImporter.get_required_icon_names()
        self.post_content_container(_cc)
        # todo: add solution icon into image list
        _view = ProjectExplorerView(**kwargs, manager=self, image_names=_image_names)
        self.post_view(_view)
        # _view.PushEventHandler(self) could be useful if emit event to other object
        self.menuBuilder = WxMenuBuilder(self, self.view.treeView)
        self.menuBuilder.sigCommandSendTriggered.connect(self.on_menu_builder_message_send_required, self.menuBuilder)
        self.view.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_proj_item_context_menu)
        self.view.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_proj_item_select_changed)
        self.view.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_proj_item_activate)
        self.view.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.on_proj_item_get_tooltip)
        self.view.treeView.Bind(wx.EVT_MENU, self.on_menu)
        self.view.Bind(wx.EVT_TOOL, self.on_tool)
        # self.view.Bind(wx.EVT_CLOSE, self.on_close)
        self.undoStack.Submit(_TstCmd())
        return self._view

    def set_project_tree(self, model: TreeModel, expand_all=True):
        self.view.treeView.set_model(model)
        # todo: select the root item.
        if model is not None:
            self.view.enable_tools(True)
        if expand_all:
            self.view.treeView.ExpandAll()

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
                EnumProjectExplorerContextMenuIDs.RENAME: not node.has_flag(EnumProjectItemFlag.LABEL_READONLY),
                EnumProjectExplorerContextMenuIDs.OPEN: node.has_flag(EnumProjectItemFlag.CAN_EDIT_CONTENT),
                }

    def close_project(self):
        if self._contentContainer.project is None:
            return
        # todo: check if changed if not then return, otherwise pop yes or no msgbox prompt user option. finally close the project.

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
        self.close_project()
        # todo: show process dialog while loading content
        # assume the project name same as the dir name
        if self._contentContainer.open_project(_path):
            # todo: label and description of node must be updated from content.
            self.set_project_tree(self._contentContainer.project.projectTreeModel)
            # loading content
            # self._loading_project_node_content(_app)
            # self._panelProjectMgr.treeView.set_model(_app.project.projectTreeModel)
            # self._panelProjectMgr.treeView.expand_node(_app.project.projectTreeRoot, False)
            # self._panelProjectMgr.treeView.RefreshItems()
            # self._update_title_with_project_name(_app.project.name)
            # _app.save_project_info_to_recent(_app.project.name, _app.project.projectPath)
            # _full_path = os.path.join(_app.project.projectPath, _app.project.name + '.proj')
            # self._save_to_file_history(_full_path)
            # gv.MAIN_APP = _app
            # if _app.project.mainPerspective is not None:
            #     self._auiMgr.LoadPerspective(_app.project.mainPerspective)
            self.emit_event(self._T_PROJECT_OPENED, project=self._contentContainer.project)
        else:
            wx.MessageBox('can not open the project.\n%s' % self._contentContainer.pop_error())

    def create_project(self):
        self.close_project()
        _proj_name, _project_path = self.view.show_create_new_project_dialog()
        if _proj_name is not None and _project_path is not None:
            _ret = self._contentContainer.create_new_project(_proj_name, _project_path)
            if not _ret:
                wx.MessageBox('Can not create the project %s, at %s.\nError:%s' % (
                    _proj_name, _project_path, self._contentContainer.pop_error()))
                self._contentContainer.delete_project(_proj_name, _project_path)
            else:
                self.set_project_tree(self._contentContainer.project.projectTreeModel)
                self._contentContainer.set_default_node_content()
                self.expand_node(self._contentContainer.projectRoot, False)
                self.emit_event(self._T_PROJECT_CREATED, project=self._contentContainer.project)

    def _create_new_file(self):
        wx.MessageBox(' fail to create file, see you next version', 'Fail')

    def _run_wizard_for_new_or_edit_node(self, **options) -> (bool, dict):
        _title = options.get('title', _('NewNode'))
        _profile_title = options.get('profile_title', _('Profile'))
        _profile_desc = options.get('profile_description', _('Here input the node profile information.'))
        _profile_content = options.get('profile_content', dict())
        _profile_content_validator = options.get('profile_content_validator')
        _choice_label = options.get('choice_label', 'SelectOne:')
        _choice_content = options.get('choice_content')
        _choice_validator = options.get('choice_validator')
        _choice_title = options.get('choice_title', _('Select'))
        _choice_desc = options.get('choice_description', _('Here select an option from given options.'))
        _bmp_id = options.get('bmp_id', 'pi.list-plus')
        _bmp = wx.ArtProvider.GetBitmap(_bmp_id, wx.ART_OTHER, wx.Size(64, 64))
        _wz = wx.adv.Wizard(self.view, wx.ID_ANY, _title, _bmp, style=wx.DEFAULT_DIALOG_STYLE)
        _wz.SetBitmapPlacement(wx.adv.WIZARD_VALIGN_CENTRE)
        _wz.SetBitmapBackgroundColour('#ddd')
        _wz.SetPageSize(wx.Size(360, -1))

        _page1 = ZWizardPage(_wz)
        _page1.add_widget('header', gui_util_get_simple_text_header(_page1, _profile_title, _profile_desc), (0, 0))
        _profile_panel = ProfileEditPanel(_page1)
        _profile_panel.set_content(_profile_content, _profile_content_validator)
        _page1.add_widget('profile', _profile_panel, (1, 0))
        if _choice_content is not None:
            _page2 = ZWizardPage(_wz)
            _page2.add_widget('header', gui_util_get_simple_text_header(_page2, _choice_title, _choice_desc), (0, 0))
            _choice_panel = ChoiceEditPanel(_page2, label=_choice_label, use_bitmap=True)
            _choice_panel.set_content(_choice_content, _choice_validator)
            _page2.add_widget('choice', _choice_panel, (1, 0))
            _page1.nextPage = _page2
            _page2.previousPage = _page1
        else:
            _page2 = None

        _wz.GetPageAreaSizer().Add(_page1, 1, wx.EXPAND)
        if _wz.RunWizard(_page1):
            _ret = dict()
            _ret.update({'profile': _page1.get_widget('profile').get_content()})
            if _page2 is not None:
                _ret.update(_page2.get_widget('choice').get_content())
            _wz.Destroy()
            return True, _ret
        else:
            _wz.Destroy()
            return False, None

    def save_project(self):
        pass

    def add_node(self, role: EnumProjectItemRole):
        try:
            _cc: ProjectExplorerContentContainer = self._contentContainer
            _describable = _cc.check_flag_of_role_config(role, EnumProjectItemFlag.DESCRIBABLE)
            _parent = _cc.find_parent_node_by_child_role(role)
            _meta = dict()
            _name = EnumProjectItemRole(role).name.capitalize()
            if _describable:
                _wz_options = dict()
                _wz_options['title'] = 'New%sNode' % _name
                _wz_options['profile_content'] = {'name': 'New%s' % _name, 'description': 'description of %s' % _name}
                _has_choice = False
                _choice_update = lambda x: x
                if role == EnumProjectItemRole.BEHAVIOUR.value:
                    _has_choice = True
                    _app_ctx = self.root.appContext
                    _slt_mgr = _app_ctx.get_property('mbtSolutionManager')
                    _bmps = [x.get_icon() for x in _slt_mgr.solutions.values() if x.isValid]
                    _slts = {x.name: (x.uuid, x.type_) for x in _slt_mgr.solutions.values() if x.isValid}
                    _choice_update = lambda x: _slts[x]
                    _slt_descs = {v.name: v.description for v in _slt_mgr.solutions.values() if v.isValid}
                    _wz_options['choice_content'] = {'choices': list(_slts.keys()),
                                                     'bmps': _bmps,
                                                     'descriptions': _slt_descs}
                    _wz_options['choice_title'] = 'Select Solution'
                    _wz_options['choice_description'] = 'Select a solution from given list.'
                    _wz_options['choice_label'] = 'Solution:'
                _ret, _res = self._run_wizard_for_new_or_edit_node(**_wz_options)
                if _ret:
                    if _has_choice:
                        _slt_uid, _slt_typ = _choice_update(_res['selected'])
                        _res.update({'typeUri': 'type://solution?name={}?uid={}'.format(_slt_typ, _slt_uid)})
                        _res.pop('selected')
                    _res['profile'] = ProjectNodeProfile(**_res['profile'])
                    _res['role']=role
                    # todo: assigned icon
                    _res['icon']='role'
                    _meta = _res
                _cmd = CommandAppendNode(self, _parent.uuid, _meta, name='New%sNode' % _name)
                _ret = self.undoStack.Submit(_cmd)
                assert _ret, 'command not be executed successfully.'
        except Exception as e:
            FeedbackDialogs.show_msg_dialog(_('Error'), _('Can not add node.since:%s') % e,
                                            icon=wx.ICON_ERROR)

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
            _cmd = CommandAppendNode(self, _parent.uuid, _meta, name='PasteNode')
            _ret = self.undoStack.Submit(_cmd)
            assert _ret, 'command not be executed successfully.'
        except Exception as e:
            FeedbackDialogs.show_msg_dialog('Error', _('can not paste node.\n%s') % e,
                                            icon=wx.ICON_ERROR)
            self.log.error('can not execute paste node, since:\n%s' % e)

    def delete_node(self, node: ProjectTreeNode):
        try:
            _ret = FeedbackDialogs.show_yes_no_dialog(_('Delete'), _('Are you sure to delete?'))
            if _ret:
                _cmd = CommandRemoveNode(self, node, name='DeleteNode')
                _ret = self.undoStack.Submit(_cmd)
                assert _ret, 'command not be executed successfully.'
        except Exception as e:
            FeedbackDialogs.show_msg_dialog('Error', _('can not delete node.\n%s') % e, icon=wx.ICON_ERROR)
            self.log.error('can not execute delete node, since:\n%s' % e)

    def open_node(self, node: ProjectTreeNode):
        print('open_node node', node)

    def rename_node(self, node: ProjectTreeNode):
        print('rename_node node', node)

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

    # --------------------------------------------------------------
    # event handling
    # --------------------------------------------------------------
    def on_menu(self, evt: wx.ContextMenuEvent):
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
        elif _id == EnumProjectExplorerContextMenuIDs.RENAME:
            self.rename_node(_node)

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
        _cm_cfg = copy.deepcopy(self._contentContainer.get_project_node_cm_config(_node.role))
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
        self.view.enable_tools(_node.has_flag(EnumProjectItemFlag.CAN_EDIT_CONTENT), self.view.tbIdLinkEditor)
        # self.view.enable_tools(_node.has_flag(EnumProjectItemFlag.ORDERABLE),self.view.tbIdLinkEditor)
        EnumAppSignal.sigSupportedOperationChanged.send(self, op=self.get_node_sop(_node))
        _evt = self._T_NODE_SELECTED(self.view.GetId(), node=_node)
        wx.PostEvent(self.view, _evt)
        evt.Skip()

    def on_proj_item_activate(self, evt: wx.TreeEvent):
        _item = evt.GetItem()
        _view: TreeView = self.view.treeView
        _node: ProjectTreeNode = _view.item_to_node(_item)
        # todo: let root open node content editor. if has children collapse or expand it.
        if _node.children:
            _view.Toggle(_item)
            return
        # _view = self.view.treeView
        # _node = _view.item_to_node(_item)
        # if _node.children:
        #     if _view.IsExpanded(_item):
        #         _view.Collapse(_item)
        #     else:
        #         _view.Expand(_item)
        # if _node.fileAttr == EnumProjectNodeFileAttr.FOLDER:
        #     return
        # self.proj_edit_node(_node)

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
            # todo: must some node selected, get the node uid, find editor with this uid, then activate editor
            pass
        elif _id == self.view.tbIdSort:
            # todo: sort and change icon
            pass
