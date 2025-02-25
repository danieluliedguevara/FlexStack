# import unittest
# from unittest.mock import MagicMock, patch
# from flexstack.facilities.ca_basic_service.ca_basic_service import (
#     CooperativeAwarenessBasicService,
# )


# class TestCooperativeAwarenessBasicService(unittest.TestCase):
#     @patch("flexstack.facilities.ca_basic_service.cam_coder.CAMCoder")
#     @patch(
#         "flexstack.facilities.ca_basic_service.cam_reception_management.CAMReceptionManagement"
#     )
#     @patch(
#         "flexstack.facilities.ca_basic_service.cam_transmission_management.CAMTransmissionManagement"
#     )
#     def test__init__(self, mock_transmission, mock_reception, mock_coder):
#         # Arrange
#         btp_router = MagicMock()
#         vehicle_data = MagicMock()
#         ldm = MagicMock()
#         mock_coder.return_value = MagicMock()
#         mock_transmission.return_value = MagicMock()
#         mock_reception.return_value = MagicMock()
#         # Act
#         ca_service = CooperativeAwarenessBasicService(btp_router, vehicle_data, ldm)
#         # Assert
#         self.assertEqual(ca_service.btp_router, btp_router)
#         self.assertEqual(ca_service.vehicle_data, vehicle_data)
#         mock_coder.assert_called_once()
#         print(ca_service.cam_coder.__module__)
#         print(ca_service.cam_coder.__class__)

#         self.assertEqual(ca_service.cam_coder, mock_coder.return_value)
#         mock_transmission.assert_called_once_with(
#             btp_router=btp_router,
#             cam_coder=mock_coder.return_value,
#             vehicle_data=vehicle_data,
#         )
#         self.assertEqual(
#             ca_service.cam_transmission_management, mock_transmission.return_value
#         )
#         mock_reception.assert_called_once_with(
#             cam_coder=mock_coder.return_value, btp_router=btp_router, ldm=ldm
#         )
#         self.assertEqual(
#             ca_service.cam_reception_management, mock_reception.return_value
#         )
