"""Conftest is used to configure pytest fixtures.

Consult the pytest documentation for more details on fixtures and test setup/teardown.
"""

import pytest


@pytest.fixture
def hello_fixture(monkeypatch):
    """An example fixture: see the usage in test_getting_started.py"""
    # set an environment variable HELLO_FIXTURE
    env_var = "HELLO_FIXTURE"
    monkeypatch.setenv(env_var, "Why hello there.")
