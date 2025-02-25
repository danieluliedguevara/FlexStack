import unittest
from unittest.mock import MagicMock, patch

from flexstack.facilities.local_dynamic_map.if_ldm_4 import InterfaceLDM4
from flexstack.facilities.local_dynamic_map.ldm_classes import (
    DeregisterDataConsumerReq,
    DeregisterDataConsumerResp,
    Filter,
    FilterStatement,
    OrderTuple,
    RegisterDataConsumerReq,
    RegisterDataConsumerResp,
    RequestDataObjectsReq,
    SubscribeDataobjectsReq,
    UnsubscribeDataobjectsReq,
    ComparisonOperators,
)

from flexstack.facilities.local_dynamic_map.ldm_constants import (
    VAM,
    DENM,
    CAM,
    MAPEM,
)

white_cam = {
    "header": {
        "protocolVersion": 2,
        "messageID": 2,
        "stationID": 0,
    },
    "cam": {
        "generationDeltaTime": 0,
        "camParameters": {
            "basicContainer": {
                "stationType": 0,
                "referencePosition": {
                    "latitude": 900000001,
                    "longitude": 1800000001,
                    "positionConfidenceEllipse": {
                        "semiMajorConfidence": 4095,
                        "semiMinorConfidence": 4095,
                        "semiMajorOrientation": 201,
                    },
                    "altitude": {
                        "altitudeValue": 800001,
                        "altitudeConfidence": "unavailable",
                    },
                },
            },
            "highFrequencyContainer": (
                "basicVehicleContainerHighFrequency",
                {
                    "heading": {"headingValue": 201, "headingConfidence": 127},
                    "speed": {"speedValue": 16383, "speedConfidence": 127},
                    "driveDirection": "unavailable",
                    "vehicleLength": {
                        "vehicleLengthValue": 1023,
                        "vehicleLengthConfidenceIndication": "unavailable",
                    },
                    "vehicleWidth": 62,
                    "longitudinalAcceleration": {
                        "longitudinalAccelerationValue": 161,
                        "longitudinalAccelerationConfidence": 102,
                    },
                    "curvature": {
                        "curvatureValue": 1023,
                        "curvatureConfidence": "unavailable",
                    },
                    "curvatureCalculationMode": "unavailable",
                    "yawRate": {
                        "yawRateValue": 32767,
                        "yawRateConfidence": "unavailable",
                    },
                },
            ),
        },
    },
}


class Test_if_ldm_4(unittest.TestCase):
    def setUp(self) -> None:
        self.ldm_service = MagicMock()
        self.if_ldm_4 = InterfaceLDM4(self.ldm_service)

    def test_check_its_aid(self):
        self.assertEqual(self.if_ldm_4.check_its_aid(1), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(2), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(3), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(4), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(5), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(6), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(7), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(8), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(9), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(10), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(11), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(12), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(13), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(14), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(15), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(16), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(17), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(18), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(19), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(20), True)
        self.assertEqual(self.if_ldm_4.check_its_aid(21), True)

    def test_check_permissions(self):
        access_permisions = [DENM, CAM]
        data_object_id = VAM
        self.assertEqual(self.if_ldm_4.check_permissions(1, data_object_id), False)
        self.assertEqual(
            self.if_ldm_4.check_permissions(access_permisions, data_object_id), False
        )

        access_permisions = [VAM]
        data_object_id = VAM
        self.assertEqual(
            self.if_ldm_4.check_permissions(access_permisions, data_object_id), True
        )

        access_permisions = [VAM, CAM, DENM, MAPEM]
        data_object_id = DENM
        self.assertEqual(
            self.if_ldm_4.check_permissions(access_permisions, data_object_id), True
        )

    def test_register_data_consumer(self):
        permission_list = [CAM]
        data_consumer_correct = RegisterDataConsumerReq(CAM, permission_list, None)
        data_consumer_incorrect = RegisterDataConsumerReq(CAM, None, None)
        self.assertIsInstance(
            self.if_ldm_4.register_data_consumer(data_consumer_correct),
            RegisterDataConsumerResp,
        )

        self.assertEqual(
            str(self.if_ldm_4.register_data_consumer(data_consumer_correct).result),
            "accepted",
        )
        self.assertEqual(
            str(self.if_ldm_4.register_data_consumer(data_consumer_incorrect).result),
            "rejected",
        )

    def test_deregister_data_consumer(self):
        self.ldm_service.del_data_consumer_its_aid = MagicMock(return_value=None)
        self.ldm_service.get_data_consumer_its_aid = MagicMock(
            return_value=[
                2,
            ]
        )
        data_consumer_correct = DeregisterDataConsumerReq(CAM)
        data_consumer_incorrect = DeregisterDataConsumerReq(50)

        self.assertIsInstance(
            self.if_ldm_4.deregister_data_consumer(data_consumer_correct),
            DeregisterDataConsumerResp,
        )

        self.assertEqual(
            str(self.if_ldm_4.deregister_data_consumer(data_consumer_correct).ack),
            "succeed",
        )
        self.assertEqual(
            str(self.if_ldm_4.deregister_data_consumer(data_consumer_incorrect).ack),
            "failed",
        )

    def test_request_data_objects(self):
        # Hay un ldm_service con el registro de un data-consumer
        self.ldm_service.get_data_consumer_its_aid = MagicMock(
            return_value=[
                2,
            ]
        )
        self.ldm_service.query = MagicMock(
            return_value=[
                white_cam,
            ]
        )

        # Se hace un datarequest
        filter_statement_1 = FilterStatement(
            "cam.camParameters.basicContainer.referencePosition.latitude",
            ComparisonOperators(0),
            900000001,
        )
        filter_statement_1_incorrect = FilterStatement(
            "cam.camParameters.referencePosition.latitude",
            ComparisonOperators(0),
            900000001,
        )  # wrong attribute
        filter_statement_2 = FilterStatement(
            "cam.camParameters.basicContainer.referencePosition.longitude",
            ComparisonOperators(1),
            1800000001,
        )

        # Se hace un query
        filter = Filter(filter_statement_1, 0, filter_statement_2)
        data_request = RequestDataObjectsReq(
            35,
            [
                2,
            ],
            1,
            None,
            filter,
        )
        self.assertEqual(
            str(self.if_ldm_4.request_data_objects(data_request).result),
            "invalidITSAID",
        )

        data_request = RequestDataObjectsReq(
            2,
            [
                69,
            ],
            1,
            None,
            None,
        )
        self.assertEqual(
            str(self.if_ldm_4.request_data_objects(data_request).result),
            "invalidDataObjectType",
        )

        data_request = RequestDataObjectsReq(
            2,
            [
                2,
            ],
            256,
            None,
            None,
        )
        self.assertEqual(
            str(self.if_ldm_4.request_data_objects(data_request).result),
            "invalidPriority",
        )

        filter = [filter_statement_1_incorrect, 0, filter_statement_2]
        data_request = RequestDataObjectsReq(
            2,
            [
                2,
            ],
            1,
            None,
            filter,
        )
        self.assertEqual(
            str(self.if_ldm_4.request_data_objects(data_request).result),
            "invalidFilter",
        )

        data_request = RequestDataObjectsReq(
            2,
            [
                2,
            ],
            1,
            3,
            None,
        )
        self.assertEqual(
            str(self.if_ldm_4.request_data_objects(data_request).result), "invalidOrder"
        )

        data_request = RequestDataObjectsReq(
            2,
            [
                2,
            ],
            None,
            None,
            None,
        )
        self.assertEqual(
            str(self.if_ldm_4.request_data_objects(data_request).result), "succeed"
        )

        filter = Filter(filter_statement_1, 0, filter_statement_2)
        data_request = RequestDataObjectsReq(
            2,
            [
                2,
            ],
            None,
            None,
            filter,
        )
        self.assertEqual(
            self.if_ldm_4.request_data_objects(data_request).data_objects,
            [
                white_cam,
            ],
        )

    @patch(
        "flexstack.facilities.local_dynamic_map.if_ldm_4.LDMService.subscriptions_service"
    )
    def test_subscribe_data_consumer(self, ldm_service_subscriptions_service):
        callback_function = MagicMock()
        self.ldm_service.get_data_consumer_its_aid = MagicMock(
            return_value=[
                2,
            ]
        )

        subscribe_data_consumer = SubscribeDataobjectsReq(
            5, [2, 1], None, None, None, None, None
        )
        self.assertEqual(
            str(
                self.if_ldm_4.subscribe_data_consumer(
                    subscribe_data_consumer, callback_function
                ).result
            ),
            "invalidITSAID",
        )

        subscribe_data_consumer = SubscribeDataobjectsReq(
            2, [123, 42], None, None, None, None, None
        )
        self.assertEqual(
            str(
                self.if_ldm_4.subscribe_data_consumer(
                    subscribe_data_consumer, callback_function
                ).result
            ),
            "invalidDataObjectType",
        )

        subscribe_data_consumer = SubscribeDataobjectsReq(
            2, [2, 1], 256, None, None, None, None
        )
        self.assertEqual(
            str(
                self.if_ldm_4.subscribe_data_consumer(
                    subscribe_data_consumer, callback_function
                ).result
            ),
            "invalidPriority",
        )

        filter_statement_1_incorrect = FilterStatement(
            "cam.camParameters.referencePosition.latitude",
            ComparisonOperators(0),
            900000001,
        )  # wrong attribute
        filter_statement_2 = FilterStatement(
            "cam.camParameters.basicContainer.referencePosition.longitude",
            ComparisonOperators(1),
            1800000001,
        )
        filter = Filter(filter_statement_1_incorrect, 0, filter_statement_2)
        subscribe_data_consumer = SubscribeDataobjectsReq(
            2, [2, 1], None, filter, None, None, None
        )

        subscribe_data_consumer = SubscribeDataobjectsReq(
            2, [2, 1], None, None, -3, None, None
        )
        self.assertEqual(
            str(
                self.if_ldm_4.subscribe_data_consumer(
                    subscribe_data_consumer, callback_function
                ).result
            ),
            "invalidNotificationInterval",
        )

        subscribe_data_consumer = SubscribeDataobjectsReq(
            2, [2, 1], None, None, None, 256, None
        )
        self.assertEqual(
            str(
                self.if_ldm_4.subscribe_data_consumer(
                    subscribe_data_consumer, callback_function
                ).result
            ),
            "invalidMultiplicity",
        )

        subscribe_data_consumer = SubscribeDataobjectsReq(
            2, [2, 1], None, None, None, None, OrderTuple(2, 0)
        )
        self.assertEqual(
            str(
                self.if_ldm_4.subscribe_data_consumer(
                    subscribe_data_consumer, callback_function
                ).result
            ),
            "invalidOrder",
        )

        subscribe_data_consumer = SubscribeDataobjectsReq(
            2, [2, 1], None, None, None, None, None
        )
        self.assertEqual(
            str(
                self.if_ldm_4.subscribe_data_consumer(
                    subscribe_data_consumer, callback_function
                ).result
            ),
            "successful",
        )

    def test_unsubscribe_data_consumer(self):
        self.ldm_service.delete_subscription = MagicMock(return_value=False)
        self.ldm_service.get_data_consumer_its_aid = MagicMock(
            return_value=[
                2,
            ]
        )

        unsubscribe_data_consumer = UnsubscribeDataobjectsReq(5, 1212)
        self.assertEqual(
            str(
                self.if_ldm_4.unsubscribe_data_consumer(
                    unsubscribe_data_consumer
                ).result
            ),
            "failed",
        )

        unsubscribe_data_consumer = UnsubscribeDataobjectsReq(2, 1)
        self.assertEqual(
            str(
                self.if_ldm_4.unsubscribe_data_consumer(
                    unsubscribe_data_consumer
                ).result
            ),
            "failed",
        )

        self.ldm_service.delete_subscription = MagicMock(return_value=True)
        unsubscribe_data_consumer = UnsubscribeDataobjectsReq(2, 1212)
        self.assertEqual(
            str(
                self.if_ldm_4.unsubscribe_data_consumer(
                    unsubscribe_data_consumer
                ).result
            ),
            "accepted",
        )


if __name__ == "__main__":
    unittest.main()
