import asyncio
import pytest
try:
    import uvloop
except:  # pragma: no cover
    uvloop = None


LOOP_INIT = None


def pytest_configure(config):
    loop_name = config.getoption('--loop')
    factory = {
        "aioloop": asyncio.new_event_loop,
    }
    if uvloop is not None:
        factory["uvloop"] = uvloop.new_event_loop

    if loop_name:
        if loop_name not factory:
            raise ValueError(
                "{name} is not valid option".format(name=loop_name)
            )
        LOOP_INIT = factory[loop_name]
    else:
        LOOP_INIT = factory["aioloop"]


@pytest.yield_fixture
def loop():
    loop = LOOP_INIT()
    yield loop
    loop.close()
