from yaml.events import StreamEndEvent, DocumentStartEvent, MappingEndEvent
from yaml.parser import Parser as YamlParser, ParserError
from yaml.tokens import DocumentEndToken, StreamEndToken, DocumentStartToken, StreamStartToken, KeyToken, ValueToken, BlockEndToken


class Parser(YamlParser):

    def __init__(self):
        super(Parser, self).__init__()
        self.parsing_inverted_scalar = False
        self.non_default_tags = None

    def parse_document_start(self):

        # Parse any extra document end indicators.
        while self.check_token(DocumentEndToken):
            self.get_token()

        # Parse an explicit document.
        if not self.check_token(StreamEndToken):
            token = self.peek_token()
            start_mark = token.start_mark
            # UNITY: only process directives(version and tags) on the first document
            if self.check_prev_token(StreamStartToken):
                version, tags = self.process_directives()
                # UNITY: keep track of tags explicitly defined in the document
                if self.non_default_tags is None:
                    self.non_default_tags = tags
            else:
                version, tags = self.yaml_version, self.tag_handles.copy() if self.tag_handles else None
            if not self.check_token(DocumentStartToken):
                raise ParserError(None, None,
                                  "expected '<document start>', but found %r"
                                  % self.peek_token().id,
                                  self.peek_token().start_mark)
            token = self.get_token()
            end_mark = token.end_mark
            event = DocumentStartEvent(start_mark, end_mark,
                                       explicit=True, version=version, tags=tags)
            self.states.append(self.parse_document_end)
            self.state = self.parse_document_content
        else:
            # Parse the end of the stream.
            token = self.get_token()
            event = StreamEndEvent(token.start_mark, token.end_mark)
            assert not self.states
            assert not self.marks
            self.state = None
        return event

    def parse_block_mapping_key(self):
        if self.check_token(KeyToken):
            token = self.get_token()
            if not self.check_token(KeyToken, ValueToken, BlockEndToken):
                self.states.append(self.parse_block_mapping_value)
                return self.parse_block_node_or_indentless_sequence()
            else:
                self.state = self.parse_block_mapping_value
                return self.process_empty_scalar(token.end_mark)
        # UNITY: https://github.com/socialpoint-labs/unity-yaml-parser/issues/32
        if not self.check_token(BlockEndToken) and not self.parsing_inverted_scalar:
            if self.check_token(ValueToken):
                self.get_token()
                self.parsing_inverted_scalar = True
                self.states.append(self.parse_block_mapping_value)
                return self.parse_block_node_or_indentless_sequence()
            else:
                token = self.peek_token()
                raise ParserError("while parsing a block mapping", self.marks[-1],
                        "expected <block end>, but found %r" % token.id, token.start_mark)
        token = self.get_token()
        event = MappingEndEvent(token.start_mark, token.end_mark)
        self.state = self.states.pop()
        self.marks.pop()
        self.parsing_inverted_scalar = False
        return event
