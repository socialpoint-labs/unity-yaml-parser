from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def fixtures():
    """
    :return: Avaliable fixtures. Key is the name of the file, value the path to it.
    :rtype: Dict[str,str]
    """
    fixtures_folder = Path(__file__).parent / Path('fixtures')
    fixtures_dict = dict(map(lambda x: (x.name, str(x.resolve())), fixtures_folder.rglob('*')))
    return fixtures_dict
