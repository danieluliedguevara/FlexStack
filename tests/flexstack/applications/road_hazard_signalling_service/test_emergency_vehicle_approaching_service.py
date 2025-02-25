import unittest
from unittest.mock import MagicMock

from flexstack.applications.road_hazard_signalling_service.emergency_vehicle_approaching_service import (
    EmergencyVehicleApproachingService
)


class TestEmergencyVehicleApproachingService(unittest.TestCase):
    """Test class for the EmergencyVehicleApproachingService."""

    def setUp(self):
        btp_router = MagicMock()
        vehicle_data = MagicMock()
        self.denm_eva_service = EmergencyVehicleApproachingService(
            btp_router, vehicle_data)

    def test_trigger_basic_service(self):
        """Test the trigger_basic_service method."""
        # Given
        self.denm_eva_service.den_service = MagicMock()
        self.denm_eva_service.den_service.denm_transmission_management = MagicMock()
        self.denm_eva_service.den_service.denm_transmission_management.request_denm_sending = MagicMock()
        tpv_data = {"class": "TPV", "device": "/dev/ttyACM0", "mode": 3, "time": "2020-03-13T13:01:14.000Z",
                    "ept": 0.005, "lat": 41.453606167, "lon": 2.073707333, "altHAE": 163.500, "epx": 8.754,
                    "epy": 10.597, "epv": 31.970, "track": 0.0000, "speed": 0.011, "climb": 0.000, "eps": 0.57}

        # denm_request = MagicMock()

        # When
        self.denm_eva_service.trigger_denm_sending(tpv_data)

        # Then
        self.denm_eva_service.den_service.denm_transmission_management.request_denm_sending.\
            assert_called_once()
        self.assertEqual(self.denm_eva_service.event_position["latitude"], int(tpv_data["lat"] * 10000000))
        self.assertEqual(self.denm_eva_service.event_position["longitude"], int(tpv_data["lon"] * 10000000))
        self.assertEqual(self.denm_eva_service.event_position["altitude"]["altitudeValue"],
                         int(tpv_data["altHAE"] * 100))


if __name__ == '__main__':
    unittest.main()
