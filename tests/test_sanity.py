import openseespy as opy


def test_basic():
    opy.wipe()
    assert 1 == 1
