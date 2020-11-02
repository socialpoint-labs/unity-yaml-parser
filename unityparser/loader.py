from yaml.reader import Reader

from .scanner import Scanner
from .composer import Composer
from .constants import UNITY_TAG_URI, OrderedFlowDict, UnityClassIdMap
from .constructor import Constructor
from .parser import Parser
from .resolver import Resolver


class UpgradeVersionError(Exception):
    def __init__(self, *args, should_upgrade=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.should_upgrade = should_upgrade

    def __str__(self):
        msg = super().__str__()
        if self.should_upgrade:
            msg = msg.strip()
            msg += '. ' if msg[-1] != '.' else ' '
            msg += 'This might be an unsupported new Unity version, consider updating this module.'
        return msg


class LoaderVersionError(UpgradeVersionError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, should_upgrade=True, **kwargs)


class UnityLoader(Reader, Scanner, Parser, Composer, Constructor, Resolver):

    def __init__(self, stream, register=None):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        Constructor.__init__(self, register)
        Resolver.__init__(self)


def construct_unity_class(loader, tag_suffix, node):
    try:
        classid = tag_suffix
        classname = node.value[0][0].value
    except (ValueError, KeyError):
        raise LoaderVersionError('Unknown class id {}.'.format(tag_suffix))
    class_attributes_node = node.value[0][1]
    # use ordered dict
    loader.flatten_mapping(class_attributes_node)

    cls = UnityClassIdMap.get_or_create_class_id(classid, classname)
    anchor = loader.get_anchor_from_node(node)
    extra_anchor_data = loader.get_extra_anchor_data_from_node(anchor)
    value = cls(anchor, extra_anchor_data)
    value.update_dict(loader.construct_mapping(class_attributes_node, deep=True))
    return value


def construct_yaml_map(loader, node):
    data = OrderedFlowDict()
    data.set_flow_style(node.flow_style)
    yield data
    value = loader.construct_mapping(node)
    data.update(value)


UnityLoader.add_constructor('tag:yaml.org,2002:map', construct_yaml_map)
UnityLoader.add_multi_constructor(UNITY_TAG_URI, construct_unity_class)
