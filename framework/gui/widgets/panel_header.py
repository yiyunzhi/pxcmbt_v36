import wx
from framework.gui.utils import gui_util_get_default_font


# todo: use wx.adv.BannerWindow(self, dir=wx.TOP) reimplement
class HeaderPanel(wx.Panel):
    def __init__(self,
                 parent,
                 title,
                 sub_title=None,
                 description=None,
                 h_border=15,
                 v_border=15,
                 v_space=5,
                 wrap_width=360,
                 background_color='#f8f8ff',
                 title_color='#555',
                 sub_title_color='#555',
                 description_color='#aaa',
                 title_font_size=14,
                 subtitle_font_size=10,
                 desc_font_size=8):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        assert wrap_width > 0
        self.hBorder = h_border
        self.vBorder = v_border
        self.vSpace = v_space
        self.wrapWidth = wrap_width
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.titleFont = gui_util_get_default_font(title_font_size)
        self.titleFont.SetWeight(wx.FONTWEIGHT_BOLD)
        self.subtitleFont = gui_util_get_default_font(subtitle_font_size)
        self.descriptionFont = gui_util_get_default_font(desc_font_size)
        self.descriptionFont.SetStyle(wx.FONTSTYLE_ITALIC)
        self.titleColor = wx.Colour(title_color)
        self.subTitleColor = wx.Colour(sub_title_color)
        self.descriptionColor = wx.Colour(description_color)
        self.title = title
        self.backgroundColor = wx.Colour(background_color)
        self.subTitle = sub_title
        self.description = description
        self.SetBackgroundColour(self.backgroundColor)
        self.ctrlTitle = wx.StaticText(self, wx.ID_ANY, self.title)
        self.ctrlTitle.SetFont(self.titleFont)
        self.ctrlTitle.SetForegroundColour(self.titleColor)
        # bind event
        # layout
        self.ctrlTitle.Wrap(self.wrapWidth)
        self.SetSizer(self.mainSizer)
        self.mainSizer.AddSpacer(v_border)
        self.mainSizer.Add(self.ctrlTitle, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, h_border)
        if self.subTitle is not None or self.description is not None:
            self.mainSizer.AddSpacer(v_space)
        else:
            self.mainSizer.AddSpacer(v_border)
        if self.subTitle is not None:
            self.ctrlSubTitle = wx.StaticText(self, wx.ID_ANY, self.subTitle)
            self.ctrlSubTitle.SetFont(self.subtitleFont)
            self.ctrlSubTitle.SetForegroundColour(self.subTitleColor)
            self.ctrlSubTitle.Wrap(self.wrapWidth)
            self.mainSizer.Add(self.ctrlSubTitle, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, h_border)
            if self.description is not None:
                self.mainSizer.AddSpacer(v_space)
            else:
                self.mainSizer.AddSpacer(v_border)
        if self.description is not None:
            self.ctrlDesc = wx.StaticText(self, wx.ID_ANY, self.description)
            self.ctrlDesc.SetFont(self.descriptionFont)
            self.ctrlDesc.SetForegroundColour(self.descriptionColor)
            self.ctrlDesc.Wrap(self.wrapWidth)
            self.mainSizer.Add(self.ctrlDesc, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, h_border)
            self.mainSizer.AddSpacer(v_border)
        self.Layout()

    def set_background_color(self, color):
        if isinstance(color, wx.Colour):
            self.SetBackgroundColour(color)
        else:
            self.SetBackgroundColour(wx.Colour(color))
        self.Refresh()

    def set_title(self, title):
        self.title = title
        self.ctrlTitle.SetLabelText(title)
        self.Layout()

    def set_sub_title(self, text):
        if self.subTitle is not None:
            self.subTitle = text
            self.ctrlSubTitle.SetLabelText(text)
            self.Layout()

    def set_description(self, text):
        if self.description is not None:
            self.description = text
            self.ctrlDesc.SetLabelText(text)
            self.Layout()

    def set_warp_width(self, wrap_width):
        assert wrap_width > 0
        self.wrapWidth = wrap_width
        if self.title is not None:
            self.ctrlTitle.Wrap(wrap_width)
        if self.subTitle is not None:
            self.ctrlSubTitle.Wrap(wrap_width)
        if self.description is not None:
            self.ctrlDesc.Wrap(wrap_width)
        self.Layout()
