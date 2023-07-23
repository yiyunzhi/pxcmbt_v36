import wx
from wx.lib.mixins.treemixin import VirtualTree, ExpansionState

try:
    import wx.lib.agw.customtreectrl as custom_tc
except ImportError:
    import wx.lib.customtreectrl as custom_tc
try:
    from agw.hypertreelist import HyperTreeList as TreeListCtrl
except ImportError:  # if it's not there locally, try the wxPython lib.
    from wx.lib.agw.hypertreelist import HyperTreeList as TreeListCtrl


class AbstractTreeViewMixin(VirtualTree):
    """Abstract tree view class for displaying tree model.
    Concrete implementation must inherit both this mixin class and a wx tree widget.
    More functionality and signals can be added if needed.
    Signals:
        selectionChanged - attribute 'node'
        itemActivated - attribute 'node'
        contextMenu - attribute 'node'
    """

    def __init__(self, parent, model=None, *args, **kwargs):
        _imgList = kwargs.pop('image_list') if 'image_list' in kwargs else None
        _imgListMap = kwargs.pop('image_list_map') if 'image_list_map' in kwargs else None
        super(AbstractTreeViewMixin, self).__init__(parent=parent, *args, **kwargs)
        self._imgList = _imgList
        self._imgListMap = _imgListMap
        if self._imgList is not None:
            assert self._imgListMap is not None
            self.AssignImageList(self._imgList)
            self.iconSize = self._imgList.GetSize()
        else:
            self.iconSize = wx.Size(16, 16)
        self._model = None
        if model is not None:
            self.set_model(model)

    def set_model(self, model):
        """Set tree model and refresh.
        :param model: tree model
        """
        self._model = model
        self.RefreshItems()

    def get_model(self):
        return self._model

    def OnGetItemText(self, index, column=0):
        """Overridden method necessary to communicate with tree model.
        :param index: index as explained in VirtualTree doc
        :param column: column index if applicable
        """
        _node = self._model.get_node_by_index(index)
        # remove & because of & needed in menu (&Files)
        _label = _node.label.replace("&", "")
        return _label

    def OnGetItemImage(self, index, which=wx.TreeItemIcon_Normal, column=0):
        if self._imgList is None:
            return wx.NO_IMAGE
        _node = self._model.get_node_by_index(index)
        _icon_var_name = _node.get_icon_variant()
        if _icon_var_name is None:
            return self._imgListMap.get('default',wx.NO_IMAGE)
        return self._imgListMap.get(_icon_var_name,wx.NO_IMAGE)

    def OnGetItemTextColour(self, index):
        _node = self._model.get_node_by_index(index)
        if _node.highlighted:
            return wx.Colour('#9acd32')
        else:
            return wx.Colour(wx.TEXT_ATTR_TEXT_COLOUR)

    def OnGetChildrenCount(self, index):
        """Overridden method necessary to communicate with tree model."""
        return len(self._model.get_children_by_index(index))

    def get_selected(self):
        """Get currently selected items.
        :return: list of nodes representing selected items (can be empty)
        """
        _selected = []
        for sel in self.GetSelections():
            _index = self.GetIndexOfItem(sel)
            _selected.append(self._model.get_node_by_index(_index))
        return _selected

    def select(self, node, select=True):
        """Select items.
        :param node: node representing item
        :param select: True/False to select/deselect
        """
        if node is None or self._model is None:
            return
        _index = self._model.get_index_of_node(node)
        for i in range(len(_index))[1:]:
            _item = self.GetItemByIndex(_index[:i])
            self.Expand(_item)
            # needed for wxPython 3:
            self.EnsureVisible(_item)
        _item = self.GetItemByIndex(_index)
        self.SelectItem(_item, select)

    def expand_node(self, node, recursive=True):
        """Expand items.
        :param node: node representing item
        :param recursive: True/False to expand all children
        """
        _index = self._model.get_index_of_node(node)
        _item = self.GetItemByIndex(_index)
        if recursive:
            self.ExpandAllChildren(_item)
        else:
            self.Expand(_item)
        self.EnsureVisible(_item)

    def ExpandAll(self, item=None):
        """Expand all items."""

        def _expand(item, root=False):
            if not root:
                self.Expand(item)
            _child, _cookie = self.GetFirstChild(item)
            while _child:
                _expand(_child)
                _child, _cookie = self.GetNextChild(item, _cookie)

        item = self.GetRootItem() if item is None else item
        _expand(item, True)

    def is_node_expanded(self, node):
        """Check if node is expanded"""
        _index = self._model.get_index_of_node(node)
        _item = self.GetItemByIndex(_index)

        return self.IsExpanded(_item)

    def collapse_node(self, node, recursive=True):
        """Collapse items.
        :param node: node representing item
        :param recursive: True/False to collapse all children
        """
        _index = self._model.get_index_of_node(node)
        _item = self.GetItemByIndex(_index)
        if recursive:
            self.CollapseAllChildren(_item)
        else:
            self.Collapse(_item)

    def refresh_node(self, node, recursive=False):
        """Refreshes node."""
        _index = self._model.get_index_of_node(node)
        if recursive:
            try:
                _item = self.GetItemByIndex(_index)
            except IndexError:
                return
            self.RefreshItemRecursively(_item, _index)
        else:
            self.RefreshItem(_index)

    def item_to_node(self, item):
        """Helper method for emitting signals.
        :param item: tree item
        """
        if not item or not item.IsOk():
            return
        _index = self.GetIndexOfItem(item)
        return self._model.get_node_by_index(_index)

    def node_to_item(self, node):
        _index = self._model.get_index_of_node(node)
        return self.GetItemByIndex(_index)


class TreeView(AbstractTreeViewMixin, wx.TreeCtrl):
    """Tree view class inheriting from wx.TreeCtrl"""

    def __init__(self, parent, model=None, *args, **kwargs):
        super(TreeView, self).__init__(parent=parent, model=model, *args, **kwargs)


class CustomTreeView(AbstractTreeViewMixin, custom_tc.CustomTreeCtrl):
    """Tree view class inheriting from wx.TreeCtrl"""

    def __init__(self, parent, model=None, **kwargs):
        if 'agwStyle' not in kwargs:
            kwargs['agwStyle'] = (
                    custom_tc.TR_HIDE_ROOT
                    | custom_tc.TR_FULL_ROW_HIGHLIGHT
                    | custom_tc.TR_HAS_BUTTONS
                    | custom_tc.TR_LINES_AT_ROOT
                    | custom_tc.TR_SINGLE
            )
        super(CustomTreeView, self).__init__(parent, model=model, **kwargs)
        self.SetBackgroundColour(wx.SystemSettings().GetColour(wx.SYS_COLOUR_WINDOW))


class TreeListView(AbstractTreeViewMixin, ExpansionState, TreeListCtrl):
    def __init__(self, parent, model=None, columns=[], **kwargs):
        self._columns = columns
        super(TreeListView, self).__init__(parent, model=model, **kwargs)
        for column in self._columns:
            self.AddColumn(column)
        self.SetMainColumn(0)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_right_click)
        self.evenRowsBackColor = wx.Colour(240, 248, 255)  # ALICE BLUE
        self.oddRowsBackColor = wx.Colour(255, 250, 205)  # LEMON CHIFFON
        self.useAlternativeColoring = False
        self.lastColumnFillSpace = False
        # self.groupTextColour = wx.Colour(33, 33, 33, 255)
        # self.groupBackgroundColour = wx.Colour(159, 185, 250, 249)
        self.Bind(wx.EVT_LIST_COL_END_DRAG, self.on_col_end_drag)

    def _apply_last_column_width(self):
        _w, _h = self.GetSize()
        _column_cnt = self.GetColumnCount()
        _used_width = sum([self.GetColumnWidth(i) for i in range(_column_cnt)])
        _free_space = _w - _used_width
        _col_w = self.GetColumnWidth(_column_cnt - 1)
        _set_w = _free_space + _col_w - 10
        if _set_w < 0:
            return
        self.SetColumnWidth(_column_cnt - 1, _set_w)

    def on_col_end_drag(self, evt):
        if self.lastColumnFillSpace:
            self._apply_last_column_width()
        evt.Skip()

    def OnSize(self, event):
        super(TreeListView, self).OnSize(event)
        if self.lastColumnFillSpace:
            self._apply_last_column_width()

    def use_alternative_coloring(self, state=True):
        self.useAlternativeColoring = state
        if self._model is not None:
            self.RefreshItems()

    def set_last_col_auto_fill(self, state=True):
        self.lastColumnFillSpace = state
        if self._model is not None:
            self.RefreshItems()

    def OnGetItemText(self, index, column=0):
        """Overridden method necessary to communicate with tree model.
        :param index: index as explained in VirtualTree doc
        :param column: column index if applicable
        """
        _node = self._model.get_node_by_index(index)
        # remove & because of & needed in menu (&Files)
        if column > 0:
            return _node.columns.get(self._columns[column], "")
        else:
            _label = _node.label.replace("&", "")
            return _label

    def OnGetItemBackgroundColour(self, index):
        if self.useAlternativeColoring:
            _col_cnt = self.GetColumnCount()
            _list_item = self.GetItemByIndex(index)
            _node = self._model.get_node_by_index(index)
            if _node.children:
                if _col_cnt > 1:
                    for i in range(1, _col_cnt):
                        _list_item.SetBackgroundColour(self.evenRowsBackColor, i)
                return self.evenRowsBackColor
            else:
                _idx = index[-1]
                if _idx % 2 == 0:
                    if _col_cnt > 1:
                        for i in range(1, _col_cnt):
                            _list_item.SetBackgroundColour(self.oddRowsBackColor, i)
                    return self.oddRowsBackColor
                else:
                    if _col_cnt > 1:
                        for i in range(1, _col_cnt):
                            _list_item.SetBackgroundColour(self.evenRowsBackColor, i)
                    return self.evenRowsBackColor
        else:
            return wx.NullColour

    def OnGetItemImage(self, index, which=wx.TreeItemIcon_Normal, column=0):
        if column > 0:
            return -1
        else:
            _node = self._model.get_node_by_index(index)
            if self._imgList is None or _node is None:
                return wx.NO_IMAGE
            _icon_var_name = _node.get_icon_variant()
            if _icon_var_name is None:
                return self._imgListMap.get('default', wx.NO_IMAGE)
            return self._imgListMap.get(_icon_var_name, wx.NO_IMAGE)

    def on_right_click(self, event):
        """Select item on right click.
        With multiple selection we don't want to deselect all items
        """
        _item = event.GetItem()
        if not self.IsSelected(_item):
            self.SelectItem(_item)
        event.Skip()
