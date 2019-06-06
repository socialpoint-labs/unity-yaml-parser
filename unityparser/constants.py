from collections import OrderedDict
from copy import copy
from multiprocessing import RLock

lock = RLock()


class UnityClassIdMap:
    __class_id_map = {}

    @classmethod
    def get_or_create_class_id(cls, classid, classname):
        lock.acquire()
        unity_cls = UnityClassIdMap.__class_id_map.setdefault(classid,
                                                              type(classname, (UnityClass,),
                                                                   {'__class_id': classid}))
        lock.release()
        return unity_cls


class UnityClass:
    __class_id = ''

    def __init__(self, anchor):
        self.anchor = anchor

    def update_dict(self, d):
        # replace and append current object attributes to self dict
        old_d = self.__dict__
        self.__dict__ = d
        self.__dict__.update(old_d)

    def get_serialized_properties_dict(self):
        # return a copy of the objects attributes but the ones we don't want
        d = copy(self.__dict__)
        del d['anchor']
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
