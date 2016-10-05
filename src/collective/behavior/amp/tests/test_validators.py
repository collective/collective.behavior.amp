# -*- coding: utf-8 -*-
from collective.behavior.amp.tests.utils import get_file_b64encoded
from collective.behavior.amp.validators import is_json
from collective.behavior.amp.validators import is_valid_logo
from zope.interface import Invalid

import unittest

VALID_JSON = """
{
  "requests": {
    "event": "https://amp-publisher-samples-staging.herokuapp.com/amp-analytics/ping?user=amp-EIXNmvC5F0DQszcXToppEEyfTWUFtT7cmqEf5Vloauoka65MIRmE0Qc8RDwrbOBV&account=ampbyexample&event=${eventId}"
  },
  "triggers": {
    "trackPageview": {
      "on": "visible",
      "request": "event",
      "vars": {
        "eventId": "pageview"
      }
    }
  }
}
"""


class ValidatorsTestCase(unittest.TestCase):

    def test_is_json_empty_value(self):
        self.assertTrue(is_json(u''))

    def test_is_json_valid_value(self):
        self.assertTrue(is_json(VALID_JSON))

    def test_is_json_invalid_value(self):
        self.assertFalse(is_json(u'invalid'))

    def test_is_valid_logo_empty_value(self):
        self.assertTrue(is_valid_logo(None))

    def test_is_valid_logo(self):
        logo = get_file_b64encoded('logo-plone-ok.png')
        self.assertTrue(is_valid_logo(logo))

    def test_is_valid_logo_square(self):
        # logo should have a wide aspect ratio
        logo = get_file_b64encoded('logo-plone-square.png')
        with self.assertRaises(Invalid):
            is_valid_logo(logo)

    def test_is_valid_logo_bigger(self):
        # logo should be no wider than 600px, and no taller than 60px
        logo = get_file_b64encoded('logo-plone-bigger.png')
        with self.assertRaises(Invalid):
            is_valid_logo(logo)
