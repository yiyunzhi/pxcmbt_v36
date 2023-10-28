# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_diagram_element_ortho_sizer.py
# ------------------------------------------------------------------------------
#
# File          : class_diagram_element_ortho_sizer.py
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
import anytree
from framework.gui.wxgraph import (WxShapeBase, RectShape, RectShapeStylesheet,
                                   EnumShapeStyleFlags, EnumShapeBBCalculationFlag,
                                   EnumShapeVAlign, EnumShapeHAlign)


class ElementOrthoSizerShapeStylesheet(RectShapeStylesheet):
    def __init__(self, **kwargs):
        RectShapeStylesheet.__init__(self, **kwargs)
        # self.backgroundStyle = wx.BRUSHSTYLE_TRANSPARENT
        # self.fillStyle = wx.BRUSHSTYLE_TRANSPARENT
        # self.borderStyle = wx.PENSTYLE_TRANSPARENT


class CellInfo(anytree.NodeMixin):
    def __init__(self):
        self.row = -1
        self.col = -1
        self.colRatio = -1
        self.rowRatio = -1

    def update(self):
        pass


class ElementOrthoSizerShape(RectShape):
    __identity__ = "ElementSizerShape"

    def __init__(self, **kwargs):
        RectShape.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', ElementOrthoSizerShapeStylesheet())
        self.set_style(EnumShapeStyleFlags.ALWAYS_INSIDE |
                       EnumShapeStyleFlags.RESIZE |
                       EnumShapeStyleFlags.PROPAGATE_SELECTION |
                       EnumShapeStyleFlags.PROPAGATE_HOVERING |
                       EnumShapeStyleFlags.DISABLE_DO_ALIGNMENT)
        self._cellIds = list()

    @property
    def cellIds(self):
        return self._cellIds

    def set_rect_size(self, w, h):
        super().set_rect_size(w, h)
        self.do_layout()

    def append(self, shape: WxShapeBase) -> bool:
        if shape.uid in self._cellIds:
            raise ValueError('cell id already exist')
        if shape not in self.descendants:
            shape.reparent(self)
        self._cellIds.append(shape.uid)
        self.update()
        return True

    def get_shape(self, uid: str) -> WxShapeBase:
        if uid in self._cellIds:
            _shape = self.find(self, lambda x: x.uid == uid)
            return _shape

    def remove(self, uid: str):
        _shape = self.find(self, lambda x: x.uid == uid)
        if _shape:
            _shape.parent = None

    def do_layout(self):
        # self.parentShape.set_rect_size(self.parentShape.stylesheet.size.x,self.parentShape.stylesheet.size.y*1.1)
        _shapes = [self.find(self, lambda x: x.uid == n) for n in self._cellIds]
        _this_bb = self.get_boundingbox()
        _this_h = _this_bb.GetHeight()
        _this_w = _this_bb.GetWidth()
        _x_offset, _y_offset = self.stylesheet.space, self.stylesheet.space

        for shape in _shapes:
            _shp_bb = shape.get_boundingbox()
            _trg_size = wx.Size()
            _trg_size.SetWidth(_this_w)
            _trg_size.SetHeight(max([_this_h, 60, _shp_bb.GetHeight()]))
            _trg_rect = wx.Rect(_x_offset,
                                _y_offset,
                                _trg_size.GetWidth(),
                                _trg_size.GetHeight())
            self._fit_shape_to_rect(shape, _trg_rect)
            print('layout--->WH:', _trg_rect)
        # _processed = list()
        # _size_map = list()
        # _this_bb = self.get_boundingbox()
        # _this_h = _this_bb.GetHeight()
        # _this_w = _this_bb.GetWidth()
        # _rest_h = _this_h
        # _rest_w = _this_w
        # _placed_shapes=list()
        # _x_offset, _y_offset = self.stylesheet.space, self.stylesheet.space
        # _placed_h=0
        # for shape in _shapes:
        #     _shp_bb = shape.get_boundingbox()
        #     _trg_size = wx.Size()
        #     _rest_shapes = [x for x in _shapes]
        #     [_rest_shapes.remove(x) for x in _processed]
        #     if self.stylesheet.orientation==EnumSizerOrientation.VERTICAL:
        #         if shape.horizontalAlign==EnumShapeHAlign.EXPAND:
        #             _trg_size.SetWidth(max(_shp_bb.GetWidth(), _this_w))
        #         else:
        #             _trg_size.SetWidth(_shp_bb.GetWidth())
        #         if shape.verticalAlign==EnumShapeVAlign.EXPAND:
        #             _trg_size.SetHeight(_this_h-_placed_h)
        #         _trg_size.SetHeight(max(_shp_bb.GetHeight(),60))
        #
        #     # if shape.horizontalAlign == EnumShapeHAlign.EXPAND:
        #     #             #     if self.stylesheet.orientation == EnumSizerOrientation.VERTICAL:
        #     #             #         _trg_size.SetWidth(max(_shp_bb.GetWidth(), _this_w))
        #     #             #     else:
        #     #             #         # _bw=max(self._get_best_size(_rest_shapes),_shp_bb.GetWidth())
        #     #             #         _trg_size.SetWidth(max(_shp_bb.GetWidth(), 10))
        #     #             #         # _rest_w
        #     #             # else:
        #     #             #     _trg_size.SetWidth(max(_shp_bb.GetWidth(), 10))
        #     #             # if shape.verticalAlign == EnumShapeVAlign.EXPAND:
        #     #             #     if self.stylesheet.orientation == EnumSizerOrientation.HORIZONTAL:
        #     #             #         _trg_size.SetHeight(max(_this_h, _shp_bb.GetHeight()))
        #     #             #     else:
        #     #             #         _trg_size.SetHeight(max(_shp_bb.GetHeight(),100))
        #     #             # else:
        #     #             #     _trg_size.SetHeight(max(_shp_bb.GetHeight(),10))
        #     _processed.append(shape)
        #     _trg_rect = wx.Rect(_x_offset,
        #                         _y_offset,
        #                         _trg_size.GetWidth() - 2 * self.stylesheet.space,
        #                         _trg_size.GetHeight() - 2 * self.stylesheet.space)
        #     #if _trg_rect.GetHeight()<60:
        #     #    print('--->',shape,_trg_rect)
        #     self._fit_shape_to_rect(shape, _trg_rect)
        #     if self.stylesheet.orientation == EnumSizerOrientation.VERTICAL:
        #         _y_offset += _trg_rect.GetHeight()
        #     elif self.stylesheet.orientation == EnumSizerOrientation.HORIZONTAL:
        #         _x_offset += _trg_rect.GetWidth()

    def do_layout1(self):
        # todo: do like add(proportion,expandFlag)???
        _shapes = [self.find(self, lambda x: x.uid == n) for n in self._cellIds]
        _this_bb = self.get_boundingbox()
        _this_h = _this_bb.GetHeight()
        _this_w = _this_bb.GetWidth()
        _size_map = {x.uid: (wx.Size(-1, -1), x.get_boundingbox()) for x in _shapes}
        # first determine the not expanded align
        for shape in _shapes:
            _shp_bb = shape.get_boundingbox()
            if shape.horizontalAlign != EnumShapeHAlign.EXPAND:
                _size_map[shape.uid][0].SetWidth(_shp_bb.GetWidth())
            if shape.verticalAlign != EnumShapeVAlign.EXPAND:
                _size_map[shape.uid][0].SetHeight(_shp_bb.GetWidth())
        _rest_space_h = _this_h - sum([v[0].GetHeight() for k, v in _size_map.items() if v[0].GetHeight() != -1])
        _rest_space_w = _this_w - sum([v[0].GetWidth() for k, v in _size_map.items() if v[0].GetWidth() != -1])
        _n_h_expand = len([v for k, v in _size_map.items() if v[0].GetHeight() == -1])
        _n_w_expand = len([v for k, v in _size_map.items() if v[0].GetWidth() == -1])
        _n_w_expand = max(_n_w_expand, 1)
        _n_h_expand = max(_n_h_expand, 1)
        _avg_h = int(_rest_space_h / _n_h_expand)
        _avg_w = int(_rest_space_w / _n_w_expand)
        _x_offset, _y_offset = self.stylesheet.space, self.stylesheet.space

        for k, v in _size_map.items():
            # todo: update the rest space
            _trg_size, _bb = v
            _shape = self.find(self, lambda x: x.uid == k)
            print('---->', _bb)
            if _trg_size.GetWidth() == -1:
                if self.stylesheet.orientation == EnumSizerOrientation.VERTICAL:
                    _trg_size.SetWidth(_this_w)
                else:
                    _trg_size.SetWidth(_avg_w)
                    _n_w_expand -= 1
            if _trg_size.GetHeight() == -1:
                if self.stylesheet.orientation == EnumSizerOrientation.VERTICAL:
                    _trg_size.SetHeight(max(_avg_h, _bb.GetHeight()))
                    _n_h_expand -= 1
                else:
                    _trg_size.SetHeight(_this_h)

            _trg_rect = wx.Rect(_x_offset,
                                _y_offset,
                                _trg_size.GetWidth() - 2 * self.stylesheet.space,
                                _trg_size.GetHeight() - 2 * self.stylesheet.space)
            self._fit_shape_to_rect(_shape, _trg_rect)
            if self.stylesheet.orientation == EnumSizerOrientation.VERTICAL:
                _y_offset += _trg_rect.GetHeight()
            elif self.stylesheet.orientation == EnumSizerOrientation.HORIZONTAL:
                _x_offset += _trg_rect.GetWidth()

    def do_alignment(self):
        super().do_alignment()

    def update(self, **kwargs):
        print('update-> isLeaf:%s' % self.is_leaf, self)
        # invalid ids
        _invalid_ids = list()
        for idd in self._cellIds:
            _shape = self.find(self, lambda x: x.uid == idd)
            if _shape is None:
                _invalid_ids.append(idd)
        [self._cellIds.remove(x) for x in _invalid_ids]
        self.do_alignment()
        self.do_layout()
        # fit the shape to its children
        if not self.has_style(EnumShapeStyleFlags.NO_FIT_TO_CHILDREN):
            self.fit_to_children()
        # do it recursively on all parent shapes
        if self.parentShape and kwargs.get('update_parent', True): self.parentShape.update()

    # def fit_to_children(self):
    #     _pos = self.absolutePosition
    #     _bb = wx.Rect(wx.Point(_pos), wx.Size(0, 0))
    #     for x in self.children:
    #         if x.has_style(EnumShapeStyleFlags.ALWAYS_INSIDE):
    #             _bb = _bb.Union(x.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF | EnumShapeBBCalculationFlag.CHILDREN))
    #     # do not let the grid shape 'disappear' due to zero sizes...
    #     if (not _bb.GetWidth() or not _bb.GetHeight()) and not self.stylesheet.space:
    #         _bb.SetWidth(10)
    #         _bb.SetHeight(10)
    #     self.stylesheet.size = wx.RealPoint(_bb.GetSize().x + 2 * self.stylesheet.space,
    #                                         _bb.GetSize().y + 2 * self.stylesheet.space)

    def handle_child_dropped(self, pos: wx.RealPoint, child: 'WxShapeBase'):
        if child is not None and isinstance(child, WxShapeBase):
            # todo: finish this
            self.append(child)

    def _fit_shape_to_rect(self, shape: WxShapeBase, rect: wx.Rect):
        _bb = shape.get_boundingbox()
        _prev_pos = shape.position
        _v_align = shape.verticalAlign
        if _v_align == EnumShapeVAlign.TOP:
            shape.position = wx.RealPoint(_prev_pos.x, rect.GetTop() + shape.verticalBorder)
        elif _v_align == EnumShapeVAlign.MIDDLE:
            shape.position = wx.RealPoint(_prev_pos.x, rect.GetTop() + (rect.GetHeight() / 2 - _bb.GetHeight() / 2))
        elif _v_align == EnumShapeVAlign.BOTTOM:
            shape.position = wx.RealPoint(_prev_pos.x, rect.GetBottom() - _bb.GetHeight() - shape.verticalBorder)
        elif _v_align == EnumShapeVAlign.EXPAND:
            if shape.has_style(EnumShapeStyleFlags.RESIZE):
                shape.position = wx.RealPoint(_prev_pos.x, rect.GetTop() + shape.verticalBorder)
                shape.scale(1.0, (rect.GetHeight() - 2 * shape.verticalBorder - shape.positionOffset.y) / _bb.GetHeight())
        else:
            shape.position = wx.RealPoint(_prev_pos.x, rect.GetTop())
        _prev_pos = shape.position
        _h_align = shape.horizontalAlign
        if _h_align == EnumShapeHAlign.LEFT:
            shape.position = wx.RealPoint(rect.GetLeft() + shape.horizontalBorder, _prev_pos.y)
        elif _h_align == EnumShapeHAlign.CENTER:
            shape.position = wx.RealPoint(rect.GetLeft() + rect.GetWidth() / 2 - _bb.GetWidth() / 2, _prev_pos.y)
        elif _h_align == EnumShapeHAlign.RIGHT:
            shape.position = wx.RealPoint(rect.GetRight() - _bb.GetWidth() - shape.horizontalBorder, _prev_pos.y)
        elif _h_align == EnumShapeHAlign.EXPAND:
            if shape.has_style(EnumShapeStyleFlags.RESIZE):
                shape.position = wx.RealPoint(rect.GetLeft() + shape.horizontalBorder, _prev_pos.y)
                shape.scale((rect.GetWidth() - 2 * shape.horizontalBorder - shape.positionOffset.x) / _bb.GetWidth(), 1.0)
        else:
            shape.position = wx.RealPoint(rect.GetLeft(), _prev_pos.y)
