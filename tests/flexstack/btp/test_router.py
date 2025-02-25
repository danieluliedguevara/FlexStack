import unittest
from unittest.mock import MagicMock

from flexstack.btp.router import Router
from flexstack.btp.service_access_point import BTPDataRequest, PacketTransportType, CommunicationProfile, TrafficClass, CommonNH


class TestRouter(unittest.TestCase):

    def test__init__(self):
        gn_router = MagicMock()
        router = Router(gn_router)
        self.assertEqual(router.indication_callbacks, {})
        self.assertEqual(router.gn_router, gn_router)

    def test_register_indication_callback(self):
        gn_router = MagicMock()
        router = Router(gn_router)
        callback = MagicMock()
        router.register_indication_callback_btp(1, callback)
        self.assertEqual(router.indication_callbacks[1], callback)

    def test_BTPDataRequest(self):
        """
        Test to be improved!
        """
        gn_router = MagicMock()
        gn_router.gn_data_request = MagicMock()
        router = Router(gn_router)
        request = BTPDataRequest()
        request.btp_type = CommonNH.BTP_B
        request.destination_port = 2001
        request.gn_packet_transport_type = PacketTransportType()
        request.communication_profile = CommunicationProfile.UNSPECIFIED
        request.traffic_class = TrafficClass()
        request.data = b'Hello World'
        request.length = len(request.data)
        router.btp_data_request(request)
        gn_router.gn_data_request.assert_called_once()


if __name__ == '__main__':
    unittest.main()
