# -*- coding: utf-8 -*-
import copy
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : base.py
# ------------------------------------------------------------------------------
#
# File          : base.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import typing
import wx, anytree
from framework.application.base import ClassProperty, Serializable
from .define import *
from .events import *
from .class_base import DrawObject, DrawObjectState, DrawObjectStylesheet
from .class_handle import HandleShapeObject
from .class_shape_connection_point import ConnectionPointShapeObject
from .class_action_proxy import BaseShapeActionProxy
from .class_basic import BasicLineShape, BasicTextShape


class WxShapeBaseState(DrawObjectState):
    def __init__(self, **kwargs):
        DrawObjectState.__init__(self, **kwargs)
        self.active = kwargs.get('active', True)
        self.firstMove = kwargs.get('firstMove', False)


class WxShapeBaseStylesheet(DrawObjectStylesheet):
    def __init__(self, **kwargs):
        DrawObjectStylesheet.__init__(self, **kwargs)
        self.vAlign = kwargs.get('vAlign', EnumShapeVAlign.TOP)
        self.hAlign = kwargs.get('hAlign', EnumShapeHAlign.LEFT)
        self.hBorder = kwargs.get('hBorder', 1)
        self.vBorder = kwargs.get('vBorder', 1)
        self.dockPoint = kwargs.get('dockPoint', -3)


class WxShapeBase(DrawObject, anytree.NodeMixin):
    __identity__ = "WxShapeBase"

    def __init__(self, **kwargs):
        DrawObject.__init__(self, **kwargs)
        self.states = kwargs.get('states', WxShapeBaseState())
        self.style = kwargs.get('style', EnumShapeStyleFlags.STYLE_DEFAULT)
        self.stylesheet = kwargs.get('stylesheet', WxShapeBaseStylesheet())
        self.userData = kwargs.get('userData')
        self.handles = kwargs.get('handles', list())
        self.connectionPts = kwargs.get('connectionPts', list())
        self.actionProxy = BaseShapeActionProxy(self)

        self._sAcceptedSrcNeighbours = list()
        self._sAcceptedDstNeighbours = list()
        self._wAcceptedConnections = list()
        self._ddAcceptedChildren = list()
        self._lstProcessed = list()
        self.mouseOffset = None
        self.highlightParent = False

        _children = kwargs.get('children')
        if _children:
            self.children = _children

    @ClassProperty
    def identity(cls):
        return cls.__identity__

    @property
    def className(self):
        return self.__class__.__name__

    @staticmethod
    def find(node, filter_=None, stop=None, max_level=None):
        return anytree.find(node, filter_, stop, max_level)

    @staticmethod
    def find_all(node, filter_=None, stop=None, max_level=None, min_count=None, max_count=None) -> list:
        return list(anytree.findall(node, filter_, stop, max_level, min_count, max_count))

    @staticmethod
    def find_by_attr(node, value, name="className", max_level=None):
        return anytree.find_by_attr(node, value, name, max_level)

    @staticmethod
    def findall_by_attr(node, value, name="className", max_level=None, min_count=None, max_count=None) -> list:
        return list(anytree.findall_by_attr(node, value, name, max_level, min_count, max_count))

    @staticmethod
    def bfs(node: 'WxShapeBase', filter_=None):
        _ret = list()
        for x in anytree.iterators.LevelOrderIter(node, filter_=filter_):
            _ret.append(x)
        return _ret

    @staticmethod
    def dfs(node: 'WxShapeBase', filter_=None):
        _ret = [node]
        for x in node.children:
            if filter_(x):
                _ret.extend(WxShapeBase.dfs(x, filter_))
        return _ret

    def reparent(self, parent: 'WxShapeBase'):
        if parent is not None:
            if self.parentShape:
                self.parent = None
            self.parent = parent
        else:
            self.parent = self.scene.rootShape

    def post_init(self):
        """
        method will be called if shape added into scene.
        Returns: None

        """
        assert self.scene is not None
        self.create_handles()
        self.selected = False
        if self.view:
            self.stylesheet.hoverColor = self.view.shapeCommonHoverColor
        if self.children:
            # gather all shapes recursive the post init it
            _bfs_children = self.get_child_shapes(recursive=True)
            for x in _bfs_children:
                x.post_init()
            # for x in self.children:
            #     x.update(update_parent=False)
            # the update be triggerd always by the leaf shapes of this shape, since in update() function
            # it will start a recursive update to its ancestors.
        #self.update()

    def update_all(self):
        for x in self.get_leaf_shapes():
            x.update()

    def update(self, **kwargs):
        """
        Update shape (align all child shapes a resize it to fit them)
        Returns:

        """
        print('update-> isLeaf:%s' % self.is_leaf, self)
        self.do_alignment()
        # alignment start from top shape of the tree then to the leafs,
        # since the alignment depends on its parent position.
        for n in self.get_child_shapes(recursive=True):
            n.do_alignment()
        if not self.has_style(EnumShapeStyleFlags.NO_FIT_TO_CHILDREN):
            self.fit_to_children()
        if self.parentShape and kwargs.get('update_parent', True):
            self.parentShape.update()

    def refresh(self, rect: wx.Rect = None, delayed=False):
        if self.scene is None or self.view is None:
            return
        if rect is None:
            rect = self.get_boundingbox()
        if delayed:
            self.view.invalidate_rect(rect)
        else:
            self.view.refresh_with(False, rect)

    def draw(self, dc: wx.DC, draw_children: bool = True, **kwargs) -> None:
        """
        Draw shape. Default implementation tests basic shape visual states
        (normal/ready, mouse is over the shape, dragged shape can be accepted) and
        call appropriate virtual functions (DrawNormal, DrawHover, DrawHighlighted)
        for its visualisation. The function can be override if neccessary.
        Returns:

        """
        if self.scene is None or self.view is None:
            return
        if not self.states.visible:
            return
        # draw shadow if required
        if not self.states.selected and self.has_style(EnumShapeStyleFlags.SHOW_SHADOW):
            self.draw_with(dc, state=EnumDrawObjectState.SHADOWED)
        # draw itself
        if self.states.mouseOver and (self.highlightParent or self.has_style(EnumShapeStyleFlags.HOVERING)):
            if self.highlightParent:
                self.draw_with(dc, state=EnumDrawObjectState.HIGHLIGHTED)
                self.highlightParent = False
            else:
                self.draw_with(dc, state=EnumDrawObjectState.HOVERED)
        else:
            self.draw_with(dc, state=EnumDrawObjectState.NORMAL)
        # draw if selected
        if self.states.selected:
            self.draw_with(dc, state=EnumDrawObjectState.SELECTED)
        # draw connections points
        for x in self.connectionPts:
            x.draw(dc)
        # draw children
        if draw_children:
            for x in self.children:
                x.draw(dc, draw_children)

    def draw_with(self, dc: wx.DC, **kwargs) -> None:
        """
        Draw shape. Default implementation tests basic shape visual states
        (normal/ready, mouse is over the shape, dragged shape can be accepted) and
        call appropriate virtual functions (DrawNormal, DrawHover, DrawHighlighted)
        for its visualisation. The function can be override if neccessary.
        Returns:

        """
        raise NotImplementedError

    def contains(self, pos: wx.Point) -> bool:
        """
        Test whether the given point is inside the shape. The function
        can be override if neccessary.
        Args:
            pos:

        Returns:

        """
        return self.get_boundingbox().Contains(pos)

    def is_inside(self, rect: wx.Rect) -> bool:
        """
        Test whether the shape is completely inside given rectangle. The function
        can be override if neccessary.
        Args:
            rect:

        Returns:

        """
        return rect.Contains(self.get_boundingbox())

    def intersects(self, rect: wx.Rect) -> bool:
        """
        Test whether the given rectangle intersects the shape.
        Args:
            rect:

        Returns:

        """
        return rect.Intersects(self.get_boundingbox())

    @property
    def absolutePosition(self) -> wx.RealPoint:
        """
        Get the shape's absolute position in the canvas calculated as a sumation
        of all relative positions in the shapes' hierarchy. The function can be override if neccessary.

        Returns:

        """
        if self.parentShape:
            return self.relativePosition + self.parent.absolutePosition
        else:
            return wx.RealPoint(self.relativePosition)

    @property
    def parentAbsolutePosition(self) -> wx.RealPoint:
        _pt = wx.RealPoint(0, 0)
        if self.parentShape:
            if isinstance(self.parentShape, BasicLineShape) and self.customDockPoint != BASE_SHAPE_DOCK_POINT:
                return self.parentShape.get_dock_point_position(self.customDockPoint)
            else:
                return self.parentShape.absolutePosition
        return _pt

    def get_border_point(self, start: wx.RealPoint, end: wx.RealPoint) -> wx.RealPoint:
        """
        Get intersection point of the shape border and a line leading from
        'start' point to 'end' point.  Default implementation does nothing.
        The function can be override if neccessary.

        Args:
            start:
            end:

        Returns:

        """
        raise NotImplementedError

    def get_center(self) -> wx.RealPoint:
        """
        Get shape's center. Default implementation does nothing. The function can be override if neccessary.
        Returns:

        """
        _bb = self.get_boundingbox()
        return wx.RealPoint(_bb.GetLeft() + _bb.GetWidth() / 2, _bb.GetTop() + _bb.GetHeight() / 2)

    def get_boundingbox(self) -> wx.Rect:
        """
        Get shapes's bounding box. The function can be override if necessary.
        Returns:

        """
        return wx.Rect()

    def get_complete_boundingbox(self, flag: EnumShapeBBCalculationFlag = EnumShapeBBCalculationFlag.ALL) -> wx.Rect:
        """
        Get shape's bounding box which includes also associated child shapes and connections.
        the result will be updated in given rect
        Returns: None

        """
        self._lstProcessed.clear()
        return self._calc_complete_bb(flag)

    def _calc_complete_bb(self, flag: EnumShapeBBCalculationFlag):
        if self.scene is None:
            return
        if self in self._lstProcessed: return
        self._lstProcessed.append(self)
        _rect = wx.Rect()
        _lst_children = list()
        # first, get bounding box of the current shape
        if flag & EnumShapeBBCalculationFlag.SELF:
            _sr = self.get_boundingbox().Inflate(abs(self.horizontalBorder), abs(self.verticalBorder))
            if _rect.IsEmpty():
                _rect = _sr
            else:
                _rect = _rect.Union(_sr)
            # add also shadow offset if necessary
            if flag & EnumShapeBBCalculationFlag.SHADOW and self.has_style(EnumShapeStyleFlags.SHOW_SHADOW) and self.view is not None:
                _n_offset = self.view.setting.shadowOffset
                if _n_offset.x < 0:
                    _rect.SetX(_rect.GetX() + int(_n_offset.x))
                    _rect.SetWidth(_rect.GetWidth() - int(_n_offset.x))
                else:
                    _rect.SetWidth(_rect.GetWidth() + int(_n_offset.x))
                if _n_offset.y < 0:
                    _rect.SetY(_rect.GetY() + int(_n_offset.y))
                    _rect.SetHeight(_rect.GetHeight() - int(_n_offset.y))
                else:
                    _rect.SetHeight(_rect.GetHeight() + int(_n_offset.y))
        else:
            flag |= EnumShapeBBCalculationFlag.SELF
        # get list of all connection lines assigned to the shape and find their child shapes
        if flag & EnumShapeBBCalculationFlag.CONNECTIONS:
            _lines = self.get_assigned_connections(BasicLineShape, EnumShapeConnectionSearchMode.BOTH)
            for x in _lines:
                _lst_children.append(x)
                [_lst_children.append(n) for n in x.get_child_shapes()]
        # get children of this shape
        if flag & EnumShapeBBCalculationFlag.CHILDREN:
            [_lst_children.append(n) for n in self.get_child_shapes(recursive=False)]
            for n in _lst_children:
                _rect = _rect.Union(n.get_complete_boundingbox(flag))
        return _rect

    def scale(self, x: float, y: float, children: bool = True) -> None:
        """
        Scale the shape size by in both directions. The function can be override if necessary
        Returns:

        """
        if children:
            _des = self.get_child_shapes(recursive=True)
            for n in _des:
                if n.has_style(EnumShapeStyleFlags.RESIZE) and not isinstance(n, BasicTextShape):
                    n.scale(x, y, False)
                if n.has_style(EnumShapeStyleFlags.REPOSITION) and (n.verticalAlign == EnumShapeVAlign.NONE or n.horizontalAlign == EnumShapeHAlign.NONE):
                    # n.relativePosition.x *= x
                    # n.relativePosition.y *= y
                    n.position.x *= x
                    n.position.y *= y
                n.do_alignment()
        if self.scene: self.scene.isModified = True

    def move_to(self, pos: wx.RealPoint, mark=True) -> None:
        """
        Move the shape to the given absolute position. The function can be override if necessary.
        Returns:
        GetParentAbsolutePosition()
            wxSFShapeBase * pParentShape = GetParentShape();
            if(pParentShape)
            {
                if( m_pParentItem->IsKindOf(CLASSINFO(wxSFLineShape)) && m_nCustomDockPoint != sfdvBASESHAPE_DOCK_POINT)
                {
                    return ((wxSFLineShape*) m_pParentItem)->GetDockPointPosition( m_nCustomDockPoint );
                }
                else
                    return pParentShape->GetAbsolutePosition();
            }

            return wxRealPoint( 0, 0 );
        }

        """

        if self.parentShape:
            _p_apos = wx.RealPoint(self.parentAbsolutePosition)
        else:
            _p_apos = wx.RealPoint(0, 0)
        self.position = pos - _p_apos
        if self.scene and mark: self.scene.isModified = True

    def move_by(self, dx: float, dy: float, mark=True) -> None:
        """
        Move the shape by the given offset. The function can be override if necessary.
        Returns:

        """
        self.position.x += dx
        self.position.y += dy
        if self.scene and mark: self.scene.isModified = True

    # --------------------------------------------------------------
    # hierarchy handling
    # --------------------------------------------------------------
    @property
    def parentShape(self) -> 'WxShapeBase':
        return self.parent if self.parent and not self.parent.is_root else None

    def is_ancestor(self, child: 'WxShapeBase'):
        return child in self.descendants

    def is_descendant(self, parent: 'WxShapeBase'):
        return self in parent.descendants

    # --------------------------------------------------------------
    # common properties
    # --------------------------------------------------------------
    @property
    def customDockPoint(self) -> int:
        return self.stylesheet.dockPoint

    @customDockPoint.setter
    def customDockPoint(self, val):
        self.stylesheet.dockPoint = val

    @property
    def shapeUserData(self):
        return self.userData

    @shapeUserData.setter
    def shapeUserData(self, val: 'Serializable'):
        self.userData = val

    @property
    def scene(self):
        return self._shapeManager

    @scene.setter
    def scene(self, mgr):
        self._shapeManager = mgr
        for x in self.children:
            x.scene = mgr

    # --------------------------------------------------------------
    # style handling
    # --------------------------------------------------------------
    def set_style(self, style: int):
        self.style = style

    def add_style(self, style: int):
        self.style |= style

    def remove_style(self, style: int):
        self.style &= ~style

    def has_style(self, style):
        return self.style & style != 0

    def do_alignment(self):
        """
        Update the shape's position in order to its alignment
        Returns:

        """
        _parent_shape = self.parentShape
        if _parent_shape is None or _parent_shape.has_style(EnumShapeStyleFlags.DISABLE_DO_ALIGNMENT):
            return
        _parent_bb = wx.Rect()
        _line_pos = wx.RealPoint()
        _line_start = wx.RealPoint()
        _line_end = wx.RealPoint()
        _is_line_part = isinstance(_parent_shape, BasicLineShape)
        if _is_line_part:
            _line_pos = self.parentAbsolutePosition
            _parent_bb = wx.Rect(_line_pos.x, _line_pos.y, 1, 1)
        else:
            _parent_bb = _parent_shape.get_boundingbox()
        _this_bb = self.get_boundingbox()
        # do vertical alignment
        if self.verticalAlign == EnumShapeVAlign.TOP:
            self.position.y = self.verticalBorder
        elif self.verticalAlign == EnumShapeVAlign.MIDDLE:
            self.position.y = _parent_bb.GetHeight() / 2 - _this_bb.GetHeight() / 2
        elif self.verticalAlign == EnumShapeVAlign.BOTTOM:
            self.position.y = _parent_bb.GetHeight() - _this_bb.GetHeight() - self.verticalBorder
        elif self.verticalAlign == EnumShapeVAlign.EXPAND:
            if self.has_style(EnumShapeStyleFlags.RESIZE):
                self.position.y = self.verticalBorder
                # print('y scale--->',(_parent_bb.GetHeight() - 2 * self.verticalBorder) / _this_bb.GetHeight())
                self.scale(1.0, (_parent_bb.GetHeight() - 2 * self.verticalBorder - self.positionOffset.y) / _this_bb.GetHeight())
        elif self.verticalAlign == EnumShapeVAlign.LINE_START:
            if _is_line_part:
                _line_start, _line_end = _parent_shape.get_line_segment(0)
                if _line_end.y >= _line_start.y:
                    self.position.y = _line_start.y - _line_pos.y + self.verticalBorder
                else:
                    self.position.y = _line_start.y - _line_pos.y - _this_bb.GetHeight() - self.verticalBorder
        elif self.verticalAlign == EnumShapeVAlign.LINE_END:
            if _is_line_part:
                _line_start, _line_end = _parent_shape.get_line_segment(len(_parent_shape.controlPoints))
                if _line_end.y >= _line_start.y:
                    self.position.y = _line_start.y - _line_pos.y - _this_bb.GetHeight() - self.verticalBorder
                else:
                    self.position.y = _line_end.y - _line_pos.y + self.verticalBorder
        # do horizontal aligment
        if self.horizontalAlign == EnumShapeHAlign.LEFT:
            self.position.x = self.horizontalBorder
        elif self.horizontalAlign == EnumShapeHAlign.CENTER:
            self.position.x = _parent_bb.GetWidth() / 2 - _this_bb.GetWidth() / 2
        elif self.horizontalAlign == EnumShapeHAlign.EXPAND:
            if self.has_style(EnumShapeStyleFlags.RESIZE):
                self.position.x = self.horizontalBorder
                # print('x scale--->', (_parent_bb.GetWidth() - 2 * self.horizontalBorder-self.positionOffset.x) / _this_bb.GetWidth())
                self.scale((_parent_bb.GetWidth() - 2 * self.horizontalBorder) / _this_bb.GetWidth(), 1.0)
        elif self.horizontalAlign == EnumShapeHAlign.LINE_START:
            if _is_line_part:
                _parent_shape.get_line_segment(0, _line_start, _line_end)
                if _line_end.x >= _line_start.x:
                    self.position.x = _line_start.x - _line_pos.x + self.horizontalBorder
                else:
                    self.position.x = _line_start.x - _line_pos.x - _this_bb.GetWidth() - self.horizontalBorder
        elif self.horizontalAlign == EnumShapeHAlign.LINE_END:
            if _is_line_part:
                _parent_shape.get_line_segment(len(_parent_shape.controlPoints), _line_start, _line_end)
                if _line_end.x >= _line_start.x:
                    self.position.x = _line_start.x - _line_pos.x - _this_bb.GetWidth() - self.horizontalBorder
                else:
                    self.position.x = _line_end.x - _line_pos.x + self.horizontalBorder

    def fit_to_children(self):
        """
        Resize the shape to bound all child shapes. The function can be override if necessary.
        Returns:

        """
        pass

    @property
    def shapeStylesheet(self):
        return self.stylesheet

    @shapeStylesheet.setter
    def shapeStylesheet(self, ss: WxShapeBaseStylesheet):
        self.stylesheet = ss

    @property
    def selected(self):
        return self.states.selected

    @selected.setter
    def selected(self, state: bool):
        self.states.selected = state
        self.show_handles(state & (self.has_style(EnumShapeStyleFlags.SHOW_HANDLES)))

    @property
    def shown(self):
        return self.states.visible

    @shown.setter
    def shown(self, state: bool):
        self.states.visible = state

    @property
    def hoverColor(self):
        return self.stylesheet.hoverColor

    @hoverColor.setter
    def hoverColor(self, color: wx.Colour):
        self.stylesheet.hoverColor = color

    @property
    def activate(self):
        return self.states.active

    @activate.setter
    def activate(self, val: bool):
        """
        Shape's activation/deactivation
        Deactivated shapes are visible, but don't receive (process) any events.
        Args:
            val:

        Returns:

        """
        self.states.active = val

    # --------------------------------------------------------------
    # layout handling
    # --------------------------------------------------------------
    @property
    def relativePosition(self) -> wx.RealPoint:
        return self.position + self.positionOffset

    @relativePosition.setter
    def relativePosition(self, pos: wx.RealPoint):
        """
        Set shape's relative position. Absolute shape's position is then calculated
        as a sumation of the relative positions of this shape and all parent shapes in the shape's hierarchy
        Returns:

        """
        _diff = pos - self.positionOffset
        self.position.x = _diff.x
        self.position.y = _diff.y

    @property
    def verticalAlign(self) -> EnumShapeVAlign:
        return self.stylesheet.vAlign

    @verticalAlign.setter
    def verticalAlign(self, val: EnumShapeVAlign):
        self.stylesheet.vAlign = val

    @property
    def verticalBorder(self) -> float:
        return self.stylesheet.vBorder

    @verticalBorder.setter
    def verticalBorder(self, val: float):
        self.stylesheet.vBorder = val

    @property
    def horizontalAlign(self) -> EnumShapeHAlign:
        return self.stylesheet.hAlign

    @horizontalAlign.setter
    def horizontalAlign(self, val: EnumShapeHAlign):
        self.stylesheet.hAlign = val

    @property
    def horizontalBorder(self) -> float:
        return self.stylesheet.hBorder

    @horizontalBorder.setter
    def horizontalBorder(self, val: float):
        self.stylesheet.hBorder = val

    # --------------------------------------------------------------
    # handles handling
    # --------------------------------------------------------------
    def create_handles(self) -> None:
        """
        Function called by the framework responsible for creation of shape handles
        at the creation time. Default implementation does nothing. The function can be override if neccesary.
        Returns:

        """
        raise NotImplementedError

    def show_handles(self, show: bool) -> None:
        """
        Show/hide shape handles. Hidden handles are inactive.
        Returns:

        """
        for x in self.handles:
            if show:
                x.show()
            else:
                x.hide()

    @property
    def shapeHandles(self) -> list:
        return self.handles

    def get_handle(self, handle_type: EnumHandleType, id_=-1) -> HandleShapeObject:
        """
        id Handle ID (usefully only for line control points)
        Returns:

        """
        for x in self.handles:
            if x.type == handle_type and (id_ == -1 or id_ == x.id):
                return x

    def add_handle(self, handle_type: EnumHandleType, id_=-1) -> HandleShapeObject:
        """
        Add new handle to the shape.
        id Handle ID (usefully only for line control points)
        Returns:

        """
        _hnd = self.get_handle(handle_type, id_)
        if _hnd is None:
            _hnd = HandleShapeObject(parent=self, type=handle_type, n_id=id_)
            self.handles.append(_hnd)
        return _hnd

    def remove_handle(self, handle_type: EnumHandleType, id_=-1) -> None:
        """
        Remove given shape handle (if exists).
        id Handle ID (usefull only for line control points)
        Returns:

        """
        _hnd = self.get_handle(handle_type, id_)
        if _hnd is not None:
            self.handles.remove(_hnd)

    # --------------------------------------------------------------
    # shapes handling
    # --------------------------------------------------------------
    def get_leaf_shapes(self) -> list:
        _children = self.get_child_shapes(recursive=True)
        return [x for x in _children if x.is_leaf]

    def get_child_shapes(self, class_info: typing.Union[str, type] = None, recursive: bool = False, tree_search_mode=EnumShapeTreeSearchMode.BFS) -> list:
        """
        Get child shapes associated with this (parent) shape.
        Returns:

        """
        if recursive:
            if tree_search_mode == EnumShapeTreeSearchMode.BFS:
                if isinstance(class_info, str):
                    _descendants = self.bfs(self, filter_=lambda x: x.className == class_info)
                elif isinstance(class_info, type):
                    _descendants = self.bfs(self, filter_=lambda x: isinstance(x, class_info))
                else:
                    _descendants = self.bfs(self)
            elif tree_search_mode == EnumShapeTreeSearchMode.DFS:
                if isinstance(class_info, str):
                    _descendants = self.dfs(self, filter_=lambda x: x.className == class_info)
                elif isinstance(class_info, type):
                    _descendants = self.dfs(self, filter_=lambda x: isinstance(x, class_info))
                else:
                    _descendants = self.dfs(self)
            else:
                _descendants = self.descendants
        else:
            _descendants = self.children

        if self in _descendants:
            _descendants.remove(self)

        return list(_descendants)

    def get_neighbour_shapes(self, type_: type, connection_mode: EnumShapeConnectionSearchMode, direct: bool = True) -> list:
        """
        Get neighbour shapes connected to this shape.
        Returns:

        """
        if not isinstance(self, BasicLineShape):
            self._lstProcessed.clear()
            return self._get_neighbours(type_, connection_mode, direct)
        else:
            return []

    def _get_neighbours(self, type_: type, connection_mode: EnumShapeConnectionSearchMode, direct: bool = True) -> list:
        _ret = list()
        if self.scene is None:
            return _ret
        if self in self._lstProcessed:
            return _ret
        _conns = self.get_assigned_connections(type_, connection_mode)
        for con in _conns:
            if connection_mode == EnumShapeConnectionSearchMode.STARTING:
                _shp = self.scene.find_shape(con.srcShapeId)
            elif connection_mode == EnumShapeConnectionSearchMode.ENDING:
                _shp = self.scene.find_shape(con.dstShapeId)
            else:
                if self.uid == con.srcShapeId:
                    _shp = self.scene.find_shape(con.dstShapeId)
                else:
                    _shp = self.scene.find_shape(con.srcShapeId)
            # add opposite shape to the list
            if _shp is not None and not isinstance(_shp, BasicLineShape) and _shp not in _ret:
                _ret.append(_shp)
            # find next shape
            if not direct and _shp:
                # in the case of indirect branches we must differentiate between connections and ordinary shapes
                self._lstProcessed.append(self)
                if isinstance(_shp, BasicLineShape):
                    if connection_mode == EnumShapeConnectionSearchMode.STARTING:
                        _shp = self.scene.find_shape(_shp.srcShapeId)
                        if isinstance(_shp, BasicLineShape):
                            _ret.extend(self._get_neighbours(BasicLineShape, connection_mode, direct))
                        elif _shp not in _ret:
                            _ret.append(_shp)
                    elif connection_mode == EnumShapeConnectionSearchMode.ENDING:
                        _shp = self.scene.find_shape(_shp.dstShapeId)
                        if isinstance(_shp, BasicLineShape):
                            _ret.extend(self._get_neighbours(BasicLineShape, connection_mode, direct))
                        elif _shp not in _ret:
                            _ret.append(_shp)
                    else:
                        _shp = self.scene.find_shape(_shp.srcShapeId)
                        if isinstance(_shp, BasicLineShape):
                            _ret.extend(self._get_neighbours(BasicLineShape, connection_mode, direct))
                        elif _shp not in _ret:
                            _ret.append(_shp)

                        _shp = self.scene.find_shape(_shp.dstShapeId)
                        if isinstance(_shp, BasicLineShape):
                            _ret.extend(self._get_neighbours(BasicLineShape, connection_mode, direct))
                        elif _shp not in _ret:
                            _ret.append(_shp)
                else:
                    _ret.extend(self._get_neighbours(type_, connection_mode, direct))
        return _ret

    def get_assigned_connections(self, type_: type, mode: EnumShapeConnectionSearchMode) -> typing.Union[None, list]:
        """
        Get list of connections assigned to this shape.
        Returns:

        """
        if self.scene is None:
            return
        return self.scene.get_assigned_connections(self, type_, mode)

    # --------------------------------------------------------------
    # connection handling
    # --------------------------------------------------------------
    def is_connection_accepted(self, type_: str) -> bool:
        """
        Tells whether the given connection type is accepted by this shape (it means
        whether this shape can be connected to another one by a connection of given type).

        The function is typically used by the framework during interactive connection creation.
        Returns:

        """
        return type_ in self._wAcceptedConnections or IDENTITY_ALL in self._wAcceptedConnections

    def accept_connection(self, identity: str) -> None:
        """
        Add given connection type to an acceptance list. The acceptance list contains class
        names of the connection which can be accepted by this shape.
        Note: Keyword 'All' behaves like any class name.
        Returns:

        """
        self._wAcceptedConnections.append(identity)

    def clear_accepted_connections(self):
        self._wAcceptedConnections.clear()

    @property
    def acceptedConnections(self):
        return self._wAcceptedConnections

    def is_src_neighbour_accepted(self, type_: type) -> bool:
        """
        Tells whether the given shape type is accepted by this shape as its source neighbour(it means
        whether this shape can be connected from another one of given type).

        The function is typically used by the framework during interactive connection creation.
        Returns:

        """
        return type_ in self._sAcceptedSrcNeighbours or IDENTITY_ALL in self._sAcceptedSrcNeighbours

    def accept_src_neighbour(self, identity: str) -> None:
        """
        Add given shape type to an source neighbours' acceptance list. The acceptance list contains class
        names of the shape types which can be accepted by this shape as its source neighbour.
        Note: Keyword 'All' behaves like any class name.
        Returns:

        """
        self._sAcceptedSrcNeighbours.append(identity)

    @property
    def acceptedSrcNeighbours(self):
        return self._sAcceptedSrcNeighbours

    def is_dst_neighbour_accepted(self, type_: type) -> bool:
        """
        Tells whether the given shape type is accepted by this shape as its source neighbour(it means
        whether this shape can be connected from another one of given type).

        The function is typically used by the framework during interactive connection creation.
        Returns:

        """
        return type_ in self._sAcceptedDstNeighbours or IDENTITY_ALL in self._sAcceptedDstNeighbours

    def accept_dst_neighbour(self, identity: str) -> None:
        """
        Add given shape type to a source neighbours' acceptance list. The acceptance list contains class
        names of the shape types which can be accepted by this shape as its source neighbour.
        Note: Keyword 'All' behaves like any class name.
        Returns:

        """
        self._sAcceptedDstNeighbours.append(identity)

    @property
    def acceptedDstNeighbours(self):
        return self._sAcceptedDstNeighbours

    def clear_accepted_src_neighbour(self):
        self._sAcceptedSrcNeighbours.clear()

    def clear_accepted_dst_neighbour(self):
        self._sAcceptedDstNeighbours.clear()

    @property
    def shapeConnectionPoints(self) -> list:
        return self.connectionPts

    def get_connection_point(self, c_type: EnumConnectionPointType, id_=-1) -> ConnectionPointShapeObject:
        """
        Get connection point of given type assigned to the shape.
        Optional connection point ID
        Returns:

        """
        for pt in self.connectionPts:
            if pt.type_ == c_type and pt.uid == id_:
                return pt

    def get_closest_connection_point(self, pos: wx.RealPoint) -> ConnectionPointShapeObject:
        """
        Get connection point closest to the given position.
        Returns:

        """
        _lst = copy.deepcopy(self.connectionPts)
        if _lst:
            _sorted = sorted(_lst, key=lambda x: x.distance_to(pos))
            return _sorted[0]

    def add_connection_point_with(self, pos: wx.RealPoint, type_: EnumConnectionPointType, persistent: bool = True) -> ConnectionPointShapeObject:
        """
        Assign connection point of given type to the shape.
        Returns:

        """
        _pt = self.get_connection_point(type_)
        if _pt is not None:
            return _pt
        _pt = ConnectionPointShapeObject(self, pos, type_)
        _pt.enable_serialization(persistent)
        self.connectionPts.append(_pt)
        return _pt

    def add_connection_point(self, pt: ConnectionPointShapeObject, persistent: bool = True) -> None:
        """
        Assigned given connection point to the shape.
        Returns:

        """
        if pt is not None and pt not in self.connectionPts:
            pt.enable_serialization(persistent)
            self.connectionPts.append(pt)

    def remove_connection_point(self, type_: EnumConnectionPointType) -> None:
        """
        Remove connection point of given type from the shape (if present).
        Returns:

        """
        _pt = self.get_connection_point(type_)
        if _pt is not None:
            self.connectionPts.remove(_pt)

    # --------------------------------------------------------------
    # shapes drag drop handling
    # --------------------------------------------------------------
    def is_child_accepted(self, type_: typing.Union[str, 'WxShapeBase']) -> bool:
        """
        Tells whether the given shape type is accepted by this shape (it means
        whether this shape can be its parent).

        The function is typically used by the framework for determination whether a dropped
        shape can be assigned to an underlying shape as its child.
        Returns:

        """
        if isinstance(type_, WxShapeBase):
            type_ = type_.identity
        return type_ in self._ddAcceptedChildren or IDENTITY_ALL in self._ddAcceptedChildren

    def accept_currently_dragged_shapes(self) -> bool:
        """
        Function returns TRUE if all currently dragged shapes can be accepted
        Returns:

        """
        if self.scene is None or self.view is None: return False
        if not self.is_child_accepted(IDENTITY_ALL):
            for n in self.view.get_selected_shaped():
                if n.__class__.__name__ not in self._ddAcceptedChildren:
                    return False
        return True

    def accept_child(self, identity: str) -> None:
        """
        Add given shape type to an acceptance list. The acceptance list contains class
        names of the shapes which can be accepted as children of this shape.
        Note: Keyword 'All' behaves like any class name.
        Returns:

        """
        self._ddAcceptedChildren.append(identity)

    @property
    def ddAcceptedChildren(self):
        return self._ddAcceptedChildren

    def clear_accepted_children(self):
        self._ddAcceptedChildren.clear()

    # --------------------------------------------------------------
    # event emitting
    # --------------------------------------------------------------
    def handle_left_click(self, pos: wx.Point):
        """
        Event handler called when the shape is clicked by
        the left mouse button. The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emmits wxEVT_SF_SHAPE_LEFT_DOWN event.
        Args:
            pos:

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeMouseEvent(T_EVT_LEFT_DOWN)
            _evt.SetShape(self)
            _evt.SetMousePosition(pos)
            self.view.GetEventHandler().ProcessEvent(_evt)

    def handle_right_click(self, pos: wx.Point):
        """
        Event handler called when the shape is clicked by
        the right mouse button. The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emmits wxEVT_SF_SHAPE_RIGHT_DOWN event.
        Args:
            pos:

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeMouseEvent(T_EVT_RIGHT_DOWN)
            _evt.SetShape(self)
            _evt.SetMousePosition(pos)
            self.view.GetEventHandler().ProcessEvent(_evt)

    def handle_left_double_click(self, pos: wx.Point):
        """
        Event handler called when the shape is double-clicked by
        the left mouse button. The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emmits wxEVT_SF_SHAPE_LEFT_DCLICK event.
        Args:
            pos:

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeMouseEvent(T_EVT_LEFT_DCLICK)
            _evt.SetShape(self)
            _evt.SetMousePosition(pos)
            self.view.GetEventHandler().ProcessEvent(_evt)

    def handle_right_double_click(self, pos: wx.Point):
        """
        Event handler called when the shape is double-clicked by
        the left mouse button. The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emmits wxEVT_SF_SHAPE_RIGHT_DCLICK event.
        Args:
            pos:

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeMouseEvent(T_EVT_RIGHT_DCLICK)
            _evt.SetShape(self)
            _evt.SetMousePosition(pos)
            self.view.GetEventHandler().ProcessEvent(_evt)

    def handle_begin_drag(self, pos: wx.Point):
        """
        Event handler called at the begining of the shape dragging process.
        The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emmits wxEVT_SF_SHAPE_DRAG_BEGIN event.
        Args:
            pos:

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeMouseEvent(T_EVT_ON_DRAG_BEGIN)
            _evt.SetShape(self)
            _evt.SetMousePosition(pos)
            self.view.GetEventHandler().ProcessEvent(_evt)

    def handle_dragging(self, pos: wx.Point):
        """
        Event handler called during the shape dragging process.
        The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emmits wxEVT_SF_SHAPE_DRAG event.
        Args:
            pos:

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeMouseEvent(T_EVT_ON_DRAG)
            _evt.SetShape(self)
            _evt.SetMousePosition(pos)
            self.view.GetEventHandler().ProcessEvent(_evt)

    def handle_end_drag(self, pos: wx.Point):
        """
        Event handler called at the end of the shape dragging process.
        The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emits wxEVT_SF_SHAPE_DRAG_END event.
        Args:
            pos:

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeMouseEvent(T_EVT_ON_DRAG_END)
            _evt.SetShape(self)
            _evt.SetMousePosition(pos)
            self.view.GetEventHandler().ProcessEvent(_evt)

    def handle_begin_handle(self, handle: HandleShapeObject):
        """
        Event handler called when the user started to drag the shape handle.
        The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emits wxEVT_SF_SHAPE_HANDLE_BEGIN event.
        Args:
            handle: HandleShapeObject

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeHandleEvent(T_EVT_HANDLE_BEGIN)
            _evt.SetShape(self)
            _evt.SetHandle(handle)
            self.view.GetEventHandler().ProcessEvent(_evt)

    def handle_handle(self, handle: HandleShapeObject):
        """
        Event handler called when the user started to drag the shape handle.
        The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emmits wxEVT_SF_SHAPE_HANDLE event.
        Args:
            handle: HandleShapeObject

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeHandleEvent(T_EVT_HANDLE)
            _evt.SetShape(self)
            _evt.SetHandle(handle)
            self.view.GetEventHandler().ProcessEvent(_evt)

    def handle_end_handle(self, handle: HandleShapeObject):
        """
        Event handler called when the user started to drag the shape handle.
        The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emmits wxEVT_SF_SHAPE_HANDLE_END event.
        Args:
            handle: HandleShapeObject

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeHandleEvent(T_EVT_HANDLE_END)
            _evt.SetShape(self)
            _evt.SetHandle(handle)
            self.view.GetEventHandler().ProcessEvent(_evt)

    def handle_mouse_enter(self, pos: wx.Point):
        """
        Event handler called when a mouse pointer enters the shape area.
        The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emmits wxEVT_SF_SHAPE_MOUSE_ENTER event.
        Args:
            pos:

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeMouseEvent(T_EVT_MOUSE_ENTER)
            _evt.SetShape(self)
            _evt.SetMousePosition(pos)
            self.view.GetEventHandler().ProcessEvent(_evt)

    def handle_mouse_over(self, pos: wx.Point):
        """
        Event handler called when a mouse pointer moves above the shape area.
        The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emmits wxEVT_SF_SHAPE_MOUSE_OVER event.
        Args:
            pos:

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeMouseEvent(T_EVT_MOUSE_OVER)
            _evt.SetShape(self)
            _evt.SetMousePosition(pos)
            self.view.GetEventHandler().ProcessEvent(_evt)

    def handle_mouse_leave(self, pos: wx.Point):
        """
        Event handler called when a mouse pointer leaves the shape area.
        The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emmits wxEVT_SF_SHAPE_MOUSE_LEAVE event.
        Args:
            pos:

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeMouseEvent(T_EVT_MOUSE_LEAVE)
            _evt.SetShape(self)
            _evt.SetMousePosition(pos)
            self.view.GetEventHandler().ProcessEvent(_evt)

    def handle_key(self, key: int) -> bool:
        """
        Event handler called when any key is pressed (in the shape canvas).
        The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emmits wxEVT_SF_SHAPE_KEYDOWN event.
        Args:
            key:

        Returns: bool

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeKeyEvent(T_EVT_KEY_DOWN)
            _evt.SetShape(self)
            _evt.SetKeyCode(key)
            self.view.GetEventHandler().ProcessEvent(_evt)
        return True

    def handle_child_dropped(self, pos: wx.RealPoint, child: 'WxShapeBase'):
        """
        Event handler called when any shape is dropped above this shape (and the dropped
        shape is accepted as a child of this shape). The function can be override if necessary.

        The function is called by the framework (by the shape canvas).
        Default implementation emmits wxEVT_SF_SHAPE_CHILD_DROP event.
        Args:
            pos: wx.RealPoint
            child: WxShapeBase

        Returns:

        """
        if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS) and self.view is not None:
            _evt = WGShapeChildDropEvent(T_EVT_ON_CHILD_DROP)
            _evt.SetShape(self)
            _evt.SetChildShape(child)
            self.view.GetEventHandler().ProcessEvent(_evt)
