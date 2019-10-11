from yaml.emitter import (
    Emitter as YamlEmitter,
    EmitterError)
from yaml.events import (
    DocumentStartEvent,
    StreamEndEvent,
    AliasEvent,
    ScalarEvent,
    CollectionStartEvent,
    SequenceStartEvent,
    MappingStartEvent)


class Emitter(YamlEmitter):

    def expect_document_start(self, first=False):
        if isinstance(self.event, DocumentStartEvent):
            # UNITY: omit document end separator
            # if (self.event.version or self.event.tags) and self.open_ended:
            #     self.write_indicator('...', True)
            #     self.write_indent()
            # UNITY: version only written before first document start
            if self.event.version and first:
                version_text = self.prepare_version(self.event.version)
                self.write_version_directive(version_text)
            self.tag_prefixes = self.DEFAULT_TAG_PREFIXES.copy()
            if self.event.tags:
                handles = sorted(self.event.tags.keys())
                for handle in handles:
                    prefix = self.event.tags[handle]
                    self.tag_prefixes[prefix] = handle
                    # UNITY: tag only written before first document start
                    if first:
                        handle_text = self.prepare_tag_handle(handle)
                        prefix_text = self.prepare_tag_prefix(prefix)
                        self.write_tag_directive(handle_text, prefix_text)
            implicit = (first and not self.event.explicit and not self.canonical
                        and not self.event.version and not self.event.tags
                        and not self.check_empty_document())
            if not implicit:
                self.write_indent()
                self.write_indicator('---', True)
                if self.canonical:
                    self.write_indent()
            self.state = self.expect_document_root
        elif isinstance(self.event, StreamEndEvent):
            # UNITY: omit document end separator
            # if self.open_ended:
            #     self.write_indicator('...', True)
            #     self.write_indent()
            self.write_stream_end()
            self.state = self.expect_nothing
        else:
            raise EmitterError("expected DocumentStartEvent, but got %s"
                               % self.event)

    def expect_node(self, root=False, sequence=False, mapping=False,
                    simple_key=False):
        self.root_context = root
        self.sequence_context = sequence
        self.mapping_context = mapping
        self.simple_key_context = simple_key
        if isinstance(self.event, AliasEvent):
            self.expect_alias()
        elif isinstance(self.event, (ScalarEvent, CollectionStartEvent)):
            # UNITY: tag and anchor appearance order swithced
            self.process_tag()
            self.process_anchor('&')
            self.process_anchor_extra()
            if isinstance(self.event, ScalarEvent):
                self.expect_scalar()
            elif isinstance(self.event, SequenceStartEvent):
                if self.flow_level or self.canonical or self.event.flow_style \
                        or self.check_empty_sequence():
                    self.expect_flow_sequence()
                else:
                    self.expect_block_sequence()
            elif isinstance(self.event, MappingStartEvent):
                if self.flow_level or self.canonical or self.event.flow_style \
                        or self.check_empty_mapping():
                    self.expect_flow_mapping()
                else:
                    self.expect_block_mapping()
        else:
            raise EmitterError("expected NodeEvent, but got %s" % self.event)

    def write_plain(self, text, split=True):
        if self.root_context:
            self.open_ended = True
        # UNITY: empty values contain a whitespace before line break
        # if not text:
        #     return
        if not self.whitespace:
            data = ' '
            self.column += len(data)
            if self.encoding:
                data = data.encode(self.encoding)
            self.stream.write(data)
        self.whitespace = False
        self.indention = False
        spaces = False
        breaks = False
        start = end = 0
        while end <= len(text):
            ch = None
            if end < len(text):
                ch = text[end]
            if spaces:
                if ch != ' ':
                    if start+1 == end and self.column > self.best_width and split:
                        self.write_indent()
                        self.whitespace = False
                        self.indention = False
                    else:
                        data = text[start:end]
                        self.column += len(data)
                        if self.encoding:
                            data = data.encode(self.encoding)
                        self.stream.write(data)
                    start = end
            elif breaks:
                if ch not in '\n\x85\u2028\u2029':
                    if text[start] == '\n':
                        self.write_line_break()
                    for br in text[start:end]:
                        if br == '\n':
                            self.write_line_break()
                        else:
                            self.write_line_break(br)
                    self.write_indent()
                    self.whitespace = False
                    self.indention = False
                    start = end
            else:
                if ch is None or ch in ' \n\x85\u2028\u2029':
                    data = text[start:end]
                    self.column += len(data)
                    if self.encoding:
                        data = data.encode(self.encoding)
                    self.stream.write(data)
                    start = end
            if ch is not None:
                spaces = (ch == ' ')
                breaks = (ch in '\n\x85\u2028\u2029')
            end += 1

    def write_double_quoted(self, text, split=True):
        self.write_indicator('"', True)
        start = end = 0
        while end <= len(text):
            ch = None
            if end < len(text):
                ch = text[end]
            if ch is None or ch in '"\\\x85\u2028\u2029\uFEFF' \
                    or not ('\x20' <= ch <= '\x7E'
                        or (self.allow_unicode
                            and ('\xA0' <= ch <= '\uD7FF'
                                or '\uE000' <= ch <= '\uFFFD'))):
                if start < end:
                    data = text[start:end]
                    self.column += len(data)
                    if self.encoding:
                        data = data.encode(self.encoding)
                    self.stream.write(data)
                    start = end
                if ch is not None:
                    if ch in self.ESCAPE_REPLACEMENTS:
                        data = '\\'+self.ESCAPE_REPLACEMENTS[ch]
                    elif ch <= '\xFF':
                        data = '\\x%02X' % ord(ch)
                    elif ch <= '\uFFFF':
                        data = '\\u%04X' % ord(ch)
                    else:
                        data = '\\U%08X' % ord(ch)
                    self.column += len(data)
                    if self.encoding:
                        data = data.encode(self.encoding)
                    self.stream.write(data)
                    start = end+1
            if 0 < end < len(text)-1 and (ch == ' ' or start >= end)    \
                    and self.column+(end-start) > self.best_width and split:
                # UNITY: do not append \ at the end of each split line
                data = text[start:end]
                if start < end:
                    start = end
                self.column += len(data)
                if self.encoding:
                    data = data.encode(self.encoding)
                self.stream.write(data)
                self.write_indent()
                self.whitespace = False
                self.indention = False
                if text[start] == ' ':
                    # UNITY: skip leading whitespace on new line
                    self.column += 1
                    start += 1
            end += 1
        self.write_indicator('"', False)

    def process_anchor_extra(self):
        if self.event.anchor is None or self.event.anchor not in self.extra_anchor_data:
            return
        self.write_indicator(self.extra_anchor_data[self.event.anchor], False)
