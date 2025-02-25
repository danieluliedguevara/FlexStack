from typing import Dict
import unittest
from unittest.mock import MagicMock, patch
from flexstack.utils.gpsd_location_service import GPSDLocationService


class TestGPSDLocationService(unittest.TestCase):
    @patch('threading.Thread')
    @patch('socket.socket')
    def test__init__(self, mock_socket, mock_thread):
        # Given
        socket = MagicMock()
        mock_socket.return_value = socket
        thread = MagicMock()
        thread.start = MagicMock()
        mock_thread.return_value = thread
        # When
        location_service = GPSDLocationService()

        # Then
        self.assertEqual(location_service.socket, socket)
        self.assertEqual(location_service.callbacks, [])
        self.assertEqual(location_service.gpsd_host, "localhost")
        self.assertEqual(location_service.gpsd_port, 2947)
        mock_thread.assert_called_once_with(target=location_service.start, daemon=True)
        thread.start.assert_called_once()

    @patch("threading.Thread")
    @patch("socket.socket")
    def test_reconnect(self, socket_lib_mock, mock_thread):
        # Given
        thread = MagicMock()
        thread.start = MagicMock()
        mock_thread.return_value = thread
        socket_mock = MagicMock()
        socket_mock.connect = MagicMock()
        socket_mock.send = MagicMock()
        socket_lib_mock.return_value = socket_mock
        # When
        location_service = GPSDLocationService()
        location_service.reconnect()
        # Then
        socket_mock.connect.assert_called_once_with(("localhost", 2947))
        socket_mock.send.assert_called_once_with(b'?WATCH={"enable":true,"json":true};')

    @patch("json.loads")
    @patch("threading.Thread")
    @patch("socket.socket")
    def test_start(self, socket_lib_mock, mock_thread, json_loads_mock):
        # Given
        thread = MagicMock()
        thread.start = MagicMock()
        mock_thread.return_value = thread
        socket_mock = MagicMock()
        socket_mock.recv = MagicMock()
        data = b'{"class": "TPV", "device": "/dev/pts/1", "time": "2005-06-08T10:34:48.283Z", "ept": 0.005, "lat": 46.498293369, "lon": 7.567411672, "alt": 1343.127, "eph": 36.0, "epv": 32.321, "track": 10.3788, "speed": 0.091, "climb": -0.085, "mode": 3}'
        socket_mock.recv.return_value = data
        socket_lib_mock.return_value = socket_mock
        json_loads_mock.return_value = {
            "class": "TPV",
            "device": "/dev/pts/1",
            "time": "2005-06-08T10:34:48.283Z",
            "ept": 0.005,
            "lat": 46.498293369,
            "lon": 7.567411672,
            "alt": 1343.127,
            "eph": 36.0,
            "epv": 32.321,
            "track": 10.3788,
            "speed": 0.091,
            "climb": -0.085,
            "mode": 3,
        }

        stop_event = MagicMock()
        stop_event.is_set = MagicMock(return_value=False)

        # When
        location_service = GPSDLocationService()

        def raise_Keyboard_interrupt(whatever: Dict):
            raise KeyboardInterrupt()

        location_service.add_callback(raise_Keyboard_interrupt)
        location_service.reconnect = MagicMock()

        # Then
        self.assertRaises(KeyboardInterrupt, location_service.start)
        socket_mock.recv.assert_called_once_with(1024)
        json_loads_mock.assert_called_once_with(data)
