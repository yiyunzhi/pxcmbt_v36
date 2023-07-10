from application import (iod_action_ext_entity,
                         ArgumentMeta,
                         IODBasedAction,
                         EnumIPODArgumentNamespace)

__category_name = 'DevSpecified'


@iod_action_ext_entity(__category_name)
class ActionFormatDiagStr(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionFormatDiagStr, self).__init__(**kwargs)
        self.base = ''
        self.location = 0
        self.result = ''

    @classmethod
    def get_description(cls):
        _desc = 'result=base.format(location).location require [0,1,2,3,...]'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='base', type=str, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='location', type=int, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='result', type=str, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.result = self.base % (self.location * 2, self.location)
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False
