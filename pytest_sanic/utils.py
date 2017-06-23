from aiohttp import ClientSession
from sanic.server import serve, trigger_events
from sanic.app import Sanic
import socket


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

	def __init__(self, app, host, loop):
		self._app = app
		self._loop = loop

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

	async def start_server(self):
		await self._server.start_server(loop=self.loop)
	
	