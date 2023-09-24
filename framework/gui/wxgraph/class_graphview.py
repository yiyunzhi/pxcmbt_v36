# -*- coding: utf-8 -*-
import typing

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : canvas.py
# ------------------------------------------------------------------------------
#
# File          : canvas.py
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
from .class_shape_base import WxShapeBase
from .class_shape_line import LineShape
from .class_shape_data_object import ShapeDataObject
from .class_graphview_gui_mode import BaseGUIMode
from .class_graphscene import GraphScene
from .class_shape_control import ControlShape
from .class_shape_bitmap import BitmapShape
from .class_handle import HandleShapeObject
from .class_shape_text import TextShape
from .class_shape_edit_text import EditTextShape
from .utils import *
from .events import *
from .define import *
from .__version__ import __VERSION__


class GraphViewDropTarget(wx.DropTarget):
    def __init__(self, data, view):
        wx.DropTarget.__init__(self)
        self.data = data
        self.view = view

    def OnData(self, x, y, def_result):
        _data = self.GetData()
        if _data is None:
            return wx.DragNone
        self.view.on_drop(x, y, def_result, self.GetDataObject())
        return def_result


class GraphViewSetting:

    # todo: make it serializable
    def __init__(self, **kwargs):
        self.enableGC = kwargs.get('enableGC', True)
        self.backgroundColor = kwargs.get('backgroundColor', '#f0f0f0')
        self.commonHoverColor = kwargs.get('commonHoverColor', '#7878ff')
        self.gradientFrom = kwargs.get('gradientFrom', '#f0f0f0')
        self.gradientTo = kwargs.get('gradientTo', '#d8d8ff')

        self.gridSize = kwargs.get('gridSize', wx.Size(5, 5))
        self.gridLineMult = kwargs.get('gridLineMult', 20)
        self.gridColor = kwargs.get('gradientTo', '#c8c8ff')
        self.gridStyle = kwargs.get('gridStyle', wx.PENSTYLE_DOT_DASH)

        self.shadowOffset = kwargs.get('shadowOffset', wx.Size(2, 2))
        self.shadowFillColor = kwargs.get('shadowFillColor', wx.Colour(150, 150, 150, 128))
        self.shadowStyle = kwargs.get('shadowFillStyle', wx.BRUSHSTYLE_SOLID)

        self.acceptedShapes = []

        self.scale = kwargs.get('scale', 1.0)
        self.minScale = kwargs.get('minScale', 0.25)
        self.maxScale = kwargs.get('maxScale', 5.0)

        self.style = kwargs.get('style', EnumGraphViewStyleFlag.DEFAULT)

        self.printHAlign = kwargs.get('printHAlign', EnumHAlignFunction.CENTER)
        self.printVAlign = kwargs.get('printVAlign', EnumVAlignFunction.MIDDLE)
        self.printMode = kwargs.get('printMode', EnumPrintMode.FIT_TO_MARGIN)
        self.printData = kwargs.get('printData')
        self.printPageSetupData = kwargs.get('printPageSetupData')

    @property
    def shadowBrush(self):
        return wx.Brush(wx.Colour(*self.shadowFillColor), self.shadowStyle)


class GraphView(wx.ScrolledWindow):
    """
    Class encapsulating a Shape canvas. The shape canvas is window control
    which extends the wxScrolledWindow and is responsible for displaying of shapes scenes.
    It also supports clipboard and drag&drop operations, undo/redo operations,
    and graphics exporting functions.

    This class is a core framework class and provides many member functions suitable for adding,
    removing, moving, resizing and drawing of shape objects. It can be used as it is or as a base class
    if necessary. In that case, the default class functionality can be enhanced by overriding of
    its virtual functions or by manual events handling. In both cases the user is responsible
    for invoking of default event handlers/virtual functions otherwise the
    builtin functionality won't be available.
    """

    def __init__(self, parent, scene: GraphScene, undo_stack=None, setting: GraphViewSetting = None):
        wx.ScrolledWindow.__init__(self, parent)
        self._shapeDataObjectType = None
        self._scene: GraphScene = None
        self._guiMode = BaseGUIMode(self)
        self._invalidateRect = wx.Rect(0, 0, 0, 0)
        self.topMostShapeUnderCursor = None
        self.selectedShapeUnderCursor = None
        self.unselectedShapeUnderCursor = None
        self.mapPrevPositions = dict()
        self.shapesDataFormat = wx.DataFormat()
        self.dndStartedHere = False
        self.dndStartedAt = wx.Point(0, 0)
        self.viewportTopLeft = wx.RealPoint(0, 0)

        self.currentShapes = list()
        self.setting = GraphViewSetting() if setting is None else setting
        self.undoStack = undo_stack
        # initialize
        self.shapesDataFormat.SetId(GV_DAT_FORMAT_ID)
        self.shapeDataObjectType = ShapeDataObject
        self.scene = scene
        self.SetScrollbars(5, 5, 100, 100)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self._guiMode.setup()
        # initialize others
        self._initialize_printing()

    @property
    def scene(self) -> GraphScene:
        return self._scene

    @scene.setter
    def scene(self, scene: GraphScene):
        self._scene = scene
        if scene is not None:
            self._scene.view = self
            self._guiMode.on_scene_updated()

    @property
    def shapeDataObjectType(self):
        return self._shapeDataObjectType

    @shapeDataObjectType.setter
    def shapeDataObjectType(self, type_: type):
        self._shapeDataObjectType = type_
        self.SetDropTarget(GraphViewDropTarget(type_(self.shapesDataFormat), self))

    @property
    def guiMode(self):
        return self._guiMode

    @guiMode.setter
    def guiMode(self, mode):
        if self._guiMode is not None:
            self._guiMode.teardown()
        self._guiMode = mode
        self._guiMode.setup()

    @property
    def gcEnabled(self) -> bool:
        return self.setting.enableGC

    @gcEnabled.setter
    def gcEnabled(self, state):
        self.setting.enableGC = state

    @property
    def backgroundColor(self):
        return self.setting.backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, color: str):
        self.setting.backgroundColor = color

    @property
    def workingState(self):
        return self._guiMode.workingState if self._guiMode else EnumGraphViewWorkingState.READY

    def initial_event_table(self):
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
        self.Bind(wx.EVT_RIGHT_UP, self.on_right_up)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_left_double_clicked)
        self.Bind(wx.EVT_RIGHT_DCLICK, self.on_right_double_clicked)
        self.Bind(wx.EVT_MOTION, self.on_mouse_move)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter_window)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_window)
        self.Bind(wx.EVT_SIZE, self.on_size)
        # self.Bind(wx.EVT_SCROLLWIN, self.on_scroll)

    def export_to_bmp(self, file: typing.IO):
        self.export_to_image(file)

    def export_to_image(self, file: typing.IO, image_type: int = wx.BITMAP_TYPE_BMP, background=True, scale=-1):
        _prev_scale = self.setting.scale
        if scale == -1: scale = _prev_scale
        _bmp_bb = self.get_total_boundingbox()
        _bmp_bb.SetLeft(_bmp_bb.left * scale)
        _bmp_bb.SetTop(_bmp_bb.top * scale)
        _bmp_bb.SetWidth(_bmp_bb.width * scale)
        _bmp_bb.SetHeight(_bmp_bb.height * scale)
        _bmp_bb = _bmp_bb.Inflate(self.setting.gridSize * scale)
        _out_bmp = wx.Bitmap(_bmp_bb.width, _bmp_bb.height)
        _dc = wx.MemoryDC(_out_bmp)
        _out_dc = wx.WindowDC(self)
        _out_dc.SetUserScale(scale, scale)
        if _out_dc.IsOk():
            if scale != _prev_scale:
                self.set_scale(scale)
            _out_dc.SetDeviceOrigin(-_bmp_bb.left, -_bmp_bb.top)
            _prev_style = self.setting.style
            _prev_bg_color = self.setting.backgroundColor
            if not background:
                self.remove_style(EnumGraphViewStyleFlag.GRADIENT_BACKGROUND)
                self.remove_style(EnumGraphViewStyleFlag.GRID_SHOW)
                self.backgroundColor = '#ffffff'
            self.draw_background(_out_dc, False)
            self.draw_content(_out_dc, False)
            self.draw_foreground(_out_dc, False)
            if not background:
                self.set_style(_prev_style)
                self.backgroundColor = _prev_bg_color
            if scale != _prev_scale:
                self.set_scale(_prev_scale)
            if _out_bmp.SaveFile(file, image_type):
                wx.MessageBox('image has been saved to %s' % file.name, 'Info')
            else:
                wx.MessageBox('unable save image to %s' % file.name, 'Error')
        else:
            wx.MessageBox('unable create the image output buffer.', 'Error')

    def select_all(self):
        if self._scene is None or self._guiMode is None:
            return
        _shapes = self._scene.find_shapes_by_type(WxShapeBase)
        if not _shapes:
            return
        for x in _shapes:
            x.selected = True
        _selected_shapes = self.get_selected_shapes()
        self.validate_selection(_selected_shapes)
        self.hide_all_handles()
        self.update_multi_edit_shape_size()
        self._guiMode.multiEditShape.show()
        self._guiMode.multiEditShape.show_handles(True)
        self.Refresh(False)

    def deselect_all(self):
        if self._scene is None or self._guiMode is None:
            return
        _shapes = self._scene.find_shapes_by_type(WxShapeBase)
        for x in _shapes:
            x.selected = False
        self._guiMode.multiEditShape.hide()

    def hide_all_handles(self):
        if self._scene is None:
            return
        _shapes = self._scene.find_shapes_by_type(WxShapeBase)
        for x in _shapes:
            x.show_handles(False)

    def refresh_with(self, erase: bool, rect: wx.Rect):
        _l_pos = self.dp2lp(wx.Point(0, 0))
        _update_rect = rect
        _update_rect = _update_rect.Inflate((20 / self.setting.scale), 20 / self.setting.scale)
        _update_rect.Offset(-_l_pos.x, -_l_pos.y)
        self.RefreshRect(wx.Rect(_update_rect.x * self.setting.scale,
                                 _update_rect.y * self.setting.scale,
                                 _update_rect.width * self.setting.scale,
                                 _update_rect.height * self.setting.scale),
                         erase)

    def invalidate_rect(self, rect: wx.Rect):
        """
        Mark given rectangle as an invalidated one, i.e. as a rectangle which should
        be refreshed (by using wxSFShapeCanvas::RefreshInvalidatedRect()).
        Args:
            rect:

        Returns:

        """
        if self._invalidateRect.IsEmpty():
            self._invalidateRect = rect
        else:
            self._invalidateRect = self._invalidateRect.Union(rect)

    def refresh_invalidate_rect(self):
        """
        Refresh all canvas rectangles marked as invalidated.
        Args:

        Returns:

        """
        if not self._invalidateRect.IsEmpty():
            self.refresh_with(False, self._invalidateRect)
            self._invalidateRect = wx.Rect(0, 0, 0, 0)
            self.Refresh(False)

    def invalidate_visible_rect(self):
        """
        Mark whole visible canvas portion as an invalidated rectangle.
        Args:

        Returns:

        """
        self.invalidate_rect(self.dr2lr(self.GetClientRect()))

    def show_shadows(self, show: bool = True, style: EnumShapeShadowMode = EnumShapeShadowMode.TOP_MOST):
        if self._scene is None:
            return
        _shapes = self._scene.find_shapes_by_type(WxShapeBase)
        for x in _shapes:
            if show:
                x.remove_style(EnumShapeStyleFlags.SHOW_SHADOW)
            if style == EnumShapeShadowMode.TOP_MOST:
                _parent_shape = x.parentShape
                if _parent_shape:
                    if show:
                        x.add_style(EnumShapeStyleFlags.SHOW_SHADOW)
                    else:
                        x.remove_style(EnumShapeStyleFlags.SHOW_SHADOW)
            elif style == EnumShapeShadowMode.ALL:
                if show:
                    x.add_style(EnumShapeStyleFlags.SHOW_SHADOW)
                else:
                    x.remove_style(EnumShapeStyleFlags.SHOW_SHADOW)

    def do_drag_drop(self, shapes: list, start_pos: wx.Point = wx.Point(-1, -1)) -> int:
        """
        Start Drag&Drop operation with shapes included in the given list.
        Args:
            shapes:
            start_pos:

        Returns:

        """
        if not self.has_style(EnumGraphViewStyleFlag.DND):
            return wx.DragNone
        if self._guiMode:
            return self._guiMode.do_drag_drop(shapes, start_pos)
        return wx.DragNone

    # --------------------------------------------------------------
    # sop
    # --------------------------------------------------------------
    def restore_prev_positions(self):
        for id_, pos in self.mapPrevPositions:
            _shape = self._scene.find_shape(id_)
            if _shape:
                _shape.position = pos
        self.mapPrevPositions.clear()

    def store_prev_position(self, shape: WxShapeBase):
        self.mapPrevPositions.update({shape.uid: wx.RealPoint(shape.position)})

    def copy(self):
        if not self.has_style(EnumGraphViewStyleFlag.CLIPBOARD):
            return
        if self._scene is None:
            return
        if wx.TheClipboard.IsOpened() or (not wx.TheClipboard.IsOpened() and wx.TheClipboard.Open()):
            _selected_shapes = self.get_selected_shapes()
            self.validate_selection_for_clipboard(_selected_shapes, True)
            if _selected_shapes:
                _data = self._shapeDataObjectType(GV_DAT_FORMAT_ID, _selected_shapes, self.scene)
                wx.TheClipboard.SetData(_data)
                self.restore_prev_positions()
            if wx.TheClipboard.IsOpened(): wx.TheClipboard.Close()

    def cut(self):
        if not self.has_style(EnumGraphViewStyleFlag.CLIPBOARD):
            return
        if self._scene is None or self._guiMode is None:
            return
        self.copy()
        self.clear_temporaries()
        # remove selected shapes
        _selected_shapes = self.get_selected_shapes()
        self.validate_selection_for_clipboard(_selected_shapes, True)
        self._scene.remove_shapes(_selected_shapes)
        self._guiMode.multiEditShape.hide()
        self.save_view_state()
        self.Refresh(False)

    def paste(self):
        if not self.has_style(EnumGraphViewStyleFlag.CLIPBOARD):
            return
        if self._scene is None:
            return
        if wx.TheClipboard.IsOpened() or (not wx.TheClipboard.IsOpened() and wx.TheClipboard.Open()):
            _to_store = self._scene.find_shapes_by_type(WxShapeBase)
            # read data object from the clipboard
            _do = self._shapeDataObjectType(GV_DAT_FORMAT_ID)
            if wx.TheClipboard.GetData(_do):
                _stream = _do.data.GetText()
                # deserialize data
                self._scene.deserialize(_stream)
                # find dropped shapes
                _lst_current = self._scene.find_shapes_by_type(WxShapeBase)
                _lst_new = list()
                for x in _lst_current:
                    if x not in _to_store:
                        _lst_new.append(x)
                # todo: position,uid how handle it?
                # call use define handler
                self.on_paste(_lst_new)
                self.save_view_state()
                self.Refresh(False)
        if wx.TheClipboard.IsOpened(): wx.TheClipboard.Close()

    def undo(self):
        if not self.has_style(EnumGraphViewStyleFlag.UNDOREDO) or self._guiMode is None:
            return
        self.clear_temporaries()
        self.undoStack.RestoreOlderState()
        self._guiMode.multiEditShape.hide()

    def redo(self):
        if not self.has_style(EnumGraphViewStyleFlag.UNDOREDO) or self._guiMode is None:
            return
        self.clear_temporaries()
        self.undoStack.RestoreNewerState()
        self._guiMode.multiEditShape.hide()

    def can_copy(self):
        if not self.has_style(EnumGraphViewStyleFlag.CLIPBOARD):
            return False
        _lst = self.get_selected_shapes()
        return len(_lst) != 0

    def can_cut(self):
        return self.can_copy()

    def can_paste(self):
        if not self.has_style(EnumGraphViewStyleFlag.CLIPBOARD):
            return False
        _result = False
        if wx.TheClipboard.IsOpened() or (not wx.TheClipboard.IsOpened() and wx.TheClipboard.Open()):
            _result = wx.TheClipboard.IsSupported(self.shapesDataFormat)
            if wx.TheClipboard.IsOpened(): wx.TheClipboard.Close()
        return _result

    def can_undo(self):
        if not self.has_style(EnumGraphViewStyleFlag.UNDOREDO):
            return False
        return self.undoStack.can_undo()

    def can_redo(self):
        if not self.has_style(EnumGraphViewStyleFlag.UNDOREDO):
            return False
        return self.undoStack.can_redo()

    def can_align_selected(self):
        if self._guiMode is None:
            return False
        return self._guiMode.multiEditShape.states.visible and self._guiMode.workingState == EnumGraphViewWorkingState.READY

    def save_view_state(self):
        if not self.has_style(EnumGraphViewStyleFlag.UNDOREDO):
            return
        if self.undoStack is None:
            return
        self.undoStack.save_view_state()

    def clear_view_history(self):
        if self.undoStack is not None:
            self.undoStack.clear()

    # --------------------------------------------------------------
    # coordination conversation
    # --------------------------------------------------------------
    def dp2lp(self, pos: wx.Point) -> wx.Point:
        """
        Convert device position to logical position.
        Args:
            pos:

        Returns:

        """
        _pt_x, _pt_y = self.CalcUnscrolledPosition(pos.x, pos.y)
        return wx.Point(int(_pt_x / self.setting.scale), int(_pt_y / self.setting.scale))

    def dr2lr(self, rect: wx.Rect) -> wx.Rect:
        """
        Convert device rect to logical rect.
        Args:
            rect:

        Returns:

        """
        _pt_x, _pt_y = self.CalcUnscrolledPosition(rect.x, rect.y)
        return wx.Rect(int(_pt_x / self.setting.scale), int(_pt_y / self.setting.scale),
                       int(rect.GetWidth() / self.setting.scale), int(rect.GetHeight() / self.setting.scale))

    def lr2dr(self, rect: wx.Rect) -> wx.Rect:
        """
        Convert logical rect to device rect.
        Args:
            rect:

        Returns:

        """
        _pt_x, _pt_y = self.CalcScrolledPosition(rect.x, rect.y)
        return wx.Rect(int(_pt_x * self.setting.scale), int(_pt_y * self.setting.scale),
                       int(rect.GetWidth() * self.setting.scale), int(rect.GetHeight() * self.setting.scale))

    def lp2dp(self, pos: wx.Point) -> wx.Point:
        """
        Convert logical position to device position.
        Args:
            pos:

        Returns:

        """
        _pt_x, _pt_y = self.CalcScrolledPosition(pos.x, pos.y)
        return wx.Point(int(_pt_x * self.setting.scale), int(_pt_y * self.setting.scale))

    # --------------------------------------------------------------
    # shape accessing
    # --------------------------------------------------------------
    def reparent_shape_by_pos(self, shape: WxShapeBase, parent_pos: wx.Point):
        # is shape dropped into accepting shape?
        _parent_shape = self.get_shape_at_position(parent_pos, 1, EnumShapeSearchMode.UNSELECTED)
        if _parent_shape is not None and not _parent_shape.is_child_accepted(shape):
            _parent_shape = None
        if _parent_shape is not None and _parent_shape in shape .descendants:
            return
        # set new parent
        if shape.has_style(EnumShapeStyleFlags.REPARENT) and not isinstance(shape, LineShape):
            _prev_parent = shape.parentShape
            if _parent_shape:
                if _parent_shape.parentShape is not shape:
                    _apos = shape.absolutePosition - _parent_shape.absolutePosition
                    shape.position = _apos
                    shape.reparent(_parent_shape)
                    # notify the parent shape about dropped child
                    _parent_shape.handle_child_dropped(_apos, shape)
            else:
                if self._scene.is_top_shape_accepted(shape):
                    if shape.parentShape:
                        _apos = shape.parentShape.absolutePosition
                        shape.move_by(_apos.x, _apos.y)
                    shape.reparent(self._scene.rootShape)
            if _prev_parent:
                _prev_parent.update()
            if _parent_shape:
                _parent_shape.update()
            if isinstance(shape, ControlShape):
                shape.update()

    def remove_from_temporaries(self, shape: WxShapeBase):
        if shape is None or self._guiMode is None:
            return
        if shape in self.currentShapes:
            self.currentShapes.remove(shape)
        if self._guiMode.newLineShape is shape:
            self._guiMode.newLineShape = None
        if self.unselectedShapeUnderCursor is shape:
            self.unselectedShapeUnderCursor = None
        if self.selectedShapeUnderCursor is shape:
            self.selectedShapeUnderCursor = None
        if self.topMostShapeUnderCursor is shape:
            self.topMostShapeUnderCursor = None

    def save_canvas_state(self):
        # todo: finish this.
        pass

    def about_to_remove_shapes(self, shapes: typing.List[WxShapeBase]) -> bool:
        if not shapes:
            return False
        return wx.MessageBox('do you really wanna remove the selected shapes?', 'RemoveShapes', style=wx.YES_NO) == wx.YES

    def clear_temporaries(self):
        self.currentShapes.clear()
        if self._guiMode:
            self._guiMode.newLineShape = None
        self.unselectedShapeUnderCursor = None
        self.selectedShapeUnderCursor = None
        self.topMostShapeUnderCursor = None

    def update_shape_under_cursor_cache(self, pos: wx.Point):
        self.currentShapes.clear()
        _shapes = self.scene.find_shapes_by_type(WxShapeBase)
        self.currentShapes = _shapes
        _top_line = None
        _top_shape = None
        _sel_line = None
        _sel_shape = None
        _unsel_line = None
        _unsel_shape = None
        for x in reversed(_shapes):
            if x.states.visible and x.states.active and x.contains(pos):
                if isinstance(x, LineShape):
                    if _top_line is None:
                        _top_line = x
                    if x.selected:
                        if _sel_line is None:
                            _sel_line = x
                        elif _unsel_line is None:
                            _unsel_line = x
                else:
                    if _top_shape is None:
                        _top_shape = x
                    if x.selected:
                        if _sel_shape is None:
                            _sel_shape = x
                        elif _unsel_shape is None:
                            _unsel_shape = x

        # set pointer to logically topmost selected and unselected shape under the mouse cursor
        if _top_line:
            self.topMostShapeUnderCursor = _top_line
        else:
            self.topMostShapeUnderCursor = _top_shape
        if _sel_line:
            self.selectedShapeUnderCursor = _sel_line
        else:
            self.selectedShapeUnderCursor = _sel_shape
        if _unsel_line:
            self.unselectedShapeUnderCursor = _unsel_line
        else:
            self.unselectedShapeUnderCursor = _unsel_shape

    def get_shape_under_cursor(self, search_mode=EnumShapeSearchMode.BOTH) -> typing.Union[None, WxShapeBase]:
        if search_mode == EnumShapeSearchMode.BOTH:
            return self.topMostShapeUnderCursor
        elif search_mode == EnumShapeSearchMode.SELECTED:
            return self.selectedShapeUnderCursor
        elif search_mode == EnumShapeSearchMode.UNSELECTED:
            return self.unselectedShapeUnderCursor
        return None

    def get_shape_at_position(self, pos: wx.Point, z_val: int = 1, search_mode: EnumShapeSearchMode = EnumShapeSearchMode.BOTH) -> typing.Union[
        WxShapeBase, None]:
        if self._scene is None:
            return
        return self._scene.get_shape_at_position(pos, z_val, search_mode)

    def get_top_most_handle_at_position(self, pos: wx.Point) -> typing.Union[HandleShapeObject, None]:
        if self._scene is None or self._guiMode is None:
            return
        # first test multiEdit handles
        if self._guiMode.multiEditShape.states.visible:
            for x in self._guiMode.multiEditShape.handles:
                if x.states.visible and x.contains(pos):
                    return x
        # then test normal handles
        _shapes = self._scene.find_shapes_by_type(WxShapeBase)
        for x in _shapes:
            if x.has_style(EnumShapeStyleFlags.RESIZE):
                for hnd in x.handles:
                    if hnd.states.visible and hnd.contains(pos):
                        return hnd
        return

    def get_shape_inside(self, rect: wx.Rect) -> typing.Union[WxShapeBase, None]:
        if self._scene is None:
            return
        return self._scene.get_shape_inside(rect)

    def get_selected_shapes(self) -> typing.List[WxShapeBase]:
        _ret = list()
        if self._scene is None:
            return _ret
        _shapes = self._scene.find_shapes_by_type(WxShapeBase)
        for x in _shapes:
            if x.selected:
                _ret.append(x)
        return _ret

    def get_total_boundingbox(self) -> wx.Rect:
        _rect = wx.Rect()
        if self._scene:
            _shapes = self._scene.find_shapes_by_type(WxShapeBase)
            for x in _shapes:
                _rect = _rect.Union(x.get_boundingbox())
        return _rect

    def get_selection_boundingbox(self):
        _rect = wx.Rect()
        if self._scene:
            _shapes = self.get_selected_shapes()
            for x in _shapes:
                _rect = _rect.Union(x.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF |
                                                               EnumShapeBBCalculationFlag.CHILDREN |
                                                               EnumShapeBBCalculationFlag.CONNECTIONS |
                                                               EnumShapeBBCalculationFlag.SHADOW))
        return _rect

    def align_selected(self, h_align, v_align):
        _selected_shapes = self.get_selected_shapes()
        # if only one non-line shape is in the selection then alignment has no sense so exit...
        if len(_selected_shapes) < 2: return
        _upt_rect = self.get_selection_boundingbox()
        _upt_rect = _upt_rect.Inflate(DEFAULT_ME_OFFSET, DEFAULT_ME_OFFSET)
        _min_pos = wx.RealPoint()
        _max_pos = wx.RealPoint()
        # find far distant position
        for idx, x in enumerate(_selected_shapes):
            if not isinstance(x, LineShape):
                _apos = x.absolutePosition
                _bb = x.get_boundingbox()
                if idx == 0:
                    _min_pos = _apos
                    _max_pos.x = _apos.x + _bb.GetWidth()
                    _max_pos.y = _apos.y + _bb.GetHeight()
                else:
                    if _apos.x < _min_pos.x:
                        _min_pos.x = _apos.x
                    if _apos.y < _min_pos.y:
                        _min_pos.y = _apos.y
                    if _apos.x + _bb.GetWidth() > _max_pos.x:
                        _max_pos.x = _apos.x + _bb.GetWidth()
                    if _apos.y + _bb.GetHeight() > _max_pos.y:
                        _max_pos.y = _apos.y + _bb.GetHeight()
        # set new position
        for x in _selected_shapes:
            if not isinstance(x, LineShape):
                _apos = x.absolutePosition
                _bb = x.get_boundingbox()
                if h_align == EnumShapeHAlign.LEFT:
                    x.move_to(wx.RealPoint(_min_pos.x, _apos.y))
                elif h_align == EnumShapeHAlign.RIGHT:
                    x.move_to(wx.RealPoint(_max_pos.x - _bb.GetWidth(), _apos.y))
                elif h_align == EnumShapeHAlign.CENTER:
                    x.move_to(wx.RealPoint((_max_pos.x + _min_pos.x) / 2 - _bb.GetWidth() / 2,
                                           _apos.y))
                if v_align == EnumShapeVAlign.TOP:
                    x.move_to(wx.RealPoint(_apos.x, _min_pos.y))
                elif h_align == EnumShapeVAlign.BOTTOM:
                    x.move_to(wx.RealPoint(_apos.x, _max_pos.y - _bb.GetHeight()))
                elif h_align == EnumShapeVAlign.MIDDLE:
                    x.move_to(wx.RealPoint(_apos.x, (_max_pos.y + _min_pos.y) / 2 - _bb.GetHeight() / 2))
                x.update()
                if x.parentShape:
                    x.parentShape.update()
        if not _upt_rect.IsEmpty():
            self.update_multi_edit_shape_size()
            self.save_view_state()
            self.refresh_with(False, _upt_rect)

    # --------------------------------------------------------------
    # style handling
    # --------------------------------------------------------------
    def set_style(self, style: int):
        self.setting.style = style

    def add_style(self, style: int):
        self.setting.style |= style

    def remove_style(self, style: int):
        self.setting.style &= ~style

    def has_style(self, style):
        return self.setting.style & style != 0

    # --------------------------------------------------------------
    # setting .stylesheet
    # --------------------------------------------------------------
    @property
    def shapeCommonHoverColor(self):
        return self.setting.commonHoverColor

    @shapeCommonHoverColor.setter
    def shapeCommonHoverColor(self, color: str):
        if self._scene is None:
            return
        self.setting.commonHoverColor = color
        _shapes = self._scene.find_shapes_by_type(WxShapeBase)
        for x in _shapes:
            x.hoverColor = color

    def set_scale(self, scale: float):
        if self._scene is None:
            return
        if scale != 1:
            _shapes = self._scene.find_shapes_by_type(ControlShape)
            if _shapes:
                wx.MessageBox('could not change scale of shapeView, since ControlShape contains.', 'Error')
                scale = 1
        if scale == 0:
            scale = 1
        if scale < self.setting.minScale: scale = self.setting.minScale
        if scale > self.setting.maxScale: scale = self.setting.maxScale
        self.setting.scale = scale
        if not self.setting.enableGC:
            _shapes = self._scene.find_shapes_by_type(BitmapShape)
            for x in _shapes:
                x.scale(1, 1)
        self.update_virtual_size()

    def set_scale_to_view_all(self):
        _phy_rect = self.GetClientSize()
        _vir_rect = self.get_total_boundingbox()
        _hz = _phy_rect.GetWidth() / _vir_rect.GetRight()
        _vz = _phy_rect.GetHeight() / _vir_rect.GetBottom()
        if _hz < _vz:
            if _hz < 1:
                self.set_scale(_hz)
            else:
                self.set_scale(1)
        else:
            if _vz < 1:
                self.set_scale(_vz)
            else:
                self.set_scale(1)

    def scroll_to_shape(self, shape: WxShapeBase):
        if shape is None:
            return
        _ux, _uy = self.GetScrollPixelsPerUnit()
        _size = self.GetClientSize()
        _pots = shape.get_center()
        self.Scroll(((_pots.x * self.setting.scale) - _size.x / 2) / _ux, ((_pots.y * self.setting.scale) - _size.y / 2) / _uy)

    @property
    def enableGC(self):
        return self.setting.enableGC

    @enableGC.setter
    def enableGC(self, state):
        self.setting.enableGC = state

    def fit_position_to_grid(self, pos: wx.Point) -> wx.Point:
        if self.has_style(EnumGraphViewStyleFlag.GRID_USE):
            return wx.Point(int(pos.x / self.setting.gridSize.x) * self.setting.gridSize.x, int(pos.y / self.setting.gridSize.y) * self.setting.gridSize.y)
        else:
            return pos

    def update_multi_edit_shape_size(self):
        if self._guiMode is None:
            return
        _selected_shapes = self.get_selected_shapes()
        if not _selected_shapes:
            return
        _union_rect = wx.Rect()
        for x in _selected_shapes:
            _union_rect = _union_rect.Union(x.get_boundingbox())
        _union_rect = _union_rect.Inflate(DEFAULT_ME_OFFSET, DEFAULT_ME_OFFSET)
        # draw rectangle
        self._guiMode.multiEditShape.position = wx.RealPoint(_union_rect.GetPosition())
        _w, _h = _union_rect.GetSize()
        self._guiMode.multiEditShape.set_rect_size(_w, _h)

    def update_virtual_size(self):
        _rect = self.get_total_boundingbox()
        self.on_update_virtual_size(_rect)
        if not _rect.IsEmpty():
            self.SetVirtualSize(_rect.GetRight() * self.setting.scale, _rect.GetBottom() * self.setting.scale)
        else:
            self.SetVirtualSize(500, 500)

    def move_shapes_from_negative(self):
        if self._scene:
            self._scene.move_shapes_from_negatives()

    def center_shapes(self):
        """
        Center scene in accordance to the shape canvas extent.
        Returns:

        """
        _bb = self.get_total_boundingbox()
        _prev_bb = _bb
        _bb = _bb.CenterIn(wx.Rect(wx.Point(0, 0), self.GetSize()))
        _dx = _bb.GetLeft() - _prev_bb.GetLeft()
        _dy = _bb.GetTop() - _prev_bb.GetTop()
        for x in self.currentShapes:
            if x.parentShape is None:
                x.move_by(_dx, _dy)
        self.move_shapes_from_negative()

    def validate_selection(self, selections: typing.List[WxShapeBase]):
        """
        Validate selection (remove redundantly selected shapes etc...)
        Args:
            selections:

        Returns:

        """
        if self._scene is None:
            return
        _popped_shapes = list()
        for x in selections:
            if x.parentShape in selections or any([n in selections for n in x.ancestors]):
                _popped_shapes.append(x)
        for x in _popped_shapes:
            x.selected = False
            selections.remove(x)
        # todo: what is below codes for?
        """
        node = selection.GetFirst();
        while(node)
        {
            pShape = node->GetData();
    
            // move selected shapes to the back of the global list
            ((xsSerializable*)pShape->GetParent())->GetChildrenList().DeleteObject(pShape);
            ((xsSerializable*)pShape->GetParent())->GetChildrenList().Append(pShape);
    
            node = node->GetNext();
        }
        """

    def validate_selection_for_clipboard(self, selections: typing.List[WxShapeBase], store_previous=False):
        """
        Validate selection (remove redundantly selected shapes etc...)
        Args:
            selections:
            store_previous:

        Returns:

        """
        if self._scene is None:
            return
        _to_remove = list()
        for x in selections:
            if x.parentShape:
                if not x.has_style(EnumShapeStyleFlags.REPARENT) and x.parentShape not in selections:
                    # remove child shapes without parent and with sfsPARENT_CHANGE style
                    _to_remove.append(x)
                    continue
                # convert relative position to absolute position if the shape is copied
                # without its parent
                if x.parentShape not in selections:
                    if store_previous:
                        self.store_prev_position(x)
                        x.position = x.absolutePosition
            self.append_assigned_connection(x, selections, False)

    def append_assigned_connection(self, shape: WxShapeBase, selections: list, children_only: bool = True):
        """
        Append connections assigned to shapes in given list to this list as well
        Args:
            shape:
            selections:
            children_only:

        Returns:

        """
        if self._scene is None:
            return
        # add connections assigned to copied topmost shapes and their children to the copy list
        _des = shape.descendants
        _all_cons = list()
        if not children_only:
            _cons = self._scene.get_assigned_connections(shape, LineShape, EnumShapeConnectionSearchMode.BOTH)
            for ln in _cons:
                _all_cons.extend(self._scene.get_assigned_connections(ln, LineShape, EnumShapeConnectionSearchMode.BOTH))
        # insert connections to the copy list
        for ln in _all_cons:
            if ln not in selections:
                selections.append(ln)

    # --------------------------------------------------------------
    # drawing
    # --------------------------------------------------------------

    def draw_content(self, dc: wx.DC, from_paint: bool = True):
        """
        Function responsible for drawing of the canvas's content to given DC. The default
        implementation draws actual objects managed by assigned scene.
        Args:
            dc:
            from_paint:

        Returns:

        """
        if self.scene is None:
            return
        if self.scene.rootShape is None:
            return
        _update_rect = wx.Rect()
        # get all existing shapes use DFS tree search
        _shapes_to_draw = self.scene.find_shapes_by_type(WxShapeBase, tree_search_mode=EnumShapeTreeSearchMode.DFS)
        if from_paint:
            _ri = wx.RegionIterator(self.GetUpdateRegion())
            _first_run = True
            while _ri:
                if _first_run:
                    _update_rect = self.dr2lr(_ri.GetRect().Inflate(5, 5))
                    _first_run = False
                else:
                    _update_rect = _update_rect.Union(self.dr2lr(_ri.GetRect().Inflate(5, 5)))
                _ri.Next()
        if self._guiMode:
            self._guiMode.render_content(dc, _shapes_to_draw, _update_rect, from_paint)

    def draw_background(self, dc: wx.DC, from_paint: bool = True):
        if self.has_style(EnumGraphViewStyleFlag.GRADIENT_BACKGROUND):
            _bcg_size = self.GetVirtualSize() + self.setting.gridSize
            if self.setting.scale != 1.0:
                dc.GradientFillLinear(wx.Rect(wx.Point(0, 0), wx.Size(_bcg_size.x / self.setting.scale, _bcg_size.y / self.setting.scale)),
                                      self.setting.gradientFrom, self.setting.gradientTo, wx.SOUTH)
            else:
                dc.GradientFillLinear(wx.Rect(wx.Point(0, 0), self.GetVirtualSize() + self.setting.gridSize),
                                      self.setting.gradientFrom, self.setting.gradientTo, wx.SOUTH)
        else:
            dc.SetBackground(wx.Brush(self.setting.backgroundColor))
            dc.Clear()
        # show grid
        if self.has_style(EnumGraphViewStyleFlag.GRID_SHOW):
            _line_dist = self.setting.gridSize.x * self.setting.gridLineMult
            if _line_dist * self.setting.scale > 3:
                _grid_rect = wx.Rect(wx.Point(0, 0), self.GetVirtualSize() + self.setting.gridSize)
                _max_x = _grid_rect.GetRight() / self.setting.scale
                _max_y = _grid_rect.GetBottom() / self.setting.scale
                dc.SetPen(wx.Pen(self.setting.gridColor, 1, self.setting.gridStyle))
                _x = _grid_rect.GetLeft()
                _y = _grid_rect.GetTop()
                while _x <= _max_x:
                    dc.DrawLine(_x, 0, _x, _max_y)
                    _x += _line_dist
                while _y <= _max_y:
                    dc.DrawLine(0, _y, _max_x, _y)
                    _y += _line_dist

    def draw_foreground(self, dc: wx.DC, from_paint: bool = True):
        if self.scene is None:
            return
        if self.scene.isEmpty:
            return
        _update_rect = wx.Rect()
        # get all existing shapes
        _shapes_to_draw = self.scene.find_shapes_by_type(WxShapeBase, start_from=self._scene.foregroundRootShape)
        if from_paint and _shapes_to_draw:
            _x, _y = self.CalcUnscrolledPosition(0, 0)
            _diff = wx.RealPoint(_x, _y) - self.viewportTopLeft
            # todo: not good choice in here update viewportTopLeft
            self.viewportTopLeft = wx.RealPoint(_x, _y)
            for x in _shapes_to_draw:
                x.move_by(_diff.x, _diff.y, False)
                x.draw(dc, False)
            for x in _shapes_to_draw:
                _update_rect = _update_rect.Union(x.get_boundingbox())
            _update_rect = self.dr2lr(_update_rect)
            _r_rect = wx.Rect()
            _ri = wx.RegionIterator(self.GetUpdateRegion())
            _first_run = True
            while _ri:
                if _first_run:
                    _r_rect = self.dr2lr(_ri.GetRect().Inflate(5, 5))
                    _first_run = False
                else:
                    _r_rect = _r_rect.Union(self.dr2lr(_ri.GetRect().Inflate(5, 5)))
                _ri.Next()
            if not _update_rect.Intersects(_r_rect):
                self.Refresh(False)

    # --------------------------------------------------------------
    # common
    # --------------------------------------------------------------
    def delete_all_text_controls(self):
        if self._scene is None:
            return
        _shapes = self._scene.find_shapes_by_type(EditTextShape)
        for x in _shapes:
            _tc = x.textControl
            if _tc:
                _tc.quit()

    # --------------------------------------------------------------
    # event handling
    # --------------------------------------------------------------
    def on_erase_background(self, evt):
        pass

    def on_size(self, evt: wx.SizeEvent):
        if self.has_style(EnumGraphViewStyleFlag.GRADIENT_BACKGROUND):
            self.Refresh(False)
        evt.Skip()

    def on_paint(self, evt: wx.PaintEvent):
        _pdc = wx.BufferedPaintDC(self)
        if self.setting.enableGC:
            _gc = wx.GCDC(_pdc)
            self.PrepareDC(_pdc)
            self.PrepareDC(_gc)
            # scaled GC
            _pgc = _gc.GetGraphicsContext()
            _pgc.Scale(self.setting.scale, self.setting.scale)
            self.draw_background(_gc, True)
            self.draw_content(_gc, True)
        else:
            _dc = _pdc
            self.PrepareDC(_dc)
            _dc.SetUserScale(self.setting.scale, self.setting.scale)
            self.draw_background(_dc, True)
            self.draw_content(_dc, True)
        # foreground use different dc, which has no scale
        _pdc.SetUserScale(1, 1)
        self.draw_foreground(_pdc, True)
        self.on_repaint()

    def on_left_down(self, evt: wx.MouseEvent):
        """
        Event handler called when the canvas is clicked by
        the left mouse button. The function can be overrided if necessary.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from overrided methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        if self._scene is None:
            return
        self.delete_all_text_controls()
        self.SetFocus()
        if self._guiMode is not None:
            self._guiMode.on_left_down(evt)
        evt.Skip()

    def on_left_double_clicked(self, evt: wx.MouseEvent):
        """
        Event handler called when the canvas is double-clicked by
        the left mouse button. The function can be overrided if necessary.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from overrided methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        if self._scene is None:
            return
        self.SetFocus()
        if self._guiMode is not None:
            self._guiMode.on_left_double_clicked(evt)
        evt.Skip()

    def on_left_up(self, evt: wx.MouseEvent):
        """
        Event handler called when the left mouse button is released

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from overrided methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        if self._scene is None:
            return
        self.SetFocus()
        if self._guiMode is not None:
            self._guiMode.on_left_up(evt)
        evt.Skip()

    def on_right_down(self, evt: wx.MouseEvent):
        """
        Event handler called when the canvas is clicked by
        the right mouse button. The function can be override if necessary.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from override methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        if self._scene is None:
            return
        self.SetFocus()
        if self._guiMode is not None:
            self._guiMode.on_right_down(evt)
        evt.Skip()

    def on_right_double_clicked(self, evt: wx.MouseEvent):
        """
        Event handler called when the canvas is double-clicked by
        the right mouse button. The function can be overrided if necessary.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from overrided methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        if self._scene is None:
            return
        self.SetFocus()
        if self._guiMode is not None:
            self._guiMode.on_right_double_clicked(evt)
        evt.Skip()

    def on_right_up(self, evt: wx.MouseEvent):
        """
        Event handler called when the right mouse button is released

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from overrided methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        if self._scene is None:
            return
        self.SetFocus()
        if self._guiMode is not None:
            self._guiMode.on_right_up(evt)
        evt.Skip()

    def on_mouse_move(self, evt: wx.MouseEvent):
        """
        Event handler called when the mouse pointer is moved.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from overrided methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        _l_pos = self.dp2lp(evt.GetPosition())
        self.update_shape_under_cursor_cache(_l_pos)
        if self._guiMode is not None:
            self._guiMode.on_mouse_move(evt)
        evt.Skip()

    def on_mouse_wheel(self, evt: wx.MouseEvent):
        """
        Event handler called when the mouse wheel position is changed.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from override methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        if self.has_style(EnumGraphViewStyleFlag.PROCESS_MOUSEWHEEL):
            if self._guiMode is not None:
                self._guiMode.on_mouse_wheel(evt)
        evt.Skip()

    def on_key_down(self, evt: wx.KeyEvent):
        """
        Event handler called when any key is pressed.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from overrided methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        if self._guiMode is not None:
            self._guiMode.on_key_down(evt)
        evt.Skip()

    def on_enter_window(self, evt: wx.MouseEvent):
        if self._guiMode is not None:
            self._guiMode.on_enter_window(evt)
        evt.Skip()

    def on_leave_window(self, evt: wx.MouseEvent):
        if self._guiMode is not None:
            self._guiMode.on_leave_window(evt)
        evt.Skip()

    def on_repaint(self):
        _evt = WGViewRepaintEvent(T_EVT_VIEW_REPAINT, self.GetId())
        _evt.SetView(self)
        self.ProcessEvent(_evt)

    def on_text_change(self, shape: 'EditTextShape'):
        """
        Event handler called when any editable text shape is changed.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from overrided methods if the default canvas behaviour
        should be preserved.
        Args:
            shape:

        Returns:

        """
        # _id = -1
        # if shape is not None: _id = shape.uid
        _evt = WGShapeTextEvent(T_EVT_TEXT_CHANGE)
        _evt.SetShape(shape)
        _evt.SetText(shape.text)
        self.ProcessEvent(_evt)

    def on_connection_finished(self, connection: 'LineShape'):
        """
        Event handler called after successfully connection creation.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from overrided methods if the default canvas behaviour
        should be preserved.
        Args:
            connection:

        Returns:

        """
        #_id = -1
        #if connection is not None: _id = connection.uid
        _evt = WGShapeEvent(T_EVT_LINE_DONE)
        _evt.SetShape(connection)
        self.ProcessEvent(_evt)

    def on_pre_connection_finished(self, connection: 'LineShape'):
        """
        Event handler called after successfully connection creation in
        order to allow developer to perform some kind of checks
        before the connection is really added to the diagram. The function
        can be override if necessary. The default implementation
        generates wxEVT_SF_LINE_DONE event.
        Args:
            connection:

        Returns:

        """
        #_id = -1
        #if connection is not None: _id = connection.id
        _evt = WGShapeEvent(T_EVT_LINE_BEFORE_DONE)
        _evt.SetShape(connection)
        self.ProcessEvent(_evt)
        if _evt.IsVetoed():
            return EnumConnectionFinishedState.FAILED_CANCELED
        return EnumConnectionFinishedState.OK

    def handle_drop(self, x, y, result, data: ShapeDataObject):
        if data is None:
            return
        _data_text = data.data.GetText()
        _news = list()
        _parents_to_update = list()
        _lpos = self.dp2lp(wx.Point(x, y))
        _dx = _dy = 0
        if self.dndStartedHere:
            _dx = _lpos.x - self.dndStartedAt.x
            _dy = _lpos.y - self.dndStartedAt.y
        """
        wxSFDiagramManager mgr;
		mgr.GetUsedIDs() = m_pManager->GetUsedIDs();
		mgr.DeserializeFromXml( instream );
        """
        _parent = self._scene.get_shape_at_position(_lpos, 1, EnumShapeSearchMode.UNSELECTED)
        _top_shapes = self._scene.rootShape.children
        for x in _top_shapes:
            x.move_by(_dx, _dy)
            # do not reparent connection lines
            if isinstance(x, LineShape) and not x.isStandalone:
                _parent = None
            _new_shape = x.clone()
            _pos = self.lp2dp(wg_util_conv2point(x.absolutePosition)) if _parent is None else self.lp2dp(
                wg_util_conv2point(x.absolutePosition - _parent.absolutePosition))
            self._scene.add_shape(_new_shape, _pos, _parent, save_state=False)
            if _parent:
                _parent.handle_child_dropped(_pos, _new_shape)
                if _parent not in _parents_to_update:
                    _parents_to_update.append(_parent)
            _news.append(_new_shape)
        self.deselect_all()
        for x in _parents_to_update:
            x.update()
        if not self.dndStartedHere:
            self.save_view_state()
            self.Refresh(False)
        self.on_drop(x, y, result, _news)

    def on_drop(self, x, y, result, shape_list: list):
        """
        Event handler called by the framework after any dragged shapes
        are dropped to the canvas. The default implementation
        generates wxEVT_SF_ON_DROP event.
        Args:
            x:
            y:
            result:
            shape_list:

        Returns:

        """
        if not self.has_style(EnumGraphViewStyleFlag.DND):
            return
        _evt = WGShapeDropEvent(T_EVT_ON_DROP, wx.Point(x, y), self, result, wx.ID_ANY)
        _evt.SetDroppedShapes(shape_list)
        self.ProcessEvent(_evt)

    def on_paste(self, shape_list: list):
        """
        Event handler called by the framework after pasting of shapes
        from the clipboard to the canvas. The default implementation
        generates wxEVT_SF_ON_PASTE event.
        Args:
            shape_list:

        Returns:

        """
        if not self.has_style(EnumGraphViewStyleFlag.CLIPBOARD):
            return
        _evt = WGShapePasteEvent(T_EVT_ON_PASTE, self, wx.ID_ANY)
        _evt.SetPasteShapes(shape_list)
        self.ProcessEvent(_evt)

    def on_update_virtual_size(self, v_rect: wx.Rect):
        _x, _y = self.CalcUnscrolledPosition(0, 0)
        self.viewportTopLeft = wx.RealPoint(_x, _y)

    # --------------------------------------------------------------
    # printing
    # --------------------------------------------------------------
    def _initialize_printing(self):
        if self.setting.printPageSetupData is None:
            self.setting.printPageSetupData = wx.PageSetupDialogData()
            self.setting.printPageSetupData.SetPaperId(wx.PAPER_A4)
            self.setting.printPageSetupData.SetMarginTopLeft(wx.Point(15, 15))
            self.setting.printPageSetupData.SetMarginBottomRight(wx.Point(15, 15))

    @property
    def printPageSetupData(self):
        return self.setting.printPageSetupData

    def print(self, prompt: bool = True, print_out: wx.Printout = None):
        if print_out is None:
            return
        _dlg_data = wx.PrintDialogData(self.setting.printData)
        _printer = wx.Printer(_dlg_data)
        self.deselect_all()
        if not _printer.Print(self, print_out, prompt):
            if wx.Printer.GetLastError() == wx.PRINTER_ERROR:
                wx.MessageBox('There was a problem printing.\nPerhaps your current printer is not set correctly?', 'PrintError', wx.OK | wx.ICON_ERROR)
            return
        else:
            self.setting.printData = _printer.GetPrintDialogData().GetPrintData()

    def print_preview(self, preview_print_out: wx.Printout, print_out: wx.Printout):
        self.deselect_all()
        _dlg_data = wx.PrintDialogData(self.setting.printData)
        _print_preview = wx.PrintPreview(preview_print_out, print_out, _dlg_data)
        if not _print_preview.IsOk():
            wx.MessageBox('There was a problem previewing.\nPerhaps your current printer is not set correctly?', 'PrintPreviewError', wx.OK | wx.ICON_ERROR)
            return
        _frame = wx.PreviewFrame(_print_preview, self, pos=wx.Point(100, 100), size=wx.Size(800, 700))
        _frame.Center()
        _frame.Initialize()
        _frame.Show()

    def print_page_setup(self):
        _setup_dlg = wx.PageSetupDialog(self, self.setting.printData)
        _setup_dlg.ShowModal()
        self.setting.printData = _setup_dlg.GetPageSetupData().GetPrintData()
        self.setting.printPageSetupData = _setup_dlg.GetPageSetupData()
