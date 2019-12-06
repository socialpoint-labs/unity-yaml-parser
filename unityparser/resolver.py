import re

from yaml.resolver import BaseResolver


class Resolver(BaseResolver):
    """
    UNITY: Resolver will convert EVERYTHING to str but for empty values which are translated to None.
    This is the safest approach as Unity doesn't follow YAML value conventions.
    """
    pass


# Resolver.add_implicit_resolver(
#     'tag:yaml.org,2002:bool',
#     re.compile(r'''^(?:yes|Yes|YES|no|No|NO
#                     |true|True|TRUE|false|False|FALSE
#                     |on|On|ON|off|Off|OFF)$''', re.X),
#     list('yYnNtTfFoO'))

Resolver.add_implicit_resolver(
    'tag:yaml.org,2002:float',
    re.compile(r'''^(?:[-+]?(?:0|[1-9][0-9]*)\.(?:[1-9]|[0-9][0-9]*[1-9])?)$''', re.X),
    list('-+0123456789.'))

Resolver.add_implicit_resolver(
    'tag:yaml.org,2002:int',
    # UNITY: Restrict to simple integer values
    re.compile(r'''^(?:[-+]?(?:0|[1-9][0-9]*))$''', re.X),
    list('-+0123456789'))

# Resolver.add_implicit_resolver(
#     'tag:yaml.org,2002:merge',
#     re.compile(r'^(?:<<)$'),
#     ['<'])

Resolver.add_implicit_resolver(
    'tag:yaml.org,2002:null',
    # UNITY: Allow only empty values as null
    re.compile(r'''^(?: )$''', re.X),
    [''])

# Resolver.add_implicit_resolver(
#     'tag:yaml.org,2002:timestamp',
#     re.compile(r'''^(?:[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]
#                     |[0-9][0-9][0-9][0-9] -[0-9][0-9]? -[0-9][0-9]?
#                      (?:[Tt]|[ \t]+)[0-9][0-9]?
#                      :[0-9][0-9] :[0-9][0-9] (?:\.[0-9]*)?
#                      (?:[ \t]*(?:Z|[-+][0-9][0-9]?(?::[0-9][0-9])?))?)$''', re.X),
#     list('0123456789'))

# Resolver.add_implicit_resolver(
#     'tag:yaml.org,2002:value',
#     re.compile(r'^(?:=)$'),
#     ['='])

# The following resolver is only for documentation purposes. It cannot work
# because plain scalars cannot start with '!', '&', or '*'.
Resolver.add_implicit_resolver(
    'tag:yaml.org,2002:yaml',
    re.compile(r'^(?:!|&|\*)$'),
    list('!&*'))
