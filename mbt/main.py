import datetime, ctypes, builtins
import os, sys, logging, logging.config
import warnings
import glob, shutil
import wx
import wx.adv
import wx.lib.mixins.inspection
import wx.html as whtml
from framework import setup_application_context
from framework.resources import LOCALE_PATH as FRAMEWORK_LOCALE_PATH
from framework.application.define import THIS_LANG_DOMAIN as FRAMEWORK_LANG_DOMAIN, _
from framework.application.uri_handle import *
from framework.application.base import GenericTypeFactory
from framework.gui.icon_repo.class_icon_repo import LocalIconRepoCategory
from framework.application.confware import ZFileConfigBase
from mbt import appCtx, setup_application_context as setup_mbt_app_ctx
from mbt.application.class_application import MBTApplication
from mbt.application.define import APP_NAME, APP_VERSION, REQ_WX_VERSION_STRING, APP_VENDOR_NAME, SUPPORTED_LANG, THIS_LANG_DOMAIN
from mbt.application.log.class_logger import get_logger
from mbt.application.mbt_solution_manager.solution_manager import MBTSolutionsManager
from .resources import LOCALE_PATH, HELP_PATH, CFG_TEMPLATE_PATH
from .application.define_path import MBT_ROOT_PATH, SOLUTIONS_PATH
from .application.confware import MBTConfigManager
from .gui.art_provider.class_art_provider import MBTArtProvider
from .gui_main_frame_mgr import AppMainFrameViewManager
from .gui_splash import SplashScreen

# from pxct_driver.application.application import Application as SessionApplication
# from pxct_driver.bootstrap import bootstrap as session_log_bootstrap

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

_log = get_logger('application')
builtins.__dict__['_'] = wx.GetTranslation

URI_HANDLE_MANAGER = URIHandleManager()


# Install a custom displayhook to keep Python from setting the global
# _ (underscore) to the value of the last evaluated expression.
# If we don't do this, our mapping of _ to gettext can get overwritten.
# This is useful/needed in interactive debugging with PyShell.
def _display_hook(obj):
    """
    Custom display hook to prevent Python stealing '_'.
    """

    if obj is not None:
        print(repr(obj))


def _init_logging():
    _log_dir = os.path.join(MBT_ROOT_PATH, 'log')
    os.environ.update({'LOG_CFG_DIR': _log_dir})
    logging.config.fileConfig(os.path.join(_log_dir, 'logger.cfg'), disable_existing_loggers=False)


class DummySplash:
    def set_message(self, message):
        pass


class App(wx.App, wx.lib.mixins.inspection.InspectionMixin, MBTApplication):
    def OnInit(self):
        # --------------------------------------------------------------
        # wx configuration
        # --------------------------------------------------------------
        if REQ_WX_VERSION_STRING != wx.VERSION_STRING:
            wx.MessageBox(caption=_("Warning"),
                          message=_("You're using version %s of wxPython, but this copy of the demo was written for version %s.\n"
                                    "There may be some version incompatibilities...")
                                  % (wx.VERSION_STRING, REQ_WX_VERSION_STRING))

        self.InitInspection()  # for the InspectionMixin base class
        wx.SystemOptions.SetOption("mac.window-plain-transition", 1)
        self.SetAppName(APP_NAME)
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Global dpi aware
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-monitor dpi aware
        except AttributeError:
            wx.MessageBox(_('can not pass the current DPI setting.\nthere could be some display issues.'))
        except OSError:
            wx.MessageBox(
                'can not pass the current DPI setting since access problem.\nthere could be some display issues.')
        # attach the displayhook in sys
        sys.displayhook = _display_hook

        _current_dt = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.configLoc = os.path.join(wx.StandardPaths.Get().GetUserConfigDir(), APP_NAME)
        self.systemConfig = wx.FileConfig(APP_NAME, APP_VENDOR_NAME, os.path.join(self.configLoc, 'system.ini'))
        self._init_app_config()
        # wx.SystemOptions.SetOption('msw.dark-mode', 2)
        _appearance_cfg = self.appConfigMgr.get_config('appearance')
        _i18n_cfg = self.appConfigMgr.get_config('i18n')
        _show_splash = _appearance_cfg.read('/startup/showSplash', True)

        # Create and show the splash screen.  It will then create and
        # show the main frame when it is time to do so.  Normally when
        # using a SplashScreen you would create it, show it and then
        # continue on with the application's initialization, finally
        # creating and showing the main application window(s).  In
        # this case we have nothing else to do so we'll delay showing
        # the main frame until later (see ShowMain above) so the users
        # can see the SplashScreen effect.
        if _show_splash:
            _splash = SplashScreen()
            wx.Yield()
        else:
            _splash = DummySplash()
        # --------------------------------------------------------------
        # logging
        # --------------------------------------------------------------
        _splash.set_message('init logger')
        _init_logging()
        # --------------------------------------------------------------
        # components
        # --------------------------------------------------------------
        _splash.set_message('init components')
        self.uriHandleMgr.register(CallExternalURIHandle(app_ctx=appCtx))
        self.uriHandleMgr.register(PubsubURIHandle())
        self.uriHandleMgr.register(AppCurrentViewExecOperationURIHandle())

        # --------------------------------------------------------------
        # Config stuff is here
        # --------------------------------------------------------------
        _splash.set_message('Setup application configuration')

        if not self.systemConfig.Exists('appVersion'):
            self.systemConfig.Write('appVersion', APP_VERSION)
        _last_date = self.systemConfig.Read("/statistic/lastStartAt")
        if _last_date:
            self.systemConfig.Write("/statistic/previousStartAt", _last_date)
        else:
            self.systemConfig.Write("/statistic/previousStartAt", _current_dt)
        self.systemConfig.Write("/statistic/lastStartAt", _current_dt)
        self.systemConfig.Flush()

        _lang = _i18n_cfg.read('/language', 'en')
        # --------------------------------------------------------------
        # locale
        # --------------------------------------------------------------
        # pot->po->mo
        _splash.set_message('init i18n')
        # Controls the current interface language
        wx.Locale.AddCatalogLookupPathPrefix(FRAMEWORK_LOCALE_PATH)
        wx.Locale.AddCatalogLookupPathPrefix(LOCALE_PATH)
        self.update_language(_lang)
        # debug code for I18N print(_('error'),_('NewProject'))
        # --------------------------------------------------------------
        # art provider
        # --------------------------------------------------------------
        self._init_art_provider()
        _mbt_art_provider = appCtx.get_property('artProvider')
        # --------------------------------------------------------------
        # help controller
        # --------------------------------------------------------------
        _splash.set_message('init help controller')
        # make a simpleHelpProvider for contextHelp on given control.
        # just pop up a text windows.
        _hlp_provider = wx.SimpleHelpProvider()
        wx.HelpProvider.Set(_hlp_provider)
        self.update_help_content()
        # --------------------------------------------------------------
        # addons
        # --------------------------------------------------------------
        _splash.set_message('load addons')
        # appCtx.set_property('addonsManager', AddonsManager(appCtx))
        # --------------------------------------------------------------
        # mbt solution
        # --------------------------------------------------------------
        _splash.set_message('loading solutions into context.')
        _mbt_solution_mgr = MBTSolutionsManager()
        _mbt_solution_mgr.resolve_solutions(SOLUTIONS_PATH)
        # add local image into artProvider.
        _solution_icon_files = dict()
        for k, v in _mbt_solution_mgr.solutions.items():
            _icon_path, _icon_name = v.iconInfo
            if _icon_path is not None:
                _solution_icon_files.update({_icon_name: _icon_path})
        if _solution_icon_files:
            _solution_icon_repo = LocalIconRepoCategory(name='solution', files=_solution_icon_files)
            _mbt_art_provider.iconRepo.register(_solution_icon_repo)
        self.mbtSolutionManager = _mbt_solution_mgr
        # --------------------------------------------------------------
        # setup application main frame
        # --------------------------------------------------------------
        # _splash.set_message('init session application.')
        # load session application
        # gv.SESSION_APP = SessionApplication()
        # session_log_bootstrap()
        # setup app ctx, there could the editor registered into factory
        setup_application_context(self)
        setup_mbt_app_ctx(self)
        _splash.set_message('start main application.')
        _main_frm_mgr = AppMainFrameViewManager()
        _main_frm = _main_frm_mgr.create_view()
        self.rootView = _main_frm
        # debug constructor and representer of yaml tag
        # for k,v in yaml.CFullLoader.yaml_constructors.items():
        #    print('yamlmeta->', k,v)
        _dw, _dh = wx.GetDisplaySize()
        _w, _h = int(_dw / 1.2), int(_dh / 1.4)
        # _dip_size=wx.Window.FromDIP(
        #     wx.Size(_w,_h),_main_frm
        # )
        _dip_size = wx.Size(_w, _h)
        _main_frm.SetClientSize(_dip_size)
        self.SetTopWindow(_main_frm)
        _main_frm.Center()
        _main_frm.Show()

        # experimental:try to set the dark mode on the given handle of window
        # _hwnd = _main_frm.GetHandle()
        # from mbt.gui.patch.low_level_sys_ui import llSetDarkWinTitlebar
        # llSetDarkWinTitlebar(_hwnd)

        del _splash
        return True

    def _init_art_provider(self):
        _mbt_art_provider = MBTArtProvider()
        wx.ArtProvider.Push(_mbt_art_provider)
        appCtx.set_property('artProvider', _mbt_art_provider)

    def _init_app_config(self):
        # the config file generally in C:\Users\xxx\AppData\Roaming\APP_NAME.ini stored.
        # nix: \home\userid\appName
        # those files store the version, last datetime, the recent file list and so on.
        _app_ver = self.systemConfig.Read('appVersion')
        if _app_ver != APP_VERSION:
            # todo: merge config for version update
            pass
        if not os.path.exists(self.configLoc):
            os.mkdir(self.configLoc)
            shutil.copytree(CFG_TEMPLATE_PATH, self.configLoc, dirs_exist_ok=True)
        # todo: if file not exist then copy it.
        # in register node_cls could also be reassigned.
        _i18n_cfg: ZFileConfigBase = self.appConfigMgr.register_with(node_cls=ZFileConfigBase, name='i18n', base_dir=self.configLoc, filename='i18n')
        _appearance_cfg: ZFileConfigBase = self.appConfigMgr.register_with(node_cls=ZFileConfigBase, name='appearance', base_dir=self.configLoc,
                                                                           filename='appearance')
        _shortcut_cfg: ZFileConfigBase = self.appConfigMgr.register_with(node_cls=ZFileConfigBase, name='shortcut', base_dir=self.configLoc,
                                                                         filename='shortcut')
        if not os.path.exists(_i18n_cfg.wareIO.filename):
            _src = os.path.join(CFG_TEMPLATE_PATH, os.path.basename(_i18n_cfg.configFilename))
            shutil.copy(_src, os.path.dirname(_i18n_cfg.wareIO.filename))
        if not os.path.exists(_appearance_cfg.wareIO.filename):
            _src = os.path.join(CFG_TEMPLATE_PATH, os.path.basename(_appearance_cfg.configFilename))
            shutil.copy(_src, os.path.dirname(_appearance_cfg.wareIO.filename))
        if not os.path.exists(_shortcut_cfg.wareIO.filename):
            _src = os.path.join(CFG_TEMPLATE_PATH, os.path.basename(_shortcut_cfg.configFilename))
            shutil.copy(_src, os.path.dirname(_shortcut_cfg.wareIO.filename))

    def update_language(self, lang: str = None):
        """
        Update the language to the requested one.

        Make *sure* any existing locale is deleted before the new
        one is created.  The old C++ object needs to be deleted
        before the new one is created, and if we just assign a new
        instance to the old Python variable, the old C++ locale will
        not be destroyed soon enough, likely causing a crash.

        :param lang: str, one of the supported language codes

        """
        # if an unsupported language is requested default to English
        if lang in SUPPORTED_LANG:
            _sel_lang = SUPPORTED_LANG[lang]
        else:
            _sel_lang = wx.LANGUAGE_ENGLISH

        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale

        # create a locale object for this language
        self.locale = wx.Locale(_sel_lang)
        if self.locale.IsOk():
            _lang_name = self.locale.GetSysName()
            self.locale.AddCatalog(FRAMEWORK_LANG_DOMAIN)
            self.locale.AddCatalog(THIS_LANG_DOMAIN)
            _pref_cfg = self.appConfigMgr.get_config('i18n')
            _pref_cfg.write("/language", _lang_name)
            _pref_cfg.flush()
        else:
            self.locale = None
            warnings.warn('localization setup failed, fall back to english.')

    def update_help_content(self):
        _hlp_ctrl = whtml.HtmlHelpController()
        _list_of_files = list()
        for filename in glob.glob(os.path.join(HELP_PATH, '*/*.hhp'), recursive=False):
            _list_of_files.append(filename)
        # todo: base on the current language or locale???
        # for (dir_path, dir_names, filenames) in os.walk(HELP_PATH):
        #     for filename in filenames:
        #         if filename.endswith('.hhp'):
        #             _list_of_files[filename] = os.sep.join(os.path.join(HELP_PATH, filename))
        for x in _list_of_files:
            _hlp_ctrl.AddBook(x)
        self.helpController = _hlp_ctrl

    def OnExit(self):
        # if gv.SESSION_APP:
        #     gv.SESSION_APP.stop()
        # del gv.SESSION_APP
        # _rest_actor_ref = ActorRegistry.get_all()
        # if _rest_actor_ref:
        #     _dlg = wx.ProgressDialog('App Exit', 'waiting until the APP EXIT finish')
        #     for x in _rest_actor_ref:
        #         # todo: think about better function for Actor
        #         x._actor.set_force_stop_flag()
        #     ActorRegistry.stop_all(False)
        #     while ActorRegistry.get_all():
        #         _dlg.Pulse()
        #     del _dlg
        return 0


def start():
    app = App(False)
    if wx.GetApp().GetComCtl32Version() >= 600 and wx.DisplayDepth() >= 32:
        # Use the 32-bit images
        wx.SystemOptions.SetOption("msw.remap", 0)
        wx.SystemOptions.SetOption("no-maskblt", 1)
    return app.MainLoop()
