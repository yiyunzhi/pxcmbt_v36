import wx
import wx.propgrid as wxpg
from framework.application.base import PropertyDef
from .property_ext import PyObjectPGProperty, SizePGProperty, SingleChoicePGProperty, SingleChoiceAndButtonPGProperty


class CategoryPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.editor = wxpg.PropertyCategory

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name)
        return self.editorInstance

    def set_editor_value(self, val):
        pass

    def get_editor_value(self):
        return None

    def set_value(self, val):
        pass

    def get_value(self):
        return None


class ArrayStringPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        assert isinstance(self.value, list)
        self.editor = wxpg.ArrayStringProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.value)
        return self.editorInstance


class BoolPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.editor = wxpg.BoolProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.value)
        if not self.options:
            self.editorInstance.SetAttribute('UseCheckbox', True)
        return self.editorInstance


class ColorPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.editor = wxpg.ColourProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.value)
        return self.editorInstance


class CursorPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.editor = wxpg.CursorProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.value)
        return self.editorInstance


class DatePropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.editor = wxpg.DateProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.value)
        return self.editorInstance


class DirPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.editor = wxpg.DirProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.value)
        return self.editorInstance


class EditEnumPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.labels = kwargs.get('labels')
        self.values = kwargs.get('values')
        self.editor = wxpg.EditEnumProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.labels, self.values, self.value)
        return self.editorInstance


class EnumPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.labels = kwargs.get('labels')
        self.values = kwargs.get('values')
        self.editor = wxpg.EnumProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.labels, self.values, self.value)
        return self.editorInstance


class FilePropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.editor = wxpg.FileProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.value)
        return self.editorInstance


class FlagsPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.labels = kwargs.get('labels')
        self.values = kwargs.get('values')
        self.editor = wxpg.FlagsProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.labels, self.values, self.value)
        if not self.options:
            self.editorInstance.SetAttribute('Bool_with_Checkbox', True)
            self.editorInstance.SetAttribute('UseCheckbox', True)
        return self.editorInstance


class FloatPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.editor = wxpg.FloatProperty
        self.max = kwargs.get('max', float('inf'))
        self.min = kwargs.get('min', -float('inf'))
        self.precision = kwargs.get('precision', 2)
        self.useSpin=kwargs.get('use_spin',False)

    def get_editor_instance(self):
        if self.value is None:
            _val = 0.0
        else:
            _val = self.value
        self.editorInstance = self.editor(self.label, self.name, _val)
        if self.useSpin:
            self.editorInstance.SetEditor('SpinCtrl')
        self.editorInstance.SetAttribute(wxpg.PG_ATTR_MIN, self.min)
        self.editorInstance.SetAttribute(wxpg.PG_ATTR_MAX, self.max)
        self.editorInstance.SetAttribute(wxpg.PG_FLOAT_PRECISION, self.precision)
        return self.editorInstance


class FontPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        assert isinstance(self.value, wx.Font)
        self.editor = wxpg.FontProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.value)
        return self.editorInstance


class ImageFilePropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.editor = wxpg.ImageFileProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.value)
        return self.editorInstance


class IntPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.editor = wxpg.IntProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.value)
        return self.editorInstance


class LongStringPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.editor = wxpg.LongStringProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.value)
        return self.editorInstance


class MultiChoicePropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.values = kwargs.get('values')
        assert isinstance(self.value, list)
        assert isinstance(self.values, list)

        self.editor = wxpg.MultiChoiceProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.values, self.value)
        return self.editorInstance


class PyObjPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.editor = PyObjectPGProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.value)
        return self.editorInstance


class SingleChoicePropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.labels = kwargs.get('labels', [])
        self.editor = SingleChoicePGProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.labels, self.name, self.value)
        return self.editorInstance


class SingleChoiceAndButtonPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.values = kwargs.get('values', [])
        self.editor = SingleChoiceAndButtonPGProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.values, self.name, self.value)
        return self.editorInstance


class StringPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        if self.value is None: self.value = ''
        self.editor = wxpg.StringProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, str(self.value))
        return self.editorInstance


class XYPropertyDef(PropertyDef):
    def __init__(self, **kwargs):
        PropertyDef.__init__(self, **kwargs)
        self.editor = SizePGProperty

    def get_editor_instance(self):
        self.editorInstance = self.editor(self.label, self.name, self.value)
        return self.editorInstance

    def set_value(self, val):
        if val is None:
            return
        if self.editorInstance is not None:
            if not isinstance(val, wx.Point):
                self.editorInstance.SetValue(wx.Point(*val))
            else:
                self.editorInstance.SetValue(val)
        super().set_value(val)
