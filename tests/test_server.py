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
