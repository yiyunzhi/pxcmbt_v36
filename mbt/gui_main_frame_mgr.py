# -*- coding: utf-8 -*-
import os.path
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : gui_main_frame_mgr.py
# ------------------------------------------------------------------------------
#
# File          : gui_main_frame_mgr.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import sys, wx, traceback, logging
import wx.lib.agw.aui as aui
import wx.lib.newevent as wxevt
from framework.application.define import _
from framework.gui.base.class_feedback_dialogs import FeedbackDialogs
from mbt import appCtx
from .application.class_application import MBTApplication
from .application.project import Project
from .application.define import (RECENT_MAX_LEN, APP_VERSION, APP_NAME, EnumAppSignal, T_EVT_APP_TOP_MENU)
from .application.log.class_logger import get_logger
from .gui.base import MBTViewManager, MBTContentContainer, MBTUniView
from .gui.navigation.define import EnumMFMenuIDs
from .gui.navigation.class_app_menubar_mgr import AppMenubarViewManager
from .gui.navigation.class_app_toolbar_mgr import AppToolbarViewManager
from .gui.base.class_pane_proj_expl_mgr import ProjectExplorerManager
from .gui.base.class_pane_console_mgr import ConsoleManager
from .gui.base.class_pane_prop_container_mgr import PropContainerManager
from .gui.base.class_pane_welcome_mgr import WelcomeManager
from .gui_main_frame import AppFrame
from .gui.prefs import MBTPreferenceMgr, PreferenceDialog

_log = get_logger('application')


class AppMainFrameViewManager(MBTViewManager):
    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)
        self.uid = '_root_'
        self._inUpdateUI = False
        if _log.getEffectiveLevel() != logging.DEBUG:
            sys.excepthook = self.except_hook
        self._viewTitle = '%s v%s' % (APP_NAME, APP_VERSION)
        self._fileHistory = wx.FileHistory(RECENT_MAX_LEN)
        self._appMenubarMgr = None
        self._appToolbarMgr = None
        self._appProjectExplMgr = None
        self._appPropContainerMgr = None
        self._appConsoleMgr = None
        self._welcomeMgr = None
        self.accelTable = []
        self.editorFactory = None
        self.currentPane = None
        # bind app signal
        EnumAppSignal.sigSupportedOperationChanged.connect(self.on_app_sig_supported_op_changed)

    @property
    def appContext(self):
        return appCtx

    @property
    def fileHistory(self):
        return self._fileHistory

    @property
    def windowsViewMenu(self):
        return self._appMenubarMgr.get_menu_item(_('&Window'), _('Views'))[0]

    def except_hook(self, etype, value, tb):
        """
        This except hook, when bound will catch all unhandled exceptions logging
        them to file and also creating a wx MessageDialog to notify the user of
        the error.
        """
        _message = '\nUncaught exception:\n'
        _message += ''.join(traceback.format_exception(etype, value, tb))
        _log.error(_message)
        if _log.getEffectiveLevel() == logging.DEBUG:
            _content = "{0!s}: {1!s}\n{2!s}".format(etype.__name__, value, _message)
        else:
            _content = "{0!s}: {1!s}".format(etype.__name__, value)
        _dlg = wx.MessageDialog(self._view, _content, "Unhandled exception", wx.OK | wx.ICON_ERROR)
        _dlg.ShowModal()
        _dlg.Destroy()

    def create_view(self, **kwargs):
        if self._view is not None:
            return self._view
        _view = AppFrame()
        self.post_view(_view)
        # _view.PushEventHandler(self) not necessary currently
        _cc = MBTApplication(appCtx)
        self.post_content_container(_cc)
        # --------------------------------------------------------------
        # create and append application toolbar
        # --------------------------------------------------------------
        _mb_view_mgr = AppMenubarViewManager(parent=self, uid='_appMenubar_')
        _mb_view_mgr.create_view()
        _view.SetMenuBar(_mb_view_mgr.view)
        self._appMenubarMgr = _mb_view_mgr
        # --------------------------------------------------------------
        # create and append application toolbar
        # --------------------------------------------------------------
        _tb_view_mgr = AppToolbarViewManager(parent=self, uid='_appToolbar_')
        _tb_view_mgr.create_view(parent=_view)
        _view.add_toolbar(_tb_view_mgr.view)
        self._appToolbarMgr = _tb_view_mgr
        # --------------------------------------------------------------
        # create and append project explorer pane
        # --------------------------------------------------------------
        _proj_expl = ProjectExplorerManager(parent=self, uid='_appProjectExplorer_', view_title=_('ProjectExplorer'))
        _proj_expl.create_view(parent=_view)
        _proj_expl_pane_info = aui.AuiPaneInfo().Name(_proj_expl.uid). \
            Caption(_proj_expl.viewTitle). \
            Left().Layer(1).Position(0).BestSize((240, -1)).MinSize((160, 360)). \
            CloseButton(False).MaximizeButton(False). \
            MinimizeButton(True)
        _view.add_pane(_proj_expl.view, _proj_expl_pane_info, False)
        self._appProjectExplMgr = _proj_expl
        # --------------------------------------------------------------
        # create and append console pane
        # --------------------------------------------------------------
        _console = ConsoleManager(parent=self, uid='_appConsole_', view_title=_('Console'))
        _console.create_view(parent=_view)
        _console_pane_info = aui.AuiPaneInfo().Name(_console.uid). \
            Caption(_console.viewTitle). \
            Bottom().BestSize((-1, 150)).MinSize((-1, 120)).Floatable(False).FloatingSize((500, 160)). \
            CloseButton(False).MaximizeButton(True). \
            MinimizeButton(True)
        _view.add_pane(_console.view, _console_pane_info, False)
        self._appConsoleMgr = _console
        # --------------------------------------------------------------
        # create and append prop container
        # --------------------------------------------------------------
        _prop = PropContainerManager(parent=self, uid='_appPropContainer_', view_title=_('Properties'))
        _prop.create_view(parent=_view)
        _prop_pane_info = aui.AuiPaneInfo().Name(_prop.uid). \
            Caption(_prop.viewTitle). \
            Left().Layer(1).Position(0).BestSize((240, 240)). \
            CloseButton(False).MaximizeButton(False). \
            MinimizeButton(True)
        _view.add_pane(_prop.view, _prop_pane_info, False)
        self._appPropContainerMgr = _prop
        # --------------------------------------------------------------
        # create and append welcome pane in center
        # --------------------------------------------------------------
        _welcome = WelcomeManager(parent=self, uid='_welcome_', view_title=_('Welcome'),
                                  view_allow_toggle_with_menu=True)
        _welcome.create_view(parent=_view)
        _welcome.toggle_view(True, _view.centerPane)
        self._welcomeMgr = _welcome
        # --------------------------------------------------------------
        # refresh layout
        # --------------------------------------------------------------
        _view.refresh()
        self._bind_event()
        self._create_acc_table()
        _view.centerPane.SetFocus()
        _view.centerPane.SetSelectionToWindow(_welcome.view)
        wx.UpdateUIEvent.SetUpdateInterval(75)
        self.view.UpdateWindowUI()
        self.send_sop()
        # todo: load default perspective
        _console.write(_('App Started'))
        return self._view

    def _bind_event(self):
        # use self.Bind(wx.EVT_MENU,self.on_menu) not works, since the menubar is belongs to view.
        self.view.Bind(wx.EVT_MENU, self.on_menu)
        self.view.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_center_pane_pg_changed)
        self.view.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_center_pane_pg_close)
        # self.view.Bind(aui.EVT_AUI_PANE_MIN_RESTORE, self.on_pane_restore_min)
        # self.view.Bind(aui.EVT_AUI_PANE_MINIMIZE, self.on_pane_min)
        self.view.Bind(wx.EVT_CLOSE, self.on_window_closed)
        # self.Bind(wx.EVT_CHILD_FOCUS, self.on_child_focused)
        self.view.Bind(aui.EVT_AUI_PANE_ACTIVATED, self.on_pane_activated)
        self.view.Bind(self._appProjectExplMgr.EVT_NODE_SELECTED, self.on_project_node_selected)
        self.view.Bind(self._appProjectExplMgr.EVT_PROJECT_CREATED, self.on_project_created)
        self.view.Bind(self._appProjectExplMgr.EVT_PROJECT_OPENED, self.on_project_opened)
        self.view.Bind(self._appProjectExplMgr.EVT_NODE_DELETED, self.on_project_node_deleted)
        self.view.Bind(wx.EVT_UPDATE_UI, self.on_spec_id_ui_updated, id=wx.ID_UNDO)
        self.view.Bind(wx.EVT_UPDATE_UI, self.on_spec_id_ui_updated, id=wx.ID_REDO)
        self.view.Bind(wx.EVT_UPDATE_UI, self.on_spec_id_ui_updated, id=wx.ID_SAVE)
        self.view.Bind(wx.EVT_UPDATE_UI, self.on_spec_id_ui_updated, id=EnumMFMenuIDs.SAVE_ALL)
        self.view.Bind(wx.EVT_UPDATE_UI, self.on_spec_id_ui_updated, id=wx.ID_SAVEAS)
        self.view.Bind(wx.EVT_UPDATE_UI, self.on_spec_id_ui_updated, id=EnumMFMenuIDs.VIEW_SHOW_PROJ_PROPS)
        self.view.Bind(wx.EVT_UPDATE_UI, self.on_spec_id_ui_updated, id=EnumMFMenuIDs.VIEW_SHOW_PROJ_IN_EXPLORER)
        self.view.Bind(wx.EVT_UPDATE_UI, self.on_spec_id_ui_updated, id=EnumMFMenuIDs.VIEW_CLOSE_EDITOR)
        self.view.Bind(wx.EVT_UPDATE_UI, self.on_spec_id_ui_updated, id=EnumMFMenuIDs.VIEW_CLOSE_ALL_EDITOR)

    def _create_acc_table(self):
        # set the acceleratorTable
        self.accelTable = [
            # ('Save', wx.ACCEL_CTRL, ord('S'), wx.ID_SAVE),
            # ('Copy', wx.ACCEL_CTRL, ord('C'), wx.ID_COPY),
            # ('Cut', wx.ACCEL_CTRL, ord('X'), wx.ID_CUT),
            # ('Paste', wx.ACCEL_CTRL, ord('V'), wx.ID_PASTE),
            # ('About', wx.ACCEL_SHIFT, ord('A'), wx.ID_ABOUT),
            # ('SelectAll', wx.ACCEL_CTRL, ord('A'), wx.ID_SELECTALL),
            # ('Delete', wx.ACCEL_NORMAL, wx.WXK_DELETE, wx.ID_DELETE),
            # ('Undo', wx.ACCEL_CTRL, wx.WXK_CONTROL_Z, wx.ID_UNDO),
            # ('Redo', wx.ACCEL_CTRL, wx.WXK_CONTROL_Y, wx.ID_REDO),
        ]
        self.view.SetAcceleratorTable(wx.AcceleratorTable([x[1::] for x in self.accelTable]))

    def send_sop(self):
        EnumAppSignal.sigSupportedOperationChanged.send(self, op={wx.ID_COPY: False,
                                                                  wx.ID_CUT: False,
                                                                  wx.ID_PASTE: False,
                                                                  wx.ID_DELETE: False})

    def load_default_perspective(self):
        pass

    @staticmethod
    def find_window_parent_by_type(win: wx.Window, parent_type: type):
        _parent = win.GetParent()
        while _parent:
            if isinstance(_parent, parent_type):
                break
            _parent = _parent.GetParent()
        return _parent if isinstance(_parent, parent_type) else None

    def get_recent_project_info(self):
        _app = wx.App.GetInstance()
        self._fileHistory.Load(_app.systemConfig)
        return [self._fileHistory.GetHistoryFile(i) for i in range(self._fileHistory.GetCount())]

    def set_recent_project_info(self, name: str, path: str):
        _app = wx.App.GetInstance()
        self._fileHistory.AddFileToHistory(path)
        self._fileHistory.Save(_app.systemConfig)
        _app.systemConfig.Flush()

    def set_menubar_menu_state(self, menu_id, state=True):
        if menu_id is None:
            return
        if self._appMenubarMgr.get_state(menu_id) != state:
            self._appMenubarMgr.set_state(menu_id, state)

    def set_toolbar_tool_state(self, tool_id, state=True):
        if tool_id is None:
            return
        if self._appToolbarMgr.get_state(tool_id) != state:
            self._appToolbarMgr.set_state(tool_id, state)

    def install_undo_stack(self, undo_stack: wx.CommandProcessor):
        _menu: wx.Menu = self._appMenubarMgr.undoRedoMenu
        undo_stack.SetEditMenu(_menu)
        undo_stack.SetMenuStrings()

    def uninstall_undo_stack(self, undo_stack: wx.CommandProcessor):
        _menu: wx.Menu = self._appMenubarMgr.undoRedoMenu
        _i1, _p = _menu.FindChildItem(wx.ID_UNDO)
        _i2, _p = _menu.FindChildItem(wx.ID_REDO)
        _i1.SetItemLabel(_('Undo'))
        _i2.SetItemLabel(_('Redo'))
        _i1.Enable(False)
        _i2.Enable(False)
        undo_stack.SetEditMenu(None)

    # --------------------------------------------------------------
    # event handling
    # --------------------------------------------------------------
    def on_spec_id_ui_updated(self, evt: wx.UpdateUIEvent):
        # Recursive call protection
        if self._inUpdateUI: return
        if self.currentPane is None:
            _can_undo = self.undoStack.CanUndo()
            _can_redo = self.undoStack.CanRedo()
        else:
            _can_undo = self.currentPane.manager.undoStack.CanUndo()
            _can_redo = self.currentPane.manager.undoStack.CanRedo()
        self._inUpdateUI = True
        _id = evt.GetId()
        _evt_obj = evt.GetEventObject()
        if _evt_obj is self._appToolbarMgr.view:
            # undo redo which in menubar located is managed by undoStack, the
            # undo redo in toolbar is wild, must be use updateUiEvent updated.
            _toolbar_update_required = False
            if _id == wx.ID_UNDO:
                _act_state = self._appToolbarMgr.get_state(_id)
                if _can_undo != _act_state:
                    evt.Enable(_can_undo)
                    _toolbar_update_required |= True
            elif _id == wx.ID_REDO:
                _act_state = self._appToolbarMgr.get_state(_id)
                if _can_redo != _act_state:
                    evt.Enable(_can_redo)
                    _toolbar_update_required |= True
            if _toolbar_update_required:
                self._appToolbarMgr.view.Refresh()
        if _id in [wx.ID_SAVE,
                   wx.ID_SAVEAS,
                   EnumMFMenuIDs.SAVE_ALL,
                   EnumMFMenuIDs.VIEW_SHOW_PROJ_PROPS,
                   EnumMFMenuIDs.VIEW_SHOW_PROJ_IN_EXPLORER,
                   EnumMFMenuIDs.VIEW_CLOSE_EDITOR,
                   EnumMFMenuIDs.VIEW_CLOSE_ALL_EDITOR]:
            evt.Enable(self._appProjectExplMgr.contentContainer.project is not None)
        self._inUpdateUI = False

    def on_project_node_deleted(self, evt: wx.CommandEvent):
        _uid = evt.uid
        print('on_project_node_deleted->', _uid)

    def on_project_node_selected(self, evt: wx.CommandEvent):
        print('on_project_node_selected->', evt.node)
        _node = evt.node
        if _node is None:
            return
        _node_desc = _node.description
        _status_bar = self.view.set_status_bar_text(_node_desc)
        # todo: show property
        # _view = self.view.treeView
        # if _item.IsOk():
        #     _node = _view.item_to_node(_item)
        #     self.GetStatusBar().SetStatusText(_node.description)
        #     _prop_panel = ProjectItemPropsContentPanel(self._propContainerPane)
        #     _prop_panel.set_item(_node)
        #     self._propContainerPane.set_content(_prop_panel)

    def on_app_sig_supported_op_changed(self, sender, op: dict):
        for id_, state in op.items():
            self.set_menubar_menu_state(id_, state)
            self.set_toolbar_tool_state(id_, state)
        self._appToolbarMgr.view.Refresh()

    def on_pane_activated(self, evt: aui.AuiManagerEvent):
        _pane = evt.GetPane()
        if _pane is self.view.centerPane:
            # todo: check if currentPane is page of this notebook
            pass
        else:
            if not isinstance(_pane, MBTUniView):
                if self.currentPane is not None:
                    self.uninstall_undo_stack(self.currentPane.manager.undoStack)
                self.currentPane = None
                return
            elif _pane is not self.currentPane:
                if self.currentPane is not None:
                    self.uninstall_undo_stack(self.currentPane.manager.undoStack)
                self.install_undo_stack(_pane.manager.undoStack)
                self.currentPane = _pane

    def on_project_opened(self, event):
        print('---------->on project opened:', event)
        _project: Project = event.project
        self._appConsoleMgr.write('project %s opened from %s' % (_project.name, _project.projectPath))
        self.view.update_title_with_project_name(_project.name)
        self.set_recent_project_info(_project.name, _project.projectPath)
        self.view.refresh()

    def on_project_created(self, event):
        _project: Project = event.project
        self.set_recent_project_info(_project.name, _project.projectPath)
        self.view.update_title_with_project_name(_project.name)
        self._appConsoleMgr.write('project %s created at %s' % (_project.name, _project.projectPath))
        self.view.refresh()

    def on_menu(self, evt: wx.CommandEvent):
        _log.debug('mainFrameReceivedMenuEvent: %s,%s' % (evt, evt.GetEventObject()))
        _id = evt.GetId()
        if _id == wx.ID_HELP:
            self.view.on_help(evt)
        if _id == wx.ID_ABOUT:
            self.view.on_about(evt)
        elif _id == wx.ID_EXIT:
            self.view.on_exit(evt)
        elif _id == EnumMFMenuIDs.NEW_PROJ:
            self._appProjectExplMgr.create_project()
        elif _id == wx.ID_OPEN:
            self._appProjectExplMgr.open_project(evt)
        elif _id == wx.ID_UNDO:
            if self.currentPane is not None:
                _undo_cmd = self.currentPane.manager.undoStack.GetCurrentCommand()
                if FeedbackDialogs.show_yes_no_dialog(_('Undo'), _('are you sure UNDO %s') % _undo_cmd.GetName()):
                    self.currentPane.manager.undoStack.Undo()
        elif _id == wx.ID_REDO:
            if self.currentPane is not None:
                _redo_cmd = self.currentPane.manager.undoStack.GetCurrentCommand()
                if FeedbackDialogs.show_yes_no_dialog(_('Redo'), _('are you sure REDO %s') % _redo_cmd.GetName()):
                    self.currentPane.manager.undoStack.Redo()
        elif _id == EnumMFMenuIDs.TOOL_PREFERENCE.value:
            _mgr: MBTPreferenceMgr = MBTPreferenceMgr()
            # send global event: AppPreferenceAboutToShow
            EnumAppSignal.sigAppPreferenceAboutToShow.send(_mgr)
            _dlg = PreferenceDialog(_mgr, parent=self.view)
            _dlg.SetSize(wx.Size(640, 640))
            _dlg.Center()
            _dlg.ShowModal()
        else:
            if self.currentPane is not None:
                _hd: wx.EvtHandler = self.currentPane.GetEventHandler()
                _hd.ProcessEvent(T_EVT_APP_TOP_MENU(_id))
            # consider the situation of view toggle menu ids
            _mgrs = self.find_all(self, lambda x: x.viewAllowToggleWithMenu)
            for x in _mgrs:
                _act = x.get_view_toggle_action()
                if _act is None:
                    continue
                if _act.GetId() == _id:
                    x.toggle_view(evt.IsChecked())
        evt.Skip()

    def on_preference_changed(self, evt: wxevt.NewCommandEvent):
        _attrs = ['container', 'name', 'items']
        _check = all([hasattr(evt, x) for x in _attrs])
        if not _check:
            return
        _app = wx.App.GetInstance()
        _container = getattr(evt, 'container')
        _name = getattr(evt, 'name')
        _items = getattr(evt, 'items')
        _more_op_required = list()
        if _container is _app.appConfigMgr:
            # todo: more if statement for preference changing
            if _name == 'i18n':
                if '/language' in _items:
                    _more_op_required.append(_('language setting requires app a restart.'))
        if _more_op_required:
            wx.CallLater(300, FeedbackDialogs.show_msg_dialog, _('Info'), '\n'.join(_more_op_required))
        EnumAppSignal.sigAppPreferenceApplied.send(self, container=_container, name=_name, items=_items)

    def on_center_pane_pg_changed(self, evt):
        _log.debug('-->on_center_pane_pg_changed')

    def on_center_pane_pg_close(self, evt: aui.AuiNotebookEvent):
        # todo: info projectExpl...
        _pg_idx = evt.GetSelection()
        if _pg_idx == -1:
            return
        _pg = self.view.centerPane.GetPage(_pg_idx)
        _pg.manager.toggle_view(False, self.view.centerPane)
        evt.Veto()

    def on_window_closed(self, evt):
        # self._process_unsaved()
        self.view.PopEventHandler()
        evt.Skip()
