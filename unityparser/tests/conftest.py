from pathlib import Path

import pytest

from unityparser.constants import UnityClassIdMap


@pytest.fixture(scope='session')
def fixtures():
    """
    :return: Available fixtures. Key is the name of the file, value the path to it.
    :rtype: Dict[str,str]
    """
    fixtures_folder = Path(__file__).parent / Path('fixtures')
    fixtures_dict = dict(map(lambda x: (x.name, str(x.resolve())), fixtures_folder.rglob('*')))
    yield fixtures_dict


@pytest.fixture(scope='function', autouse=True)
def reset_unity_class_id_map():
    """
    Provide a clean cache map for every run
    :return:
    :rtype:
    """
    UnityClassIdMap.reset()
