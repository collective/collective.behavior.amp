# -*- coding: utf-8 -*-
from collective.behavior.amp.behaviors import IAMP
from collective.behavior.amp.interfaces import IAMPPixelProvider
from collective.behavior.amp.testing import INTEGRATION_TESTING
from lxml import etree
from plone import api
from zope.component import adapter
from zope.interface import implementer

import unittest


@implementer(IAMPPixelProvider)
@adapter(IAMP)
class AMPPixelProvider(object):
    """Example adapter for amp-pixel tag."""

    def __init__(self, context):
        self.context = context

    def pixel(self):
        return u'<amp-pixel src="https://example.com/tracker/foo" layout="nodisplay"></amp-pixel>'


class AdaptersTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
            self.newsitem = api.content.create(
                container=self.portal, type='News Item', title='Lorem Ipsum')

        # the view is registered in the context of the object
        self.view = api.content.get_view(
            name='amp', context=self.newsitem, request=self.request)

    def test_amp_pixel_provider(self):
        from zope.component import getGlobalSiteManager
        gsm = getGlobalSiteManager()
        gsm.registerAdapter(AMPPixelProvider)
        amp = etree.HTML(self.view())
        self.assertIsNotNone(amp.find('.//amp-pixel'))
        gsm.unregisterAdapter(AMPPixelProvider)
        amp = etree.HTML(self.view())
        self.assertIsNone(amp.find('.//amp-pixel'))
