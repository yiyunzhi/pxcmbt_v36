import os, yaml, itertools
from framework.application.base.base import YAMLObject
from .class_base import AppFileIO

NODE_CONTENT_LOADER = YAMLObject.loader
NODE_CONTENT_DUMPER = YAMLObject.dumper


class AppYamlFileIO(AppFileIO):

    def __init__(self, **kwargs):
        AppFileIO.__init__(self, **kwargs)

    def read(self, loader=NODE_CONTENT_LOADER):
        self.error = ''
        _full_path = self.get_full_path()
        if not self.is_file_exist():
            self.error = 'file %s not exist' % _full_path
            return False
        with open(_full_path) as f:
            _data = yaml.load(f, Loader=loader)
            if _data is None:
                self.error = 'data is empty'
                return False
            self.data = _data
            return True

    def write(self, data, dumper=NODE_CONTENT_DUMPER):
        _file_full_path = self.get_full_path()
        with open(_file_full_path, "w") as f:
            yaml.dump(data, f, Dumper=dumper)


class AppYamlStreamer:
    # todo: may inherit from interface IAppStream for the extending which use xml, json some techs.
    @staticmethod
    def stream_dump(obj, dumper=yaml.CDumper):
        return yaml.dump(obj, Dumper=dumper)

    @staticmethod
    def stream_load(obj, loader=yaml.CFullLoader):
        return yaml.load(obj, loader)
