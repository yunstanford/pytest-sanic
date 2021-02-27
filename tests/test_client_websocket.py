# This is a special test. it will fail for sanic <= 0.5.4
async def test_fixture_sanic_client_ws(test_cli_ws):
    ws_conn = await test_cli_ws.ws_connect('/test_ws')
    data = 'hello world!'
    await ws_conn.send(data)
    msg = await ws_conn.recv()
    assert msg == data
    await ws_conn.close()
