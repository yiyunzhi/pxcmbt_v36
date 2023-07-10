import datetime, ctypes, builtins, platform
import os, sys, logging, logging.config
import time
import wx
import wx.adv
import wx.lib.mixins.inspection
from framework.application.io.class_yaml_file_io import AppYamlFileIO
from framework.application.uri_handle import *
from mbt import appCtx
from mbt.application.define_base import APP_NAME, APP_VERSION, REQ_WX_VERSION_STRING, BASE_PATH, APP_DATA_BUILTIN_PATH

from application.class_yaml_tags import *
from mbt.application.log.class_logger import get_logger
from application.class_content_iod_action import IOD_ACTION_EXT_MGR
from application.class_application_config import APP_CONFIG
from application.class_ipod_engine import IPOD_ENGINE_MGR
from .gui_main_frame import AppFrame
from .gui_splash import SplashScreen

# from pxct_driver.application.application import Application as SessionApplication
# from pxct_driver.bootstrap import bootstrap as session_log_bootstrap

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


# Install a custom displayhook to keep Python from setting the global
# _ (underscore) to the value of the last evaluated expression.
# If we don't do this, our mapping of _ to gettext can get overwritten.
# This is useful/needed in interactive debugging with PyShell.
def _displayHook(obj):
    """
    Custom display hook to prevent Python stealing '_'.
    """

    if obj is not None:
        print(repr(obj))


def _init_logging():
    os.environ.update({'LOG_CFG_DIR': BASE_PATH})
    logging.config.fileConfig(os.path.join(BASE_PATH, 'log', 'logger.cfg'), disable_existing_loggers=False)


def _chk_ipod_engines():
    _chk_ver_ret = True
    _chk_ver_msg = list()
    for x in IPOD_ENGINE_MGR.engines:
        _ret, _msg = x.check_version()
        _chk_ver_ret &= _ret
        if not _ret:
            _chk_ver_msg.append(_msg)
    return _chk_ver_ret, _chk_ver_msg


_log = get_logger('application')
builtins.__dict__['_'] = wx.GetTranslation


class App(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    # def InitLocale(self):
    #     if sys.platform.startswith('win') and sys.version_info > (3,8):
    #         import locale
    #         locale.setlocale(locale.LC_ALL, 'C')
    def OnInit(self):
        if REQ_WX_VERSION_STRING != wx.VERSION_STRING:
            wx.MessageBox(caption="Warning",
                          message="You're using version %s of wxPython, but this copy of the demo was written for version %s.\n"
                                  "There may be some version incompatibilities..."
                                  % (wx.VERSION_STRING, REQ_WX_VERSION_STRING))

        self.InitInspection()  # for the InspectionMixin base class
        wx.SystemOptions.SetOption("mac.window-plain-transition", 1)
        self.SetAppName(APP_NAME)
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Global dpi aware
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-monitor dpi aware
        except AttributeError:
            wx.MessageBox('can not pass the current DPI setting.\nthere could be some display issues.')
        except OSError:
            wx.MessageBox('can not pass the current DPI setting since access problem.\nthere could be some display issues.')
        # attach the displayhook in sys
        sys.displayhook = _displayHook

        _current_dt = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        # Create and show the splash screen.  It will then create and
        # show the main frame when it is time to do so.  Normally when
        # using a SplashScreen you would create it, show it and then
        # continue on with the application's initialization, finally
        # creating and showing the main application window(s).  In
        # this case we have nothing else to do so we'll delay showing
        # the main frame until later (see ShowMain above) so the users
        # can see the SplashScreen effect.
        _splash = SplashScreen()
        wx.Yield()
        # todo: init help doc
        # todo: lowercase
        URI_HANDLE_MANAGER = URIHandleManager()
        URI_HANDLE_MANAGER.register(CallExternalURIHandle(app_ctx=appCtx))
        URI_HANDLE_MANAGER.register(PubsubURIHandle())
        URI_HANDLE_MANAGER.register(AppCurrentViewExecOperationURIHandle())
        appCtx.zViewFactory = GUI_VIEW_FACTORY
        appCtx.iconResp = IconRepository(_q_app)
        appCtx.i18nResp = I18nRepository()
        appCtx.mbtSolutionManager = MBTSolutionsManager(appCtx)
        appCtx.addonsManager = AddonsManager(appCtx)
        appCtx.uriHandleMgr = URI_HANDLE_MANAGER
        appCtx.setup(_q_app)
        _splash.set_message('read global config')
        # the config file generally in C:\Users\xxx\AppData\Roaming\APP_NAME.ini stored.
        if gv.GLOBAL_CONFIG is None:
            gv.GLOBAL_CONFIG = wx.FileConfig(APP_NAME, vendorName='PxCE')
            gv.GLOBAL_CONFIG.Write("appVersion", APP_VERSION)
            # todo: if computer name different then clear the recentList
            _last_date = gv.GLOBAL_CONFIG.Read("lastStartAt")
            if _last_date:
                gv.GLOBAL_CONFIG.Write("previousStartAt", _last_date)
            else:
                gv.GLOBAL_CONFIG.Write("previousStartAt", _current_dt)
            gv.GLOBAL_CONFIG.Write("lastStartAt", _current_dt)
            if not gv.GLOBAL_CONFIG.HasEntry('recentProjectList'):
                gv.GLOBAL_CONFIG.Write("recentProjectList", '')
            gv.GLOBAL_CONFIG.Flush()
        # _splash.set_message('init local')
        # # Controls the current interface language
        # self.language_prefix = "LANGUAGE_"
        # self.language = self.language_prefix + self.app_config.Config(keys=("Settings", "Interface", "Language")).upper()
        #
        # # Setup the Locale
        # self.InitI18n()
        # self.Setlang(self.language)
        _splash.set_message('init logger')
        _init_logging()
        _splash.set_message('check IPOD Engines.')
        _ret, _msg = _chk_ipod_engines()
        if not _ret:
            [_splash.set_message('-' * 5 + x) for x in _msg]
        _splash.set_message('loading extends.')
        _ext_path = os.path.join(BASE_PATH, *APP_CONFIG.scExtIODActionsPath)
        if not IOD_ACTION_EXT_MGR.load_action_extends(_ext_path, '*.py'):
            _error = IOD_ACTION_EXT_MGR.error
            wx.MessageBox('Error on Extend init:\n%s' % _error)
            _log.error('%s' % _error)
            return False
        _ext_iod_act_io = AppYamlFileIO(APP_DATA_BUILTIN_PATH, 'ext_iod_act.obj')
        _ext_iod_act_io.write(IOD_ACTION_EXT_MGR.builtinContainer)
        _splash.set_message('init session application.')
        # load session application
        # gv.SESSION_APP = SessionApplication()
        # session_log_bootstrap()
        _splash.set_message('start main application.')
        _main_frm = AppFrame(None)
        # debug constructor and representer of yaml tag
        # for k,v in yaml.CFullLoader.yaml_constructors.items():
        #    print('yamlmeta->', k,v)
        _dw, _dh = wx.GetDisplaySize()
        _w, _h = int(_dw / 1.1), int(_dh / 1.2)
        # _dip_size=wx.Window.FromDIP(
        #     wx.Size(_w,_h),_main_frm
        # )
        _dip_size = wx.Size(_w, _h)
        _main_frm.SetClientSize(_dip_size)
        self.SetTopWindow(_main_frm)
        _main_frm.Center()
        _main_frm.Show()
        del _splash
        return True

    def OnExit(self):
        if gv.SESSION_APP:
            gv.SESSION_APP.stop()
        del gv.SESSION_APP
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

    def InitI18n(self):
        self.locale = wx.Locale(getattr(wx, self.language))
        path = os.path.abspath("./gimelstudio/locale") + os.path.sep
        self.locale.AddCatalogLookupPathPrefix(path)
        self.locale.AddCatalog(self.GetAppName())

    def Setlang(self, language):
        supported_langs = {
            "LANGUAGE_ENGLISH": "en",
            "LANGUAGE_FRENCH": "fr",
            "LANGUAGE_GERMAN": "de",
        }

        # To get some language settings to display properly on Linux
        if platform.system() == "Linux":
            try:
                os.environ["LANGUAGE"] = supported_langs[language]
            except (ValueError, KeyError) as error:
                print(error)


def start():
    app = App(False)
    if wx.GetApp().GetComCtl32Version() >= 600 and wx.DisplayDepth() >= 32:
        # Use the 32-bit images
        wx.SystemOptions.SetOption("msw.remap", 0)
        wx.SystemOptions.SetOption("no-maskblt", 1)
    return app.MainLoop()
