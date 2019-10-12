from yaml.composer import Composer as YamlComposer, ComposerError


class Composer(YamlComposer):

    def compose_document(self):
        # Drop the DOCUMENT-START event.
        self.get_event()

        # UNITY: used to store data after the anchor
        self.extra_anchor_data = {}

        # Compose the root node.
        node = self.compose_node(None, None)

        # Drop the DOCUMENT-END event.
        self.get_event()

        # UNITY: prevent reset anchors after document end so we can access them on constructors
        # self.anchors = {}
        return node

    def get_anchor_from_node(self, node):
        for k, v in self.anchors.items():
            if node == v:
                return k
        raise ComposerError("Expected anchor to be present for node")

    def get_extra_anchor_data_from_node(self, anchor):
        if anchor in self.extra_anchor_data:
            return self.extra_anchor_data[anchor]
        return ''
