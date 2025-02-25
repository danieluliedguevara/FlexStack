import unittest
from unittest.mock import MagicMock, patch

from flexstack.facilities.local_dynamic_map.ldm_maintenance_reactive import (
    LDMMaintenanceReactive,
)


class TestLDMMaintenanceReactive(unittest.TestCase):
    def setUp(self):
        self.location = MagicMock()
        self.database = MagicMock()
        self.ldm_maintenance_reactive = LDMMaintenanceReactive(
            self.location, self.database
        )

    @patch("builtins.super")
    def test_add_provider_data(self, mock_ldm_maintenace):
        mock_ldm_maintenace().add_provider_data = MagicMock(return_value=1)
        self.ldm_maintenance_reactive.collect_trash = MagicMock()
        test_dict = MagicMock()

        self.ldm_maintenance_reactive.add_provider_data(test_dict)
        mock_ldm_maintenace().add_provider_data.assert_called_once_with(test_dict)
        self.ldm_maintenance_reactive.collect_trash.assert_called_once()
