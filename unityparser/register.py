class UnityScalarRegister:
    def __init__(self):
        self.map = {}

    def pop(self, value):
        ptr_id = id(value)
        style = self.map.get(ptr_id, None)
        if style is not None:
            style = style[1]
            del self.map[ptr_id]
        return style

    def set(self, value, style):
        ptr_id = id(value)
        assert ptr_id not in self.map, "Duplicated ptr_id ({}) in UnityScalarRegister".format(ptr_id)
        self.map[ptr_id] = (value, style)
