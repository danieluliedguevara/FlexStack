import unittest
from unittest.mock import MagicMock, patch

from flexstack.facilities.local_dynamic_map.tinydb_database import TinyDB

tinydb_database_example = {
    "_default": {
        "1": {
            "applicationId": 36,
            "timeStamp": -452001707.8018279,
            "location": {
                "referencePosition": {
                    "latitude": 407143528,
                    "longitude": -740059731,
                    "positionConfidenceEllipse": {
                        "semiMajorConfidence": 5,
                        "semiMinorConfidence": 5,
                        "semiMajorOrientation": 5,
                    },
                    "altitude": {"altitudeValue": 1000, "altitudeConfidence": 0},
                },
                "referenceArea": {
                    "geometricArea": {
                        "circle": {"radius": 2},
                        "rectangle": None,
                        "ellipse": None,
                    },
                    "relevanceArea": {
                        "relevanceDistance": 0,
                        "relevaneTrafficDirection": 0,
                    },
                },
            },
            "dataObject": {
                "header": {"protocolVersion": 2, "messageID": 2, "stationID": 0},
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
                                    "semiMajorOrientation": 3601,
                                },
                                "altitude": {
                                    "altitudeValue": 800001,
                                    "altitudeConfidence": "unavailable",
                                },
                            },
                        },
                        "highFrequencyContainer": [
                            "basicVehicleContainerHighFrequency",
                            {
                                "heading": {
                                    "headingValue": 3601,
                                    "headingConfidence": 127,
                                },
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
                        ],
                    },
                },
            },
            "timeValidity": 1000,
        }
    }
}


class TestTinyDB(unittest.TestCase):
    @patch("tinydb.TinyDB")
    def setUp(self, mock_tinydb):
        self.database_name = "test_database"
        self.database_path = "test_path"
        self.tinydb = TinyDB(self.database_name, self.database_path)
        self.tinydb.database = MagicMock()

    def test__init__(self):
        self.assertEqual(self.tinydb.database_name, self.database_name)
        self.assertEqual(self.tinydb.database_path, self.database_path)

    @patch("builtins.print")
    @patch("os.remove")
    def test_delete(self, mock_remove, mock_print):
        self.tinydb.database.close = MagicMock()
        mock_remove.return_value = True
        self.assertTrue(self.tinydb.delete())
        self.tinydb.database.close.assert_called_once()

    @patch("builtins.print")
    @patch("os.remove")
    def test_delete_file_not_found(self, mock_remove, mock_print):
        mock_remove.side_effect = FileNotFoundError()
        self.assertFalse(self.tinydb.delete())

    """@patch("builtins.str")
    def test_create_query_from_filter_statement(self, mock_str):
        query = MagicMock()
        mock_str.split = MagicMock(return_value=["cam", "camParameters", "basicContainer", "stationType"])
        attribute = "cam.camParameters.basicContainer.stationType"
        query_return = self.tinydb.create_query_from_filter_statement(query, attribute)
        self.assertEqual(query_return, "query.cam.camParameters.basicContainer.stationType")

    def test_create_query_search(self):
        query_with_attribute = MagicMock()
        operator = "=="
        ref_value = 1
        query_return = self.tinydb.create_query_search(query_with_attribute, operator, ref_value)
        self.assertEqual(query_return, query_with_attribute == ref_value)"""

    """def test_parse_filter_statement(self):
        self.tinydb.create_query_from_filter_statement = MagicMock()
        self.tinydb.create_query_search = MagicMock(return_value = "cam.camParameters.basicContainer.stationType == 1")

        filter = MagicMock()
        filter_statement_1 = MagicMock()
        filter_statement_1.attribute = "cam.camParameters.basicContainer.stationType"
        filter_statement_1.operator = "=="
        filter_statement_1.ref_value = 1
        filter_statement_2 = MagicMock()
        filter_statement_2.attribute = "cam.camParameters.basicContainer.stationType"
        filter_statement_2.operator = "=="
        filter_statement_2.ref_value = 1
        filter.filter_statement_1 = filter_statement_1
        filter.filter_statement_2 = filter_statement_2
        filter.logical_operator = 0
        query_return = self.tinydb.parse_filter_statement(MagicMock(), filter)
        self.assertEqual(
            query_return, "cam.camParameters.basicContainer.stationType == 1"
        )"""

    def test_search(self):
        self.tinydb.parse_filter_statement = MagicMock()
        self.tinydb.database.search = MagicMock(return_value=tinydb_database_example)
        self.assertEqual(self.tinydb.search(MagicMock()), tinydb_database_example)

    def test_create_query_search_value_error(self):
        query_with_attribute = MagicMock()
        operator = "nothing"
        ref_value = 1
        self.assertRaises(
            ValueError,
            self.tinydb.create_query_search,
            query_with_attribute,
            operator,
            ref_value,
        )

    def test_insert(self):
        self.tinydb.database.insert = MagicMock(return_value=0)
        self.assertEqual(self.tinydb.insert(tinydb_database_example), 0)

    def test_get(self):
        self.tinydb.database.get = MagicMock(return_value=tinydb_database_example)
        self.assertEqual(self.tinydb.get(0), tinydb_database_example)

    def test_update(self):
        self.tinydb.database.update = MagicMock()
        self.tinydb.update(tinydb_database_example, 0)
        self.tinydb.database.update.assert_called_once_with(
            tinydb_database_example, doc_ids=[0]
        )

        self.assertTrue(self.tinydb.update(tinydb_database_example, 1))

    def test_remove(self):
        self.tinydb.database.remove = MagicMock()
        dictionary = MagicMock()
        dictionary.doc_id = 0
        self.tinydb.remove(dictionary)
        self.tinydb.database.remove.assert_called_once()

        self.assertTrue(self.tinydb.remove(dictionary))

    def test_all(self):
        self.tinydb.database.all = MagicMock(return_value=tinydb_database_example)
        self.assertEqual(self.tinydb.all(), tinydb_database_example)

    """def test_exists(self):
        self.tinydb.database.contains = MagicMock(return_value = True)
        self.assertTrue(self.tinydb.exists(tinydb_database_example))"""
