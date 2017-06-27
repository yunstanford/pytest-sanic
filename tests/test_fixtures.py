import pytest
from sanic.app import Sanic


def test_fixture_unused_port(unused_port):
	assert unused_port > 1024 and unused_port < 65535


@pytest.yield_fixture
def app():
	app = Sanic("test_sanic_app")
	yield app 


@pytest.fixture
def sanic_server(loop, app, test_server):
	return loop.run_until_complete(test_server(app))


async def test_fixture_test_server_start_server(sanic_server):
	assert sanic_server.is_running is True
	assert sanic_server.port is not None
	url = sanic_server.make_url('/test')
	assert url == 'http://127.0.0.1:{port}/test'.format(port=str(sanic_server.port))


async def test_fixture_test_server_close(sanic_server):
	# close
	await sanic_server.close()
	assert sanic_server.is_running is False
	assert sanic_server.closed is True
	assert sanic_server.port is None
