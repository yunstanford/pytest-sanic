import pytest
from sanic.app import Sanic
from sanic.websocket import WebSocketProtocol
from sanic import response
from aiohttp.web import Application


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


async def test_fixture_test_client_close(test_cli):
    resp = await test_cli.get('/test_get')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {"GET": True}
    await test_cli.close()
    assert test_cli._closed == True


async def test_fixture_test_client_context_manager(app, test_client):
    async with await test_client(app) as test_cli:
        resp = await test_cli.get('/test_get')
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == {"GET": True}


async def test_fixture_test_client_raise_exception_for_non_sanic_app(test_client):
    aiohttp_web = Application()
    with pytest.raises(TypeError):
        await test_client(aiohttp_web)
