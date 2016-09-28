# -*- coding: utf-8 -*-
from collective.behavior.amp.validators import isJSON

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

    def test_isJSON_default_value(self):
        self.assertTrue(isJSON(u''))

    def test_isJSON_valid_value(self):
        self.assertTrue(isJSON(VALID_JSON))

    def test_isJSON_invalid_value(self):
        self.assertFalse(isJSON(u'invalid'))
