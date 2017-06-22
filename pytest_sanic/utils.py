from aiohttp import ClientSession
from sanic.server import serve
import socket


class TestServer:

	def __init__(self, app, host='127.0.0.1', loop=None, **kwargs):
		self.server = None
		self.port = None
		self.loop = loop
		self.host = host
		self.root = None

	async start_server(self, loop=None, **kwargs):
		self.loop = loop
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.host, 0))
		self.port = self.socket.getsockname()[1]
		if kwargs.get('ssl', None):
			self.scheme = 'https'
		else:
			self.scheme = 'http'

		# before start

		# after start

		# start server


	async close(self):
		# before stop
		pass
		# stop

		# after stop and clean up



class TestClient:

	"""
	a test client class designed for easy testing in Sanic Application.
	"""

	def __init__(self, app, host):
		pass
