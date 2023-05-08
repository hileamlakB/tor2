import unittest
from ..src.client import Client
from ..src.directory_server import Server
from ..src.relay_node import Relay
class TestServer(unittest.TestCase):

    def test_create_server(self):
        server = Server()
        self.assertIsNotNone(server)

    def test_add_relay_valid(self):
        server = Server()
        relay = Relay()
        self.assertTrue(server.add_relay(relay))

    def test_add_relay_invalid(self):
        server = Server()
        relay = None
        self.assertFalse(server.add_relay(relay))

    # Add more tests for the Server component

