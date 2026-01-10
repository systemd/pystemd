"""E2E tests for pystemd Manager functionality"""

from pystemd.systemd1 import Manager


def test_manager_version():
    """Test getting systemd version"""
    with Manager() as manager:
        version = manager.Manager.Version
        assert version is not None
        assert isinstance(version, bytes)


def test_manager_architecture():
    """Test getting system architecture"""
    with Manager() as manager:
        arch = manager.Manager.Architecture
        assert arch is not None
        assert isinstance(arch, bytes)


def test_list_units():
    """Test listing units"""
    with Manager() as manager:
        units = manager.Manager.ListUnits()
        assert len(units) > 0
        # Each unit should be a tuple with multiple fields
        assert isinstance(units[0], tuple)


def test_list_unit_files():
    """Test listing unit files"""
    with Manager() as manager:
        unit_files = manager.Manager.ListUnitFiles()
        assert len(unit_files) > 0
        # Each should be (name, state) tuple
        for name, state in unit_files:
            assert isinstance(name, bytes)
            assert isinstance(state, bytes)


def test_get_unit():
    """Test getting a unit by name"""
    with Manager() as manager:
        # Get a unit that should always exist
        unit_path = manager.Manager.GetUnit(b"dbus.service")
        assert unit_path is not None
        assert isinstance(unit_path, bytes)
