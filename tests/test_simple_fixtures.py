import os


def test_fixture_unused_port(unused_port):
    assert unused_port > 1024 and unused_port < 65535


def test_fixture_tmpdir(tmpdir):
    assert os.path.isdir(tmpdir) is True
