import unittest
from ..src.client import Client
from ..src.directory_server import Server
from ..src.relay_node import Relay

class TestClient(unittest.TestCase):

    def test_create_client(self):
        client = Client()
        self.assertIsNotNone(client)

    def test_send_message_valid(self):
        client = Client()
        # Assuming a valid URL and request type
        url = "www.example.com"
        request_type = "GET"
        self.assertTrue(client.send_message(url, request_type))

    def test_send_message_invalid(self):
        client = Client()
        # Assuming an invalid URL and request type
        url = "not_a_url"
        request_type = "INVALID"
        self.assertFalse(client.send_message(url, request_type))

    # Add more tests for the Client component


if __name__ == "__main__":
    unittest.main()
