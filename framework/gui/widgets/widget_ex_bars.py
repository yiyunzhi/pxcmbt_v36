import wx
from wx.lib.agw import aui


class ExtAuiToolbar(aui.AuiToolBar):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, agwStyle=aui.AUI_TB_DEFAULT_STYLE):
        aui.AuiToolBar.__init__(self, parent, id, pos, size, style=style, agwStyle=agwStyle)

    def GetLabelSize(self, label):
        dc = wx.ClientDC(self)
        dc.SetFont(self.GetFont())
        return aui.GetLabelSize(dc, label, self._tool_orientation != aui.AUI_TBTOOL_HORIZONTAL)

    def OnPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        cli_rect = wx.Rect(wx.Point(0, 0), self.GetClientSize())

        horizontal = True
        if self._agwStyle & aui.AUI_TB_VERTICAL:
            horizontal = False

        if self._agwStyle & aui.AUI_TB_PLAIN_BACKGROUND:
            self._art.DrawPlainBackground(dc, self, cli_rect)
        else:
            self._art.DrawBackground(dc, self, cli_rect, horizontal)

        gripper_size = self._art.GetElementSize(aui.AUI_TBART_GRIPPER_SIZE)
        dropdown_size = self._art.GetElementSize(aui.AUI_TBART_OVERFLOW_SIZE)

        # paint the gripper
        if self._agwStyle & aui.AUI_TB_GRIPPER and gripper_size > 0 and self._gripper_sizer_item:
            gripper_rect = wx.Rect(*self._gripper_sizer_item.GetRect())
            if horizontal:
                gripper_rect.width = gripper_size
            else:
                gripper_rect.height = gripper_size

            self._art.DrawGripper(dc, self, gripper_rect)

        # calculated how far we can draw items
        if horizontal:
            last_extent = cli_rect.width
        else:
            last_extent = cli_rect.height

        if self._overflow_visible:
            last_extent -= dropdown_size

        # paint each individual tool
        # local opts
        _art = self._art
        DrawSeparator, DrawLabel, DrawButton, DrawDropDownButton, DrawControlLabel = (
            _art.DrawSeparator, _art.DrawLabel, _art.DrawButton,
            _art.DrawDropDownButton, _art.DrawControlLabel)
        for item in self._items:

            if not item.sizer_item:
                continue

            item_rect = wx.Rect(*item.sizer_item.GetRect())

            if (horizontal and item_rect.x + item_rect.width >= last_extent) or \
                    (not horizontal and item_rect.y + item_rect.height >= last_extent):
                break

            item_kind = item.kind
            if item_kind == wx.ITEM_SEPARATOR:
                # draw a separator
                DrawSeparator(dc, self, item_rect)

            elif item_kind == aui.ITEM_LABEL:
                # draw a text label only
                DrawLabel(dc, self, item, item_rect)

            elif item_kind == aui.ITEM_NORMAL:
                # draw a regular button or dropdown button
                if not item.dropdown:
                    DrawButton(dc, self, item, item_rect)
                else:
                    DrawDropDownButton(dc, self, item, item_rect)

            elif item_kind == aui.ITEM_CHECK:
                # draw a regular toggle button or a dropdown one
                if not item.dropdown:
                    DrawButton(dc, self, item, item_rect)
                else:
                    DrawDropDownButton(dc, self, item, item_rect)

            elif item_kind == aui.ITEM_RADIO:
                # draw a toggle button
                if not item.dropdown:
                    DrawButton(dc, self, item, item_rect)
                else:
                    DrawDropDownButton(dc, self, item, item_rect)

            elif item_kind == aui.ITEM_CONTROL:
                # draw the control's label
                DrawControlLabel(dc, self, item, item_rect)

            # fire a signal to see if the item wants to be custom-rendered
            self.OnCustomRender(dc, item, item_rect)

        # paint the overflow button
        if dropdown_size > 0 and self.GetOverflowVisible():
            dropdown_rect = self.GetOverflowRect()
            _art.DrawOverflowButton(dc, self, dropdown_rect, self._overflow_state)


class ExtStatusBar(wx.StatusBar):
    # Horizontal Alignment Constants
    ALIGN_CENTER_VERTICAL = 1
    ALIGN_TOP = 2
    ALIGN_BOTTOM = 3

    # Vertical Alignment Constants
    ALIGN_CENTER_HORIZONTAL = 11
    ALIGN_LEFT = 12
    ALIGN_RIGHT = 13

    # Exact Fit (Either Horizontal Or Vertical Or Both) Constant
    EXACT_FIT = 20

    def __init__(self, parent, wx_id=wx.ID_ANY, style=wx.STB_SIZEGRIP,
                 name='ExtStatusBar'):
        wx.StatusBar.__init__(self, parent, wx_id, style, name)

        self._widgets = {}
        self._curIdx = 0
        self.Bind(wx.EVT_SIZE, self.on_size)
        wx.CallAfter(self.on_size, None)

    def on_size(self, event):
        """Handles The wx.EVT_SIZE Events For The StatusBar.

        Actually, All The Calculations Linked To HorizontalAlignment And
        VerticalAlignment Are Done In This Function."""

        for idx, item in self._widgets.items():
            _widget, _idx, _h_align, _v_align = item
            _widget_pos = _widget.GetPosition()
            _widget_size = _widget.GetSize()
            _rect = self.GetFieldRect(idx)
            if _widget_size[1] == 0:
                _widget.SetSize((_rect.width - 2, _rect.height - 2))
            if _h_align == self.EXACT_FIT:
                if _v_align == self.EXACT_FIT:
                    _widget.SetSize((_rect.width - 2, _rect.height - 2))
                    _widget.SetPosition((_rect.x - 1, _rect.y - 1))
                elif _v_align == self.ALIGN_CENTER_VERTICAL:
                    if _widget_size[1] < _rect.width - 1:
                        _diff_y = (_rect.height - _widget_size[1]) / 2
                        _widget.SetSize((_rect.width - 2, _widget_size[1]))
                        _widget.SetPosition((_rect.x - 1, _rect.y + _diff_y))
                    else:
                        _widget.SetSize((_rect.width - 2, _widget_size[1]))
                        _widget.SetPosition((_rect.x - 1, _rect.y - 1))
                elif _v_align == self.ALIGN_TOP:
                    _widget.SetSize((_rect.width - 2, _widget_size[1]))
                    _widget.SetPosition((_rect.x - 1, _rect.y))
                elif _v_align == self.ALIGN_BOTTOM:
                    _widget.SetSize((_rect.width - 2, _widget_size[1]))
                    _widget.SetPosition((_rect.x - 1, _rect.height - _widget_size[1]))

            elif _h_align == self.ALIGN_LEFT:
                _x_pos = _rect.x - 1
                if _v_align == self.EXACT_FIT:
                    _widget.SetSize((_widget_size[0], _rect.height - 2))
                    _widget.SetPosition((_x_pos, _rect.y - 1))
                elif _v_align == self.ALIGN_CENTER_VERTICAL:
                    if _widget_size[1] < _rect.height - 1:
                        _diff_y = (_rect.height - _widget_size[1]) / 2
                        _widget.SetPosition((_x_pos, _rect.y + _diff_y))
                    else:
                        _widget.SetSize((_widget_size[0], _rect.height - 2))
                        _widget.SetPosition((_x_pos, _rect.y - 1))
                elif _v_align == self.ALIGN_TOP:
                    _widget.SetPosition((_x_pos, _rect.y))
                elif _v_align == self.ALIGN_BOTTOM:
                    _widget.SetPosition((_x_pos, _rect.height - _widget_size[1]))
            elif _h_align == self.ALIGN_RIGHT:
                _x_pos = _rect.x + _rect.width - _widget_size[0] - 1
                if _v_align == self.EXACT_FIT:
                    _widget.SetSize((_widget_size[0], _rect.height - 2))
                    _widget.SetPosition((_x_pos, _rect.y - 1))
                elif _v_align == self.ALIGN_CENTER_VERTICAL:
                    if _widget_size[1] < _rect.height - 1:
                        _diff_y = (_rect.height - _widget_size[1]) / 2
                        _widget.SetPosition((_x_pos, _rect.y + _diff_y))
                    else:
                        _widget.SetSize((_widget_size[0], _rect.height - 2))
                        _widget.SetPosition((_x_pos, _rect.y - 1))
                elif _v_align == self.ALIGN_TOP:
                    _widget.SetPosition((_x_pos, _rect.y))
                elif _v_align == self.ALIGN_BOTTOM:
                    _widget.SetPosition((_x_pos, _rect.height - _widget_size[1]))
            elif _h_align == self.ALIGN_CENTER_HORIZONTAL:
                _x_pos = _rect.x + (_rect.width - _widget_size[0]) / 2 - 1
                if _v_align == self.EXACT_FIT:
                    _widget.SetSize((_widget_size[0], _rect.height))
                    _widget.SetPosition((_x_pos, _rect.y))
                elif _v_align == self.ALIGN_CENTER_VERTICAL:
                    if _widget_size[1] < _rect.height - 1:
                        _diff_y = (_rect.height - _widget_size[1]) / 2
                        _widget.SetPosition((_x_pos, _rect.y + _diff_y))
                    else:
                        _widget.SetSize((_widget_size[0], _rect.height - 1))
                        _widget.SetPosition((_x_pos, _rect.y + 1))
                elif _v_align == self.ALIGN_TOP:
                    _widget.SetPosition((_x_pos, _rect.y))
                elif _v_align == self.ALIGN_BOTTOM:
                    _widget.SetPosition((_x_pos, _rect.height - _widget_size[1]))

        if event is not None:
            event.Skip()

    def add_widget(self, widget, index=-1, h_align=ALIGN_CENTER_HORIZONTAL, v_align=ALIGN_CENTER_VERTICAL):
        if index == -1:
            index = self._curIdx
            self._curIdx += 1

        if self.GetFieldsCount() <= index:
            raise "\nERROR: EnhancedStatusBar has a max of %d items, you tried to set item #%d" % (
                self.GetFieldsCount(), index)

        if h_align not in [self.ALIGN_CENTER_HORIZONTAL, self.EXACT_FIT,
                           self.ALIGN_LEFT, self.ALIGN_RIGHT]:
            raise AssertionError('invalid horizontal alignment')

        if v_align not in [self.ALIGN_CENTER_VERTICAL, self.EXACT_FIT,
                           self.ALIGN_TOP, self.ALIGN_BOTTOM]:
            raise AssertionError('invalid vertical alignment')

        try:
            self.RemoveChild(self._widgets[index].widget)
            self._widgets[index].widget.Destroy()
        except KeyError:
            pass
        self._widgets[index] = (widget, index, h_align, v_align)

        wx.CallAfter(self.on_size, None)
