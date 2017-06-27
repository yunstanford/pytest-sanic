import pytest
from sanic.app import Sanic
from sanic import response


def test_fixture_unused_port(unused_port):
	assert unused_port > 1024 and unused_port < 65535


@pytest.yield_fixture
def app():
	app = Sanic("test_sanic_app")

	@app.route("/test_get")
	async def test_get(request):
		return response.json({"GET": True})

	yield app


@pytest.fixture
def sanic_server(loop, app, test_server):
	return loop.run_until_complete(test_server(app))


@pytest.fixture
def test_cli(loop, app, test_client):
	return loop.run_until_complete(test_client(app))


async def test_fixture_test_server_get_properties(sanic_server):
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


async def test_fixture_test_client_get_properties(test_cli):
	assert test_cli.app is not None
	assert test_cli.host is not None
	assert test_cli.port is not None
	assert test_cli.server is not None
	assert test_cli.session is not None


async def test_fixture_test_client_make_url(test_cli):
	uri = '/test'
	url = test_cli.make_url(uri)
	assert url == "http://127.0.0.1:{port}/test".format(port=str(test_cli.port))


async def test_fixture_test_client_get(test_cli):
	resp = await test_cli.get('/test_get')
	assert resp.status == 200
	resp_json = await resp.json()
	assert resp_json == {"GET": True}
