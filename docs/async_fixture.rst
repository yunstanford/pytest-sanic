====================
asynchronous fixture
====================

``pytest-sanic`` also supports asynchronous fixtures, just writes them like common pytest fixtures.

.. code-block:: python

    @pytest.fixture
    async def async_fixture_sleep():
        await asyncio.sleep(0.1)
        return "sleep..."
