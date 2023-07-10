import typing
from framework.application.base.base import singleton
from .uri_app import AppURI, URLObject


class URIHandleRegisterError(Exception):
    pass


class URIHandleUrlError(Exception):
    pass


class URIHandleExecutionError(Exception):
    pass


class URIHandle(AppURI):
    def __init__(self, uri_scheme: str, uri_path: str, app_ctx=None):
        AppURI.__init__(self, uri_path, uri_scheme)
        assert uri_scheme is not None and uri_path is not None, URIHandleUrlError('invalid uri string')
        self.appCtx = app_ctx

    @property
    def uri_str(self):
        return self._uri

    def is_handleable(self, uri: typing.Union[str, URLObject]) -> bool:
        if isinstance(uri, str):
            uri = URLObject(uri)
        return uri.scheme == self.uri.scheme and uri.path == self.uri.path

    def exec(self, *args, **kwargs):
        pass

    def before_exec(self, *args, **kwargs):
        pass

    def after_exec(self, *args, **kwargs):
        pass


@singleton
class URIHandleManager:
    def __init__(self):
        self._handles = dict()

    def register(self, handle: URIHandle) -> None:
        assert handle.uri_str not in self._handles, URIHandleRegisterError('already exist')
        self._handles.update({handle.uri_str: handle})

    def unregister(self, uri_str: str) -> None:
        if uri_str in self._handles:
            self._handles.pop(uri_str)

    def exec(self, uri: str, *args, **kwargs) -> None:
        _handle = self._handles.get(uri)
        if _handle is None:
            # try search through to find a handle could handle this uri
            for k, v in self._handles.items():
                if v.is_handleable(uri):
                    _handle = v
                    break
        if _handle is None:
            # if still no handle found, then give an error shot.
            raise URIHandleExecutionError('no handle for uri: %s registered.' % uri)
        _kws = dict(kwargs, **_handle.query2dict(uri))
        _handle.exec(*args, **_kws)
