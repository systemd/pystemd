import pickle

from pystemd.systemd1.unit import Unit


def test_unloaded_unit():
    unit = Unit("foo.service")
    sour_unit = pickle.loads(pickle.dumps(unit))
    assert unit.external_id == sour_unit.external_id
    assert not sour_unit._loaded


def test_loaded_unit():
    unit = Unit("foo.service")
    unit.load()
    sour_unit = pickle.loads(pickle.dumps(unit))
    assert unit.external_id == sour_unit.external_id
    assert sour_unit._loaded
    assert sour_unit._interfaces
