from unityparser.utils import UnityDocument
import py
import pytest

class TestUnityDocument:

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

