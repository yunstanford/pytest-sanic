# This is a special test. it will fail for sanic <= 0.5.4
async def test_fixture_test_client_ws(test_cli):
    ws_conn = await test_cli.ws_connect('/test_ws')
    data = 'hello world!'
    await ws_conn.send_str(data)
    msg = await ws_conn.receive()
    assert msg.data == data
    await ws_conn.close()
