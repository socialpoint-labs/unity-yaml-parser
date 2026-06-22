from yaml.scanner import Scanner as YamlScanner, ScannerError
from yaml.tokens import AnchorToken


class Scanner(YamlScanner):

    def __init__(self):
        super().__init__()

        # keep track of previous tokens
        self.prev_tokens = []

    def scan_flow_scalar_spaces(self, double, start_mark):
        # UNITY: keep significant whitespace before a fold (standard YAML drops it, losing content)
        chunks = []
        length = 0
        while self.peek(length) in ' \t':
            length += 1
        whitespaces = self.prefix(length)
        self.forward(length)
        ch = self.peek()
        if ch == '\0':
            raise ScannerError("while scanning a quoted scalar", start_mark,
                               "found unexpected end of stream", self.get_mark())
        elif ch in '\r\n\x85  ':
            chunks.append(whitespaces)            # UNITY: keep, do not drop
            line_break = self.scan_line_break()
            breaks = self.scan_flow_scalar_breaks(double, start_mark)
            if line_break != '\n':
                chunks.append(line_break)
            elif not breaks:
                chunks.append(' ')
            chunks.extend(breaks)
        else:
            chunks.append(whitespaces)
        return chunks

    def check_prev_token(self, *choices):
        # Check if the previous token is one of the given types.
        if self.prev_tokens:
            if not choices:
                return True
            for choice in choices:
                if isinstance(self.prev_tokens[-1], choice):
                    return True
        return False

    def get_token(self):
        # Return the next token.
        while self.need_more_tokens():
            self.fetch_more_tokens()
        if self.tokens:
            self.tokens_taken += 1
            # UNITY: keep track of previous tokens
            self.prev_tokens.append(self.tokens.pop(0))
            return self.prev_tokens[-1]

    def fetch_anchor(self):

        # ANCHOR could start a simple key.
        self.save_possible_simple_key()

        # No simple keys after ANCHOR.
        self.allow_simple_key = False

        # Scan and add ANCHOR.
        self.tokens.append(self.scan_anchor(AnchorToken))
        
        # UNITY: look for tokens after the anchor
        self.fetch_extra_anchor_data()
        
    def fetch_extra_anchor_data(self):
        # see if we are at end of line, and it so, move
        # onto parsing the rest of the file.  Otherwise
        # we need to store the extra data on the anchor line
        if self.peek() in '\r\n\x85\u2028\u2029':
            return

        # parse the extra data after the anchor
        extra_anchor_data = ''
        while self.peek() not in '\r\n\x85\u2028\u2029':
            ch = self.peek()
            self.forward()
            extra_anchor_data += ch

        # and now store it for later serialization
        self.extra_anchor_data[self.tokens[-1].value] = extra_anchor_data
        return
