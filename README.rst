pytest-sanic
============

.. start-badges

.. list-table::
    :stub-columns: 1

    * - Build
      - | |travis|
    * - Docs
      - |docs|
    * - Package
      - | |version| |wheel| |supported-versions| |supported-implementations|

.. |travis| image:: https://travis-ci.org/yunstanford/pytest-sanic.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/yunstanford/pytest-sanic

.. |docs| image:: https://readthedocs.org/projects/pytest-sanic/badge/?style=flat
    :target: https://readthedocs.org/projects/pytest-sanic
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/pytest-sanic.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pytest-sanic

.. |wheel| image:: https://img.shields.io/pypi/wheel/pytest-sanic.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pytest-sanic

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pytest-sanic.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pytest-sanic

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pytest-sanic.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/pytest-sanic

.. end-badges

A pytest plugin for `Sanic <http://sanic.readthedocs.io/en/latest/>`_. It helps you to test your code asynchronously.

This plugin provides:

* very easy testing with async coroutines
* common and useful fixtures
* asynchronous fixture support
* test_client/sanic_client for Sanic application
* test_server for Sanic application


You can find out more here:

http://pytest-sanic.readthedocs.io/en/latest/


-------
Install
-------

.. code::

    pip install pytest-sanic


-----------
Quick Start
-----------

You don't have to load ``pytest-sanic`` explicitly. ``pytest`` will do it for you.

You can set up a fixture for your ``app`` like this:

.. code-block:: python

    import pytest
    from .app import create_app

    @pytest.yield_fixture
    def app():
        app = create_app(test_config, **params)
        yield app

This ``app`` fixture can then be used from tests:

.. code-block:: python

    async def test_sanic_db_find_by_id(app):
        """
        Let's assume that, in db we have,
            {
                "id": "123",
                "name": "Kobe Bryant",
                "team": "Lakers",
            }
        """
        doc = await app.db["players"].find_by_id("123")
        assert doc.name == "Kobe Bryant"
        assert doc.team == "Lakers"

To send requests to your ``app``, you set up a client fixture using the loop_ and sanic_client_ fixtures:

.. code-block:: python

    @pytest.fixture
    def test_cli(loop, app, sanic_client):
        return loop.run_until_complete(sanic_client(app))

This ``test_cli`` fixture can then be used to send requests to your ``app``:

.. code-block:: python

    async def test_index(test_cli):
        resp = await test_cli.get('/')
        assert resp.status == 200

    async def test_player(test_cli):
        resp = await test_cli.get('/player')
        assert resp.status == 200

--------------------
asynchronous fixture
--------------------

``pytest-sanic`` also supports asynchronous fixtures, just writes them like common pytest fixtures.

.. code-block:: python

    @pytest.fixture
    async def async_fixture_sleep():
        await asyncio.sleep(0.1)
        return "sleep..."


--------
Fixtures
--------

Some fixtures for easy testing.

``loop``
~~~~~~~~

``pytest-sanic`` creates an event loop and injects it as a fixture. ``pytest`` will use this event loop to run your ``async tests``.
By default, fixture ``loop`` is an instance of `asyncio.new_event_loop`. But `uvloop` is also an option for you, by simpy passing
``--loop uvloop``. Keep mind to just use one single event loop.


``unused_port``
~~~~~~~~~~~~~~~

an unused TCP port on the localhost.


``test_server``
~~~~~~~~~~~~~~~

Creates a TestServer instance by giving a ``Sanic`` application. It's very easy to utilize ``test_server`` to create your `Sanic`
application server for testing.

.. code-block:: python

    @pytest.yield_fixture
    def app():
        app = Sanic("test_sanic_app")

        @app.route("/test_get", methods=['GET'])
        async def test_get(request):
            return response.json({"GET": True})

        yield app

    @pytest.fixture
    def sanic_server(loop, app, test_server):
        return loop.run_until_complete(test_server(app))

You can also very easily override this ``loop`` fixture by creating your own, simply like,

.. code-block:: python

    @pytest.yield_fixture
    def loop():
        loop = MyEventLoop()
        yield loop
        loop.close()

``test_client``
~~~~~~~~~~~~~~~

``test_client`` has been deprecated, please use `sanic_client` instead, check out `issue <https://github.com/yunstanford/pytest-sanic/issues/22>`_ for more context.


``sanic_client``
~~~~~~~~~~~~~~~~

Creates a TestClient instance by giving a ``Sanic`` application. You can simply have a client by using ``sanic_client``, like

.. code-block:: python

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

        yield app

    @pytest.fixture
    def test_cli(loop, app, sanic_client):
        return loop.run_until_complete(sanic_client(app, protocol=WebSocketProtocol))

    #########
    # Tests #
    #########

    async def test_fixture_test_client_get(test_cli):
        """
        GET request
        """
        resp = await test_cli.get('/test_get')
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == {"GET": True}

    async def test_fixture_test_client_post(test_cli):
        """
        POST request
        """
        resp = await test_cli.post('/test_post')
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == {"POST": True}

    async def test_fixture_test_client_put(test_cli):
        """
        PUT request
        """
        resp = await test_cli.put('/test_put')
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == {"PUT": True}

    async def test_fixture_test_client_delete(test_cli):
        """
        DELETE request
        """
        resp = await test_cli.delete('/test_delete')
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == {"DELETE": True}

    async def test_fixture_test_client_patch(test_cli):
        """
        PATCH request
        """
        resp = await test_cli.patch('/test_patch')
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == {"PATCH": True}

    async def test_fixture_test_client_options(test_cli):
        """
        OPTIONS request
        """
        resp = await test_cli.options('/test_options')
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == {"OPTIONS": True}

    async def test_fixture_test_client_head(test_cli):
        """
        HEAD request
        """
        resp = await test_cli.head('/test_head')
        assert resp.status == 200
        resp_json = await resp.json()
        # HEAD should not have body
        assert resp_json is None

    async def test_fixture_test_client_ws(test_cli):
        """
        Websockets
        """
        ws_conn = await test_cli.ws_connect('/test_ws')
        data = 'hello world!'
        await ws_conn.send_str(data)
        msg = await ws_conn.receive()
        assert msg.data == data
        await ws_conn.close()


small notes:

``test_cli.ws_connect`` does not work in ``sanic.__version__ <= '0.5.4'``, because of a Sanic bug, but it
has been fixed in master branch. And ``websockets.__version__ >= '4.0'`` has broken websockets in ``sanic.__version__ <= '0.6.0'``, but it has been fixed in `master <https://github.com/channelcat/sanic/commit/bca1e084116335fd939c2ee226070f0428cd5de8>`_.


----
Tips
----

* `Blueprints Testing <https://github.com/yunstanford/pytest-sanic/issues/3>`_
* ``test_cli.ws_connect`` does not work in ``sanic.__version__ <= '0.5.4'``, because of a Sanic bug, but it has been fixed in master branch.
* `Importing app has loop already running <https://github.com/yunstanford/pytest-sanic/issues/1>`_ when you have `db_init` listeners.
* `Incorrect coverage report <https://github.com/pytest-dev/pytest-cov/issues/117>`_ with ``pytest-cov``, but we can have workarounds for this issue, it's a pytest loading plugin problem essentially.
* Websockets > 4.0 has broken websockets in ``sanic.__version__ <= '0.6.0'``, but it has been fixed in `this commit <https://github.com/channelcat/sanic/commit/bca1e084116335fd939c2ee226070f0428cd5de8>`_


Feel free to create issue if you have any question. You can also check out `closed issues <https://github.com/yunstanford/pytest-sanic/issues?q=is%3Aclosed>`_


-----------
Development
-----------

``pytest-sanic`` accepts contributions on GitHub, in the form of issues or pull requests.


Build.

.. code::

    poetry install


Run unit tests.

.. code::

    poetry run pytest ./tests --cov pytest_sanic


---------
Reference
---------

Some useful pytest plugins:

* `pytest-tornado <https://github.com/eugeniy/pytest-tornado>`_
* `pytest-asyncio <https://github.com/pytest-dev/pytest-asyncio>`_
* `pytest-aiohttp <https://github.com/aio-libs/pytest-aiohttp>`_
