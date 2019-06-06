import collections.abc
from .constants import OrderedFlowDict

from yaml.constructor import Constructor as YamlConstructor, ConstructorError
from yaml.nodes import MappingNode


class Constructor(YamlConstructor):

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
