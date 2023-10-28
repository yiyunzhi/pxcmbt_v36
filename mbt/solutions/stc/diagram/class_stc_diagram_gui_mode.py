# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_stc_diagram_gui_mode.py
# ------------------------------------------------------------------------------
#
# File          : class_stc_diagram_gui_mode.py
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
from framework.gui.wxgraph import BaseGUIMode, EnumGraphViewWorkingState, EnumShapeSearchMode
from .class_shape_border_mark import BorderMarkShape


class STCDiagramGUIMode(BaseGUIMode):
    def __init__(self, graph_view):
        BaseGUIMode.__init__(self, graph_view)
        self.borderMarkShape = BorderMarkShape(shapeManager=graph_view.scene, wxId=0)
        self.borderMarkShape.hide()

    def on_scene_updated(self):
        super().on_scene_updated()
        self.borderMarkShape.scene = self.graphView.scene

    def on_mouse_move(self, evt: wx.MouseEvent):
        super().on_mouse_move(evt)
        _l_pos = self.graphView.dp2lp(evt.GetPosition())
        if self.graphView.workingState == EnumGraphViewWorkingState.SHAPEMOVE:
            if evt.Dragging():
                _parent_shape = self.graphView.get_shape_at_position(_l_pos, 1, EnumShapeSearchMode.UNSELECTED)
                if _parent_shape:
                    _selected_shapes = self.graphView.get_selected_shapes()
                    _used_shapes=[]
                    for x in _selected_shapes:
                        _common_ancestors=list(self.graphView.scene.get_common_ancestors(x,_parent_shape))
                        if self.graphView.scene.rootShape in _common_ancestors:
                            _common_ancestors.remove(self.graphView.scene.rootShape)
                        _not_ancestor=x not in _parent_shape.ancestors
                        _not_descendants=x not in _parent_shape.descendants
                        if not _common_ancestors and _not_descendants and _not_ancestor:
                            _used_shapes.append(x)
                    if not all([_parent_shape.is_child_accepted(x) for x in _used_shapes]):
                        _w, _h = _parent_shape.stylesheet.size
                        self.borderMarkShape.move_to(_parent_shape.absolutePosition, False)
                        self.borderMarkShape.set_rect_size(_w, _h)
                        self.borderMarkShape.show()
                    else:
                        self.borderMarkShape.hide()
                else:
                    self.borderMarkShape.hide()
                self.graphView.refresh_invalidate_rect()

    def render_content(self, dc: wx.DC, shapes: list, update_rect: wx.Rect, from_paint: bool = True):
        super().render_content(dc, shapes, update_rect, from_paint)
        if from_paint:
            if self.borderMarkShape.states.visible:
                self.borderMarkShape.draw(dc)
