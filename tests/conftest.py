import sanic
import asyncio
import pytest
from sanic.app import Sanic
from sanic.websocket import WebSocketProtocol
from sanic import response


collect_ignore = []

if sanic.__version__ <= '0.6.0':
    collect_ignore.append("test_client_websocket.py")


# pytest_plugins = 'pytest_sanic.plugin'


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

    @app.websocket("/test_ws")
    async def test_ws(request, ws):
        data = await ws.recv()
        await ws.send(data)

    @app.listener('before_server_start')
    async def mock_init_db(app, loop):
        await asyncio.sleep(0.01)

    yield app


@pytest.fixture
def sanic_server(loop, app, test_server):
    return loop.run_until_complete(test_server(app))


@pytest.fixture
def test_cli(loop, app, test_client):
    return loop.run_until_complete(test_client(app, protocol=WebSocketProtocol))
