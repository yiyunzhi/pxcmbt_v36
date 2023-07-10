# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_view_setting.py
# ------------------------------------------------------------------------------
#
# File          : stc_view_setting.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from core.qtimp import QtCore, QtGui, QtWidgets
from core.gui.components import HeaderWidget
from core.gui.qtproperty_grid import PropertyGridManager, Property
from .graph.graph import STCNodeGraph


class STCSettingView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.mgr = None
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.header = HeaderWidget(self)
        self.header.set_content('Setting', description='Setting of GraphEditor')
        # bind event
        # layout
        self.mainLayout.addWidget(self.header)
        self.setLayout(self.mainLayout)


class STCSettingViewMgr:
    def __init__(self, content: STCNodeGraph, view_parent: QtWidgets.QWidget = None):
        self.view = STCSettingView(view_parent)
        self.view.mgr=self
        self.content = content
        self.propMgr = PropertyGridManager(parent=self.view)
        self.propMgr.sigPropertyChanged.connect(self.on_property_changed)
        self.setup()

    def on_property_changed(self, prop: Property):
        prop.do_set()
        self.content.view.apply_setting()

    def setup(self):
        self.propMgr.clear()
        _prev_view = self.propMgr.view
        for x in self.content.viewSetting.propertyDefs:
            self.propMgr.append(x)
        self.propMgr.setup()
        # todo: bad part, must in class setup
        self.propMgr.view.mainLayout.setContentsMargins(0, 0, 0, 0)
        if _prev_view:
            self.view.mainLayout.replaceWidget(_prev_view, self.propMgr.view)
        else:
            self.view.mainLayout.addWidget(self.propMgr.view)
