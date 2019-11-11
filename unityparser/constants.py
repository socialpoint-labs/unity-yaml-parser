from collections import OrderedDict
from copy import copy
from multiprocessing import RLock

lock = RLock()


class UnityClassIdMap:
    # Hold 'id-classname':UnityClass values
    # UnityClass cannot be uniquely identified by id(https://docs.unity3d.com/Manual/ClassIDReference.html)
    # because multiple serialized files in a project can belong to multiple Unity versions and some of them,
    # specially very old versions < 5.X, have different names for the same id(ie. id:1001 Prefab vs PrefabInstance)
    __class_id_map = {}

    @classmethod
    def reset(self):
        with lock:
            UnityClassIdMap.__class_id_map.clear()

    @classmethod
    def get_or_create_class_id(cls, classid, classname):
        with lock:
            k = "{}-{}".format(classid, classname)
            try:
                unity_cls = UnityClassIdMap.__class_id_map[k]
            except KeyError:
                unity_cls = type(classname, (UnityClass,), {'__class_id': classid, '__class_name': classname})
                UnityClassIdMap.__class_id_map[k] = unity_cls
            return unity_cls


class UnityClass:
    __class_id = ''
    __class_name = ''

    def __init__(self, anchor, extra_anchor_data):
        self.anchor = anchor
        self.extra_anchor_data = extra_anchor_data

    def get_attrs(self):
        # get attribute set except those belonging to the Python class
        return set(self.__dict__.keys() - ['anchor', 'extra_anchor_data'])

    def update_dict(self, d):
        # replace and append current object attributes to self dict
        old_d = self.__dict__
        self.__dict__ = d
        self.__dict__.update(old_d)

    def get_serialized_properties_dict(self):
        # return a copy of the objects attributes but the ones we don't want
        d = copy(self.__dict__)
        del d['anchor']
        del d['extra_anchor_data']
        return d


class OrderedFlowDict(OrderedDict):
    """
    OrderdDict that tracks yaml flow_style from the MappingNode which created it
    """

    def set_flow_style(self, flow_style):
        self.flow_style = flow_style

    def get_flow_style(self):
        return getattr(self, 'flow_style', None)


UNITY_TAG_URI = u'tag:unity3d.com,2011:'
