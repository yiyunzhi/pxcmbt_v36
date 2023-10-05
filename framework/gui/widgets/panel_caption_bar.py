# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : panel_caption_bar.py
# ------------------------------------------------------------------------------
#
# File          : panel_caption_bar.py
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
from ..utils import gui_util_get_default_font
from ..base import BufferedWindow


class CaptionBarStyle(object):
    CAPTIONBAR_NOSTYLE = 0
    """ The :class:`CaptionBar` has no style bit set. """
    CAPTIONBAR_GRADIENT_V = 1
    """ Draws a vertical gradient from top to bottom. """
    CAPTIONBAR_GRADIENT_H = 2
    """ Draws a vertical gradient from left to right. """
    CAPTIONBAR_SINGLE = 3
    """ Draws a single filled rectangle to draw the caption. """
    CAPTIONBAR_RECTANGLE = 4
    """ Draws a single colour with a rectangle around the caption. """
    CAPTIONBAR_FILLED_RECTANGLE = 5
    """
    This class encapsulates the styles you wish to set for the
    :class:`CaptionBar` (this is the part of the `FoldPanel` where the caption
    is displayed). It can either be applied at creation time be
    reapplied when styles need to be changed.

    At construction time, all styles are set to their default
    transparency.  This means none of the styles will be applied to
    the :class:`CaptionBar` in question, meaning it will be created using the
    default internals. When setting i.e the colour, font or panel
    style, these styles become active to be used.
    """

    def __init__(self):
        """ Default constructor for this class. """
        self.reset_to_defaults()

    def reset_to_defaults(self):
        """ Resets default :class:`CaptionBarStyle`. """
        self._firstColourUsed = False
        self._secondColourUsed = False
        self._textColourUsed = False
        self._captionFontUsed = False
        self._captionStyleUsed = False
        self._captionStyle = self.CAPTIONBAR_GRADIENT_H

    # ------- CaptionBar Font -------

    def set_caption_font(self, font):
        """
        Sets font for the caption bar.

        :param font: a valid :class:`wx.Font` object.

        :note: If this is not set, the font property is undefined and will not be used.
         Use :meth:`~CaptionBarStyle.CaptionFontUsed` to check if this style is used.
        """

        self._captionFont = font
        self._captionFontUsed = True

    def caption_font_used(self):
        """ Checks if the caption bar font is set. """

        return self._captionFontUsed

    def get_caption_font(self):
        """
        Returns the font for the caption bar.

        :note: Please be warned this will result in an assertion failure when
         this property is not previously set.

        :see: :meth:`~CaptionBarStyle.SetCaptionFont`, :meth:`~CaptionBarStyle.CaptionFontUsed`
        """

        return self._captionFont

    # ------- First Colour -------

    def set_first_colour(self, colour):
        """
        Sets first colour for the caption bar.

        :param colour: a valid :class:`wx.Colour` object.

        :note: If this is not set, the colour property is undefined and will not be used.
         Use :meth:`~CaptionBarStyle.FirstColourUsed` to check if this style is used.
        """

        self._firstColour = colour
        self._firstColourUsed = True

    def first_colour_used(self):
        """ Checks if the first colour of the caption bar is set."""

        return self._firstColourUsed

    def get_first_colour(self):
        """
        Returns the first colour for the caption bar.

        :note: Please be warned this will result in an assertion failure when
         this property is not previously set.

        :see: :meth:`~CaptionBarStyle.SetFirstColour`, :meth:`~CaptionBarStyle.FirstColourUsed`
        """

        return self._firstColour

    # ------- Second Colour -------

    def set_second_colour(self, colour):
        """
        Sets second colour for the caption bar.

        :param colour: a valid :class:`wx.Colour` object.

        :note: If this is not set, the colour property is undefined and will not be used.
         Use :meth:`~CaptionBarStyle.SecondColourUsed` to check if this style is used.
        """

        self._secondColour = colour
        self._secondColourUsed = True

    def second_colour_used(self):
        """ Checks if the second colour of the caption bar is set."""

        return self._secondColourUsed

    def get_second_colour(self):
        """
        Returns the second colour for the caption bar.

        :note: Please be warned this will result in an assertion failure when
         this property is not previously set.

        :see: :meth:`~CaptionBarStyle.SetSecondColour`, :meth:`~CaptionBarStyle.SecondColourUsed`
        """

        return self._secondColour

    # ------- Caption Text Colour -------

    def set_caption_colour(self, colour):
        """
        Sets caption colour for the caption bar.

        :param colour: a valid :class:`wx.Colour` object.

        :note: If this is not set, the colour property is undefined and will not be used.
         Use :meth:`~CaptionBarStyle.CaptionColourUsed` to check if this style is used.
        """

        self._textColour = colour
        self._textColourUsed = True

    def caption_colour_used(self):
        """ Checks if the caption colour of the caption bar is set."""

        return self._textColourUsed

    def get_caption_colour(self):
        """
        Returns the caption colour for the caption bar.

        :note: Please be warned this will result in an assertion failure
         when this property is not previously set.

        :see: :meth:`~CaptionBarStyle.SetCaptionColour`, :meth:`~CaptionBarStyle.CaptionColourUsed`
        """

        return self._textColour

    # ------- CaptionStyle  -------

    def set_caption_style(self, style):
        """
        Sets caption style for the caption bar.

        :param style: can be one of the following bits:

         =============================== ======= =============================
         Caption Style                    Value  Description
         =============================== ======= =============================
         ``CAPTIONBAR_GRADIENT_V``             1 Draws a vertical gradient from top to bottom
         ``CAPTIONBAR_GRADIENT_H``             2 Draws a horizontal gradient from left to right
         ``CAPTIONBAR_SINGLE``                 3 Draws a single filled rectangle to draw the caption
         ``CAPTIONBAR_RECTANGLE``              4 Draws a single colour with a rectangle around the caption
         ``CAPTIONBAR_FILLED_RECTANGLE``       5 Draws a filled rectangle and a border around it
         =============================== ======= =============================

        :note: If this is not set, the property is undefined and will not be used.
         Use :meth:`~CaptionBarStyle.CaptionStyleUsed` to check if this style is used.
        """

        self._captionStyle = style
        self._captionStyleUsed = True

    def caption_style_used(self):
        """ Checks if the caption style of the caption bar is set."""

        return self._captionStyleUsed

    def get_caption_style(self):
        """
        Returns the caption style for the caption bar.

        :note: Please be warned this will result in an assertion failure
         when this property is not previously set.

        :see: :meth:`~CaptionBarStyle.SetCaptionStyle`, :meth:`~CaptionBarStyle.CaptionStyleUsed`
        """

        return self._captionStyle


class StaticCaptionBar(BufferedWindow):
    """
    This class is a graphical caption component that consists of a
    caption and a clickable arrow.

    The :class:`CaptionBar` fires an event ``EVT_CAPTIONBAR`` which is a
    :class:`CaptionBarEvent`. This event can be caught and the parent window
    can act upon the collapsed or expanded state of the bar (which is
    actually just the icon which changed). The parent panel can
    reduce size or expand again.
    """

    def __init__(self, parent, wx_id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, caption="",
                 icon_size=(16, 16), cbstyle=None):
        """
        Default class constructor.

        :param parent: the :class:`CaptionBar` parent window;
        :param wx_id: an identifier for the control: a value of -1 is taken to mean a default;
        :param pos: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param size: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param caption: the string to be displayed in :class:`CaptionBar`;
        :param cbstyle: the :class:`CaptionBar` window style. Must be an instance of
         :class:`CaptionBarStyle`;
        :param icon_size: the :class:`CaptionBar` icon width;
        """
        self._isReady = False
        BufferedWindow.__init__(self, parent, wx_id, pos=pos, size=(20, 20), style=wx.NO_BORDER)
        self._style: CaptionBarStyle = None
        self.apply_caption_style(cbstyle, True)
        self._caption = caption
        self._iconWidth, self._iconHeight = icon_size
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_bg)
        self._isReady = True

    def set_caption_text(self, text):
        self._caption = text
        self.update_drawing()

    def apply_caption_style(self, cbstyle=None, apply_default=True):
        """
        Applies the style defined in `cbstyle` to the :class:`CaptionBar`.

        :param cbstyle: an instance of :class:`CaptionBarStyle`;
        :param apply_default: if ``True``, the colours used in the :class:`CaptionBarStyle`
         will be reset to their default values.
        """

        if cbstyle is None:
            cbstyle = CaptionBarStyle()

        _new_style = cbstyle

        if apply_default:

            # get first colour from style or make it default
            if not _new_style.first_colour_used():
                _new_style.set_first_colour(wx.Colour('#eee'))

            # get second colour from style or make it default
            if not _new_style.second_colour_used():
                # make the second colour slightly darker then the background
                _colour = self.GetParent().GetBackgroundColour()
                _r, _g, _b = int(_colour.Red()), int(_colour.Green()), int(_colour.Blue())
                _colour = ((_r >> 1) + 20, (_g >> 1) + 20, (_b >> 1) + 20)
                _new_style.set_second_colour(wx.Colour(*_colour))

            # get text colour
            if not _new_style.caption_colour_used():
                _new_style.set_caption_colour(wx.BLACK)

            # get font colour
            if not _new_style.caption_font_used():
                _font = gui_util_get_default_font(8)
                _new_style.set_caption_font(_font)

            # apply caption style
            if not _new_style.caption_style_used():
                _new_style.set_caption_style(CaptionBarStyle.CAPTIONBAR_GRADIENT_V)

        self._style = _new_style

    def set_caption_style(self, cbstyle=None, apply_default=True):
        """
        Sets :class:`CaptionBar` styles with :class:`CaptionBarStyle` class.

        :param cbstyle: an instance of :class:`CaptionBarStyle`;
        :param apply_default: if ``True``, the colours used in the :class:`CaptionBarStyle`
         will be reset to their default values.

        :note: All styles that are actually set, are applied. If you set `applyDefault`
         to ``True``, all other (not defined) styles will be set to default. If it is
         ``False``, the styles which are not set in the :class:`CaptionBarStyle` will be ignored.
        """

        if cbstyle is None:
            cbstyle = CaptionBarStyle()

        self.apply_caption_style(cbstyle, apply_default)
        self.Refresh()

    def get_caption_style(self):
        """
        Returns the current style of the captionbar in a :class:`CaptionBarStyle` class.

        :note: This can be used to change and set back the changes.
        """

        return self._style

    def set_bold_font(self):
        """ Sets the :class:`CaptionBar` font weight to bold."""

        self.GetFont().SetWeight(wx.FONTWEIGHT_BOLD)

    def set_normal_font(self):
        """ Sets the :class:`CaptionBar` font weight to normal."""

        self.GetFont().SetWeight(wx.FONTWEIGHT_NORMAL)

    def draw(self, dc):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`CaptionBar`.

        :param dc: a :class:`wx.Dc` to be processed.
        """
        if self._isReady:
            self.fill_caption_background(dc)
            dc.SetFont(self._style.get_caption_font())
            dc.SetTextForeground(self._style.get_caption_colour())
            dc.DrawText(self._caption, 4, 4)

    def fill_caption_background(self, dc):
        """
        Fills the background of the caption with either a gradient or
        a solid colour.

        :param dc: an instance of :class:`wx.DC`.
        """

        _style = self._style.get_caption_style()

        if _style == CaptionBarStyle.CAPTIONBAR_GRADIENT_V:
            self.draw_vertical_gradient(dc, self.GetRect())
        elif _style == CaptionBarStyle.CAPTIONBAR_GRADIENT_H:
            self.draw_horizontal_gradient(dc, self.GetRect())
        elif _style == CaptionBarStyle.CAPTIONBAR_SINGLE:
            self.draw_single_colour(dc, self.GetRect())
        elif _style == CaptionBarStyle.CAPTIONBAR_RECTANGLE or _style == CaptionBarStyle.CAPTIONBAR_FILLED_RECTANGLE:
            self.draw_single_rectangle(dc, self.GetRect())
        else:
            raise Exception("STYLE Error: Undefined Style Selected: " + repr(_style))

    def DoGetBestSize(self):
        """
        Returns the best size for this panel, based upon the font
        assigned to this window, and the caption string.

        :note: Overridden from :class:`wx.Window`.
        """
        _y, _x = self.GetTextExtent(self._caption)

        if _x < self._iconWidth:
            _x = self._iconWidth

        if _y < self._iconHeight:
            _y = self._iconHeight

        return wx.Size(_x, _y)

    def draw_vertical_gradient(self, dc, rect):
        """
        Gradient fill from colour 1 to colour 2 from top to bottom.

        :param dc: an instance of :class:`wx.DC`;
        :param rect: the :class:`CaptionBar` client rectangle.
        """

        if rect.height < 1 or rect.width < 1:
            return
        dc.SetPen(wx.TRANSPARENT_PEN)
        # calculate gradient coefficients
        _col2 = self._style.get_second_colour()
        _col1 = self._style.get_first_colour()
        dc.GradientFillLinear(rect, _col1, _col2, wx.NORTH)

    def draw_horizontal_gradient(self, dc, rect):
        """
        Gradient fill from colour 1 to colour 2 from left to right.

        :param dc: an instance of :class:`wx.DC`;
        :param rect: the :class:`CaptionBar` client rectangle.
        """

        if rect.height < 1 or rect.width < 1:
            return
        dc.SetPen(wx.TRANSPARENT_PEN)
        _col2 = self._style.get_second_colour()
        _col1 = self._style.get_first_colour()
        dc.GradientFillLinear(rect, _col1, _col2, wx.WEST)

    def draw_single_colour(self, dc, rect):
        """
        Single colour fill for :class:`CaptionBar`.

        :param dc: an instance of :class:`wx.DC`;
        :param rect: the :class:`CaptionBar` client rectangle.
        """

        if rect.height < 1 or rect.width < 1:
            return

        dc.SetPen(wx.TRANSPARENT_PEN)

        # draw simple rectangle
        dc.SetBrush(wx.Brush(self._style.get_first_colour(), wx.BRUSHSTYLE_SOLID))
        dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)

    def draw_single_rectangle(self, dc, rect):
        """
        Single rectangle for :class:`CaptionBar`.

        :param dc: an instance of :class:`wx.DC`;
        :param rect: the :class:`CaptionBar` client rectangle.
        """

        if rect.height < 2 or rect.width < 1:
            return

        # single frame, set up internal fill colour

        if self._style.get_caption_style() == CaptionBarStyle.CAPTIONBAR_RECTANGLE:
            _colour = self.GetParent().GetBackgroundColour()
            _br = wx.Brush(_colour, wx.BRUSHSTYLE_SOLID)
        else:
            _colour = self._style.get_first_colour()
            _br = wx.Brush(_colour, wx.BRUSHSTYLE_SOLID)

        # setup the pen frame

        _pen = wx.Pen(self._style.get_second_colour())
        dc.SetPen(_pen)
        dc.SetBrush(_br)
        dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height - 1)

        _bgpen = wx.Pen(self.GetParent().GetBackgroundColour())
        dc.SetPen(_bgpen)
        dc.DrawLine(rect.x, rect.y + rect.height - 1, rect.x + rect.width,
                    rect.y + rect.height - 1)

    def on_erase_bg(self, evt):
        evt.Skip()
