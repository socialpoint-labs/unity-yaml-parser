import py
import pytest

from unityparser.utils import UnityDocument


class TestInvertedScalarLoading:

    def test_inverted_scalar_loading_ok(self, fixtures, tmpdir):
        base_file_path = py.path.local(fixtures['InvertedScalar.dll.meta'])
        doc = UnityDocument.load_yaml(str(base_file_path))
        assert doc.entry['PluginImporter']['platformData'][0]['first']['Any'] is None

