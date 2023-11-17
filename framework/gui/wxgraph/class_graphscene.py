# -*- coding: utf-8 -*-
import typing

import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_scene.py
# ------------------------------------------------------------------------------
#
# File          : class_scene.py
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
from .class_shape_control import ControlShape
from .class_shape_line import LineShape
from .utils import *
from .define import *


class ConnIdPair:
    def __init__(self, new_id, old_id):
        self.newId = new_id
        self.oldId = old_id


class GraphScene:
    def __init__(self):
        self._version = '1.27'
        self._view = None
        self._isModified = False
        # initial a dummy shape as root
        self._rootShape = WxShapeBase(uid='__root__')
        self._foregroundRootShape = WxShapeBase()
        self._foregroundRootShape.style = 0
        self._rootShape.style = 0
        self._rootShape.states.visible = False
        self._foregroundRootShape.states.visible = False
        self._rootShape.states.active = False
        self._foregroundRootShape.states.active = False

        self._acceptedShapes = list()
        # the top shape means the shapes use _rootShape as parent.
        self._acceptedTopShapes = list()
        self._idPairs = list()
        self._linesForUpdate = list()
        self._gridsForUpdate = list()
        self._connIdPairs = list()

    @property
    def rootShape(self):
        return self._rootShape

    @rootShape.setter
    def rootShape(self, shape: WxShapeBase):
        if shape is self._rootShape:
            return
        self._rootShape = shape
        # fixme: need assign scene again, possible to optimize, some descedants may lose the scene, why???
        # reassign be called expectly only in undoStack method do or undo
        for x in self._rootShape.children:
            x.scene = self
            x.post_init()

    @property
    def foregroundRootShape(self):
        return self._foregroundRootShape

    def is_top_most_shape(self, shape: WxShapeBase):
        return shape.parentShape is not None and shape.parentShape.is_root

    def is_foreground_shape(self, shape: WxShapeBase):
        return shape.root is self._foregroundRootShape

    def get_common_ancestors(self, *shapes: WxShapeBase):
        _ancestors = [node.ancestors for node in shapes]
        _common = []
        for parent_nodes in zip(*_ancestors):
            parent_node = parent_nodes[0]
            if all([parent_node is p for p in parent_nodes[1:]]):
                _common.append(parent_node)
            else:
                break
        return tuple(_common)

    def create_connection(self, src_id: int, dst_id: int, line: LineShape, save_state=True) -> (bool, str):
        _ret, _res = self.add_shape(line, wx.DefaultPosition, None, initialize=True, save_state=False)
        if not _ret:
            return _ret, _res
        line.srcShapeId = src_id
        line.dstShapeId = dst_id
        if self.view:
            if save_state:
                self.view.save_state(reason='ConnectionCreated')
            line.refresh()
        return True, ''

    def update_connections(self):
        if self._linesForUpdate:
            for x in self._linesForUpdate:
                _new_src_id = _old_src_id = x.srcShapeId
                _new_dst_id = _old_dst_id = x.srcShapeId
                for id_pair in self._idPairs:
                    if _old_src_id == id_pair.oldId:
                        _new_src_id = id_pair.newId
                    if _old_dst_id == id_pair.oldId:
                        _new_dst_id = id_pair.newId
                x.srcShapeId = _new_src_id
                x.dstShapeId = _new_dst_id
                # check whether line's src and trg shapes really exists
                _src_shape = self.find_shape(x.srcShapeId)
                _dst_shape = self.find_shape(x.dstShapeId)
                if _src_shape is None or _dst_shape is None:
                    self.remove_shape(x.uid)
            self._linesForUpdate.clear()

    def update_grids(self):
        if self._gridsForUpdate:
            for g in self._gridsForUpdate:
                for id_pair in self._idPairs:
                    _n_idx = g.cells.index(id_pair.oldId)
                    if _n_idx != -1:
                        g.cells[_n_idx] = id_pair.newId
                # check whether grid's children really exists
                for c_id in g.cells:
                    _s = self.find_shape(c_id)
                    if _s is None:
                        g.remove_from_grid(c_id)
            self._gridsForUpdate.clear()

    def add_shape(self, shape: WxShapeBase, pos: wx.Point = None, parent_shape: WxShapeBase = None, initialize=True, save_state=True) -> (bool, str):
        if shape is None:
            return False, 'shape instance is None'
        _is_foreground = shape.isForeground
        if parent_shape is None:
            if _is_foreground:
                parent_shape = self._foregroundRootShape
            else:
                parent_shape = self._rootShape
        if not self.is_shape_accepted(shape):
            return False, 'not accepted shape type.'
        if pos is None:
            pos = self.view.lp2dp(shape.absolutePosition)
            # _pos = wx.GetMousePosition()
            # pos = self.view.ScreenToClient(wx.GetMousePosition())
        if self.view:
            _a_pos = self.view.fit_position_to_grid(self.view.dp2lp(pos))
            shape.relativePosition = wg_util_conv2realpoint(_a_pos)
        else:
            shape.relativePosition = wg_util_conv2realpoint(pos)
        if not isinstance(shape, LineShape):
            if parent_shape is None:
                parent_shape = self.get_shape_at_position(shape.relativePosition)
            if parent_shape:
                if not parent_shape.is_child_accepted(shape.identity):
                    parent_shape = None
                else:
                    shape.relativePosition = wx.RealPoint(pos - wx.Point(parent_shape.absolutePosition))
        else:
            parent_shape = self.rootShape

        if parent_shape and parent_shape is not self._rootShape:
            self._add_item(shape, parent_shape)
        else:
            if self.is_top_shape_accepted(shape):
                self._add_item(shape, self.rootShape)
            else:
                return False, 'not accepted top shape type.'
        if shape.scene is not self:
            shape.scene = self
        if initialize:
            shape.post_init()
        # reset scale of assigned shape canvas
        if self.view and isinstance(shape, ControlShape):
            self.view.set_scale(1)
        if self.view:
            if save_state:
                self.view.save_view_state('Create')
        self._isModified = True
        return True, ''

    def remove_shape(self, shape_info: typing.Union[WxShapeBase, int], refresh=True, start_from: WxShapeBase = None):
        if isinstance(shape_info, WxShapeBase):
            _shape = shape_info
        else:
            _shape = self.find_shape(shape_info, start_from)
        if _shape is None or _shape.is_root:
            return
        _shape_parent = _shape.parentShape
        _lst_conns=list()
        _lst_conns.extend(self.get_assigned_connections(_shape,LineShape,EnumShapeConnectionSearchMode.BOTH))
        for x in _shape.descendants:
            _lst_conns.extend(self.get_assigned_connections(x, LineShape, EnumShapeConnectionSearchMode.BOTH))
        for l in _lst_conns:
            self.remove_shape(l.uid, False)
        # remove the shape also from currentShapes list
        if self.view: self.view.remove_from_temporaries(_shape)
        self._remove_item(_shape)
        self._isModified = True
        if _shape_parent is not None and not _shape_parent.is_root:
            _shape_parent.update()
        if refresh and self.view is not None: self.view.Refresh(False)

    def remove_shapes(self, shape_ids: list):
        for x in shape_ids:
            self.remove_shape(x, False)
        if self.view is not None: self.view.Refresh(False)

    def clear(self, start_from: WxShapeBase = None):
        if not start_from.children:
            # ignore while no shapes managed by start_from node.
            return
        self._remove_all_item(start_from)
        if self.view:
            self.view.clear()
            self.view.update_virtual_size()

    def _add_item(self, node: WxShapeBase, parent_node: WxShapeBase):
        node.parent = parent_node

    def _remove_all_item(self, start_from: WxShapeBase = None):
        if start_from is None:
            start_from = self._rootShape
        for x in start_from.children:
            x.parent = None

    def _remove_item(self, node: WxShapeBase):
        node.parent = None

    def move_shapes_from_negatives(self):
        _shapes = self.find_shapes_by_type(WxShapeBase)
        _min_x, _min_y = 0, 0
        for x in _shapes:
            _min_x = min(_min_x, x.absolutePosition.x)
            _min_y = min(_min_y, x.absolutePosition.y)
        # move all parents shape so they (and their children) will be located in the positive values only
        if _min_x < 0 or _min_y < 0:
            for x in _shapes:
                if x.parentShape is None:
                    if _min_x < 0: x.move_by(abs(_min_x), 0)
                    if _min_y < 0: x.move_by(0, abs(_min_y))

    def update_all(self, start_from: WxShapeBase = None):
        _shapes = self.find_shapes_by_type(WxShapeBase, start_from)
        for x in _shapes:
            if not self.shape_has_children(x):
                x.update()

    def accept_shape(self, type_: typing.Union[str, WxShapeBase]):
        """
        Add given shape type to an acceptance list. The acceptance list contains class
        names of the shapes which can be inserted into this instance of shapes canvas.
        Note: Keyword 'All' behaves like any class name.
        Args:
            type_:

        Returns:

        """
        if isinstance(type_, WxShapeBase):
            type_ = type_.identity
        if type_ not in self._acceptedShapes:
            self._acceptedShapes.append(type_)

    def is_shape_accepted(self, type_: typing.Union[str, WxShapeBase]):
        """
        Add given shape type to an acceptance list. The acceptance list contains class
        names of the shapes which can be inserted into this instance of shapes canvas.
        Note: Keyword 'All' behaves like any class name.
        Args:
            type_:

        Returns:

        """
        if isinstance(type_, WxShapeBase):
            type_ = type_.identity
        return type_ in self._acceptedShapes or IDENTITY_ALL in self._acceptedShapes

    def is_top_shape_accepted(self, type_: typing.Union[str, WxShapeBase]):
        """
        Add given shape type to an acceptance list. The acceptance list contains class
        names of the shapes which can be inserted into this instance of shapes canvas.
        Note: Keyword 'All' behaves like any class name.
        Args:
            type_:

        Returns:

        """
        if isinstance(type_, WxShapeBase):
            type_ = type_.identity
        return type_ in self._acceptedTopShapes or IDENTITY_ALL in self._acceptedTopShapes

    def accept_top_shape(self, type_: str):
        """
        Add given shape type to list of accepted top shapes. The acceptance list contains class
        names of the shapes which can be inserted into this instance of shapes canvas as a shape without
        any parent (i.e. shape placed directly onto the canvas).
        Note: Keyword 'All' behaves like any class name.
        Args:
            type_:

        Returns:

        """
        if type_ not in self._acceptedTopShapes:
            self._acceptedTopShapes.append(type_)

    def clear_accepted_shapes(self):
        self._acceptedShapes.clear()

    def clear_accepted_top_shapes(self):
        self._acceptedTopShapes.clear()

    @property
    def acceptedShapes(self):
        return self._acceptedShapes

    @property
    def acceptedTopShapes(self):
        return self._acceptedTopShapes

    def find_shape(self, uid: str, start_from: WxShapeBase = None) -> WxShapeBase:
        if start_from is None:
            start_from = self._rootShape
        return start_from.find(start_from, lambda x: x.uid == uid and not x.is_root)

    def find_shapes_by_type(self, type_: type, start_from: WxShapeBase = None, tree_search_mode=EnumShapeTreeSearchMode.BFS) -> list:
        if start_from is None:
            start_from = self._rootShape

        def _filter(node):
            return isinstance(node, type_) and not node.is_root

        if tree_search_mode == EnumShapeTreeSearchMode.BFS:
            return start_from.bfs(start_from, filter_=_filter)
        elif tree_search_mode == EnumShapeTreeSearchMode.DFS:
            return start_from.dfs(start_from, filter_=_filter)
        else:
            return list(start_from.find_all(start_from, _filter))

    def find_shapes_by_class_name(self, class_name: str, start_from: WxShapeBase = None, tree_search_mode=EnumShapeTreeSearchMode.BFS) -> list:
        if start_from is None:
            start_from = self._rootShape

        def _filter(node):
            return node.className == class_name and not node.is_root

        if tree_search_mode == EnumShapeTreeSearchMode.BFS:
            return start_from.bfs(start_from, filter_=_filter)
        elif tree_search_mode == EnumShapeTreeSearchMode.DFS:
            return start_from.dfs(start_from, filter_=_filter)
        else:
            return list(start_from.find_all(start_from, _filter))

    def find_shapes_by_identity(self, identity: str, start_from: WxShapeBase = None, tree_search_mode=EnumShapeTreeSearchMode.BFS) -> list:
        if start_from is None:
            start_from = self._rootShape

        def _filter(node):
            return node.identity == identity and not node.is_root

        if tree_search_mode == EnumShapeTreeSearchMode.BFS:
            return start_from.bfs(start_from, filter_=_filter)
        elif tree_search_mode == EnumShapeTreeSearchMode.DFS:
            return start_from.dfs(start_from, filter_=_filter)
        else:
            return list(start_from.find_all(start_from, _filter))

    def get_shapes(self, shape_class_name: str, start_from: WxShapeBase = None, tree_search_mode=EnumShapeTreeSearchMode.BFS):
        """
        Get list of shapes of given type.
        Args:
            shape_class_name
            start_from
            tree_search_mode

        Returns:

        """
        return self.find_shapes_by_class_name(shape_class_name, start_from, tree_search_mode)

    def get_shape_at_position(self, pos, z_val=1, search_mode: EnumShapeSearchMode = EnumShapeSearchMode.BOTH) -> WxShapeBase:
        # sort shapes list in the way that the line shapes will be at the top of the list
        _shapes = self.find_shapes_by_type(WxShapeBase)
        _sorted_shapes = list()
        _cnt = 0
        for s in _shapes:
            if isinstance(s, LineShape):
                _sorted_shapes.insert(0, s)
                _cnt += 1
            else:
                _sorted_shapes.insert(_cnt, s)
        # find the topmost shape according to the given rules
        _cnt = 1
        for s in _sorted_shapes:
            if s.states.visible and s.states.active and s.contains(pos):
                if search_mode == EnumShapeSearchMode.SELECTED:
                    if s.states.selected:
                        if _cnt == z_val:
                            return s
                        else:
                            _cnt += 1
                elif search_mode == EnumShapeSearchMode.UNSELECTED:
                    if not s.states.selected:
                        if _cnt == z_val:
                            return s
                        else:
                            _cnt += 1
                elif search_mode == EnumShapeSearchMode.BOTH:
                    if _cnt == z_val:
                        return s
                    else:
                        _cnt += 1

    def get_shape_inside(self, rect: wx.Rect):
        _shapes = self.find_shapes_by_type(WxShapeBase)
        _ret = list()
        for s in _shapes:
            if s.state.visible and s.state.active and s.intersects(rect):
                _ret.append(s)
        return _ret

    @property
    def isEmpty(self):
        return self._rootShape is None or len(self._rootShape.children) < 1

    @property
    def isModified(self):
        return self._isModified

    @isModified.setter
    def isModified(self, state):
        self._isModified = state

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, val):
        self._view = val

    def shape_has_children(self, shape: WxShapeBase) -> bool:
        return len(shape.children) > 0

    def get_neighbours(self, shape: WxShapeBase, neighbours_class_name, connection_mode: EnumShapeConnectionSearchMode, direct: bool = True) -> list:
        _ret = list()
        if shape.is_root:
            return _ret
        if shape:
            return shape.get_neighbour_shapes(neighbours_class_name, connection_mode, direct)
        else:
            for x in self._rootShape.children:
                _ret.extend(x.get_neighbour_shapes(neighbours_class_name, connection_mode, direct))
        return _ret

    def get_assigned_connections(self, parent_shape: WxShapeBase, shape_class: type, connection_mode: EnumShapeConnectionSearchMode) -> list:
        """
        Get list of connections assigned to given parent shape.
        Args:
            parent_shape:
            shape_class:
            connection_mode:

        Returns:

        """
        _ret = list()
        if parent_shape.is_root:
            return _ret
        _lines = self.find_shapes_by_type(shape_class)
        for x in _lines:
            if connection_mode == EnumShapeConnectionSearchMode.STARTING:
                if x.srcShapeId == parent_shape.uid:
                    _ret.append(x)
            elif connection_mode == EnumShapeConnectionSearchMode.ENDING:
                if x.dstShapeId == parent_shape.uid:
                    _ret.append(x)
            elif connection_mode == EnumShapeConnectionSearchMode.BOTH:
                if x.srcShapeId == parent_shape.uid or x.dstShapeId == parent_shape.uid:
                    _ret.append(x)
        return _ret

    def deserialize(self, stream: any):
        raise NotImplementedError
