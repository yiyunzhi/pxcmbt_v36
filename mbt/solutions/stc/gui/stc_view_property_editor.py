# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_view_property_editor.py
# ------------------------------------------------------------------------------
#
# File          : stc_view_property_editor.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import logging
from core.qtimp import QtCore, QtWidgets, QtGui
from core.gui.components import HeaderWidget,TodoBlockWidget
from core.gui.qtproperty_grid import PropertyGridManager, Property, PropertyModel
from mbt.gui.node_graph import NodeGraph, NodeObject
from mbt import appCtx

_log = logging.getLogger(__name__)


class STCGraphPropertyView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.mgr = None
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.header = HeaderWidget(self)
        self.header.set_content('Property Edit', description='Prompt Property detail')
        self.todoWidget=TodoBlockWidget(self)
        # todo: finish this
        self.todoWidget.append_todo('all properties will be as readonly implemented, update support only.')
        # bind event
        # layout
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.header)
        self.mainLayout.addWidget(self.todoWidget)


class STCGraphPropertyViewMgr:
    def __init__(self, content: NodeGraph, view_parent=None):
        self.view = STCGraphPropertyView(view_parent)
        self.view.mgr = self
        self.content = content
        self.propMgr = PropertyGridManager(parent=self.view)
        self.propMgr.sigPropertyChanged.connect(self.on_property_changed)
        # bind event
        self.content.sigNodeSelectionChanged.connect(self.on_node_selection_changed)
        self.content.sigPropertyChanged.connect(self.on_node_prop_changed)
        # setup
        self.setup()

    def setup(self):
        self.propMgr.clear()
        _prev_view = self.propMgr.view
        self.propMgr.setup()
        # todo: default view is tree, but set content margin here is bad thing, must in class setup
        self.propMgr.view.mainLayout.setContentsMargins(0, 0, 0, 0)
        if _prev_view:
            self.view.mainLayout.replaceWidget(_prev_view, self.propMgr.view)
        else:
            self.view.mainLayout.addWidget(self.propMgr.view)

    def on_property_changed(self, prop: Property):
        pass
        # prop.do_set()

    def on_node_selection_changed(self, sel_lst: list, unsel_lst: list):
        _log.debug('------->STCGraphPropertyViewMgr on_node_selection_changed: selected: %s, unselected: %s' % (sel_lst, unsel_lst))
        if not sel_lst:
            # todo: maybe show the properties things not relate to node
            return
        _node: NodeObject = sel_lst[0]
        self.propMgr.set_model(_node.propertyManager.propertyModel)
        self.propMgr.view.expand_all()

    def on_node_prop_changed(self, node, key, value):
        pass
