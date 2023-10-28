# -*- coding: utf-8 -*-
import copy
import os.path

import anytree
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_code_slot.py
# ------------------------------------------------------------------------------
#
# File          : _test_code_slot.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, wx.adv
from framework.application.base import TreeModel, TreeModelAnyTreeNode
from framework.application.define import _
from framework.gui.widgets import GenericBackgroundDialog
from framework.gui.base import TreeView, FeedbackDialogs
from mbt.application.code import CodeItem, FunctionItem, VariableItem
from mbt.application.define import EnumDataType, EnumValueType
from mbt.gui.code import FunctionCodeItemEditor, FunctionCodeItemParameterEditor, VariableCodeItemEditor
from mbt.gui.local_image_repo import MBTCodeItemImageList
from mbt.resources import IMAGES_PATH


class BaseCodeItemNode(TreeModelAnyTreeNode):
    def __init__(self, item: CodeItem = None):
        _label = str(item) if item is not None else 'Node'
        TreeModelAnyTreeNode.__init__(self, label=_label)
        self.item = item
        if isinstance(self.item, FunctionItem):
            self.icon = 'function'
        elif isinstance(self.item, VariableItem):
            self.icon = 'variable'
        else:
            self.icon = 'default'

    @property
    def ordId(self) -> int:
        if self.item is None:
            return -1
        return self.item.ordId


class CodeSlotTreeModel(TreeModel):
    def __init__(self):
        TreeModel.__init__(self, BaseCodeItemNode)
        self.functionsRootNode = self.append_node(self.root, item_class=CodeItem, name='Functions')
        self.functionsRootNode.label = _('Functions')

    def append_node(self, parent, **kwargs):
        _item_cls = kwargs.get('item_class')
        _cnode = _item_cls(**kwargs)
        _node = self.nodeClass(item=_cnode)
        _node.parent = parent
        return _node

    def add_function(self, **kwargs):
        self.append_node(self.functionsRootNode, item_class=FunctionItem, **kwargs)

    def _iter_children(self, parent: BaseCodeItemNode, item: CodeItem):
        for x in item.children:
            _snode = self.nodeClass(item=x)
            _snode.parent = parent
            if x.children:
                self._iter_children(_snode, x)

    def add_function_item(self, fi: FunctionItem):
        _node = self.nodeClass(item=fi)
        _node.parent = self.functionsRootNode
        self._iter_children(_node, fi)

    def remove_function_item(self, fi: FunctionItem):
        _node = anytree.find(self.functionsRootNode, lambda x: x.item is fi)
        if _node is not None:
            fi.parent = None
            self.remove_node(_node)
            del fi

    def remove_variable_item(self, vi: VariableItem):
        _node = anytree.find(self.functionsRootNode, lambda x: x.item is vi)
        if _node is not None:
            vi.parent = None
            self.remove_node(_node)
            del vi

    def update_function_item(self, fi: FunctionItem):
        _node = anytree.find(self.functionsRootNode, lambda x: x.item is fi)
        if _node is not None:
            _node.label = fi.to_string()
            _node.children = ()
            self._iter_children(_node, fi)

    def update_variable_item(self, vi: VariableItem):
        _node = anytree.find(self.functionsRootNode, lambda x: x.item is vi)
        if _node is not None:
            _node.label = vi.to_string()


class TestFrame(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.tb = wx.ToolBar(self)
        self._id_add = wx.NewIdRef()
        self._id_del = wx.NewIdRef()
        self._id_srt = wx.NewIdRef()
        self.tb.AddTool(self._id_add, 'Add', wx.ArtProvider.GetBitmap(wx.ART_PLUS))
        self.tb.AddTool(self._id_del, 'Delete', wx.ArtProvider.GetBitmap(wx.ART_MINUS))
        self.tb.AddTool(self._id_srt, 'Sort', wx.ArtProvider.GetBitmap(wx.ART_GO_UP))
        self.tb.Realize()
        self.model = CodeSlotTreeModel()
        _il = MBTCodeItemImageList()
        _il.initialize()
        self.treeView = TreeView(self, image_list=_il, image_list_map=_il.idxMap)
        self.treeView.set_model(self.model)

        self.model.add_function(name='TestFunc1')

        _tfi2 = FunctionItem(name='TestFunc2')
        _tfi2.add_parameter(VariableItem(name='var1'))
        _tfi2.add_parameter(VariableItem(name='var2'))
        _tfi2.add_parameter(VariableItem(name='var3'))

        self.model.add_function_item(_tfi2)

        self.treeView.RefreshItems()
        self.treeView.ExpandAll()

        # self.clockAnimation=wx.adv.Animation(os.path.join(IMAGES_PATH,'clock.gif'),type=wx.adv.ANIMATION_TYPE_GIF)
        # self.clockAnimationCtrl=wx.adv.AnimationCtrl(self,wx.ID_ANY,self.clockAnimation)
        # self.clockAnimationCtrl.SetInitialSize(wx.Size(36,36))
        # self.clockAnimationCtrl.Play()
        # bind event
        self.tb.Bind(wx.EVT_TOOL, self.on_tool)
        self.treeView.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_tree_item_activated)
        # layout
        self.SetSizer(self.mainSizer)
        # self.mainSizer.Add(self.clockAnimationCtrl,0,wx.EXPAND)
        self.mainSizer.Add(self.tb, 0, wx.EXPAND)
        self.mainSizer.Add(self.treeView, 1, wx.EXPAND)
        self.Layout()

    def on_tool(self, evt: wx.CommandEvent):
        _id = evt.GetId()
        if _id == self._id_add:
            _new_fi = FunctionItem(name=_('NewFunction'))
            _dlg = GenericBackgroundDialog(self)
            _dlg.SetTitle(_('Edit %s') % _new_fi.profile.name)
            _editor = FunctionCodeItemEditor(_dlg)
            _dlg.set_panel(_editor)
            _editor.set_content(_new_fi)
            _ret = _dlg.ShowModal()
            if _ret == wx.ID_OK:
                _editor.apply()
                self.model.add_function_item(_new_fi)
                self.treeView.RefreshItems()
        elif _id == self._id_del:
            if FeedbackDialogs.show_yes_no_dialog('Delete', 'Are you sure wanna delete selected item?'):
                _lst = self.treeView.get_selected()
                for x in self.treeView.get_selected():
                    if isinstance(x.item, FunctionItem):
                        self.model.remove_function_item(x.item)
                    elif isinstance(x.item, VariableItem):
                        self.model.remove_variable_item(x.item)
                self.treeView.RefreshItems()

    def edit_function_node(self, node: BaseCodeItemNode):
        if isinstance(node.item, FunctionItem):
            _dlg = GenericBackgroundDialog(self)
            _dlg.SetTitle(_('Edit %s') % node.item.profile.name)
            _editor = FunctionCodeItemEditor(_dlg)
            _dlg.set_panel(_editor)
            _org = node.item
            _for_editing = copy.deepcopy(_org)
            _editor.set_content(_for_editing)
            _ret = _dlg.ShowModal()
            if _ret == wx.ID_OK:
                _editor.apply()
                _org.update_from(_for_editing)
                self.model.update_function_item(_org)
                self.model.sort_children(node, attr='ordId')
                self.treeView.RefreshItems()

    def edit_variable_node(self, node: BaseCodeItemNode):
        if isinstance(node.item, VariableItem):
            _dlg = GenericBackgroundDialog(self)
            _dlg.SetTitle(_('Edit %s') % node.item.profile.name)
            _editor = VariableCodeItemEditor(_dlg)
            _dlg.set_panel(_editor)
            _org = node.item
            _for_editing = copy.deepcopy(_org)
            _editor.set_content(_for_editing)
            _ret = _dlg.ShowModal()
            if _ret == wx.ID_OK:
                _editor.apply()
                _org.update_from(_for_editing)
                self.model.update_variable_item(_org)
                self.treeView.RefreshItems()
            _dlg.Destroy()

    def on_tree_item_activated(self, evt: wx.TreeEvent):
        _item = evt.GetItem()
        _node: BaseCodeItemNode = self.treeView.item_to_node(_item)
        if _node.item is not None:
            if isinstance(_node.item, FunctionItem):
                self.edit_function_node(_node)
            elif isinstance(_node.item, VariableItem):
                self.edit_variable_node(_node)
            else:
                evt.Skip()


app = wx.App()
frame = TestFrame()
frame.Show()
app.MainLoop()
