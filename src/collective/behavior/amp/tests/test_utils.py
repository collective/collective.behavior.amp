# -*- coding: utf-8 -*-
from collective.behavior.amp.testing import INTEGRATION_TESTING
from collective.behavior.amp.utils import Html2Amp
from lxml import html

import unittest


class Html2AmpTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.util = Html2Amp()

    def test_replace_tags(self):
        code = (
            '<img src="/img/amp.jpg" width="1080" height="610" alt="an image"></img>'
        )
        el = html.fromstring(code)
        self.util.replace_tags(el)
        expected = (
            '<amp-img src="/img/amp.jpg" width="1080" height="610" '
            'alt="an image" layout="responsive"></amp-img>'
        )
        self.assertEqual(html.tostring(el), expected)

    def test_remove_invalid_tags(self):
        code = (
            '<div>'
            '<img src="/img/amp.jpg" width="1080" height="610" alt="an image"></img>'
            '</div>'
        )
        el = html.fromstring(code)
        self.util.remove_invalid_tags(el)
        self.assertEqual(html.tostring(el), '<div></div>')

    def test_utility(self):
        code = (
            '<img src="/img/amp.jpg" width="1080" height="610" alt="an image"></img>'
            '<iframe frameborder="0" height="428" src="" width="760"></iframe>'
        )
        expected = (
            '<div class="amp-text">'
            '<amp-img src="/img/amp.jpg" width="1080" height="610" '
            'alt="an image" layout="responsive"></amp-img>'
            '</div>'
        )
        self.assertEqual(self.util(code), expected)
