import asyncio
import pytest
import inspect
import socket
from .utils import TestServer, TestClient
try:
    import uvloop
except:  # pragma: no cover
    uvloop = None


LOOP_INIT = None
LOOP_KEY = 'loop'

def pytest_addoption(parser):
    parser.addoption(
        '--loop', default=None,
        help='run tests with specific loop: aioloop, uvloop')


def pytest_configure(config):
    global LOOP_INIT
    loop_name = config.getoption('--loop')
    factory = {
        "aioloop": asyncio.new_event_loop,
    }
    if uvloop is not None:
        factory["uvloop"] = uvloop.new_event_loop

    if loop_name:
        if loop_name not in factory:
            raise ValueError(
                "{name} is not valid option".format(name=loop_name)
            )
        LOOP_INIT = factory[loop_name]
    else:
        LOOP_INIT = factory["aioloop"]


@pytest.yield_fixture
def loop():
    """
    Default event loop, you should only use this event loop in your tests.
    """
    loop = LOOP_INIT()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


def pytest_pycollect_makeitem(collector, name, obj):
    """
    pytest should also collect coroutines.
    """
    if collector.funcnamefilter(name) and _is_coroutine(obj):
        return list(collector._genfunctions(name, obj))


def pytest_pyfunc_call(pyfuncitem):
    """
    Run test coroutines in an event loop.
    """
    if _is_coroutine(pyfuncitem.function):
        loop = pyfuncitem.funcargs[LOOP_KEY]
        funcargs = pyfuncitem.funcargs
        testargs = {}
        for arg in pyfuncitem._fixtureinfo.argnames:
            testargs[arg] = funcargs[arg]
        loop.run_until_complete(
            loop.create_task(
                pyfuncitem.obj(**testargs)
            )
        )
        return True


def pytest_runtest_setup(item):
    """
    append a loop fixture to all test func.
    """
    if hasattr(item, 'fixturenames') and LOOP_KEY not in item.fixturenames:
        item.fixturenames.append(LOOP_KEY)


@pytest.fixture
def unused_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


@pytest.yield_fixture
def test_server(loop):
    """
    Create a TestServer instance based on a Sanic Application.

    test_server(app, **kwargs)
    """

    servers = []

    async def create_server(app, **kwargs):
        server = TestServer(app, loop=loop, **kwargs)
        await server.start_server()
        servers.append(server)
        return server

    yield create_server

    # Close Server
    if servers:
        for server in servers:
            loop.run_until_complete(server.close())


@pytest.yield_fixture
def test_client(loop):
    """
    Create a TestClient instance for test easy use.

    test_client(app, **kwargs)
    """
    clients = []

    async def create_client(app, **kwargs):
        client = TestClient(app, loop=loop, **kwargs)
        await client.start_server()
        clients.append(client)
        return client

    yield create_client

    # Clean up
    if clients:
        for client in clients:
            loop.run_until_complete(client.close())


# Helper Functions

def _is_coroutine(obj):
    return asyncio.iscoroutinefunction(obj) or inspect.isgeneratorfunction(obj)
