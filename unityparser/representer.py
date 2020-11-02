from yaml.representer import Representer as YamlRepresenter


class Representer(YamlRepresenter):

    def __init__(self, default_style=None, default_flow_style=False,
                 sort_keys=True, register=None):
        super(Representer, self).__init__(default_style=default_style,
                                          default_flow_style=default_flow_style,
                                          sort_keys=sort_keys)
        self.register = register
