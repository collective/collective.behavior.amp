# -*- coding: utf-8 -*-
from collective.behavior.amp.interfaces import IAMPSettings
from collective.behavior.amp.testing import INTEGRATION_TESTING
from lxml import etree
from plone import api

import unittest


class AMPViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
            self.newsitem = api.content.create(
                container=self.portal, type='News Item', title='Lorem Ipsum')
        self.view = api.content.get_view(
            name='amp', context=self.newsitem, request=self.request)

    def test_byline(self):
        # byline must contain the name of the author
        # and the last modification date only
        amp = etree.HTML(self.view())
        text = ''.join(amp.find('.//div[@class="amp-byline"]').itertext())
        self.assertIn('test_user_1_', text)
        self.assertNotIn('published', text)
        self.assertIn('last modified', text)

        # mark item as published
        from DateTime import DateTime
        self.newsitem.effective_date = DateTime()
        amp = etree.HTML(self.view())
        text = ''.join(amp.find('.//div[@class="amp-byline"]').itertext())
        self.assertIn('published', text)

    def test_amp_analytics(self):
        amp = etree.HTML(self.view())
        self.assertIsNotNone(amp.find('.//amp-analytics'))
        self.assertIsNotNone(amp.find('.//amp-analytics/script'))
        self.assertEqual(
            amp.find('*//amp-analytics/script').attrib['type'], 'application/json')
        self.assertIsNone(amp.find('*//amp-analytics/script').text)

        amp_analytics = IAMPSettings.__identifier__ + '.amp_analytics'
        api.portal.set_registry_record(amp_analytics, u'"foo": "bar"')
        amp = etree.HTML(self.view())
        self.assertEqual(
            amp.find('*//amp-analytics/script').text, u'"foo": "bar"')
