import unittest
from ..src.client import Client
from ..src.directory_server import Server
from ..src.relay_node import Relay

class TestRelay(unittest.TestCase):

    def test_create_relay(self):
        relay = Relay()
        self.assertIsNotNone(relay)

    def test_forward_message_valid(self):
        relay = Relay()
        # Assuming valid input parameters
        message = b"Example message"
        encrypted_key = b"Encrypted key"
        iv = b"Initialization vector"
        session_id = "Session ID"
        client_address = "127.0.0.1"
        self.assertTrue(relay.forward_message(message, encrypted_key, iv, session_id, client_address))

    def test_forward_message_invalid(self):
        relay = Relay()
        # Assuming invalid input parameters
        message = None
        encrypted_key = None
        iv = None
        session_id = None
        client_address = None
        self.assertFalse(relay.forward_message(message, encrypted_key, iv, session_id, client_address))

    # Add more tests for the Relay component
