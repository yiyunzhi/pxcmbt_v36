import wx
import wx.lib.filebrowsebutton as filebrowser
from framework.gui.widgets import OLVSelectorPanel,HeaderPanel
from framework.application.validator import DirNameValidator


class NewProjectDialog(wx.Dialog):
    def __init__(self, default_path: str, workbench_choices: list, parent, wx_id=wx.ID_ANY, title='NewProject', size=wx.DefaultSize,
                 pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE, name='NewProjectDialog'):
        wx.Dialog.__init__(self, parent, wx_id, title, pos, size, style, name)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.formSizer = wx.GridBagSizer(8, 8)
        self.projectPath = default_path
        self.workbenchChoices = workbench_choices
        self.selectedWorkbench = []
        self.wbSelectorPanel = OLVSelectorPanel(self, style=OLVSelectorPanel.OLV_SEL_STYLE_SEL_MULTI)
        self.wbSelLabel = wx.StaticText(self, wx.ID_ANY, 'Select workbenches from below list:')
        self.projNameLabel = wx.StaticText(self, wx.ID_ANY, 'ProjectName:')
        self.projNameTextEdit = wx.TextCtrl(self, wx.ID_ANY)
        self.projNameTextEdit.SetValidator(DirNameValidator())
        self.projPathLabel = wx.StaticText(self, wx.ID_ANY, 'ProjectPath:')
        self.projPathEdit = filebrowser.FileBrowseButton(self, wx.ID_ANY, changeCallback=self.fbb_callback)
        self.projPathEdit.SetValue(default_path)
        self.projPathEdit.GetBorder()
        self.projPathEdit.SetLabel('')
        self.wbSelectorPanel.render_form(self.workbenchChoices)
        # layout
        self.formSizer.Add(self.projNameLabel, (0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.formSizer.Add(self.projNameTextEdit, (0, 1), span=(0, 8), flag=wx.ALIGN_LEFT | wx.LEFT, border=8)
        self.formSizer.Add(self.projPathLabel, (1, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.formSizer.Add(self.projPathEdit, (1, 1), span=(0, 25), flag=wx.EXPAND)
        self.btnSizer = wx.StdDialogButtonSizer()
        _btn_ok = wx.Button(self, wx.ID_OK)
        _btn_ok.SetHelpText("The OK button completes the dialog")
        _btn_ok.SetDefault()
        self.btnSizer.AddButton(_btn_ok)

        _btn_cancel = wx.Button(self, wx.ID_CANCEL)
        _btn_cancel.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        self.btnSizer.AddButton(_btn_cancel)
        self.btnSizer.Realize()

        self.projNameTextEdit.SetFocus()
        # bind event

        # layout
        self.mainSizer.Add(HeaderPanel(self, 'New Project', 'create a project with given information.'), 0, wx.EXPAND | wx.ALL, 5)
        self.mainSizer.Add(self.formSizer, 0, wx.EXPAND | wx.ALL, 8)
        self.mainSizer.Add(self.wbSelLabel, 0, wx.EXPAND | wx.ALL, 8)
        self.mainSizer.Add(self.wbSelectorPanel, 1, wx.EXPAND | wx.ALL, 8)
        self.mainSizer.Add(self.btnSizer, 0, wx.ALL, 8)
        self.SetSizer(self.mainSizer)
        self.Layout()
        self.Fit()

    def fbb_callback(self, evt):
        self.projectPath = evt.GetString()
