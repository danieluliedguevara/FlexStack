import unittest
from unittest.mock import MagicMock, patch
from flexstack.facilities.decentralized_environmental_notification_service.denm_reception_management import (
    DENMReceptionManagement
)
from flexstack.facilities.decentralized_environmental_notification_service.denm_coder import DENMCoder
from flexstack.btp.service_access_point import BTPDataIndication
from flexstack.btp.router import Router as BTPRouter
from flexstack.facilities.local_dynamic_map.ldm_facility import LDMFacility
from flexstack.facilities.local_dynamic_map.ldm_classes import AddDataProviderResp


class TestDENMReceptionManagement(unittest.TestCase):
    """Test class for the DENM Reception Management."""
    def setUp(self):
        self.denm_coder = MagicMock(spe=DENMCoder)
        self.btp_router = MagicMock(spe=BTPRouter)
        self.ldm = MagicMock(spe=LDMFacility)
        self.reception_management = DENMReceptionManagement(self.denm_coder,
                                                            self.btp_router, self.ldm)

    def test_feed_ldm(self):
        """Test the feed_ldm method."""
        # Given
        denm = MagicMock()
        self.reception_management.ldm_facility = MagicMock(spe=LDMFacility)
        self.reception_management.ldm_facility.if_ldm_3 = MagicMock()
        self.reception_management.ldm_facility.if_ldm_3.add_data_provider = MagicMock()
        response = MagicMock(spe=AddDataProviderResp)
        data = MagicMock()
        self.reception_management.ldm_facility.if_ldm_3.add_data_provider(data).return_value = response

        # When
        self.reception_management.feed_ldm(denm)

        # Then
        self.reception_management.ldm_facility.if_ldm_3.add_data_provider.assert_called_once()

    @patch.object(DENMReceptionManagement, 'feed_ldm')
    def test_reception_callback(self, mock_feed_ldm):
        """Test the reception callback function."""
        # Given
        btp_indication = MagicMock(spec=BTPDataIndication)
        btp_indication.data = MagicMock()
        self.denm_coder.decode = MagicMock()

        # When
        self.reception_management.reception_callback(btp_indication)

        # Then
        self.denm_coder.decode.assert_called_once_with(btp_indication.data)
        mock_feed_ldm.assert_called_once()
