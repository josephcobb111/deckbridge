from os.path import abspath, dirname, exists
from subprocess import PIPE, Popen

import pytest

import deckbridge

TOP_PATH = abspath(dirname(deckbridge.__file__))


def run_flake8(directory):
    """Run flake8 tests for a directory."""
    args = ["flake8", directory]
    if exists("setup.cfg"):
        args.append("--config={}".format(abspath("setup.cfg")))
    print(args)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()

    if proc.returncode != 0:
        raise AssertionError("Flake8 issues:\nCalled as : %s\n%s" % (" ".join(args), out.decode("utf-8")))


@pytest.mark.quality
def test_flake8():
    """Execute flake8 test."""
    print("Executing flake against: {}".format(TOP_PATH))
    run_flake8(TOP_PATH)
