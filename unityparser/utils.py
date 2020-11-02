import io

from .dumper import UnityDumper
from .errors import UnityDocumentError
from .loader import UnityLoader
from .register import UnityScalarRegister

UNIX_LINE_ENDINGS = '\n'


class UnityDocument:

    def __init__(self, data, newline=None, file_path=None, register=None):
        self.newline = newline
        self.data = data
        self.file_path = file_path
        self.register = register or UnityScalarRegister()

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
        assert_or_raise(file_path is not None, UnityDocumentError("file_path parameter must be passed"))
        with open(file_path, 'w', newline=self.newline) as fp:
            dump_all(self.data, stream=fp, register=self.register)

    @classmethod
    def load_yaml(cls, file_path):
        register = UnityScalarRegister()
        with open(file_path, newline='') as fp:
            data = [d for d in load_all(fp, register)]
            # use document line endings if no mixed lien endings found, else default to linux
            line_endings = UNIX_LINE_ENDINGS if isinstance(fp.newlines, tuple) else fp.newlines
        doc = UnityDocument(data, newline=line_endings, file_path=file_path, register=register)
        return doc

    # region Filtering

    def filter(self, class_names=None, attributes=None):
        """
        Filter a group of entries
        :param class_names: iterable of class names to filter
        :type class_names:
        :param attributes: iterable of attribute names that classes must have to be selected
        :type attributes:
        :return: list entries selected
        :rtype:
        """
        entries = self.entries
        if class_names:
            s_class_names = set(class_names)
            entries = filter(lambda x: x.__class__.__name__ in s_class_names, entries)
        if attributes:
            s_attributes = set(attributes)
            entries = filter(lambda x: s_attributes <= x.get_attrs(), entries)
        return list(entries)

    def get(self, class_name=None, attributes=None):
        """
        Filter a single entry. Only, and at least one must exist else it will except
        :param class_name: a class name to get
        :type class_name:
        :param attributes: iterable of attribute names that define the unique entry
        :type attributes:
        :return: a single entry
        :rtype:
        """
        if class_name:
            t_class_name = (class_name,)
        else:
            t_class_name = tuple()
        entries = self.filter(class_names=t_class_name, attributes=attributes)
        assert_or_raise(len(entries) > 0, UnityDocumentError("get method must return on entry. none found"))
        assert_or_raise(len(entries) == 1, UnityDocumentError("get method must return on entry. multiple found"))
        return entries[0]

    # endregion


def assert_or_raise(condition, exception):
    if not condition:
        raise exception


def load_all(stream, register=None):
    """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.
    """
    loader = UnityLoader(stream, register)
    try:
        while loader.check_data():
            yield loader.get_data()
    finally:
        loader.dispose()


def dump_all(documents, stream=None, default_style=None,
             default_flow_style=False,
             canonical=None, indent=None, width=None,
             allow_unicode=None, line_break=None,
             encoding=None, explicit_start=None, explicit_end=None,
             version=None, tags=None, sort_keys=True, register=None):
    """
    Serialize a sequence of Python objects into a YAML stream.
    If stream is None, return the produced string instead.
    """
    getvalue = None
    if stream is None:
        if encoding is None:
            stream = io.StringIO()
        else:
            stream = io.BytesIO()
        getvalue = stream.getvalue
    dumper = UnityDumper(stream, default_style=default_style,
                         default_flow_style=default_flow_style,
                         canonical=canonical, indent=indent, width=width,
                         allow_unicode=allow_unicode, line_break=line_break,
                         encoding=encoding, version=version, tags=tags,
                         explicit_start=explicit_start,
                         explicit_end=explicit_end,
                         sort_keys=sort_keys, register=register)
    try:
        dumper.open()
        for data in documents:
            dumper.represent(data)
        dumper.close()
    finally:
        dumper.dispose()
    if getvalue:
        return getvalue()
