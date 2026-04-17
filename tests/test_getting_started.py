"""Testing getting started!

This is a getting started file for reference.
"""

import os

from deckbridge.getting_started import hello_world


def test_hello_world():
    """Testing our greeting!"""
    greeting = hello_world()
    assert len(greeting) > 0


def test_hello_fixture(hello_fixture):
    """Testing the fixture!"""
    msg = os.getenv("HELLO_FIXTURE")
    assert len(msg) > 0
