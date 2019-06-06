import yaml

from .dumper import UnityDumper
from .loader import UnityLoader

UNIX_LINE_ENDINGS = '\n'


class UnityDocument:

    def __init__(self, data, newline=None, file_path=None):
        self.newline = newline
        self.data = data
        self.file_path = file_path

    @property
    def entry(self):
        # as many documents contain a single document entry, this might be handy
        return self.data[0]

    @property
    def entries(self):
        return self.data

    def dump_yaml(self, file_path=None):
        """
        :param file_path: If self.file_path is None, it must be passed
        :type file_path:
        :return:
        :rtype:
        """
        file_path = file_path or self.file_path
        assert file_path is not None, "file_path parameter must be passed"
        with open(file_path, 'w', newline=self.newline) as fp:
            yaml.dump_all(self.data, stream=fp, Dumper=UnityDumper)

    @classmethod
    def load_yaml(cls, file_path):
        with open(file_path, newline='') as fp:
            data = [d for d in yaml.load_all(fp, Loader=UnityLoader)]
            # use document line endings if no mixed lien endings found, else default to linux
            line_endings = UNIX_LINE_ENDINGS if isinstance(fp.newlines, tuple) else fp.newlines
        doc = UnityDocument(data, newline=line_endings, file_path=file_path)
        return doc
