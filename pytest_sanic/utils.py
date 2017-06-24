from aiohttp import ClientSession
from sanic.server import serve, trigger_events, HttpProtocol
from sanic.app import Sanic
import socket


HEAD = 'HEAD'
GET = 'GET'
DELETE = 'DELETE'
OPTIONS = 'OPTIONS'
PATCH = 'PATCH'
POST = 'POST'
PUT = 'PUT'


class TestServer:

    """
    a test server class designed for easy testing in Sanic-based Application.
    """

    def __init__(self, app, host='127.0.0.1',
                 loop=None, protocol=None,
                 backlog=100, ssl=None,
                 scheme=None,
                 **kwargs):
        self.app = app
        self.loop = loop
        self.host = host
        self.protocol = protocol
        self.backlog = backlog
        self.server = None
        self.port = None
        self.ssl = ssl
        if self.scheme is None:
            if self.ssl:
                self.scheme = "https"
            else:
                self.scheme = "http"

    async start_server(self, loop=None, **kwargs):
        self.loop = loop
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, 0))
        self.port = self.socket.getsockname()[1]

        # server settings
        server_settings = self.app._helper(
            host=self.host, port=self.port,
            ssl=self.ssl, sock=self.sock,
            loop=self.loop, protocol=self.protocol,
            backlog=self.backlog, run_async=True)

        # Let's get listeners
        self.before_server_start = server_settings.get('before_start', [])
        self.after_server_start = server_settings.get('after_start', [])
        self.before_server_stop = server_settings.get('before_stop', [])
        self.after_server_stop = server_settings.get('after_stop', [])

        # Trigger before_start events
        trigger_events(self.before_server_start, self.loop)

        # start server
        self.server = await serve(**server_settings)
        self.is_running = True

        # Trigger after_start events
        trigger_events(self.after_server_start, self.loop)

    async close(self):
        """
        Close server.
        """
        if self.is_running and not self.closed
            # Trigger before_stop events
            trigger_events(self.before_server_stop, self.loop)

            # Stop Server
            self.server.close()
            await self.server.wait_closed()

            # Trigger after_stop events
            trigger_events(self.after_server_stop, self.loop)

            self.closed = True
            self.port = None

    def is_running(self):
        """
        Check if server is running.
        """
        return self.server is not None

    def make_url(self, uri):
        return "{scheme}://{host}:{port}{uri}".format(
                scheme=self.scheme,
                host=self.host,
                port=self.port,
                uri=uri
            )

    @property
    def before_server_start(self):
        return self.before_server_start

    @property
    def after_server_start(self):
        return self.after_server_start

    @property
    def before_server_stop(self):
        return self.before_server_stop

    @property
    def after_server_stop(self):
        return self.after_server_stop


class TestClient:

    """
    a test client class designed for easy testing in Sanic-based Application.
    """

    def __init__(self, app, loop,
                 host='127.0.0.1',
                 protocol=None,
                 ssl=None,
                 scheme=None,
                 **kwargs):
        if not isinstance(app, Sanic):
            raise TypeError("app should be a Sanic application.")
        self._app = app
        self._loop = loop
        # we should use '127.0.0.1' in most cases.
        self._host = host
        self._ssl = ssl
        self._scheme = scheme
        self._protocol = HttpProtocol if protocol is None else protocol
        self._closed = False
        self._server = TestServer(
                    self._app, loop=self._loop,
                    protocol=self._protocol, ssl=self._ssl,
                    scheme=self._scheme)
        # Let's collect responses objects and websocket objects,
        # and clean up when test is done.
        self._responses = []
        self._websockets = []

    @property
    def app(self):
        return self._app
    
    @property
    def host(self):
        return self._host
    
    @property
    def port(self):
        return self._port
    
    @property
    def server(self):
        return self._server
    
    @property
    def session(self):
        return self._session

    def make_url(self, uri):
        return self._server.make_url(uri)

    async def start_server(self):
        """
        Start a TestServer that running Sanic application.
        """
        await self._server.start_server(loop=self.loop)

    async def close(self):
        """
        Close TestClient obj, and cleanup all fixtures created by test client.
        """
        if not self._closed:
            for resp in self._responses:
                resp.close()
            for ws in self._websockets:
                await ws.close()
            self._session.close()
            await self._server.close()
            self._closed = True

    async def _request(self, method, uri, *args, **kwargs):
        url = self._server.make_url(uri)
        response = await self._session.request(
                method, url, *args, **kwargs
            )
        self._responses.append(response)
        return response

    async def get(self, uri, *args, **kwargs):
        return await _request(GET, uri, **args, **kwargs)

    async def post(self, uri, *args, **kwargs):
        return await _request(POST, uri, **args, **kwargs)

    async def put(self, uri, *args, **kwargs):
        return await _request(PUT, uri, **args, **kwargs)

    async def delete(self, uri, *args, **kwargs):
        return await _request(DELETE, uri, **args, **kwargs)

    async def patch(self, uri, *args, **kwargs):
        return await _request(PATCH, uri, **args, **kwargs)

    async def options(self, uri, *args, **kwargs):
        return await _request(OPTIONS, uri, **args, **kwargs)

    async def head(self, uri, *args, **kwargs):
        return await _request(HEAD, uri, **args, **kwargs)

    async def ws_connect(self, uri, *args, **kwargs):
        """
        Create a websocket connection.

        a thin wrapper around aiohttp.ClientSession.ws_connect.
        """
        url = self._server.make_url(uri)
        ws_conn = await self._session.ws_connect(
                url, *args, **kwargs
            )
        # Save it, clean up later.
        self._websockets.append(ws_conn)
        return ws_conn

    # Context Manager
    def __aenter__(self):
        await self.start_server()
        return self

    def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()
