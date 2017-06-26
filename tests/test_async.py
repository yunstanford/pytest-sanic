import pytest
import asyncio


async def test_simple_async_func():
	await asyncio.sleep(0.1)
	assert True