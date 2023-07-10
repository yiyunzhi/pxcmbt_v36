import subprocess, logging, copy
import sys, os, traceback
import anytree.iterators
import wx
import wx.lib.agw.aui as aui
import wx.lib.sized_controls as wxsc
import application.global_vars as gv
from wx.lib.agw import pybusyinfo as pbi
from pubsub import pub
from application.define import (EnumProjectItemRole,
                                EnumAppMsg,
                                EnumProjectItemFlag,
                                EnumEditorFlag,
                                EnumProjectNodeFileAttr,
                                APP_NAME,
                                APP_VERSION,
                                APP_PROJECT_PATH,
                                EnumBuiltinPaneInfo,
                                EnumConsoleItemFlag,
                                MB_ATTACH_LABEL_REGEX)

from application.log.class_logger import get_logger
from application.class_application_config import APP_CONFIG
from application.class_application import Application
from application.utils_helper import util_is_dir_exist
from application.io.class_base import AppFileIOBody
from application.class_ipod_engine import IPOD_ENGINE_MGR
from application.class_config_importer import MenuNodeDef
from gui.utils.util_icon_repo import UtilIconRepo16x16
from gui.core.assets_images import *
from gui.core.define_gui import (_,
                                 ID_MF_MENU_NEW_FILE,
                                 ID_MF_MENU_NEW_PROJ)
from gui.core.class_base import MBTAuiToolbarContentPaneMixin, MakeMenuMixin
from gui.editor.editor_base import BaseEditor, ProjectNodeEditor
from gui.widgets.dialog_new_project import NewProjectDialog
# from gui.widgets.dialog_new_model import NewModelDialog
# from gui.requirements_mgr.dialog_new_repo_item import NewRepoDialog
# from gui.ipod.dialog_new_feature_impl import NewFeatureImplDialog
from gui.widgets.panel_project_manager import ProjectManagerPanel
from gui.widgets.panel_props_container import PropContainerPanel, ProjectItemPropsContentPanel
from gui.widgets.panel_console import ConsolePanel
from gui.widgets.dialog_content_panel import ContentPanelDialog
from gui.widgets.panel_general_name_desc import GeneralInfoEditorPanel
from gui.widgets.panel_os_stat_result import OSStatInfoPanel
from gui.widgets.panel_welcome import WelcomePanel
from .frame_lib import LibraryFrame

# from gui.ipod.panel_ipod_library_editor import IPODLibraryEditorPanel
# from gui.flow.panel_flow_editor import FlowEditorPanel
# from gui.tc.dialog_create_tc_wiz import CreateTCItemDialog
# from gui.define_event_editor.panel_event_define_editor import EventDefineEditorPanel

_log = get_logger('application')


class AppFrame(wx.Frame, MakeMenuMixin):

    def __init__(self, parent, wx_id=wx.ID_ANY, title='', pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER):
        sys.excepthook = self.except_hook
        super(AppFrame, self).__init__(parent, wx_id, title, pos, size, style)
        # self.SetBackgroundStyle(wx.BG_STYLE_ERASE)
        self._auiMgr = aui.AuiManager(agwFlags=aui.AUI_MGR_DEFAULT |
                                               aui.AUI_MGR_ALLOW_ACTIVE_PANE)
        # tell AuiManager to manage this frame
        self._auiMgr.SetManagedWindow(self)
        self.frameTitle = '%s v%s' % (APP_NAME, APP_VERSION)
        self.SetTitle(self.frameTitle)
        self._icon_size = (16, 16)
        self._paneTbs = dict()
        self._editorMap = dict()
        self.iconRepo = UtilIconRepo16x16()
        self.fileHistory = wx.FileHistory(3)
        self.fileHistory.Load(gv.GLOBAL_CONFIG)
        self.sizerTimer = wx.Timer(self)
        # set up center pane aui info
        # self._centerTargetAuiInfo = aui.AuiPaneInfo().BestSize((600, 600)). \
        #     DestroyOnClose(True).Centre().Snappable().Dockable(). \
        #     MinimizeButton(True).MaximizeButton(True).Floatable(False)

        # Attributes
        self._toolbar = None
        self._propsPaneCaptionFmt = "%s Properties"
        self._currentPropPane = None
        self._textCount = 1
        self._transparency = 255
        self._snapped = False
        self._customPaneButtons = False
        self._customTabButtons = False
        self._paneIcons = False
        self._vetoTree = self._veto_text = False

        # set frame icon
        self.SetIcon(Mondrian.GetIcon())
        self.CreateStatusBar()
        self.GetStatusBar().SetStatusText("Ready")
        self.create_acc_table()
        self.create_menu_bar()
        self.create_tool_bar()
        self.build_panes()
        self.bind_event()
        self.config_editor_map()
        self.Fit()
        self.SetSize((720, 640))
        self.Center()
        self._consolePane.write('App started.')
        wx.CallAfter(self.SendSizeEvent)

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
        _dlg = wx.MessageDialog(self, _content, "Unhandled exception", wx.OK | wx.ICON_ERROR)
        _dlg.ShowModal()
        _dlg.Destroy()

    def create_acc_table(self):

        # set the acceleratorTable
        _id_ctrl_s = wx.NewId()

        self.Bind(wx.EVT_MENU, self.on_ctrl_s_pressed, id=_id_ctrl_s)

        _accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, wx.WXK_CONTROL_S, _id_ctrl_s)
        ])
        self.SetAcceleratorTable(_accel_tbl)

    def create_menu_bar(self):
        # create menu
        _mb = wx.MenuBar()
        _file_new_project_id = ID_MF_MENU_NEW_PROJ
        _file_new_file_id = ID_MF_MENU_NEW_FILE
        _file_menu = wx.Menu()
        _file_new_sub_menu = wx.Menu()
        _recent_menu = wx.Menu()
        self.fileHistory.UseMenu(_recent_menu)
        self.fileHistory.AddFilesToMenu()

        _new_project_id = _file_new_sub_menu.Append(_file_new_project_id, _('NewProject'))
        _new_file_id = _file_new_sub_menu.Append(_file_new_file_id, _('NewFile'))
        _file_menu.AppendSubMenu(_file_new_sub_menu, 'New')
        _file_menu.Append(wx.ID_OPEN, _('Open'))
        _file_menu.Append(wx.ID_SAVE, _('Save'))
        _file_menu.Append(wx.ID_SAVEAS, _('Save As'))
        _file_menu.AppendSeparator()
        _file_menu.Append(wx.ID_ANY, "&Recent Fiels", _recent_menu)
        _file_menu.AppendSeparator()
        _file_menu.Append(wx.ID_EXIT, _('Exit'))
        self.Bind(wx.EVT_MENU, self.on_menu_new_project_clicked, _new_project_id)
        self.Bind(wx.EVT_MENU, self.on_menu_new_file_clicked, _new_file_id)
        self.Bind(wx.EVT_MENU_RANGE, self.on_file_history_item_clicked, id=wx.ID_FILE1, id2=wx.ID_FILE3)
        _view_menu = wx.Menu()
        # _view_in_tab_id = wx.NewIdRef()
        # _view_menu.Append(_view_in_tab_id, 'Tab')
        # self.Bind(wx.EVT_MENU, self.on_menu_view_in_tab_layout, _view_in_tab_id)
        # _view_menu.AppendSeparator()
        _view_proj_loc_id = wx.NewIdRef()
        _view_op_proj_prop_id = wx.NewIdRef()
        _view_menu.Append(_view_proj_loc_id, 'ShowProjectInExplorer')
        _view_menu.Append(_view_op_proj_prop_id, 'ShowProjectProperty')
        self.Bind(wx.EVT_MENU, self.on_menu_v_open_proj_in_explr, _view_proj_loc_id)
        self.Bind(wx.EVT_MENU, self.on_menu_v_proj_info, _view_op_proj_prop_id)

        _tools_menu = wx.Menu()
        _tool_dcp_id = wx.NewIdRef()
        _tool_boot_id = wx.NewIdRef()
        _tool_discovery_menu = wx.Menu()
        _tool_discovery_menu.Append(_tool_dcp_id, 'DCP')
        _tool_discovery_menu.Append(_tool_boot_id, 'BootP')
        _tools_menu.AppendSubMenu(_tool_discovery_menu, 'DiscoveryTools')
        self.Bind(wx.EVT_MENU, self.on_menu_tool_dcp, _tool_dcp_id)
        self.Bind(wx.EVT_MENU, self.on_menu_tool_bootp, _tool_boot_id)
        _window_menu = wx.Menu()
        _win_save_ly_id = wx.NewIdRef()
        _win_rst_ly_id = wx.NewIdRef()
        _window_menu.Append(_win_save_ly_id, 'SaveCurrentLayout')
        _window_menu.Append(_win_rst_ly_id, 'RestoreDefaultLayout')
        self.Bind(wx.EVT_MENU, self.on_menu_win_save_persp, _win_save_ly_id)
        self.Bind(wx.EVT_MENU, self.on_menu_win_restore_default_persp, _win_rst_ly_id)

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, _('About...'))

        _mb.Append(_file_menu, "&File")
        _mb.Append(_view_menu, "&View")
        _mb.Append(_tools_menu, "&Tool")
        _mb.Append(_window_menu, "&Window")
        _mb.Append(help_menu, "&Help")
        self.SetMenuBar(_mb)

    def create_tool_bar(self):
        _tb_icon_size = wx.Size(16, 16)
        _img_lst = self.iconRepo.get_image_list()
        _tb = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)
        _tb.SetToolBitmapSize(_tb_icon_size)
        _new_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, _tb_icon_size)
        _open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, _tb_icon_size)
        _save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, _tb_icon_size)
        _save_as_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, _tb_icon_size)
        _copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, _tb_icon_size)
        _paste_bmp = wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, _tb_icon_size)
        _lib_bmp = self.iconRepo.get_bmp(self.iconRepo.libIcon)

        _new_id = wx.NewIdRef()
        _new_project_id = wx.NewIdRef()
        _new_file_id = wx.NewIdRef()
        _open_id = wx.NewIdRef()
        _save_id = wx.NewIdRef()
        _save_as_id = wx.NewIdRef()
        _lib_id = wx.NewIdRef()

        # self._tbIdMap.update({EnumTBKeys.TB_NEW: _new_id})
        # self._tbIdMap.update({EnumTBKeys.TB_NEW_PROJECT: _new_project_id})
        # self._tbIdMap.update({EnumTBKeys.TB_NEW_FILE: _new_file_id})
        # self._tbIdMap.update({EnumTBKeys.TB_OPEN: _open_id})
        # self._tbIdMap.update({EnumTBKeys.TB_SAVE: _save_id})
        # self._tbIdMap.update({EnumTBKeys.TB_SAVE_AS: _save_as_id})

        _tb.AddSimpleTool(_new_id, 'NewProject', _new_bmp, 'NewProject')
        _tb.AddSimpleTool(_open_id, 'OpenProject', _open_bmp, 'OpenProject')
        _tb.AddSimpleTool(_save_id, 'SaveProject', _save_bmp, 'SaveProject')
        _tb.AddSimpleTool(_save_as_id, 'SaveProjectAs', _save_as_bmp, 'SaveProjectAs')
        _tb.AddSeparator()
        _tb.AddSimpleTool(_lib_id, 'BuiltinBlocks', _lib_bmp, 'BuiltinBlocks')
        _tb.SetToolDropDown(_new_id, True)
        _tb.Realize()
        self.Bind(aui.EVT_AUITOOLBAR_TOOL_DROPDOWN, self.on_tb_new_drop_down, id=_new_id)
        self.Bind(wx.EVT_TOOL, self.on_tb_save, _save_id)
        self.Bind(wx.EVT_TOOL, self.on_tb_save_as, _save_as_id)
        self.Bind(wx.EVT_TOOL, self.on_tb_new_project_clicked, _new_project_id)
        self.Bind(wx.EVT_TOOL, self.on_tb_new_file_clicked, _new_file_id)
        self.Bind(wx.EVT_TOOL, self.on_tb_open_clicked, _open_id)
        self.Bind(wx.EVT_TOOL, self.on_tb_open_lib_frame, _lib_id)
        # _tb.EnableTool(_play_id, False)
        self._toolbar = _tb
        self._auiMgr.AddPane(_tb, aui.AuiPaneInfo().Name("AppTool").Caption("App Tools").
                             ToolbarPane().Top().Layer(1).Position(0).BestSize((-1, 24)))
        self._auiMgr.Update()

    def build_panes(self):
        self._panelProjectMgr = ProjectManagerPanel(self)
        self._auiMgr.AddPane(self._panelProjectMgr,
                             aui.AuiPaneInfo().Name(EnumBuiltinPaneInfo.PANE_PROJECT_EXPLR_NAME).
                             Caption(EnumBuiltinPaneInfo.PANE_PROJECT_EXPLR_CAPTION).
                             Left().Layer(1).Position(0).BestSize((240, -1)).MinSize((160, 360)).
                             CloseButton(False).MaximizeButton(False).
                             MinimizeButton(True))

        self._propContainerPane = PropContainerPanel(parent=self)
        self._auiMgr.AddPane(self._propContainerPane,
                             aui.AuiPaneInfo().Name(EnumBuiltinPaneInfo.PANE_PROP_NAME).
                             Caption(EnumBuiltinPaneInfo.PANE_PROP_CAPTION).
                             Left().Layer(1).Position(0).BestSize((240, 240)).
                             CloseButton(False).MaximizeButton(False).
                             MinimizeButton(True))
        self._consolePane = ConsolePanel(parent=self)
        self._auiMgr.AddPane(self._consolePane, aui.AuiPaneInfo().Name(EnumBuiltinPaneInfo.PANE_CONSOLE_NAME).
                             Caption(EnumBuiltinPaneInfo.PANE_CONSOLE_CAPTION).
                             Bottom().BestSize((-1, 150)).MinSize((-1, 120)).Floatable(False).FloatingSize((500, 160)).
                             CloseButton(False).MaximizeButton(True).
                             MinimizeButton(True))
        _wp = WelcomePanel(self)
        self._auiMgr.AddPane(_wp, aui.AuiPaneInfo().
                             Name("_CNB_").Caption("Welcome").DockFixed(True).FloatingSize((500, 160)).MinSize((240, 240)).
                             Center().MinimizeButton(True).CloseButton(False))

        self._auiMgr.Update()

    def bind_event(self):
        # bind general event
        self.Bind(wx.EVT_TIMER, self.on_size_time_up)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_CLOSE, self.on_window_closed)
        self.Bind(wx.EVT_CHILD_FOCUS, self.on_child_focused)
        self.Bind(aui.EVT_AUI_PANE_ACTIVATED, self.on_aui_pane_activated)
        # self.Bind(aui.EVT_AUI_PANE_BUTTON, self.on_aui_pane_button)
        self.Bind(aui.EVT_AUI_PANE_CLOSED, self.on_aui_pane_closed)
        self.Bind(aui.EVT_AUI_PANE_CLOSE, self.on_aui_pane_close)
        self.Bind(wx.EVT_KILL_FOCUS, self.on_child_kill_focused)
        # bind menu event
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.Bind(wx.EVT_MENU, self.on_menu_save_clicked, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.on_menu_open_clicked, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.on_menu_save_as_clicked, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)
        # bind project mgr event
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_proj_item_select_changed, self._panelProjectMgr.treeView)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_proj_item_activate, self._panelProjectMgr.treeView)
        self.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.on_proj_item_get_tooltip, self._panelProjectMgr.treeView)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_proj_item_context_menu, self._panelProjectMgr.treeView)
        self.Bind(wx.EVT_IDLE, self.on_idle)
        # bind event update UI, multi allowed
        pub.subscribe(self.on_ext_sig_topic_project, 'project')
        pub.subscribe(self.on_ext_sig_topic_os, 'os')
        pub.subscribe(self.on_ext_sig_topic_console, 'console')
        pub.subscribe(self.on_ext_sig_close_node_editor, EnumAppMsg.sigViewCloseNodeEditor)
        pub.subscribe(self.on_ext_sig_project_node_profile_changed, EnumAppMsg.sigProjectNodeProfileChanged)
        pub.subscribe(self.on_ext_sig_put_msg_in_console, EnumAppMsg.sigPutMsgInConsole)
        # pub.subscribe(self.on_ext_sig_canvas_node_show_props, EnumAppSignals.sigV2VCanvasNodeShowProps.value)
        # pub.subscribe(self.on_ext_sig_lib_removed, EnumAppSignals.sigV2VLibRemoved.value)

    def on_menu_v_open_proj_in_explr(self, evt):
        _project = self.get_project()
        if _project is not None:
            gv.MAIN_APP.open_path_in_explorer(_project.projectPath)

    def on_menu_v_proj_info(self, evt):
        _proj = self.get_project()
        if _proj is None:
            return
        _dlg = wxsc.SizedDialog(self, wx.ID_ANY,
                                title='ProjectInfo',
                                name='ProjectInfo',
                                style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        _dlg_pane = _dlg.GetContentsPane()
        _olv = OSStatInfoPanel(_dlg_pane)
        _olv.SetSizerProps(expand=True, proportion=1)
        _olv.set_content(_proj.projectPath)
        _dlg.Center()
        _dlg.ShowModal()
        _dlg.Destroy()

    def on_menu_tool_dcp(self, evt):
        wx.MessageBox('todo: open DCP Panel')

    def on_menu_tool_bootp(self, evt):
        wx.MessageBox('todo: open BootP Panel')
        pass

    def on_menu_win_save_persp(self, evt):
        _proj = self.get_project()
        if _proj is None:
            return
        _main_perspective = self._auiMgr.SavePerspective()
        _proj.save_perspective(_main_perspective)

    def on_menu_win_restore_default_persp(self, evt):
        if gv.MAIN_APP is None:
            return
        try:
            _main_persp = gv.MAIN_APP.load_default_perspective()
            self._auiMgr.LoadPerspective(_main_persp)
            _proj = self.get_project()
            if _proj is None:
                return
            _proj.save_perspective(_main_persp)
        except Exception as e:
            wx.MessageBox('can not restore the default perspective, since:\n%s' % e)

    def config_editor_map(self):
        _map = APP_CONFIG.scAppEditorMapCfg
        for k, v in _map.items():
            _vm, _vc = v
            exec('from %s import %s' % (_vm, _vc))
            self._editorMap.update({k: locals().get(_vc)})
        for x in IPOD_ENGINE_MGR.engines:
            self._editorMap.update(x.get_editor_map())

    def _update_title_with_project_name(self, name):
        self.SetTitle(self.frameTitle + ' [CurrentProject: %s]' % name)

    def _set_text_to_clipboard(self, text):
        _clip_data = wx.TextDataObject()
        _clip_data.SetText(text)
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(_clip_data)
        wx.TheClipboard.Close()
        wx.MessageBox('write text in clipboard successful!')

    def _show_dialog_gather_name_desc(self, name, description, title, cb_validate):
        _dlg = ContentPanelDialog(self, title=title)
        _dlg.set_content_panel(GeneralInfoEditorPanel)
        _dlg.contentPanel.set_content(name=name, description=description)
        _dlg.Fit()
        _dlg.Center()
        _ret = _dlg.ShowModal()
        if _ret == wx.ID_OK:
            _name = _dlg.contentPanel.get_name()
            _desc = _dlg.contentPanel.get_description()
            if not cb_validate(_name):
                wx.MessageBox('invalid name "%s", please correct.' % _name)
                _dlg.Destroy()
                self._show_dialog_gather_name_desc(_name, _desc, title, cb_validate)
            else:
                return True, _name, _desc
        else:
            return False, name, description

    def _loading_project_node_content(self, app):
        _proj_root = app.project.projectTreeModel.p_root
        _descendants = _proj_root.descendants
        _max = len(_descendants)
        _count = 0
        _dlg = wx.ProgressDialog("Loading ProjectContent",
                                 "Loading ProjectContent",
                                 maximum=_max,
                                 parent=self,
                                 style=0 | wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
                                 # | wx.PD_CAN_ABORT
                                 # | wx.PD_CAN_SKIP
                                 # | wx.PD_ELAPSED_TIME
                                 # | wx.PD_ESTIMATED_TIME
                                 # | wx.PD_REMAINING_TIME
                                 # | wx.PD_AUTO_HIDE
                                 )
        for x in _descendants:
            _count += 1
            _dlg.Update(_count, 'loading %s' % x.label)
            self.set_node_default_content(x)
            if x.has_flag(EnumProjectItemFlag.SAVABLE) and x.fileAttr in [EnumProjectNodeFileAttr.FILE,
                                                                          EnumProjectNodeFileAttr.LINK]:
                _content_io = app.read_content_of_project_node(x)
                if _content_io:
                    _body = _content_io.body
                    x.set_content(_body if not isinstance(_body, AppFileIOBody) else None)
            wx.Yield()
        _dlg.Destroy()

    def get_project_tree_view(self):
        return self._panelProjectMgr.treeView

    def get_project_tree_model(self):
        return self._panelProjectMgr.treeView.get_model()

    def get_selected_project_tree_nodes(self):
        return self._panelProjectMgr.treeView.get_selected()

    def get_project(self):
        """
        convenient method to get the project form the global MAIN_APP scope.
        :return: Project
        """
        if gv.MAIN_APP is not None:
            return gv.MAIN_APP.project
        else:
            return None

    def get_editor_by_role(self, role):
        """
        method get the editor class by given role.
        :param role: str, in define.py defined role
        :return: type
        """
        return self._editorMap.get(role)

    def set_node_default_content(self, node):
        """
        method to set the node default content
        :param node: ProjectNode
        :return: None
        """
        if node.role in gv.PROJ_NODE_DEFAULT_CONTENT:
            _content = gv.PROJ_NODE_DEFAULT_CONTENT[node.role]()
            node.set_content(_content)

    def get_editor_instances(self, cls_name):
        """
        method to get all editor instances by given class name.
        :param cls_name: str
        :return: list
        """
        return list(filter(lambda x: x.window.__class__.__name__ == cls_name, self._auiMgr.GetAllPanes()))

    def get_icon_in_bitmap(self, icon_name):
        """
        method get the icon in bitmap by given icon_name
        :param icon_name: str
        :return: wx.Bitmap
        """
        _idx = getattr(self.iconRepo, icon_name, None)
        if _idx is None:
            return wx.NullBitmap
        return self.iconRepo.get_bmp(_idx, self._icon_size)

    def proj_edit_node2(self, node, flags=0):
        print('----->debug: edit node....')
        import time
        _centerDefaultAuiInfo = aui.AuiPaneInfo().Caption('%s' % time.time()).Name('%s' % time.time()). \
            Center().MinimizeButton(True).MaximizeButton(True)

        self._auiMgr.AddPane(self.CreateTreeCtrl(), _centerDefaultAuiInfo, target=self._auiMgr.GetPaneByName("_CNB_"))
        self._auiMgr.Update()

    def proj_edit_node(self, node, flags=0):
        _view = self.get_project_tree_view()
        if node is None:
            return
        _uid = node.uuid
        _exist = self._auiMgr.GetPaneByName(_uid)
        _exist_frm = self.FindWindowByName(node.uuid, self)
        if _exist_frm:
            if isinstance(_exist_frm, wx.Dialog):
                _exist_frm.SetFocus()
            return
        if _exist.IsOk():
            self._auiMgr.RequestUserAttention(_exist.window)
            return
        _editor = self._editorMap.get(node.role)
        _editor_cls_name = _editor.__name__
        if _editor is None:
            wx.MessageBox('no editor associated to the role of this node')
            return
        _role = node.role
        _caption = '/'.join([x.p_label for x in node.path])
        _dlg = wx.ProgressDialog("Loading...",
                                 "Loading...",
                                 maximum=5,
                                 parent=self,
                                 style=0 | wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
                                 # | wx.PD_CAN_ABORT
                                 # | wx.PD_CAN_SKIP
                                 # | wx.PD_ELAPSED_TIME
                                 # | wx.PD_ESTIMATED_TIME
                                 # | wx.PD_REMAINING_TIME
                                 # | wx.PD_AUTO_HIDE
                                 )
        _dlg.Update(1, 'Content initialing')
        if node.content is None:
            self.set_node_default_content(node)
            # if node.content is empty, then read it from the file io
            _content_io = gv.MAIN_APP.read_content_of_project_node(node)
            if not _content_io:
                _dlg.Destroy()
                wx.MessageBox('can not read content of this node.\n%s' % gv.MAIN_APP.error)
                return
            _body = _content_io.body
            node.set_content(_body if not isinstance(_body, AppFileIOBody) else None)
        _dlg.Update(2, 'Editor preparing')
        _editor_flag = 0
        if not node.has_flag(EnumProjectItemFlag.SAVABLE):
            _editor_flag |= EnumEditorFlag.READONLY
        _editor = _editor(self, _editor_flag, size=(0, 0))
        if hasattr(_editor, 'Hide'):
            _editor.Hide()
        _dlg.Update(3, 'Editor applying')
        _editor.apply_edit_mode()
        _editor.set_content(node)
        # prepare the editor menubar config
        _editor_mb_cfg = gv.MAIN_APP.get_editor_mb_config(_editor_cls_name)
        if _editor_mb_cfg is not None:
            _editor.set_mb_config(_editor_mb_cfg)
        _dlg.Update(4, 'Editor setup')
        _bw, _bh = _editor.GetBestSize()
        _bw = max(_bw, 240)
        _bh = max(_bh, 240)
        _editor.SetMinSize(wx.Size(_bw, _bh))
        # prepare the editor layout and styles
        if isinstance(_editor, wx.Dialog):
            _dlg.Destroy()
            _editor.Center()
            _editor.ShowModal()
            _editor.Destroy()
        else:
            _centerDefaultAuiInfo = aui.AuiPaneInfo().Caption(_caption).Name(_uid). \
                DestroyOnClose(True).Center().MinimizeButton(True).MaximizeButton(True).Hide()
            # self._centerTargetAuiInfo.BestSize(_bestSize)
            if isinstance(_editor, MBTAuiToolbarContentPaneMixin):
                _tb, _tb_aui_info = _editor.setup_toolbar(self)
                _name = _uid + '_tb'
                # self._paneTbs.update({_name: _tb})
                self._auiMgr.AddPane(_tb, _tb_aui_info.Name(_uid + '_tb').Caption(_caption + '_toolbar'))
            _log.debug('editor actual size:%s' % _editor.GetSize())
            self._auiMgr.AddPane(_editor, _centerDefaultAuiInfo, target=self._auiMgr.GetPane("_CNB_"))
            """
            use for creating a float windows
            self._mgr.AddPane(self.CreateTreeCtrl(), aui.AuiPaneInfo().
                          Caption("Tree Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(150, 300)).MinimizeButton(True))
            """
            self._auiMgr.Update()
            _centerDefaultAuiInfo.Show(True)
            wx.CallAfter(_editor.ensure_view)
            _dlg.Destroy()
            # self._auiMgr.ActivatePane(_pane)

    # -------------------------------------------------------------------
    # handler for the pubsub system
    # -------------------------------------------------------------------
    def on_ext_sig_topic_project(self, topic: pub.Topic = pub.AUTO_TOPIC, **msg_data):
        _wx_evt = msg_data.get('wx_evt')
        _node_obj = msg_data.get('object')
        _topic_node_name = topic.getNodeName()
        _project = self.get_project()
        if _topic_node_name == 'copy_project_path':
            self._set_text_to_clipboard(_project.projectPath)
        elif _topic_node_name == 'copy_project_name':
            self._set_text_to_clipboard(_project.name)

    def on_ext_sig_topic_os(self, topic: pub.Topic = pub.AUTO_TOPIC):
        _topic_node_name = topic.getNodeName()
        _project = self.get_project()
        if _topic_node_name == 'open_project_in_explorer':
            if _project is not None:
                gv.MAIN_APP.open_path_in_explorer(_project.projectPath)

    def on_ext_sig_topic_console(self, topic: pub.Topic = pub.AUTO_TOPIC, **msg_data):
        _level = msg_data.get('level')
        _content = msg_data.get('content')
        _topic_node_name = topic.getNodeName()
        if _topic_node_name == 'warning':
            self._consolePane.write_warning_content(_content)
        elif _topic_node_name == 'error':
            self._consolePane.write_error_content(_content)
        else:
            self._consolePane.write(_content)

    def on_ext_sig_close_node_editor(self, node):
        if node is not None:
            _uid = node.uuid
            _pane = self._auiMgr.GetPaneByName(_uid)
            if _pane.IsOk():
                self._auiMgr.ClosePane(_pane)
            if node.children:
                for x in node.children:
                    self.on_ext_sig_close_node_editor(x)
        self._auiMgr.Update()

    def on_ext_sig_project_node_profile_changed(self, node):
        if node is not None:
            _uid = node.uuid
            _pane = self._auiMgr.GetPaneByName(_uid)
            if _pane.IsOk():
                _caption = '/'.join([x.p_label for x in node.path])
                _pane.Caption(_caption)
        _view = self.get_project_tree_view()
        _view.refresh_node(node, False)

    def on_ext_sig_put_msg_in_console(self, msg_type, msg):
        if msg_type == EnumConsoleItemFlag.FLAG_WARNING:
            self._consolePane.write_warning_content(msg)
        elif msg_type == EnumConsoleItemFlag.FLAG_ERROR:
            self._consolePane.write_error_content(msg)
        else:
            self._consolePane.write(msg)

    # -------------------------------------------------------------------
    # handler the event of project tree view
    # -------------------------------------------------------------------
    def on_proj_item_context_menu(self, evt):
        _item = evt.GetItem()
        _view = self.get_project_tree_view()
        _node = _view.item_to_node(_item)
        _cm_cfg = copy.deepcopy(gv.MAIN_APP.get_project_node_cm_config(_node.role))
        if _cm_cfg is None or not _cm_cfg:
            return
        _menu = self.get_menu(_cm_cfg, obj=_node)
        _view.PopupMenu(_menu)
        _menu.Destroy()

    def on_proj_item_select_changed(self, evt):
        _item = evt.GetItem()
        _view = self.get_project_tree_view()
        if _item.IsOk():
            _node = _view.item_to_node(_item)
            self.GetStatusBar().SetStatusText(_node.description)
            _prop_panel = ProjectItemPropsContentPanel(self._propContainerPane)
            _prop_panel.set_item(_node)
            self._propContainerPane.set_content(_prop_panel)
        evt.Skip()

    def on_proj_item_activate(self, evt):
        _item = evt.GetItem()
        _view = self.get_project_tree_view()
        _node = _view.item_to_node(_item)
        if _node.children:
            if _view.IsExpanded(_item):
                _view.Collapse(_item)
            else:
                _view.Expand(_item)
        if _node.fileAttr == EnumProjectNodeFileAttr.FOLDER:
            return
        self.proj_edit_node(_node)

    def on_proj_item_get_tooltip(self, evt):
        _item = evt.GetItem()
        _view = self.get_project_tree_view()
        _node = _view.item_to_node(_item)
        if _node.description is not None:
            evt.SetToolTip(_node.description)

    # -------------------------------------------------------------------
    # handler for cm on project treeview, the function name must be same as the config
    # in project_tree_node.ctree
    # -------------------------------------------------------------------
    def cm_not_implemented(self, evt, node, **kwargs):
        wx.MessageBox('sadly the Handler was not implemented.')

    def cm_exe_cmd_on_node_editor(self, evt, node, **kwargs):
        _pane = self._auiMgr.GetPaneByName(node.uuid)
        if _pane.IsOk():
            if isinstance(_pane.window, ProjectNodeEditor):
                _pane.window.exe_cmd(**kwargs)

    def cm_exe_cmd_on_node_content(self, evt, node, **kwargs):
        _view = self.get_project_tree_view()
        if node.content is None:
            self.set_node_default_content(node)
        if node.content is not None:
            _ret, _msg = node.content.exe_cmd(**kwargs)
            if not _ret:
                wx.MessageBox('execution failed.\n%s' % _msg)
                return
            _view.RefreshItems()

    def cm_edit_node_profile(self, evt, node, **kwargs):
        if node.has_flag(EnumProjectItemFlag.DESCRIBABLE):
            _ret, _name, _desc = self._show_dialog_gather_name_desc(node.label,
                                                                    node.description,
                                                                    title='Edit Description of %s' % node.label,
                                                                    cb_validate=lambda x: x and x not in [n.label for n
                                                                                                          in
                                                                                                          node.siblings])
            if _ret:
                node.update_describable_data(_name, _desc)
                _view = self.get_project_tree_view()
                _view.refresh_node(node, False)

    def cm_expand_node(self, evt, node, **kwargs):
        _view = self.get_project_tree_view()
        if node is not None:
            _view.expand_node(node, False)

    def cm_collapse_node(self, evt, node, **kwargs):
        _view = self.get_project_tree_view()
        if node is not None:
            _view.collapse_node(node, False)

    def cm_add_project_child_node_of(self, evt, node, **kwargs):
        """
        method automatically called from config file.
        :param evt: CommandEvent
        :param node: ProjectTreeNode
        :param kwargs: arguments for add child node of node
        :return:None
        """
        _child_role = kwargs.get('role')
        if not node.has_flag(EnumProjectItemFlag.ACCEPT_CHILDREN):
            return
        if _child_role is None:
            return
        _role = node.role
        if _child_role == '*':
            if _role == EnumProjectItemRole.ENGINE_IMPL_ITEMS.value:
                _role_map = IPOD_ENGINE_MGR.get_accessible_role_maps()
                _rm_k = list(_role_map.keys())
                _rm_v = list(_role_map.values())
                if not _rm_v:
                    wx.MessageBox('invalid child role to choose. check the engines define in folder ipod_engines.')
                    return
                _dlg = wx.SingleChoiceDialog(
                    self, 'Choose a engine Type:', 'Specify a engine type',
                    _rm_v,
                    wx.CHOICEDLG_STYLE
                )
                if _dlg.ShowModal() == wx.ID_OK:
                    _selected_child_node_role_name = _dlg.GetStringSelection()
                    _idx = _rm_v.index(_selected_child_node_role_name)
                    _child_role = _rm_k[_idx]
                else:
                    return
                _dlg.Destroy()
        elif _role not in _child_role:
            wx.MessageBox('invalid child role to adding into.')
            return
        _view = self.get_project_tree_view()
        _child_role_cfg = gv.MAIN_APP.get_project_node_config(_child_role)
        if _child_role_cfg is None:
            wx.MessageBox('invalid child cfg to adding into.')
            return
        _child_node = None
        _cfg_child_node_label = _child_role_cfg['label']
        _default_child_node_label = '%s_%s' % (_cfg_child_node_label, len(node.children))
        _default_child_node_desc = 'description of %s' % _default_child_node_label
        _child_node_desc = {'label': _default_child_node_label,
                            'description': _default_child_node_desc}
        if EnumProjectItemFlag.DESCRIBABLE in _child_role_cfg['flag']:
            _ret, _name, _desc = self._show_dialog_gather_name_desc(_default_child_node_label,
                                                                    _default_child_node_desc,
                                                                    title='NewChildNode of %s' % node.label,
                                                                    cb_validate=lambda x: x and x not in [n.label for n
                                                                                                          in
                                                                                                          node.children])
            if _ret:
                _child_node_desc['label'] = _name
                _child_node_desc['description'] = _desc
                _child_node = gv.MAIN_APP.post_add_child_node_of(node, _child_role, _child_node_desc)
        else:
            _child_node = gv.MAIN_APP.post_add_child_node_of(node, _child_role, _child_node_desc)
        if _child_node is not None:
            for x in anytree.iterators.PostOrderIter(node):
                self.set_node_default_content(x)
            _view.RefreshItems()
            _view.select(_child_node, True)
            if _child_node.children:
                _view.expand_node(_child_node)
            else:
                _view.expand_node(node)

    def cm_edit_project_node(self, evt, node, **kwargs):
        self.proj_edit_node(node)

    def cm_delete_project_node(self, evt, node, **kwargs):
        _view = self.get_project_tree_view()
        _exist = gv.MAIN_APP.has_project_node(node)
        if not _exist or not node.has_flag(EnumProjectItemFlag.REMOVABLE):
            return
        _ret = wx.MessageBox('Are you sure you wanna delete node %s' % node.label, style=wx.YES_NO)
        if _ret == wx.YES:
            if node.content is not None:
                _cmd_ret, _cmd_ret_msg = node.content.exe_cmd(command='nodeDelete')
                if not _cmd_ret:
                    wx.MessageBox('can not delete the node.\n%s' % _cmd_ret_msg)
                    return
            self.on_ext_sig_close_node_editor(node)
            gv.MAIN_APP.post_delete_project_node(node)
            _view.RefreshItems()
            if node.p_parent:
                _view.select(node.p_parent, True)
            # todo: send pub message to tell the node was removed.

    # -------------------------------------------------------------------
    # handler for accelerator table
    # -------------------------------------------------------------------
    def on_ctrl_s_pressed(self, evt):
        self._save_project()

    # -------------------------------------------------------------------
    # handler for toolbar
    # -------------------------------------------------------------------
    def on_tb_new_drop_down(self, evt):
        if evt.IsDropDownClicked():
            _tb = evt.GetEventObject()
            _tb.SetToolSticky(evt.GetId(), True)
            # create the popup menu
            _drop_menu = wx.Menu()
            _new_project_id = wx.NewIdRef()
            _new_file_id = wx.NewIdRef()
            _bmp = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
            _m_new_project = wx.MenuItem(_drop_menu, _new_project_id, 'New Project')
            _m_new_project.SetBitmap(_bmp)
            _drop_menu.Append(_m_new_project)
            _m_new_file = wx.MenuItem(_drop_menu, _new_file_id, 'New File')
            _m_new_file.SetBitmap(_bmp)
            _drop_menu.Append(_m_new_file)
            self.Bind(wx.EVT_TOOL, self.on_tb_new_project_clicked, _new_project_id)
            self.Bind(wx.EVT_TOOL, self.on_tb_new_file_clicked, _new_file_id)
            self.PopupMenu(_drop_menu)
            # make sure the button is "un-stuck"
            _tb.SetToolSticky(evt.GetId(), False)

    def on_tb_open_clicked(self, evt):
        self.on_menu_open_clicked(evt)

    def on_tb_new_project_clicked(self, evt):
        self._create_new_project()

    def on_tb_new_file_clicked(self, evt):
        self._create_new_file()

    def on_tb_save(self, evt):
        self._save_project()

    def on_tb_save_as(self, evt):
        self.on_menu_save_as_clicked(evt)

    def on_tb_open_lib_frame(self, evt):
        _name = '_LIB_FRM'
        _exist = wx.FindWindowByName(_name)
        if not _exist:
            _frm = LibraryFrame()
            _frm.SetName(_name)
            _dw, _dh = wx.GetDisplaySize()
            _w, _h = int(_dw / 1.4), int(_dh / 1.5)
            _frm.SetSize((_w, _h))
            _frm.Center()
            _frm.Show()
        else:
            _exist.SetFocus()

    # -------------------------------------------------------------------
    # handler for aui manager event
    # -------------------------------------------------------------------
    def on_aui_pane_close(self, evt):
        _pane = evt.GetPane()
        _pane_name = _pane.name
        _pane_caption = _pane.caption
        _window = _pane.window
        if isinstance(_window, BaseEditor):
            _window.teardown_menubar(self.GetMenuBar())
        if isinstance(_window, ProjectNodeEditor):
            if _window.has_changed():
                _ret = wx.MessageBox('%s has changed, do you wanna apply the changes?' % _pane_caption, style=wx.YES_NO)
                if _ret == wx.YES:
                    _a_ret, _a_msg = _window.apply_content()
                else:
                    _a_ret, _a_msg = _window.restore_content()
                if not _a_ret:
                    wx.MessageBox('Action failed. \n%s' % _a_msg)
        if hasattr(_window, 'teardown'):
            _window.teardown()

    def on_aui_pane_closed(self, evt):
        _pane = evt.GetPane()
        _pane_name = _pane.name
        _window = _pane.window
        _tb_name = _pane_name + '_tb'
        _tb_pane = self._auiMgr.GetPaneByName(_tb_name)
        if _tb_pane.IsOk():
            print('---teardown toolbar....', _tb_name)
            self._paneTbs.pop(_tb_name)
            _window.teardown_toolbar(self)
            self._auiMgr.ClosePane(_tb_pane)

    def on_aui_pane_activated(self, evt):
        _win = evt.GetPane()
        if _win is None:
            return
        _pane_name = self._auiMgr.GetPaneByWidget(_win).name
        if isinstance(_win, aui.AuiNotebook):
            try:
                _win = _win.GetPage(_win.GetSelection())
                _pane_name = self._auiMgr.GetPane(_win).name
            except Exception as e:
                pass
        if isinstance(_win, BaseEditor):
            _win.setup_menubar(self.GetMenuBar())
        if isinstance(_win, ProjectNodeEditor):
            _node = _win.node
            if _node is not None:
                self._panelProjectMgr.treeView.select(_node)
        for k, v in self._paneTbs.items():
            _tb_pane = self._auiMgr.GetPaneByName(k)
            if k == _pane_name + '_tb':
                _tb_pane.window.Enable()
            else:
                _tb_pane.window.Disable()
        if self._paneTbs:
            self._auiMgr.Update()
        # evt.Skip()

    def on_window_closed(self, evt):
        # self._process_unsaved()
        evt.Skip()

    # -------------------------------------------------------------------
    # handler for menubar
    # -------------------------------------------------------------------
    def on_menu(self, evt):
        print('--->on_menu, id=', evt.GetId())
        # for x in self._auiMgr.GetAllPanes():
        #     if isinstance(x.window, BaseEditor) and x.state & aui.optionActive:
        #         x.exe_menu(evt.GetId())
        evt.Skip()

    def on_menu_save_clicked(self, evt):
        self._save_project()
        # todo: save the other like ui...???

    def _save_project(self):
        if gv.MAIN_APP is None:
            return
        _busy = pbi.PyBusyInfo('Apply the changes...')
        # apply all the panes
        _a_ret = True
        _a_msg = list()
        for x in self._auiMgr.GetAllPanes():
            if hasattr(x, 'window') and isinstance(x.window, ProjectNodeEditor):
                if not x.window.has_edit_flag(EnumEditorFlag.READONLY):
                    _r_ret, _r_msg = x.window.apply_content()
                    _a_ret &= _r_ret
                    if not _r_ret:
                        _a_msg.append(_r_msg)
        if not _a_ret:
            del _busy
            wx.MessageBox('Apply failed.\n%s' % '\n'.join(_a_msg))
            return
        self.GetStatusBar().SetStatusText("Project Saving...")
        _busy._infoFrame._message = 'Saving the content...'
        _busy.Update()
        _ret = gv.MAIN_APP.save_project()
        del _busy
        if not _ret:
            wx.MessageBox('Project save failed:\n%s' % gv.MAIN_APP.error)
            self.GetStatusBar().SetStatusText("Project Save failed")
        else:
            self.GetStatusBar().SetStatusText("Project Saved")
        self._panelProjectMgr.treeView.RefreshItems()

    def _process_unsaved(self):
        if gv.MAIN_APP is None:
            return
        if gv.MAIN_APP.project is not None:
            pass
            # _project_save_state = gv.MAIN_APP.project.savedState
            # _app_save_state = gv.MAIN_APP.savedState
            # if not _project_save_state or not _app_save_state:
            #     _ret = wx.MessageBox('Project or Content not saved, do you want save it?', style=wx.YES_NO)
            #     if _ret == wx.YES:
            #         if not _project_save_state:
            #             self._save_project()
            #         if not _app_save_state:
            #             self._save_activated_pane_content()

    def on_menu_save_as_clicked(self, evt):
        if gv.MAIN_APP is None:
            return
        self._process_unsaved()
        _proj_name, _project_path = self._show_create_new_project_dialog()
        if _proj_name is not None and _project_path is not None:
            _ret = gv.MAIN_APP.save_project_as(_proj_name, _project_path)
            if _ret:
                self._panelProjectMgr.treeView.RefreshItems()
                self._update_title_with_project_name(_proj_name)
            else:
                wx.MessageBox('Can not create the project %s, at %s' % (_proj_name, _project_path))

    def on_menu_open_clicked(self, evt):
        self._process_unsaved()
        _dlg = wx.FileDialog(self, defaultDir=APP_PROJECT_PATH,
                             wildcard='Project file (*.proj)|*.proj')
        _ret = _dlg.ShowModal()
        if _ret == wx.ID_OK:
            _dlg.GetPath()
            _path = _dlg.GetPath()
            self.do_open_project(_path)

    def do_open_project(self, path):
        _app = Application()
        if _app.open_project(path):
            # loading content
            self._loading_project_node_content(_app)
            self._panelProjectMgr.treeView.set_model(_app.project.projectTreeModel)
            self._panelProjectMgr.treeView.expand_node(_app.project.projectTreeRoot, False)
            self._panelProjectMgr.treeView.RefreshItems()
            self._update_title_with_project_name(_app.project.name)
            _app.save_project_info_to_recent(_app.project.name, _app.project.projectPath)
            _full_path = os.path.join(_app.project.projectPath, _app.project.name + '.proj')
            self._save_to_file_history(_full_path)
            gv.MAIN_APP = _app
            if _app.project.mainPerspective is not None:
                self._auiMgr.LoadPerspective(_app.project.mainPerspective)
            self._consolePane.write('project %s opened from %s' % (_app.project.name, path))
        else:
            wx.MessageBox('can not open the project.\n%s' % _app.error)

    def on_menu_new_project_clicked(self, evt):
        self._create_new_project()

    def _save_to_file_history(self, path):
        self.fileHistory.AddFileToHistory(path)
        self.fileHistory.Save(gv.GLOBAL_CONFIG)
        gv.GLOBAL_CONFIG.Flush()

    def _create_new_file(self):
        wx.MessageBox(' fail to create file, see you next version', 'Fail')

    def _create_new_project(self):
        self._process_unsaved()
        _proj_name, _project_path = self._show_create_new_project_dialog()
        if _proj_name is not None and _project_path is not None:
            _app = Application()
            # set the global vars
            gv.MAIN_APP = _app
            _ret = _app.create_new_project(_proj_name, _project_path)
            if not _ret:
                wx.MessageBox('Can not create the project %s, at %s.\n%s' % (_proj_name, _project_path, _app.error))
            else:
                self._panelProjectMgr.treeView.set_model(_app.project.projectTreeModel)
                _project_root = _app.project.projectTreeRoot
                _descendants = _project_root.descendants
                for x in _descendants:
                    self.set_node_default_content(x)
                self._panelProjectMgr.treeView.expand_node(_project_root, False)
                self._update_title_with_project_name(_proj_name)
                _app.save_project_info_to_recent(_app.project.name, _app.project.projectPath)
                _full_path = os.path.join(_app.project.projectPath, _app.project.name + '.proj')
                self._save_to_file_history(_full_path)
                self._consolePane.write('project %s created at %s' % (_proj_name, _project_path))

    def _show_create_new_project_dialog(self):
        _dlg = NewProjectDialog(APP_PROJECT_PATH, self)
        _ret = _dlg.ShowModal()
        if _ret == wx.ID_OK:
            if _dlg.projNameTextEdit.IsEmpty():
                _msg = wx.MessageBox(' fail to create project, since project name is empty', 'Fail')
                return None, None
            _project_name = _dlg.projNameTextEdit.GetValue()
            _project_path = _dlg.projectPath
            _project_full_path = os.path.join(_project_path, _project_name)
            _exist = util_is_dir_exist(_project_full_path)
            if _exist:
                _msg = wx.MessageBox(' fail to create project, since project already exist', 'Fail')
                return None, None
            return _project_name, _project_path
        else:
            return None, None

    def on_menu_new_file_clicked(self, evt):
        self._create_new_file()

    def on_file_history_item_clicked(self, evt):
        _fileNum = evt.GetId() - wx.ID_FILE1
        _path = self.fileHistory.GetHistoryFile(_fileNum)
        self.fileHistory.AddFileToHistory(_path)
        # do whatever you want with the file path...
        self.do_open_project(_path)

    def on_update_ui(self, event):
        _agw_flags = self._auiMgr.GetAGWFlags()
        _evt_src_id = event.GetId()
        event.Skip()

    def on_child_focused(self, evt):
        _win = evt.GetWindow()
        evt.Skip()

    def on_child_kill_focused(self, evt):
        print('---->kill focused:', evt)
        evt.Skip()

    def on_size(self, event: wx.Event):
        if not self.sizerTimer.IsRunning():
            self.sizerTimer.StartOnce(100)

    def on_size_time_up(self, evt):
        self.Update()

    def on_erase_background(self, event: wx.Event):
        # Do nothing, to avoid flashing on MSWin
        pass

    def on_idle(self, evt):
        _panes = self._auiMgr.GetAllPanes()
        for pane in _panes:
            pass

    def on_exit(self, event: wx.Event):
        self.Close(force=True)
        event.Skip()

    def on_about(self, event: wx.Event):
        _msg = "ModelBasedTest Editor. v" + APP_VERSION + "\n\n" + \
               "Author: Gaofeng Zhang @ 19 Sep 2020\n\n" + \
               "wxPython: " + wx.VERSION_STRING + '\n\n' + \
               "Canvas: wxGraph\n\n"
        with open('./todo', 'r') as f:
            _msg += '\n' + f.read()
        _dlg = wx.MessageDialog(self, _msg, "About MBT",
                                wx.OK | wx.ICON_INFORMATION)

        if wx.Platform != '__WXMAC__':
            _dlg.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                                 False, '', wx.FONTENCODING_DEFAULT))

        _dlg.ShowModal()
        _dlg.Destroy()
