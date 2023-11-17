# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_view_manager.py
# ------------------------------------------------------------------------------
#
# File          : class_view_manager.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import anytree, wx
import wx, typing
import warnings
import anytree
import blinker
from framework.application.base import Serializable, ZViewContentContainer
from framework.application.uri_handle import AppURI
from framework.application.urlobject import URLObject


class SupportedOpQueryManager:
    def __init__(self):
        self._map = dict()
        self._vMap = dict()

    def is_op_supported(self, op_name: str):
        if op_name not in self._vMap:
            return False
        return self._vMap[op_name]

    def register(self, sop_id: str, default_value: typing.Any, getter: typing.Callable = None):
        if getter is not None:
            assert callable(getter)
        self._map.update({sop_id: (default_value, getter)})
        self._vMap.update({sop_id: default_value})

    def update(self):
        for k, v in self._map.items():
            _dv, _g = v
            if _g is None:
                self._vMap[k] = _dv
            else:
                self._vMap[k] = _g()

    def get_query_uri(self):
        self.update()
        _q = URLObject()
        for k, v in self._vMap.items():
            _q.add_query_param(k, str(v))
        return _q


class ISupportedOpContainer:
    sigSupportedOperationURIChanged = blinker.signal('sigSupportedOperationURIChanged')

    def __init__(self):
        self.sopQueryMgr = SupportedOpQueryManager()
        self.supportedOperationUri = AppURI(uri_path='supportedOperation', scheme='ISupportedOpContainer')
        self.supportedOperationUri.sigUriQueryChanged.connect(self.emit_sop_changed_evt)

    @staticmethod
    def format_sop_id(group, name):
        return '%s.%s' % (group, name)

    def emit_sop_changed_evt(self):
        self.sigSupportedOperationURIChanged.send(self, uri=self.supportedOperationUri)

    def exec_operation(self, op_name, **kwargs):
        raise NotImplementedError


class ZView:
    def __init__(self, **kwargs):
        self._title = kwargs.get('title', 'Untitled')
        self._mgr = kwargs.get('manager')
        if not hasattr(self, 'GetId') and not isinstance(self, wx.Window):
            raise RuntimeError('this class could not be instanced lonely, mixed with derived wx.Windows required.')

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val: str):
        self._title = val

    @property
    def manager(self):
        return self._mgr

    @manager.setter
    def manager(self, val: 'ViewManager'):
        self._mgr = val


class ViewManager(anytree.NodeMixin):
    """
    two ways to creating a view from this object:
    1: pass ZView instance as 'view' key argument
    2: pass ZView instance factory,viewId and view options in key arguments.
    additional you could inherit this class and the attribute _view override, important is, do calling post_view() once.
    """

    def __init__(self, **kwargs):
        self._view = kwargs.get('view')
        self._viewId = kwargs.get('view_id')
        self._viewTitle = kwargs.get('view_title')
        self._contentContainer = kwargs.get('content_container')
        self._userAttributes = kwargs.get('user_attributes', dict())
        if self._contentContainer is not None:
            self.post_content_container(self._contentContainer)
        self._undoStack = kwargs.get('undo_stack', wx.CommandProcessor(kwargs.get('max_undo_stack_depth', 10)))
        if self._view is not None:
            self.post_view(self._view)
        else:
            if not kwargs.get('ignore_warning', False):
                warnings.warn('view could not be initialized.')
        self.parent = kwargs.get('parent')
        _children = kwargs.get('children')
        if _children:
            self.children = _children
        # bind event
        # self._undoStack.canUndoChanged.connect(self.on_can_undo_changed)
        # self._undoStack.canRedoChanged.connect(self.on_can_redo_changed)

    def post_view(self, view: ZView):
        if self._view is not None:
            raise 'invalid post process, Instance already associated.'
        assert view is not None and isinstance(view, ZView), 'Type ZView is required, actual %s' % type(view)
        if self._view is None:
            self._view = view
        self._view.manager = self
        self._view.title = self._viewTitle

    def post_content_container(self, cc: ZViewContentContainer):
        if self._contentContainer is not None:
            raise 'invalid post process, Instance already associated.'
        assert cc is not None and isinstance(cc, ZViewContentContainer), 'Type ContentContainer is required'
        if self._contentContainer is None:
            self._contentContainer = cc
        self._contentContainer.manager = self

    def create_view(self, **kwargs) -> ZView:
        return self._view

    def create_content_container(self, **kwargs):
        return self._contentContainer

    @property
    def view(self) -> ZView:
        return self._view

    @property
    def viewTitle(self) -> str:
        return self._viewTitle if self._viewTitle is not None else self._view.title

    @viewTitle.setter
    def viewTitle(self, title):
        self._viewTitle = title
        self._view.title = title

    @property
    def contentContainer(self) -> ZViewContentContainer:
        return self._contentContainer

    @property
    def contentChanged(self):
        return self._contentContainer.hasChanged

    @property
    def undoStack(self) -> wx.CommandProcessor:
        return self._undoStack

    @property
    def appInstance(self):
        return wx.App.GetInstance()

    def set_view(self, view):
        self._view = view
        setattr(self._view, 'zViewManager', self)

    def on_can_undo_changed(self, state):
        pass

    def on_can_redo_changed(self, state):
        pass

    def set_state(self, *args, **kwargs):
        """
        method for update the state of view, like disable, enabled ...
        Args:
            *args:
            **kwargs:

        Returns:

        """
        pass

    def set_content(self, content: [Serializable, any]):
        if content is None:
            self.contentContainer.reset_to_default()
            return
        self.contentContainer.set(content=content)
        self._undoStack.ClearCommands()

    def restore_content(self):
        pass

    def save_content(self):
        # do something save actions
        self._undoStack.MarkAsSaved()

    def ensure_view(self):
        """
        method for ensure the view content in right position, like scrollbar,
        selected rows in list in viewport and so on.
        Returns:

        """
        pass

    def update(self):
        """
        method called by parent update or explicit
        Returns:

        """
        pass

    def idle(self):
        """
        method called by parent idle or explicit
        Returns:

        """
        pass

    @staticmethod
    def find(node, filter_=None, stop=None, maxlevel=None):
        return anytree.find(node, filter_, stop, maxlevel)

    @staticmethod
    def find_all(node, filter_=None, stop=None, maxlevel=None, mincount=None, maxcount=None):
        return anytree.findall(node, filter_, stop, maxlevel, mincount, maxcount)

    @staticmethod
    def find_by_attr(node, value, name="name", maxlevel=None):
        return anytree.find_by_attr(node, value, name, maxlevel)

    @staticmethod
    def findall_by_attr(node, value, name="name", maxlevel=None, mincount=None, maxcount=None):
        return anytree.findall_by_attr(node, value, name, maxlevel, mincount, maxcount)

    def add_user_attribute(self, key: str, value):
        self._userAttributes.update({key: value})

    def get_user_attribute(self, key, fallback=None):
        _val = self._userAttributes.get(key)
        return fallback if _val is None else _val
