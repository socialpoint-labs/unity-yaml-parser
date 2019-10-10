from yaml.events import StreamEndEvent, DocumentStartEvent
from yaml.parser import Parser as YamlParser, ParserError
from yaml.tokens import DocumentEndToken, StreamEndToken, DocumentStartToken, StreamStartToken


class Parser(YamlParser):

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
