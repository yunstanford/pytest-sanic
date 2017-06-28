import pytest
from sanic.app import Sanic
from sanic.websocket import WebSocketProtocol
from sanic import response


def test_fixture_unused_port(unused_port):
    assert unused_port > 1024 and unused_port < 65535


@pytest.yield_fixture
def app():
    app = Sanic("test_sanic_app")

    @app.route("/test_get", methods=['GET'])
    async def test_get(request):
        return response.json({"GET": True})

    @app.route("/test_post", methods=['POST'])
    async def test_post(request):
        return response.json({"POST": True})

    @app.route("/test_put", methods=['PUT'])
    async def test_put(request):
        return response.json({"PUT": True})

    @app.route("/test_delete", methods=['DELETE'])
    async def test_delete(request):
        return response.json({"DELETE": True})

    @app.route("/test_patch", methods=['PATCH'])
    async def test_patch(request):
        return response.json({"PATCH": True})

    @app.route("/test_options", methods=['OPTIONS'])
    async def test_options(request):
        return response.json({"OPTIONS": True})

    @app.route("/test_head", methods=['HEAD'])
    async def test_head(request):
        return response.json({"HEAD": True})

    @app.websocket('/test_ws')
    async def test_ws(request, ws):
        data = await ws.recv()
        await ws.send(data)

    yield app


@pytest.fixture
def sanic_server(loop, app, test_server):
    return loop.run_until_complete(test_server(app))


@pytest.fixture
def test_cli(loop, app, test_client):
    return loop.run_until_complete(test_client(app, protocol=WebSocketProtocol))


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


async def test_fixture_test_client_post(test_cli):
    resp = await test_cli.post('/test_post')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {"POST": True}


async def test_fixture_test_client_put(test_cli):
    resp = await test_cli.put('/test_put')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {"PUT": True}


async def test_fixture_test_client_delete(test_cli):
    resp = await test_cli.delete('/test_delete')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {"DELETE": True}


async def test_fixture_test_client_patch(test_cli):
    resp = await test_cli.patch('/test_patch')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {"PATCH": True}


async def test_fixture_test_client_options(test_cli):
    resp = await test_cli.options('/test_options')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {"OPTIONS": True}


async def test_fixture_test_client_head(test_cli):
    resp = await test_cli.head('/test_head')
    assert resp.status == 200
    resp_json = await resp.json()
    # HEAD should not have body
    assert resp_json is None


# async def test_fixture_test_client_ws(test_cli):
#     ws_conn = await test_cli.ws_connect('/test_ws', protocols=(WebSocketProtocol,))
#     data = 'hello world!'
#     await ws_conn.send_str(data)
#     assert await ws_conn.receive() == data
