import wx, keyword
import wx.stc as stc
from ..base.define import SCRIPT_EDITOR_FACES


class JsonSTC(stc.StyledTextCtrl):
    fold_symbols = 3

    def __init__(self, parent, wx_id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0):
        stc.StyledTextCtrl.__init__(self, parent, wx_id, pos, size, style)
        self.customKW = list()
        self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        self.SetLexer(stc.STC_LEX_JSON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetMargins(0, 0)

        self.SetViewWhiteSpace(False)
        # self.SetBufferedDraw(False)
        # self.SetViewEOL(True)
        # self.SetEOLMode(stc.STC_EOL_CRLF)
        # self.SetUseAntiAliasing(True)

        self.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        self.SetEdgeColumn(78)

        # Setup a margin to hold fold markers
        # self.SetFoldFlags(16)  ###  WHAT IS THIS VALUE?  WHAT ARE THE OTHER FLAGS?  DOES IT MATTER?
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        if self.fold_symbols == 0:
            # Arrow pointing right for contracted folders, arrow pointing down for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_ARROWDOWN, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_ARROW, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

        elif self.fold_symbols == 1:
            # Plus for contracted folders, minus for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_MINUS, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_PLUS, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

        elif self.fold_symbols == 2:
            # Like a flattened tree control using circular headers and curved joins
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_CIRCLEMINUS, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_CIRCLEPLUS, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNERCURVE, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_CIRCLEPLUSCONNECTED, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE, "white", "#404040")

        elif self.fold_symbols == 3:
            # Like a flattened tree control using square headers
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, "white", "#808080")

        self.Bind(stc.EVT_STC_UPDATEUI, self.on_update_ui)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.on_margin_click)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_pressed)

        # Make some styles,  The lexer defines what each style is used for, we
        # just have to define what each style looks like.  This set is adapted from
        # Scintilla sample property files.

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % SCRIPT_EDITOR_FACES)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % SCRIPT_EDITOR_FACES)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % SCRIPT_EDITOR_FACES)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % SCRIPT_EDITOR_FACES)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FF0000,bold")

        # Json styles
        # Default
        self.StyleSetSpec(stc.STC_JSON_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Comments
        self.StyleSetSpec(stc.STC_JSON_BLOCKCOMMENT, "fore:#007F00,face:%(other)s,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Number
        self.StyleSetSpec(stc.STC_JSON_NUMBER, "fore:#007F7F,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # String
        self.StyleSetSpec(stc.STC_JSON_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Keyword
        self.StyleSetSpec(stc.STC_JSON_KEYWORD, "fore:#00007F,bold,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Operators
        self.StyleSetSpec(stc.STC_JSON_OPERATOR, "bold,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_JSON_STRINGEOL,
                          "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % SCRIPT_EDITOR_FACES)

        self.SetCaretForeground("BLUE")

        # register some images for use in the AutoComplete box.
        # self.RegisterImage(1, images.Smiles.GetBitmap())
        self.RegisterImage(2,
                           wx.ArtProvider.GetBitmap(wx.ART_NEW, size=(16, 16)))
        self.RegisterImage(3,
                           wx.ArtProvider.GetBitmap(wx.ART_COPY, size=(16, 16)))

    def show_line_number(self, state):
        # show the line number
        if state:
            self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
            self.SetMarginWidth(1, 25)
        else:
            self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
            self.SetMarginWidth(1, 0)

    def on_key_pressed(self, event):
        if self.CallTipActive():
            self.CallTipCancel()
        _key = event.GetKeyCode()

        if _key == 32 and event.ControlDown():
            # if equal space
            _pos = self.GetCurrentPos()

            # Tips
            if event.ShiftDown():
                self.CallTipSetBackground("yellow")
                self.CallTipShow(_pos, 'lots of of text: blah, blah, blah\n\n'
                                       'show some suff, maybe parameters..\n\n'
                                       'fubar(param1, param2)')
            # Code completion
            else:
                # lst = []
                # for x in range(50000):
                #    lst.append('%05d' % x)
                # st = " ".join(lst)
                # print(len(st))
                # self.AutoCompShow(0, st)

                _kw = keyword.kwlist[:]
                _kw += self.customKW
                _kw.sort()  # Python sorts are case sensitive
                self.AutoCompSetIgnoreCase(False)  # so this needs to match

                # Images are specified with a appended "?type"
                for i in range(len(_kw)):
                    if _kw[i] in keyword.kwlist:
                        _kw[i] = _kw[i] + "?1"

                self.AutoCompShow(0, " ".join(_kw))
        else:
            event.Skip()

    def on_update_ui(self, evt):
        # check for matching braces
        _brace_at_caret = -1
        _brace_opposite = -1
        _char_before = None
        _caret_pos = self.GetCurrentPos()

        if _caret_pos > 0:
            _char_before = self.GetCharAt(_caret_pos - 1)
            _style_before = self.GetStyleAt(_caret_pos - 1)

        # check before
        if _char_before and chr(_char_before) in "[]{}()" and _style_before == stc.STC_P_OPERATOR:
            _brace_at_caret = _caret_pos - 1

        # check after
        if _brace_at_caret < 0:
            _char_after = self.GetCharAt(_caret_pos)
            _style_after = self.GetStyleAt(_caret_pos)

            if _char_after and chr(_char_after) in "[]{}()" and _style_after == stc.STC_P_OPERATOR:
                _brace_at_caret = _caret_pos

        if _brace_at_caret >= 0:
            _brace_opposite = self.BraceMatch(_brace_at_caret)

        if _brace_at_caret != -1 and _brace_opposite == -1:
            self.BraceBadLight(_brace_at_caret)
        else:
            self.BraceHighlight(_brace_at_caret, _brace_opposite)
            # pt = self.PointFromPosition(braceOpposite)
            # self.Refresh(True, wxRect(pt.x, pt.y, 5,5))
            # print(pt)
            # self.Refresh(False)

    def on_margin_click(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll(None)
            else:
                _line_clicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(_line_clicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(_line_clicked, True)
                        self.Expand(_line_clicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(_line_clicked):
                            self.SetFoldExpanded(_line_clicked, False)
                            self.Expand(_line_clicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(_line_clicked, True)
                            self.Expand(_line_clicked, True, True, 100)
                    else:
                        self.ToggleFold(_line_clicked)

    def FoldAll(self, action):
        _line_count = self.GetLineCount()
        _expanding = True

        # find out if we are folding or unfolding
        for line_num in range(_line_count):
            if self.GetFoldLevel(line_num) & stc.STC_FOLDLEVELHEADERFLAG:
                _expanding = not self.GetFoldExpanded(line_num)
                break
        _line_num = 0
        while _line_num < _line_count:
            _level = self.GetFoldLevel(_line_num)
            if _level & stc.STC_FOLDLEVELHEADERFLAG and (_level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:
                if _expanding:
                    self.SetFoldExpanded(_line_num, True)
                    _line_num = self.Expand(_line_num, True)
                    _line_num = _line_num - 1
                else:
                    _last_child = self.GetLastChild(_line_num, -1)
                    self.SetFoldExpanded(_line_num, False)
                    if _last_child > _line_num:
                        self.HideLines(_line_num + 1, _last_child)
            _line_num += 1

    def Expand(self, line, do_expand, force=False, vis_levels=0, level=-1):
        _last_child = self.GetLastChild(line, level)
        _line = line + 1
        while line <= _last_child:
            if force:
                if vis_levels > 0:
                    self.ShowLines(_line, _line)
                else:
                    self.HideLines(_line, _line)
            else:
                if do_expand:
                    self.ShowLines(_line, _line)
            if level == -1:
                level = self.GetFoldLevel(_line)
            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if vis_levels > 1:
                        self.SetFoldExpanded(_line, True)
                    else:
                        self.SetFoldExpanded(_line, False)
                    _line = self.Expand(line, do_expand, force, vis_levels - 1)

                else:
                    if do_expand and self.GetFoldExpanded(line):
                        _line = self.Expand(_line, True, force, vis_levels - 1)
                    else:
                        _line = self.Expand(_line, False, force, vis_levels - 1)
            else:
                _line += 1

        return _line


class PythonSTC(stc.StyledTextCtrl):
    fold_symbols = 3

    def __init__(self, parent, wx_id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0):
        stc.StyledTextCtrl.__init__(self, parent, wx_id, pos, size, style)
        self.customKW = list()
        self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        self.SetUseTabs(True)
        self.SetTabIndents(True)
        self.SetTabWidth(4)

        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetMargins(0, 0)

        self.SetViewWhiteSpace(False)
        # self.SetBufferedDraw(False)
        # self.SetViewEOL(True)
        # self.SetEOLMode(stc.STC_EOL_CRLF)
        self.SetUseAntiAliasing(True)

        self.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        self.SetEdgeColumn(78)

        # Setup a margin to hold fold markers
        # self.SetFoldFlags(16)  ###  WHAT IS THIS VALUE?  WHAT ARE THE OTHER FLAGS?  DOES IT MATTER?
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        if self.fold_symbols == 0:
            # Arrow pointing right for contracted folders, arrow pointing down for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_ARROWDOWN, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_ARROW, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

        elif self.fold_symbols == 1:
            # Plus for contracted folders, minus for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_MINUS, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_PLUS, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

        elif self.fold_symbols == 2:
            # Like a flattened tree control using circular headers and curved joins
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_CIRCLEMINUS, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_CIRCLEPLUS, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNERCURVE, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_CIRCLEPLUSCONNECTED, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE, "white", "#404040")

        elif self.fold_symbols == 3:
            # Like a flattened tree control using square headers
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, "white", "#808080")

        self.Bind(stc.EVT_STC_UPDATEUI, self.on_update_ui)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.on_margin_click)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_pressed)

        # Make some styles,  The lexer defines what each style is used for, we
        # just have to define what each style looks like.  This set is adapted from
        # Scintilla sample property files.

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % SCRIPT_EDITOR_FACES)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % SCRIPT_EDITOR_FACES)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % SCRIPT_EDITOR_FACES)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % SCRIPT_EDITOR_FACES)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FF0000,bold")

        # Python styles
        # Default
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % SCRIPT_EDITOR_FACES)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL,
                          "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % SCRIPT_EDITOR_FACES)

        self.SetCaretForeground("BLUE")

        # register some images for use in the AutoComplete box.
        # self.RegisterImage(1, images.Smiles.GetBitmap())
        self.RegisterImage(2,
                           wx.ArtProvider.GetBitmap(wx.ART_NEW, size=(16, 16)))
        self.RegisterImage(3,
                           wx.ArtProvider.GetBitmap(wx.ART_COPY, size=(16, 16)))

    def show_line_number(self, state):
        # show the line number
        if state:
            self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
            self.SetMarginWidth(1, 25)
        else:
            self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
            self.SetMarginWidth(1, 0)

    def on_key_pressed(self, event):
        if self.CallTipActive():
            self.CallTipCancel()
        _key = event.GetKeyCode()

        if _key == 32 and event.ControlDown():
            # if equal space
            _pos = self.GetCurrentPos()

            # Tips
            if event.ShiftDown():
                self.CallTipSetBackground("yellow")
                self.CallTipShow(_pos, 'lots of of text: blah, blah, blah\n\n'
                                       'show some suff, maybe parameters..\n\n'
                                       'fubar(param1, param2)')
            # Code completion
            else:
                _kw = keyword.kwlist[:]
                _kw += self.customKW
                _kw.sort()  # Python sorts are case sensitive
                self.AutoCompSetIgnoreCase(False)  # so this needs to match

                # Images are specified with a appended "?type"
                for i in range(len(_kw)):
                    if _kw[i] in keyword.kwlist:
                        _kw[i] = _kw[i] + "?1"

                self.AutoCompShow(0, " ".join(_kw))
        else:
            event.Skip()

    def on_update_ui(self, evt):
        # check for matching braces
        _brace_at_caret = -1
        _brace_opposite = -1
        _char_before = None
        _caret_pos = self.GetCurrentPos()

        if _caret_pos > 0:
            _char_before = self.GetCharAt(_caret_pos - 1)
            _style_before = self.GetStyleAt(_caret_pos - 1)

        # check before
        if _char_before and chr(_char_before) in "[]{}()" and _style_before == stc.STC_P_OPERATOR:
            _brace_at_caret = _caret_pos - 1

        # check after
        if _brace_at_caret < 0:
            _char_after = self.GetCharAt(_caret_pos)
            _style_after = self.GetStyleAt(_caret_pos)

            if _char_after and chr(_char_after) in "[]{}()" and _style_after == stc.STC_P_OPERATOR:
                _brace_at_caret = _caret_pos

        if _brace_at_caret >= 0:
            _brace_opposite = self.BraceMatch(_brace_at_caret)

        if _brace_at_caret != -1 and _brace_opposite == -1:
            self.BraceBadLight(_brace_at_caret)
        else:
            self.BraceHighlight(_brace_at_caret, _brace_opposite)
            # pt = self.PointFromPosition(braceOpposite)
            # self.Refresh(True, wxRect(pt.x, pt.y, 5,5))
            # print(pt)
            # self.Refresh(False)

    def on_margin_click(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll(None)
            else:
                _line_clicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(_line_clicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(_line_clicked, True)
                        self.Expand(_line_clicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(_line_clicked):
                            self.SetFoldExpanded(_line_clicked, False)
                            self.Expand(_line_clicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(_line_clicked, True)
                            self.Expand(_line_clicked, True, True, 100)
                    else:
                        self.ToggleFold(_line_clicked)

    def FoldAll(self, action):
        _line_count = self.GetLineCount()
        _expanding = True

        # find out if we are folding or unfolding
        for line_num in range(_line_count):
            if self.GetFoldLevel(line_num) & stc.STC_FOLDLEVELHEADERFLAG:
                _expanding = not self.GetFoldExpanded(line_num)
                break
        _line_num = 0
        while _line_num < _line_count:
            _level = self.GetFoldLevel(_line_num)
            if _level & stc.STC_FOLDLEVELHEADERFLAG and (_level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:
                if _expanding:
                    self.SetFoldExpanded(_line_num, True)
                    _line_num = self.Expand(_line_num, True)
                    _line_num = _line_num - 1
                else:
                    _last_child = self.GetLastChild(_line_num, -1)
                    self.SetFoldExpanded(_line_num, False)
                    if _last_child > _line_num:
                        self.HideLines(_line_num + 1, _last_child)
            _line_num += 1

    def Expand(self, line, do_expand, force=False, vis_levels=0, level=-1):
        _last_child = self.GetLastChild(line, level)
        _line = line + 1
        while line <= _last_child:
            if force:
                if vis_levels > 0:
                    self.ShowLines(_line, _line)
                else:
                    self.HideLines(_line, _line)
            else:
                if do_expand:
                    self.ShowLines(_line, _line)
            if level == -1:
                level = self.GetFoldLevel(_line)
            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if vis_levels > 1:
                        self.SetFoldExpanded(_line, True)
                    else:
                        self.SetFoldExpanded(_line, False)
                    _line = self.Expand(line, do_expand, force, vis_levels - 1)

                else:
                    if do_expand and self.GetFoldExpanded(line):
                        _line = self.Expand(_line, True, force, vis_levels - 1)
                    else:
                        _line = self.Expand(_line, False, force, vis_levels - 1)
            else:
                _line += 1

        return _line
