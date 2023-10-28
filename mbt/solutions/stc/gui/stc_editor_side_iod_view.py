# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_editor_side_iod_view.py
# ------------------------------------------------------------------------------
#
# File          : stc_editor_side_iod_view.py
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
from mbt.application.ipod import IODItem, IODsTreeModel, IODManager, BaseIODItemTreeNode
from mbt.gui.ipod import IODItemEditor
from mbt.gui.local_image_repo import MBTModulePNGImageList


class IODViewEditor(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.tb = wx.ToolBar(self)
        self.tb.AddTool(wx.ID_ADD, 'Add', wx.ArtProvider.GetBitmap(wx.ART_PLUS))
        self.tb.AddTool(wx.ID_DELETE, 'Delete', wx.ArtProvider.GetBitmap(wx.ART_MINUS))
        self.tb.Realize()
        self.model = IODsTreeModel()
        _il = MBTModulePNGImageList()
        self.treeView = TreeView(self, image_list=_il, image_list_map=_il.idxMap)
        self.treeView.set_model(self.model)
        _iod_mgr = IODManager()
        self.model.set_iod_manager(_iod_mgr)

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
            _new_iod = IODItem(name=_('NewIOD'))
            _dlg = GenericBackgroundDialog(self)
            _dlg.Center()
            _dlg.SetTitle(_('Edit %s') % _new_iod.profile.name)
            _editor = IODItemEditor(_dlg)
            _dlg.set_panel(_editor)
            _editor.set_content(_new_iod)
            _ret = _dlg.ShowModal()
            if _ret == wx.ID_OK:
                _editor.apply()
                self.model.add_iod_item(_new_iod)
                self.treeView.RefreshItems()
        elif _id == wx.ID_DELETE:
            if not all([x.item for x in self.treeView.get_selected()]):
                return
            if FeedbackDialogs.show_yes_no_dialog('Delete', 'Are you sure wanna delete selected item?'):
                _lst = self.treeView.get_selected()
                for x in self.treeView.get_selected():
                    if isinstance(x.item, IODItem):
                        self.model.remove_iod_item(x.item)
                self.treeView.RefreshItems()

    def edit_iod_node(self, node: BaseIODItemTreeNode):
        if isinstance(node.item, IODItem):
            _dlg = GenericBackgroundDialog(self)
            _dlg.Center()
            _dlg.SetTitle(_('Edit %s') % node.item.profile.name)
            _editor = IODItemEditor(_dlg)
            _dlg.set_panel(_editor)
            _org = node.item
            _for_editing = copy.deepcopy(_org)
            _editor.set_content(_for_editing)
            _ret = _dlg.ShowModal()
            if _ret == wx.ID_OK:
                _editor.apply()
                _org.update_from(_for_editing)
                self.model.update_iod_item(_org)
                self.model.sort_children(node, attr='ordId')
                self.treeView.RefreshItems()

    def on_tree_item_activated(self, evt: wx.TreeEvent):
        _item = evt.GetItem()
        _node: BaseIODItemTreeNode = self.treeView.item_to_node(_item)
        if _node.item is not None:
            if isinstance(_node.item, IODItem):
                self.edit_iod_node(_node)
            else:
                evt.Skip()
