# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : property_ext.py
# ------------------------------------------------------------------------------
#
# File          : property_ext.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import sys
import wx, collections
import wx.propgrid as wxpg


class SizePGProperty(wxpg.PGProperty):
    """ Demonstrates a property with few children.
    """

    def __init__(self, label, name=wxpg.PG_LABEL, value=wx.Size(0, 0)):
        wxpg.PGProperty.__init__(self, label, name)
        _value = self._convert_value(value)
        self.AddPrivateChild(wxpg.IntProperty("X", value=_value.x))
        self.AddPrivateChild(wxpg.IntProperty("Y", value=_value.y))
        self.m_value = _value

    def GetClassName(self):
        return self.__class__.__name__

    def DoGetEditorClass(self):
        return wxpg.PropertyGridInterface.GetEditorByName("TextCtrl")

    def RefreshChildren(self):
        _size = self._convert_value(self.m_value)
        self.Item(0).SetValue(_size.x)
        self.Item(1).SetValue(_size.y)

    def ValueToString(self, value, flag=0):
        _value = self._convert_value(value)
        return '(%s,%s)' % (_value.x, _value.y)

    def _convert_value(self, value):
        """
        Utility convert arbitrary value to a real wx.Size.
        """
        if isinstance(value, collections.Sequence) or hasattr(value, '__getitem__'):
            value = wx.Size(*value)
        return value

    def ChildChanged(self, this_value, child_index, child_value):
        _size = self._convert_value(self.m_value)
        if child_index == 0:
            _size.x = child_value
        elif child_index == 1:
            _size.y = child_value
        else:
            raise AssertionError

        return _size


class PyObjectPGProperty(wxpg.PGProperty):
    """
    Another simple example. This time our value is a PyObject.
    NOTE: We can't return an arbitrary python object in DoGetValue. It cannot
          be a simple type such as int, bool, double, or string, nor an array
          or wxObject based. Dictionary, None, or any user-specified Python
          class is allowed.
    """

    def __init__(self, label, name=wxpg.PG_LABEL, value=None):
        wxpg.PGProperty.__init__(self, label, name)
        self.SetValue(value)

    def GetClassName(self):
        return self.__class__.__name__

    def GetEditor(self):
        return "TextCtrl"

    def ValueToString(self, value, flags=0):
        return repr(value)

    def StringToValue(self, s, flags=0):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        v = list(s)
        return True, v


class SingleChoiceDialogAdapter(wxpg.PGEditorDialogAdapter):
    """ This demonstrates use of wxpg.PGEditorDialogAdapter.
    """

    def __init__(self, choices):
        wxpg.PGEditorDialogAdapter.__init__(self)
        self.choices = choices

    def DoShowDialog(self, prop_grid: wxpg.PropertyGrid, property: wxpg.PGProperty):
        _s = wx.GetSingleChoice("Chose one for %s" % property.GetLabel(), "SingleChoice", self.choices)
        if _s:
            self.SetValue(_s)
            return True
        return False


class SingleChoicePGProperty(wxpg.PGProperty):
    def __init__(self, label, labels: list,name=wxpg.PG_LABEL, value=''):
        wxpg.PGProperty.__init__(self, label, name)
        # Prepare choices
        self.choices = wxpg.PGChoices(labels)
        self.SetChoices(self.choices)
        self.SetChoiceSelection(self.choices.Index(value))

    def DoGetEditorClass(self):
        return wxpg.PGEditor_Choice

    def ValueToString(self, value, arg_flags=0):
        return self.choices.GetLabel(value)

    def StringToValue(self, text, arg_flags=0):
        return self.choices.GetValue(self.choices.Index(text))


class SingleChoiceAndButtonPGProperty(wxpg.StringProperty):
    def __init__(self, label, values: list, name=wxpg.PG_LABEL, value=''):
        wxpg.StringProperty.__init__(self, label, name, value)
        # Prepare choices
        self.choices = values

    def DoGetEditorClass(self):
        return wxpg.PGEditor_TextCtrlAndButton

    def GetEditorDialog(self):
        # Set what happens on button click
        return SingleChoiceDialogAdapter(self.choices)
#
# Let's use some simple custom editor
#
# NOTE: Editor must be registered *before* adding a property that
# uses it.
# if not getattr(sys, '_PropGridEditorsRegistered', False):
#     wxpg.RegisterEditor(TrivialPropertyEditor)
#     wxpg.RegisterEditor(SampleMultiButtonEditor)
#     wxpg.RegisterEditor(LargeImageEditor)
#     # ensure we only do it once
#     sys._PropGridEditorsRegistered = True
