import pytest
import asynctest
import asyncio
from unittest import mock
from async_generator import async_generator, yield_


@pytest.fixture
async def async_gen_fixture_sleep():
    await asyncio.sleep(0.1)
    yield_('a value')


@pytest.fixture
async def async_fixture_sleep():
    return await asyncio.sleep(0.1)


@pytest.fixture
async def async_fixture():
	client = mock.Mock()
	client.assume_role = asynctest.CoroutineMock(return_value={"foo": "bar"})
	return await client.assume_role()


async def test_async_fixture(async_fixture):
	assert async_fixture == {"foo": "bar"}


@pytest.fixture
def mock_fixture():
    return mock.Mock(return_value={"foo": "bar"})


@pytest.fixture
@async_generator
async def async_gen_fixture(mock_fixture):
    await yield_(mock_fixture())


async def test_async_gen_fixture(async_gen_fixture, mock_fixture):
    assert mock_fixture.called
    assert async_gen_fixture == {"foo": "bar"}
