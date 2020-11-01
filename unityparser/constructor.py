import collections.abc
from .constants import OrderedFlowDict

from yaml.constructor import Constructor as YamlConstructor, ConstructorError
from yaml.nodes import MappingNode


class uniqstr(str):
    def __new__(cls, content):
        return super().__new__(cls, content)


class Constructor(YamlConstructor):

    def __init__(self, register=None):
        super(Constructor, self).__init__()
        self.register = register

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, MappingNode):
            raise ConstructorError(None, None,
                                   "expected a mapping node, but found %s" % node.id,
                                   node.start_mark)
        # UNITY: dict has to be ordered to reproduce nested maps, also save flow style
        mapping = OrderedFlowDict()
        mapping.set_flow_style(node.flow_style)
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, collections.abc.Hashable):
                raise ConstructorError("while constructing a mapping", node.start_mark,
                                       "found unhashable key", key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping

    def construct_scalar(self, node):
        value = super().construct_scalar(node)
        if isinstance(value, str) and node.style is not None:
            value = uniqstr(value)
            self.register.set(value, node.style)
        return value
