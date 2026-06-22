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


# UNITY editor scalar wrap widths
PLAIN_WIDTH = 79
SINGLE_WIDTH = 80
DOUBLE_WIDTH = 79


class Emitter(YamlEmitter):

    def _write_built(self, data):
        # write a pre-folded chunk and resync state (column = chars after last LF)
        if not data:
            return
        nl = data.rfind('\n')
        if nl >= 0:
            self.line += data.count('\n')
            self.column = len(data) - nl - 1
        else:
            self.column += len(data)
        if self.encoding:
            data = data.encode(self.encoding)
        self.stream.write(data)
        self.whitespace = False
        self.indention = False

    def expect_document_start(self, first=False):
        # UNITY: serializeInlineMappingsOnOneLine -> never wrap flow collections (scalars fold on
        # their own widths, so best_width only affects flow here)
        if getattr(self, 'serialize_inline_mappings_on_one_line', False):
            self.best_width = 1 << 30
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

    def choose_scalar_style(self):
        # UNITY: emit empty (`{class: , }`) and `...`/`---` values plain, not quoted/tagged
        if self.event.style is None and self.event.implicit[0] and (
                self.event.value == '' or self.event.value in ('...', '---')):
            return ''
        return super().choose_scalar_style()

    def write_plain(self, text, split=True):
        # UNITY: break at a space iff column > width and it's the last space of its run; the break
        # consumes it, earlier spaces stay as significant trailing whitespace
        if self.root_context:
            self.open_ended = True
        out = []
        col = self.column
        if not self.whitespace:
            out.append(' ')
            col += 1
        if text:
            indent = ' ' * (self.indent or 0)
            n = len(text)
            for i, ch in enumerate(text):
                if (ch == ' ' and split and col > PLAIN_WIDTH
                        and not (i + 1 < n and text[i + 1] == ' ')):
                    out.append('\n' + indent)
                    col = len(indent)
                else:
                    out.append(ch)
                    col += 1
        self._write_built(''.join(out))

    def write_double_quoted(self, text, split=True):
        # UNITY: only fold when the content has an escaped char (pure-ASCII stays one line)
        self.write_indicator('"', True)
        ER = self.ESCAPE_REPLACEMENTS
        au = self.allow_unicode

        def needs_escape(ch):
            return (ch in '"\\\x85\u2028\u2029\uFEFF' or ch == '\t'
                    or not ('\x20' <= ch <= '\x7E'
                            or (au and ('\xA0' <= ch <= '\uD7FF'
                                        or '\uE000' <= ch <= '\uFFFD'))))

        allow_breaks = split and any(needs_escape(c) for c in text)
        indent = ' ' * (self.indent or 0)
        out = []
        col = self.column
        n = len(text)
        i = 0
        spaces = False
        while i < n:
            ch = text[i]
            if needs_escape(ch):
                if ch in ER:
                    e = '\\' + ER[ch]
                elif ch <= '\xFF':
                    e = '\\x%02X' % ord(ch)
                elif ch <= '\uFFFF':
                    e = '\\u%04X' % ord(ch)
                else:
                    e = '\\U%08X' % ord(ch)
                out.append(e)
                col += len(e)
                i += 1
                spaces = False
            elif ch == ' ':
                # UNITY: break at the last space of a run, keeping earlier ones as trailing
                last_of_run = not (i + 1 < n and text[i + 1] == ' ')
                if (allow_breaks and col > DOUBLE_WIDTH and i != 0 and i + 1 != n
                        and last_of_run):
                    out.append('\n' + indent)
                    col = len(indent)
                    i += 1                    # the break consumes this (last) space
                else:
                    out.append(' ')
                    col += 1
                    i += 1
                spaces = True
            else:
                out.append(ch)
                col += 1
                i += 1
                spaces = False
        self._write_built(''.join(out))
        self.write_indicator('"', False)

    def write_single_quoted(self, text, split=True):
        # UNITY: content newline -> blank line; column accumulates across newlines (first +cont+2,
        # each extra +1); a fold never splits a space run; trailing \n closes the quote alone at col 0
        self.write_indicator("'", True)
        if text == "":
            self.write_indicator("'", False)
            return
        esc = text.replace("'", "''")
        segments = esc.split("\n")
        cont = self.indent or 0
        ind = ' ' * cont
        width = SINGLE_WIDTH
        out = []
        vcol = self.column
        prev_empty = False
        for s, seg in enumerate(segments):
            if s > 0:
                out.append("")
                vcol += 1 if prev_empty else cont + 2
            if seg == "":
                if s == 0:
                    out.append("")
                prev_empty = s != 0
                continue
            prev_empty = False
            cur = "" if s == 0 else ind
            firstw = True
            for word in seg.split(" "):
                if firstw:
                    cur += word
                    vcol += len(word)
                    firstw = False
                elif word != "" and split and vcol + 1 > width:
                    out.append(cur)
                    cur = ind + word
                    vcol = cont + len(word)
                else:
                    cur += " " + word
                    vcol += 1 + len(word)
            out.append(cur)
        if segments[-1] == "":
            out.append("'")
        else:
            out[-1] += "'"
        self._write_built("\n".join(out))

    def process_anchor_extra(self):
        if self.event.anchor is None or self.event.anchor not in self.extra_anchor_data:
            return
        self.write_indicator(self.extra_anchor_data[self.event.anchor], False)
