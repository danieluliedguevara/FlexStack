import platform
import unittest

from unittest.mock import MagicMock, patch

from flexstack.linklayer.raw_link_layer import RawLinkLayer


def skip_if_windows(func):
    def wrapper(*args, **kwargs):
        if platform.system() == "Windows":
            print("Skipping test on Windows.")
            return
        return func(*args, **kwargs)
    return wrapper


@skip_if_windows
class TestRawLinkLayer(unittest.TestCase):
    @patch("threading.Thread")
    @patch("socket.socket")
    def test__init__(self, mock_socket, mock_thread):
        socket_instance = MagicMock()
        mock_socket.return_value = socket_instance
        socket_instance.bind = MagicMock()
        thread_instance = MagicMock()
        mock_thread.return_value = thread_instance
        thread_instance.start = MagicMock()
        # Arrange
        mock_receive_callback = MagicMock()
        # Act
        raw_link_layer = RawLinkLayer(
            iface="lo", mac_address=b"\x00\x00\x00\x00\x00\x00", receive_callback=mock_receive_callback)
        # Assert
        mock_socket.assert_called_once()
        socket_instance.bind.assert_called_once()
        self.assertEqual(raw_link_layer.mac_address,
                         b"\x00\x00\x00\x00\x00\x00")
        mock_thread.assert_called_once()
        thread_instance.start.assert_called_once()

    @patch("threading.Thread")
    @patch("socket.socket")
    def test_send(self, mock_socket, mock_thread):
        socket_instance = MagicMock()
        mock_socket.return_value = socket_instance
        socket_instance.bind = MagicMock()
        socket_instance.send = MagicMock()
        thread_instance = MagicMock()
        mock_thread.return_value = thread_instance
        thread_instance.start = MagicMock()
        # Arrange
        mock_receive_callback = MagicMock()
        # Act
        raw_link_layer = RawLinkLayer(
            iface="lo", mac_address=b"\x00\x00\x00\x00\x00\x00", receive_callback=mock_receive_callback)
        raw_link_layer.send(b"packet")
        # Assert
        dest = b'\xff\xff\xff\xff\xff\xff'
        ethertype = b'\x89\x47'
        packet = dest + b"\x00\x00\x00\x00\x00\x00" + ethertype + b"packet"
        socket_instance.send.assert_called_once_with(packet)

    @patch("threading.Thread")
    @patch("socket.socket")
    def test_receive(self, mock_socket, mock_thread):
        socket_instance = MagicMock()
        mock_socket.return_value = socket_instance
        socket_instance.bind = MagicMock()
        socket_instance.recv = MagicMock(return_value=(
            b'\xff\xff\xff\xff\xff\xff'+b'\xaa\xbb\xcc\xaa\xbb\xcc'+b'\x89\x47'+b"packet"))
        thread_instance = MagicMock()
        mock_thread.return_value = thread_instance
        thread_instance.start = MagicMock()
        # Arrange

        def mock_receive_callback(packet):
            raise OSError
        mock_receive_callback = MagicMock(side_effect=mock_receive_callback)
        # Act
        raw_link_layer = RawLinkLayer(
            iface="lo", mac_address=b"\x00\x00\x00\x00\x00\x00", receive_callback=mock_receive_callback)
        raw_link_layer.receive()
        # Assert
        socket_instance.recv.assert_called_once()
        mock_receive_callback.assert_called_once_with(b"packet")
