import os
from pubsub import pub
from .uri_handle_manager import URIHandle


class PubsubUriHandleExecException(Exception): pass


class PubsubURIHandle(URIHandle):
    def __init__(self, uri_scheme='pubsub', uri_path='sendMessage'):
        super().__init__(uri_scheme, uri_path)

    def before_exec(self, *args):
        pass

    def after_exec(self, exit_code, exit_state):
        pass

    def exec(self, *args, **kwargs):
        try:
            pub.sendMessage(kwargs.get('msg'))
        except Exception as e:
            raise PubsubUriHandleExecException(e)
        finally:
            pass
