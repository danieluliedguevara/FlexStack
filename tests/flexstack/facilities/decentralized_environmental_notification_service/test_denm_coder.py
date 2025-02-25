import unittest
from flexstack.facilities.decentralized_environmental_notification_service.denm_coder import DENMCoder


class TestDENMCoder(unittest.TestCase):
    # pylint: disable=duplicate-code
    """Test DENMCoder class"""

    def test_init(self):
        """Test DENMCoder initialization"""
        denm_coder = DENMCoder()
        self.assertIsNotNone(denm_coder)

    def test_encode(self):
        """Test DENMCoder encoding"""
        white_denm = {
            "header": {
                "protocolVersion": 2,
                "messageId": 1,
                "stationId": 0
            },
            "denm": {
                "management": {
                    "actionId": {
                        "originatingStationId": 0,  # 4294967295
                        "sequenceNumber": 0         # 65535
                    },
                    "detectionTime": 0,
                    "referenceTime": 0,
                    "termination": "isCancellation",
                    "eventPosition": {
                        "latitude": 900000001,
                        "longitude": 1800000001,
                        "positionConfidenceEllipse": {
                            "semiMajorConfidence": 4095,
                            "semiMinorConfidence": 4095,
                            "semiMajorOrientation": 3601
                        },
                        "altitude": {
                            "altitudeValue": 800001,
                            "altitudeConfidence": "unavailable"
                        }
                    },
                    "relevanceDistance": "lessThan50m",
                    "relevanceTrafficDirection": "allTrafficDirections",
                    "validityDuration": 0,
                    "TransmissionInterval": 100,
                    "stationType": 0
                }
            }
        }
        denm_coder = DENMCoder()
        expected_denm = b'\x02\x01\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
            + b'\x03ZN\x90\x0e\xb4\x9d \x0f\xff\xff\xff\x08\xed\xdd\x0f\x80\x00\x00\x00'
        encoded_denm = denm_coder.encode(white_denm)
        # print(encoded_denm)
        self.assertEqual(expected_denm, encoded_denm)

    def test_complete_encode(self):
        """Test DENMCoder encoding"""
        complete_denm = {
            "header": {
                "protocolVersion": 2,
                "messageId": 1,
                "stationId": 0
            },
            "denm": {
                "management": {
                    "actionId": {
                        "originatingStationId": 0,  # 4294967295
                        "sequenceNumber": 0         # 65535
                    },
                    "detectionTime": 0,
                    "referenceTime": 0,
                    "termination": "isCancellation",
                    "eventPosition": {
                        "latitude": 900000001,
                        "longitude": 1800000001,
                        "positionConfidenceEllipse": {
                            "semiMajorConfidence": 4095,
                            "semiMinorConfidence": 4095,
                            "semiMajorOrientation": 3601
                        },
                        "altitude": {
                            "altitudeValue": 800001,
                            "altitudeConfidence": "unavailable"
                        }
                    },
                    "relevanceDistance": "lessThan50m",
                    "relevanceTrafficDirection": "allTrafficDirections",
                    "validityDuration": 0,
                    "TransmissionInterval": 100,
                    "stationType": 0
                },
                "situation": {
                    "informationQuality": 7,
                    "eventType": {
                        "ccAndScc": ("reserved0", 0)
                    }
                },
                "location": {
                    "eventSpeed": {
                        "speedValue": 16383,
                        "speedConfidence": 127
                    },
                    "eventPositionHeading": {
                        "value": 3601,
                        "confidence": 127
                    },
                    "detectionZonesToEventPosition": [
                        [
                            {
                                "pathPosition": {
                                    "deltaLatitude": 131072,
                                    "deltaLongitude": 131072,
                                    "deltaAltitude": 12800
                                }
                            }
                        ]
                    ]
                }
            }
        }
        denm_coder = DENMCoder()
        expected_denm = b'\x02\x01\x00\x00\x00\x00\xc9\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
            + b'\x00\x00\x03ZN\x90\x0e\xb4\x9d \x0f\xff\xff\xff\x08\xed\xdd\x0f\x80\x00\x00\x07\x00\x007\xff\xff' \
            + b'\xb8G\xf0\x05\xff\xff\xff\xff\xf8\xe7\x00'
        encoded_denm = denm_coder.encode(complete_denm)
        # print(encoded_denm)
        self.assertEqual(expected_denm, encoded_denm)

    def test_collision_warning_encode(self):
        """Test DENMCoder encoding"""
        collision_warning_denm = {
            "header": {
                "protocolVersion": 2,
                "messageId": 1,
                "stationId": 0
            },
            "denm": {
                "management": {
                    "actionId": {
                        "originatingStationId": 0,  # 4294967295
                        "sequenceNumber": 0         # 65535
                    },
                    "detectionTime": 0,
                    "referenceTime": 0,
                    "termination": "isCancellation",
                    "eventPosition": {
                        "latitude": 900000001,
                        "longitude": 1800000001,
                        "positionConfidenceEllipse": {
                            "semiMajorConfidence": 4095,
                            "semiMinorConfidence": 4095,
                            "semiMajorOrientation": 3601
                        },
                        "altitude": {
                            "altitudeValue": 800001,
                            "altitudeConfidence": "unavailable"
                        }
                    },
                    "validityDuration": 0,
                    "TransmissionInterval": 100,
                    "stationType": 0
                },
                "situation": {
                    "informationQuality": 7,
                    "eventType": {
                        "ccAndScc": ("collisionRisk97", 4),
                    }
                }
            }
        }
        denm_coder = DENMCoder()
        expected_denm = b'\x02\x01\x00\x00\x00\x00\x89\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
            b'\x00\x00\x00\x00\x00\x00\x03ZN\x90\x0e\xb4\x9d \x0f\xff\xff\xff\x08\xed\xdd\x0f\x80\x00\x00\x070\x82\x00'
        encoded_denm = denm_coder.encode(collision_warning_denm)
        # print(encoded_denm)
        self.assertEqual(expected_denm, encoded_denm)

    def test_decode(self):
        """Test DENMCoder decoding"""
        encoded_denm = b'\x02\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
            b'\x00\x00\x00\x00\x00\x06\xb4\x9d \x1di:@\x1f\xff\xff\xfe\x11\xdb\xba\x1f\x00\x00\x00\x00'
        denm_coder = DENMCoder()
        decoded_denm = denm_coder.decode(encoded_denm)
        expected_denm = {
            "header": {
                "protocolVersion": 2,
                "messageId": 1,
                "stationId": 0
            },
            "denm": {
                "management": {
                    "actionId": {
                        "originatingStationId": 0,
                        "sequenceNumber": 0
                    },
                    "detectionTime": 0,
                    "referenceTime": 0,
                    "eventPosition": {
                        "latitude": 900000001,
                        "longitude": 1800000001,
                        "positionConfidenceEllipse": {
                            "semiMajorConfidence": 4095,
                            "semiMinorConfidence": 4095,
                            "semiMajorOrientation": 3601
                        },
                        "altitude": {
                            "altitudeValue": 800001,
                            "altitudeConfidence": "unavailable"
                        }
                    },
                    "validityDuration": 0,
                    "stationType": 0
                }
            }
        }
        self.assertEqual(expected_denm, decoded_denm)
