"""Pytest configuration and shared fixtures for E2E tests"""

import pytest


@pytest.fixture
def requires_root():
    """Skip test if not running as root"""
    import os

    if os.geteuid() != 0:
        pytest.skip("Requires root privileges")
