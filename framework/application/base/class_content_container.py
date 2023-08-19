# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_content_container.py
# ------------------------------------------------------------------------------
#
# File          : class_content_container.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from .base import IContentContainer, Serializable


class ZViewContentContainer(IContentContainer):

    def __init__(self, **kwargs):
        IContentContainer.__init__(self)
        self.manager = kwargs.get('manager')
        self._content = kwargs.get('content')
        self._streamer = kwargs.get('streamer')
        self._prevContent = None
        self._errorStack = list()
        self.defaultContent = None

    @property
    def content(self):
        return self._content

    @property
    def uid(self):
        return self.manager.uid if self.manager is not None else None

    def set_init_content_to_stream(self, obj: object = None):
        if obj is None:
            obj = self._content
        if obj is None or not isinstance(obj, Serializable):
            return
        self._prevContent = self._streamer.stream_dump(obj.serializer)

    def reset_to_default(self,*args,**kwargs):
        self._content = self.defaultContent
        self.set_init_content_to_stream(self._content)

    def set(self, *args, **kwargs):
        _content = kwargs.get('content')
        if _content is not None:
            self._content = _content
            self.set_init_content_to_stream(_content)

    def get(self, *args, **kwargs):
        return self._content

    def push_error(self, error):
        self._errorStack.insert(0, error)

    def pop_error(self, all_=False):
        if self._errorStack:
            if not all_:
                return self._errorStack.pop(0)
            else:
                _d = [x for x in self._errorStack]
                self.clear_error_stack()
                return _d

    def clear_error_stack(self):
        self._errorStack.clear()

    def transform_data(self, transformer: any):
        """
        for the version compatible sometimes the data should transformed.
        Args:
            transformer:

        Returns:

        """
        # todo: transformer should be type of IContentTransformer
        raise NotImplementedError

    def check_content_changed(self, *args, **kwargs):
        if self._streamer is None:
            return False
        return self._prevContent != self._streamer.stream_dump(self._content.serializer)

    def has_changed(self):
        if self._content is None:
            return False
        return self.check_content_changed()

    def change_apply(self, *args, **kwargs):
        pass
