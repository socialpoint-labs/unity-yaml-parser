from yaml.serializer import Serializer as YamlSerializer
from yaml.events import DocumentStartEvent, DocumentEndEvent

# override serialzier class to store data needed
# for extra data on anchor lines
class Serializer(YamlSerializer):

    def __init__(self, encoding=None,
            explicit_start=None, explicit_end=None, version=None, tags=None):
        super().__init__(encoding=encoding,
            explicit_start=explicit_start, explicit_end=explicit_end, version=version,
            tags=tags)
        self.extra_anchor_data = {}

    def serialize(self, node):
        if self.closed is None:
            raise SerializerError("serializer is not opened")
        elif self.closed:
            raise SerializerError("serializer is closed")
        self.emit(DocumentStartEvent(explicit=self.use_explicit_start,
            version=self.use_version, tags=self.use_tags))
        self.anchor_node(node)
        self.serialize_node(node, None, None)
        self.emit(DocumentEndEvent(explicit=self.use_explicit_end))
        self.serialized_nodes = {}
        self.anchors = {}
        self.extra_anchor_data = {}
        self.last_anchor_id = 0

