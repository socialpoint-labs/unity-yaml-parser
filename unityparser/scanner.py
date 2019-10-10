from yaml.scanner import Scanner as YamlScanner
from yaml.tokens import AnchorToken


class Scanner(YamlScanner):

    def __init__(self):
        super().__init__()

        # keep track of previous tokens
        self.prev_tokens = []

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
        super().fetch_anchor()

        # after fetching the anchor, we need to determine if we are at
        # end of line, or if there are further tokens past the anchor.
        # If at the end of line, we can continue as normal.  If there
        # are more tokens (like the word 'stripped') then we need
        # to grab that token and save it, then we can continue
        if self.peek() in '\r\n\x85\u2028\u2029':
            return

        # pop off the old token because we will replace it with a new
        # one that contains original anchor name along with extra
        # stuff on the anchor line that Unity puts there
        #token = self.tokens.pop()
        extra_anchor_data = ''
        while self.peek() not in '\r\n\x85\u2028\u2029':
            ch = self.peek()
            self.forward()
            extra_anchor_data += ch

        # this point we can construct this anchor with the anchor
        # name and all of the extra tokens after the anchor
        # new_token = AnchorToken(new_anchor_name, token.start_mark, self.get_mark())
        # self.tokens.append(new_token)
        self.extra_anchor_data[self.tokens[-1].value] = extra_anchor_data
        return
