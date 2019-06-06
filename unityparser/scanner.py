from yaml.scanner import Scanner as YamlScanner


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
