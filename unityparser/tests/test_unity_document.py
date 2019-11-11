import py
import pytest

from unityparser.utils import UnityDocument, UnityDocumentError


class TestUnityDocumentSerialization:

    def test_single_doc_unchanged(self, fixtures, tmpdir):
        base_file_path = py.path.local(fixtures['SingleDoc.asset'])
        doc = UnityDocument.load_yaml(str(base_file_path))
        dumped_file_path = tmpdir.join('SingleDoc.asset')
        doc.dump_yaml(file_path=str(dumped_file_path))

        assert base_file_path.read() == dumped_file_path.read()

    def test_multi_doc_unchanged(self, fixtures, tmpdir):
        base_file_path = py.path.local(fixtures['MultiDoc.asset'])
        doc = UnityDocument.load_yaml(str(base_file_path))
        dumped_file_path = tmpdir.join('MultiDoc.asset')
        doc.dump_yaml(file_path=str(dumped_file_path))

        assert base_file_path.read() == dumped_file_path.read()

    def test_unity_extra_anchor_data(self, fixtures, tmpdir):
        base_file_path = py.path.local(fixtures['UnityExtraAnchorData.prefab'])
        doc = UnityDocument.load_yaml(str(base_file_path))
        dumped_file_path = tmpdir.join('UnityExtraAnchorData.prefab')
        doc.dump_yaml(file_path=str(dumped_file_path))

        assert base_file_path.read() == dumped_file_path.read()


class TestUnityDocumentFilters:

    @pytest.mark.parametrize('class_names, attributes, num_entries', [
        (('Transform', 'MonoBehaviour'), ('m_EditorHideFlags',), 1),
        (('SpriteRenderer',), tuple(), 1),
        (('NonExistingClass',), tuple(), 0),
        (('MonoBehaviour',), ('m_NonExitingAttr',), 0),
        (tuple(), tuple(), 5),
        (tuple(), ('m_Enabled',), 2)
    ])
    def test_filter_entries(self, fixtures, class_names, attributes, num_entries):
        multidoc_path = py.path.local(fixtures['MultiDoc.asset'])
        doc = UnityDocument.load_yaml(str(multidoc_path))
        entries = doc.filter(class_names=class_names, attributes=attributes)
        assert len(entries) == num_entries
        if len(class_names):
            assert set([x.__class__.__name__ for x in entries]) <= set(class_names)
        if len(attributes):
            assert all(map(lambda x: all(map(lambda attr: hasattr(x, attr), attributes)), entries))

    @pytest.mark.parametrize('class_name, attributes', [
        ('MonoBehaviour', ('m_EditorHideFlags',)),
        ('SpriteRenderer', tuple()),
        pytest.param('NonExistingClass', tuple(), marks=pytest.mark.xfail(raises=UnityDocumentError)),
        pytest.param('MonoBehaviour', ('m_NonExitingAttr',), marks=pytest.mark.xfail(raises=UnityDocumentError)),
        pytest.param(None, tuple(), marks=pytest.mark.xfail(raises=UnityDocumentError)),
        pytest.param(None, ('m_Enabled',), marks=pytest.mark.xfail(raises=UnityDocumentError))
    ])
    def test_get_entry(self, fixtures, class_name, attributes):
        multidoc_path = py.path.local(fixtures['MultiDoc.asset'])
        doc = UnityDocument.load_yaml(str(multidoc_path))
        entry = doc.get(class_name=class_name, attributes=attributes)
        if class_name is not None:
            assert entry.__class__.__name__ == class_name
        if len(attributes):
            assert all(map(lambda attr: hasattr(entry, attr), attributes))
