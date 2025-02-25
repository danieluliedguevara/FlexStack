import unittest
from unittest.mock import MagicMock, patch

from flexstack.facilities.local_dynamic_map.ldm_service_reactive import (
    LDMServiceReactive,
)


class TestLDMServiceReactive(unittest.TestCase):
    def setUp(self):
        self.ldm_maintenance = MagicMock()
        self.ldm_service = LDMServiceReactive(self.ldm_maintenance)

    @patch("builtins.super")
    def test_add_provider_data(self, mock_ldm_service):
        mock_ldm_service().add_provider_data = MagicMock(return_value=1)
        self.ldm_service.attend_subscriptions = MagicMock()
        test_dict = {"a": 1, "b": 2}

        self.ldm_service.add_provider_data(test_dict)
        mock_ldm_service().add_provider_data.assert_called_once_with(test_dict)
        self.ldm_service.attend_subscriptions.assert_called_once()
