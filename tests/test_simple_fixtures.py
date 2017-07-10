import os
import pytest


def test_fixture_unused_port(unused_port):
    assert unused_port > 1024 and unused_port < 65535


def test_fixture_tmpdir(tmpdir):
    assert os.path.isdir(tmpdir) is True


class MyEventLoop:

    def close(self):
        pass


@pytest.yield_fixture
def loop():
    loop = MyEventLoop()
    yield loop
    loop.close()


def test_loop_override(loop):
    assert isinstance(loop, MyEventLoop) is True
