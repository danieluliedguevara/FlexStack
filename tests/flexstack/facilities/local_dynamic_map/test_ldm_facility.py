import unittest
from unittest.mock import MagicMock

from flexstack.facilities.local_dynamic_map.ldm_facility import LDMFacility


class TestLDMFacility(unittest.TestCase):
    def test__init__(self):
        ldm_maintenance = MagicMock()
        ldm_service = MagicMock()
        self.ldm_facility = LDMFacility(ldm_maintenance, ldm_service)

        self.assertEqual(ldm_maintenance, self.ldm_facility.ldm_maintenance)
        self.assertEqual(ldm_service, self.ldm_facility.ldm_service)
        self.assertEqual(self.ldm_facility.if_ldm_3.ldm_service, ldm_service)
        self.assertTrue(self.ldm_facility.if_ldm_4.ldm_service, ldm_service)
