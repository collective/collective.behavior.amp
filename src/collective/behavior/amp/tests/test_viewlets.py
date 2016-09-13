# -*- coding: utf-8 -*-
from collective.behavior.amp.browser import AMPViewlet
from collective.behavior.amp.testing import INTEGRATION_TESTING
from plone import api

import unittest


class ViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
            self.newsitem = api.content.create(
                container=self.portal, type='News Item', title='Lorem Ipsum')

    def viewlet(self, context=None):
        context = context or self.portal
        viewlet = AMPViewlet(context, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_enabled_on_news_item(self):
        viewlet = self.viewlet(self.newsitem)
        self.assertTrue(viewlet.enabled)
