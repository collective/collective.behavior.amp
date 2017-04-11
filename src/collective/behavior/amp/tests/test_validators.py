# -*- coding: utf-8 -*-
from collective.behavior.amp.config import AMP_ANALYTICS_DEFAULT
from collective.behavior.amp.tests.utils import get_file_b64encoded
from collective.behavior.amp.validators import is_valid_logo
from collective.behavior.amp.validators import is_xml
from zope.interface import Invalid

import unittest


class ValidatorsTestCase(unittest.TestCase):

    def test_is_xml_empty_value(self):
        self.assertTrue(is_xml(u''))

    def test_is_xml_valid_value(self):
        self.assertTrue(is_xml(AMP_ANALYTICS_DEFAULT))

    def test_is_xml_start_tag(self):
        with self.assertRaises(Invalid) as e:
            is_xml(u'invalid')
        msg = "Start tag expected, '<' not found"
        self.assertIn(msg, e.exception.message)

    def test_is_xml_tag_mismatch(self):
        with self.assertRaises(Invalid) as e:
            is_xml(u'<foo></bar>')
        msg = 'Opening and ending tag mismatch: foo line 1 and bar'
        self.assertIn(msg, e.exception.message)

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
