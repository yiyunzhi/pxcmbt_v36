# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _tmp_olv.py
# ------------------------------------------------------------------------------
#
# File          : _tmp_olv.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
#         self.olv = OLV.GroupListView(self, wx.ID_ANY, style=wx.LC_REPORT)
#         self.olv.cellEditMode = self.olv.CELLEDIT_DOUBLECLICK
#         self.olv.SetEmptyListMsg(_('there are no settings...'))
#         # todo: maybe a extra text for helping?
#         self.itemIconIdx = self.olv.AddImages(wx.ArtProvider.GetBitmap('pi.paperclip', size=wx.Size(16, 16)))
#         self.olv.SetColumns([
#             OLV.ColumnDefn('Name', 'left', -1, 'name', isEditable=False, minimumWidth=96,
#                            groupKeyGetter=lambda x: x.category, imageGetter=self.itemIconIdx),
#             OLV.ColumnDefn('Value', 'left', -1, 'value', valueSetter='value', isEditable=True, minimumWidth=96, ),
#             OLV.ColumnDefn('Description', 'left', -1, 'description', isEditable=False, minimumWidth=96, isSpaceFilling=True),
#         ])
#         # bind event
#         self.olv.Bind(OLV.EVT_CELL_EDIT_STARTING, self.on_cell_edit_starting)