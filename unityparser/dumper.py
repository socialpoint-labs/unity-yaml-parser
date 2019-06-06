from yaml.representer import Representer
from yaml.serializer import Serializer

from .constants import UNITY_TAG_URI, UnityClass, OrderedFlowDict
from .emitter import Emitter
from .resolver import Resolver

UNITY_TAG = {'!u!': UNITY_TAG_URI}
VERSION = (1, 1)


class UnityDumper(Emitter, Serializer, Representer, Resolver):

    def __init__(self, stream,
                 default_style=None, default_flow_style=False,
                 canonical=None, indent=None, width=None,
                 allow_unicode=None, line_break=None,
                 encoding=None, explicit_start=None, explicit_end=None,
                 version=None, tags=None, sort_keys=True):
        tags = tags or {}
        tags.update(UNITY_TAG)
        version = version or VERSION
        Emitter.__init__(self, stream, canonical=canonical,
                         indent=indent, width=width,
                         allow_unicode=allow_unicode, line_break=line_break)
        Serializer.__init__(self, encoding=encoding,
                            explicit_start=explicit_start, explicit_end=explicit_end,
                            version=version, tags=tags)
        Representer.__init__(self, default_style=default_style,
                             default_flow_style=default_flow_style, sort_keys=sort_keys)
        Resolver.__init__(self)


def represent_unity_class(dumper, instance):
    data = {instance.__class__.__name__: instance.get_serialized_properties_dict()}
    node = dumper.represent_mapping('{}{}'.format(UNITY_TAG_URI, instance.__class_id), data, False)
    # UNITY: set MappingNode anchor and all set all it's descendants anchors to None
    dumper.anchors[node] = instance.anchor
    for key, value in node.value:
        dumper.anchor_node(key)
        dumper.anchor_node(value)
    return node


def represent_ordered_flow_dict(dumper, instance):
    return dumper.represent_mapping(Resolver.DEFAULT_MAPPING_TAG, instance.items(),
                                    flow_style=instance.get_flow_style())


def represent_none(dumper, instance):
    return dumper.represent_scalar('tag:yaml.org,2002:null', '')


Representer.add_multi_representer(UnityClass, represent_unity_class)
Representer.add_representer(OrderedFlowDict, represent_ordered_flow_dict)
Representer.add_representer(type(None), represent_none)
