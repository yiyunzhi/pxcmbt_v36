# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_editor_side_code_slot.py
# ------------------------------------------------------------------------------
#
# File          : stc_editor_side_code_slot.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, wx.adv, copy
from framework.application.define import _
from framework.gui.widgets import GenericBackgroundDialog
from framework.gui.base import TreeView, FeedbackDialogs
from mbt.application.code import FunctionItem, VariableItem, CodeTreeModel, BaseCodeItemTreeNode
from mbt.gui.code import FunctionCodeItemEditor, FunctionCodeItemParameterEditor, VariableCodeItemEditor
from mbt.gui.local_image_repo import MBTCodeItemImageList


class CodeSlotEditor(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.tb = wx.ToolBar(self)

        self.tb.AddTool(wx.ID_ADD, 'Add', wx.ArtProvider.GetBitmap(wx.ART_PLUS))
        self.tb.AddTool(wx.ID_DELETE, 'Delete', wx.ArtProvider.GetBitmap(wx.ART_MINUS))
        self.tb.Realize()
        self.model = CodeTreeModel()
        _il = MBTCodeItemImageList()
        _il.initialize()
        self.treeView = TreeView(self, image_list=_il, image_list_map=_il.idxMap)
        self.treeView.set_model(self.model)

        # self.model.add_function(name='TestFunc1')
        #
        # _tfi2 = FunctionItem(name='TestFunc2')
        # _tfi2.add_parameter(VariableItem(name='var1'))
        # _tfi2.add_parameter(VariableItem(name='var2'))
        # _tfi2.add_parameter(VariableItem(name='var3'))
        #
        # self.model.add_function_item(_tfi2)

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
        if _id == wx.ID_ADD:
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
        elif _id == wx.ID_DELETE:
            if FeedbackDialogs.show_yes_no_dialog('Delete', 'Are you sure wanna delete selected item?'):
                _lst = self.treeView.get_selected()
                for x in self.treeView.get_selected():
                    if isinstance(x.item, FunctionItem):
                        self.model.remove_function_item(x.item)
                    elif isinstance(x.item, VariableItem):
                        self.model.remove_variable_item(x.item)
                self.treeView.RefreshItems()

    def edit_function_node(self, node: BaseCodeItemTreeNode):
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

    def edit_variable_node(self, node: BaseCodeItemTreeNode):
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
        _node: BaseCodeItemTreeNode = self.treeView.item_to_node(_item)
        if _node.item is not None:
            if isinstance(_node.item, FunctionItem):
                self.edit_function_node(_node)
            elif isinstance(_node.item, VariableItem):
                self.edit_variable_node(_node)
            else:
                evt.Skip()
