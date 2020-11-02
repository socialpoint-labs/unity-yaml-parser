import py
import pytest

from unityparser.utils import UnityDocument, UnityDocumentError


class TestScalarValueTypes:

    def test_types(self, fixtures):
        base_file_path = py.path.local(fixtures['MultipleTypesDoc.asset'])
        doc = UnityDocument.load_yaml(str(base_file_path))
        multi_types = doc.entry

        count_map = {'int': 0, 'str': 0, 'float': 0}

        def evaluate_type(attr, parent_map):
            attr_value = parent_map[attr]
            split_attr = attr.split('_')
            if split_attr[0] == 'scalar':
                expected_type = split_attr[1]
                assert issubclass(type(attr_value), eval(expected_type))
                count_map[expected_type] += 1
            elif split_attr[0] == 'map':
                for k in attr_value:
                    evaluate_type(k, attr_value)

        multi_types_attr_map = multi_types.get_serialized_properties_dict()
        for attribute in multi_types_attr_map:
            evaluate_type(attribute, multi_types_attr_map)

        assert count_map['int'] == 4
        assert count_map['str'] == 8
        assert count_map['float'] == 6

    def test_sum_int_type(self, fixtures):
        base_file_path = py.path.local(fixtures['MultipleTypesDoc.asset'])
        doc = UnityDocument.load_yaml(str(base_file_path))
        multi_types = doc.entry

        multi_types.scalar_int_001 += 1
        assert multi_types.scalar_int_001 == 16
