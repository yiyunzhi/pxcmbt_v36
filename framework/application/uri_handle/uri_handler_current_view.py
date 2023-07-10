from .uri_handle_manager import URIHandle


class AppCurrentViewExecOperationUriHandleExecException(Exception): pass


class AppCurrentViewExecOperationURIHandle(URIHandle):
    def __init__(self, uri_scheme='appCurrentView', uri_path='execOperation'):
        super().__init__(uri_scheme, uri_path)

    def before_exec(self, *args):
        pass

    def after_exec(self):
        pass

    def exec(self, *args, **kwargs):
        try:
            _current_view = kwargs.get('currentView')
            if _current_view is None:
                return
            _vm = _current_view.zViewManager
            _sop_qs_mgr = _vm.sopQueryStringMgr
            _opg = kwargs.get('operationGroup')
            _op = kwargs.get('operation')
            _op_id='%s.%s' % (_opg, _op)
            if _op is None:
                return
            if not _sop_qs_mgr.is_op_supported(_op_id):
                return
            _vm.exec_operation(_op_id)

        except Exception as e:
            raise AppCurrentViewExecOperationUriHandleExecException(e)
        finally:
            pass
